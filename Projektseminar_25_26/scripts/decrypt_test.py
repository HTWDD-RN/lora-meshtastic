import sqlite3
import base64
#import crypto.decryptoapp
#import crypto.library
#import crypto.library.cryptor
#import entropython

import meshtastic.protobuf

from Crypto.Cipher import AES
import meshtastic.protobuf.mesh_pb2 # pycryptodome

sqlite_path = "./meshtastic.db"

dbcon = sqlite3.connect(sqlite_path, check_same_thread=False)

# cursor = dbcon.cursor()

cursor = dbcon.execute("SELECT rxTime, packets.'from', channel, payload, id FROM packets WHERE encrypted = 1 AND transport IS NOT NULL")

# https://github.com/meshtastic/firmware/blob/5ed2a4e8bb2052116295516c4fa893d7203d27c8/src/mesh/Channels.cpp
def getDefaultKey(idx = 1):
    first = b'\xd4\xf1\xbb\x3a\x20\x29\x07\x59\xf0\xbc\xff\xab\xcf\x4e\x69'
    second = int.to_bytes(idx, 1, 'little')
    return first + second

# https://github.com/meshtastic/firmware/blob/develop/src/mesh/CryptoEngine.cpp#L259
# https://github.com/meshtastic/firmware/blob/develop/src/mesh/CryptoEngine.cpp#L218


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


row = None
while (row := cursor.fetchone()) is not None:
    rxtime = row[0]
    rxFrom = row[1]
    channel = row[2]
    payload = base64.decodebytes(bytes(row[3], 'ascii'))
    packetId = row[4]

    # test all the simple keys. So far, only key 1 has actually been successful
    for skey in range(1, 2):
        decr = decrypt(payload, rxFrom, packetId, key=getDefaultKey(skey))
        #ent_enc = entropython.shannon_entropy(payload)
        #ent_dec = entropython.shannon_entropy(decr)
        #print(f"enc {payload}: {entropython.shannon_entropy(payload)}")
        #print(f"dec {decr}: {entropython.shannon_entropy(decr)}")
        #print(f"Entropy reduced by {ent_enc - ent_dec}")

        # attempt to decode
        data = meshtastic.protobuf.mesh_pb2.Data()
        try:
            data.ParseFromString(decr)
            #print([x[0].name for x in data.ListFields()])
            #print(data.payload)
            if data.portnum != 0 and len(data.payload) > 0:   # 0 is reserved, and also the default value if nothing else is set (and therefore, the message probably wasn't decoded correctly)
                print(f"success with simple key {skey} on channel {channel}!\n{data}")
            
        except Exception as e:
            #print(e)
            pass

    