import meshtastic
import meshtastic.protobuf.portnums_pb2
import meshtastic.serial_interface
from pubsub import pub
import re

import time

from Crypto.Cipher import AES
import meshtastic.protobuf.mesh_pb2

import base64

import sqlite3
from threading import Lock
# depending on sqlite here instead of using some more generic interface isn't great, but changing this in the future
# shouldn't be too hard if needed (and I have a similar setup in another project)
# SQLite not liking sharing objects across threads is a bit of an issuem, but hopefully not too bad (it just required synchronization)
sqlite_path = "./meshtastic.db"


# https://github.com/meshtastic/firmware/blob/5ed2a4e8bb2052116295516c4fa893d7203d27c8/src/mesh/Channels.cpp
def getDefaultKey(idx = 1):
    first = b'\xd4\xf1\xbb\x3a\x20\x29\x07\x59\xf0\xbc\xff\xab\xcf\x4e\x69'
    second = int.to_bytes(idx, 1, 'little')
    return first + second

def decrypt(payload, fromnode, packetid, extra = 0, key = getDefaultKey(1), keylen = 16):
    if len(payload) > 256:
        print("Payload is longer than 256 bytes, counter would have to be restarted!")
    if len(key) < keylen:
        key += b''.join([b'\x00',] * (keylen - len(key)))
    nonce = b''
    #print(f"{fromnode}:{hex(packetId)}")
    nonce += int.to_bytes(packetid, 8, 'little')
    nonce += int.to_bytes(fromnode, 4, 'little')
    nonce += int.to_bytes(0, 3, 'little')
    #print(len(nonce))
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    out = cipher.decrypt(payload)
    #print(out)
    return out
    #print(nonce)

class Packet:
    def __init__(self, p : dict):
        keys = p.keys()
        # these should probably always be present, I think
        if "from" in keys:
            self.fromaddr = p["from"]
        else:
            self.fromaddr = None

        if "to" in keys:
            self.toaddr = p["to"]
        else:
            self.toaddr = None

        if "id" in keys:
            self.packetId = p["id"]
        else:
            self.packetId = None

        if "rxTime" in keys:
            self.rxTime = p["rxTime"]
        else:
            self.rxTime = None
        if "rxSnr" in keys:
            self.rxSnr = p["rxSnr"]
        else:
            self.rxSnr = None

        if "rxRssi" in keys:
            self.rxRssi = p["rxRssi"]
        else:
            self.rxRssi = None

        if "hopStart" in keys:
            self.hopStart = p["hopStart"]
        else:
            self.hopStart = None
        if "hopLimit" in keys:
            self.hopLimit = p["hopLimit"]
        else:
            self.hopLimit = None

        if "transportMechanism" in keys:
            self.transport = p["transportMechanism"]
        else:
            self.transport = None

        # these are not always present
        if "channel" in keys:
            self.channel = p["channel"]
        else:
            self.channel = None
        if "relayNode" in keys:
            self.relayNode = p["relayNode"]
        else:
            self.relayNode = None
        if "priority" in keys:
            self.priority = p["priority"]
        else:
            self.priority = None

        # payload
        if "encrypted" in keys:
            self.isEncrypted = True
            self.payload = p["encrypted"]
            self.port = None
        else:
            self.isEncrypted = False
        if "decoded" in keys:
            self.port = p["decoded"]["portnum"]
            self.payload = p["decoded"]["payload"]

    def __repr__(self):
        s = f"{'' if self.isEncrypted else 'not'} encrypted {self.packetId} on {self.transport} from {self.fromaddr} to {self.toaddr}"
        s += f", {self.hopLimit}/{self.hopStart} hops, snr {self.rxSnr}db rssi {self.rxRssi}"
        if self.isEncrypted:
            s += f", channel {self.channel}"
        else:
            s += f", port {self.port}"
        s += f", priority {self.priority} relay {self.relayNode}"
        return s

dblock = Lock()

