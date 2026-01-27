from meshtastic.serial_interface import SerialInterface
from pubsub import pub
import time
import pprint

pp = pprint.PrettyPrinter(indent=2, width=100)

def on_receive(packet, interface=None):
    print("\nPacket received:")
    # Konvertiere Bytes in eine lesbare Form, ähnlich wie bei --listen
    def safe(obj):
        if isinstance(obj, bytes):
            try:
                return obj.decode('utf-8', errors='replace')
            except Exception:
                return obj.hex()
        if isinstance(obj, dict):
            return {k: safe(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [safe(x) for x in obj]
        return obj

    pp.pprint(safe(packet))

print("Connecting to Meshtastic device on COM3…")
iface = SerialInterface(devPath="COM3")

# Abonniere nur echte Pakete (andere Ereignisse sind nicht relevant)
pub.subscribe(on_receive, "meshtastic.receive")

print("Connected! Listening for packets… (Ctrl+C to stop)")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nStopped.")
    iface.close()
