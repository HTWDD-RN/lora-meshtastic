import meshtastic
import meshtastic.serial_interface
from meshtastic.protobuf import channel_pb2 as ch_pb2
from pubsub import pub
import datetime
import time

def on_ack(packet):
    print(f"✅ ACK received for packet ID {packet['id']} from {packet.get('fromId')}")

def list_channels(interface):
    interface.localNode.requestChannels(0)
    interface.localNode.waitForConfig(attribute="channels")
    ch_list = interface.localNode.channels
    for ch in ch_list:
        if ch.role != ch_pb2.Channel.Role.DISABLED:
            print(f"[{ch.index}] {ch.settings.name or ch.index}")
    return ch_list

def select_channel(iface):
    lst = list_channels(iface)
    sel = int(input("Index> ") or 0)
    return sel if 0 <= sel < len(lst) else 0

def main():
    iface = meshtastic.serial_interface.SerialInterface()
    pub.subscribe(on_ack, "meshtastic.receive.data.portnum")  # catch ack messages

    ch = select_channel(iface)
    interval = float(input("Interval (sec)> ") or 60)

    try:
        while True:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            msg = f"Automated message sent at {now}"
            pkt = iface.sendText(msg, wantAck=True, onResponse=on_ack, channelIndex=ch)
            print(f"📤 Sent msg ID {pkt.id}: '{msg}'")
            time.sleep(interval)
    except KeyboardInterrupt:
        pass
    finally:
        iface.close()

if __name__ == "__main__":
    main()