def dbRecordPacket(dbcon : sqlite3.Connection, packet : Packet):
    try:
        query = "INSERT INTO packets ('time', 'id', 'from', 'to', 'rxTime', 'hopStart', 'hopLimit', 'transport', 'rxSnr', 'rxRssi', 'channel', 'relayNode', 'priority', 'encrypted', 'port', 'payload')" + \
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        if not dblock.acquire(timeout=1):
            raise Exception("Failed to lock DB lock")
        # ms since the epoch should be precise enough
        dbcon.execute(query, (time.time_ns() // 1000000, packet.packetId, packet.fromaddr, packet.toaddr, packet.rxTime, packet.hopStart, \
                      packet.hopLimit, packet.transport, packet.rxSnr, packet.rxRssi, packet.channel, packet.relayNode, packet.priority, \
                      packet.isEncrypted, packet.port, packet.payload))
        dbcon.commit()
        dblock.release()
    except Exception as e:
        print(e)
        if dblock.locked():
            dblock.release()

def dbRecordPacketRaw(dbcon : sqlite3.Connection, packetId, fromaddr, toaddr, hopStart, hopLimit, channel, relayNode, wantack, nexthop, mqtt, port, payload, decrypted, rssi, snr):
    try:
        query = "INSERT INTO rawpackets ('time', 'id', 'from', 'to', 'hopStart', 'hopLimit', 'hash', 'relayNode', 'wantack', 'nexthop', 'mqtt', 'port', 'payload', 'decrypt', 'rssi', 'snr')" + \
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        if not dblock.acquire(timeout=1):
            raise Exception("Failed to lock DB lock")
        # ms since the epoch should be precise enough
        dbcon.execute(query, (time.time_ns() // 1000000, packetId, fromaddr, toaddr, hopStart, \
                      hopLimit, channel, relayNode, wantack, nexthop, mqtt, port, payload, decrypted, rssi, snr))
        dbcon.commit()
        dblock.release()
    except Exception as e:
        print(e)
        if dblock.locked():
            dblock.release()

dbcon = None

def onReceive(packet, interface):
    try:
        p = Packet(packet)
        #print(f"Received: {packet}")
        print(p)
        dbRecordPacket(dbcon, p)
    except:
        pass
    #print(f"from: {packet['long_name']} ({packet['short_name']}) {packet['macaddr']} {packet['hw_model']} in role {packet['role']}")

def recordRawPacket(bindata : bytes, rssi, snr):
    #print(bindata)
    dest = int.from_bytes(bindata[0:4], 'little')
    src = int.from_bytes(bindata[4:8], 'little')
    packetid = int.from_bytes(bindata[8:12], 'little')
    flags = bindata[12]
    hash = bindata[13]
    nexthop = bindata[14]
    relay = bindata[15]
    payload = bindata[16:]

    hoplimit = flags & 0x7
    hopstart = (flags >> 5) & 0x7
    wantack = (flags >> 3) & 1
    viamqtt = (flags >> 4) & 1

    encrypted = True

    dbpayload = payload#base64.encodebytes(payload)
    port = None
    #print(payload)
    decr = None
    try:
        decr = decrypt(payload, src, packetid)
        #print(f"decr: {decr}")
        mdata = meshtastic.protobuf.mesh_pb2.Data()
        mdata.ParseFromString(decr)

        print(mdata)
        port = mdata.portnum
        pnum = meshtastic.protobuf.portnums_pb2.PortNum.Name(port)
        #print(pnum)
        if port != 0 and len(mdata.payload) > 0:
            dbpayload = mdata.payload
            port = pnum
    except Exception as e:
        print(f"could not decrypt {packetid} from {src} to {dest}")
        pass
    #print(f"into db: {dbpayload}")
    dbRecordPacketRaw(dbcon, packetid, src, dest, hopstart, hoplimit, hash, relay, wantack, nexthop, viamqtt, port, dbpayload, decr, rssi, snr)

def onLog(line, interface):
    #print(line)
    try:
        lmatch = re.match(r"(.*\[sniff snoff\] Raw incoming packet: )(\s*\S+)(\s+\S+)(.*)", line)
        if lmatch is not None:
            rssi = 0
            snr = 0
            try:
                rssi = int(lmatch.group(2))
                snr = int(lmatch.group(3))
            except Exception:
                pass
            rdata = lmatch.group(4)
            data = bytes.fromhex(rdata)
            recordRawPacket(data, rssi, snr)
            #print(len(data))
            #print(rdata)
    except:
        pass

pub.subscribe(onReceive, "meshtastic.receive")
pub.subscribe(onLog, "meshtastic.log.line")

dbcon = sqlite3.connect(sqlite_path, check_same_thread=False)

interface = meshtastic.serial_interface.SerialInterface()

print(f"Connected on {interface.devPath}")
#interface.showInfo()

while True:
    time.sleep(1000)

