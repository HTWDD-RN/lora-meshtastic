import sys
import subprocess
import json
import pprint
import re
import ast
import time
import os
from datetime import datetime
from typing import Optional

pp = pprint.PrettyPrinter(indent=2, width=60, sort_dicts=False)

print("Starting 'meshtastic --listen' subprocess...\n")

# Startet das Meshtastic-CLI als Subprozess
process = subprocess.Popen(
    [sys.executable, "-m", "meshtastic", "--listen"],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    text=True,
    bufsize=1,
    universal_newlines=True
)

print("Listening for packets (Ctrl+C to stop)...\n")

# CSV-Header erstellen, falls Datei noch nicht existiert
if not os.path.exists("airutil.csv"):
    with open("airutil.csv", "w", encoding="utf-8") as f:
        f.write("datetime;timestamp;air_util\n")

# Muster für Logzeilen, die meist uninteressant sind
IGNORE_PATTERNS = [
    re.compile(r"\bVERBOSE\b", re.IGNORECASE),
    re.compile(r"fromRadioBytes", re.IGNORECASE),
    re.compile(r"Unexpected FromRadio payload", re.IGNORECASE),
]

PACKET_LOG_FILE = "packets.log"
UNIQUE_NODES_FILE = "unique_nodes.txt"

unique_nodes = {}

packet_fh = open(PACKET_LOG_FILE, "a", encoding="utf-8")


def write_unique_nodes_file():
    """Schreibt die Liste der eindeutigen Nodes in eine Datei."""
    try:
        with open(UNIQUE_NODES_FILE, "w", encoding="utf-8") as fh:
            for k, v in unique_nodes.items():
                fh.write(f"{k} | {v}\n")
    except Exception:
        pass


def find_balanced_braced_substring(s: str) -> Optional[str]:
    """
    Findet die erste ausgeglichene Teilzeichenkette, die mit { oder [ beginnt.
    Berücksichtigt Anführungszeichen und Escape-Sequenzen.
    """
    start_idx = None
    for i, ch in enumerate(s):
        if ch in "{[":
            start_idx = i
            break
    if start_idx is None:
        return None

    stack = []
    in_quote = None
    esc = False
    for i in range(start_idx, len(s)):
        ch = s[i]
        if esc:
            esc = False
            continue
        if ch == "\\":
            esc = True
            continue
        if in_quote:
            if ch == in_quote:
                in_quote = None
            continue
        if ch == '"' or ch == "'":
            in_quote = ch
            continue
        if ch in "{[":
            stack.append(ch)
        elif ch in "}]":
            if not stack:
                return None
            opening = stack.pop()
            if (opening == "{" and ch != "}") or (opening == "[" and ch != "]"):
                return None
            if not stack:
                return s[start_idx:i + 1]
    return None


def try_parse_substring(subs: str):
    """Versucht zuerst JSON zu parsen, dann Python-Literal."""
    if not subs:
        return None
    try:
        return json.loads(subs)
    except Exception:
        pass
    try:
        return ast.literal_eval(subs)
    except Exception:
        return None


def extract_node_key_and_summary(pkt) -> Optional[tuple]:
    """
    Extrahiert die Node-ID und eine kurze Zusammenfassung.
    Gibt (Schlüssel, Text) zurück oder None, wenn kein Nodeinfo-Paket.
    """
    if not isinstance(pkt, dict):
        return None

    user = pkt.get("user") or {}
    if not isinstance(user, dict):
        user = {}

    node_id = user.get("id") or user.get("id_str") or pkt.get("num") or pkt.get("nodeId")
    if node_id is None:
        return None

    long_name = user.get("longName") or user.get("long_name") or user.get("long")
    short_name = user.get("shortName") or user.get("short_name") or user.get("short")
    mac = user.get("macaddr") or user.get("mac") or user.get("macAddr")
    hw = user.get("hwModel") or user.get("hw_model") or user.get("hw")
    num = pkt.get("num")

    pos = pkt.get("position") or {}
    lat = pos.get("latitudeI") or pos.get("latitude_i") or pos.get("latitude")
    lon = pos.get("longitudeI") or pos.get("longitude_i") or pos.get("longitude")

    parts = []
    if long_name:
        parts.append(f"name={long_name}")
    if short_name:
        parts.append(f"short={short_name}")
    if num is not None:
        parts.append(f"num={num}")
    if mac:
        parts.append(f"mac={mac}")
    if hw:
        parts.append(f"hw={hw}")
    if lat is not None and lon is not None:
        parts.append(f"pos={lat},{lon}")

    summary = " | ".join(parts) if parts else str(pkt)
    return str(node_id), summary


def classify_packet(pkt: dict) -> str:
    """Klassifiziert ein Paket in eine der Hauptgruppen."""
    if not isinstance(pkt, dict):
        return "unbekannt"
    if "user" in pkt:
        return "nodeinfo"
    if "decoded" in pkt:
        return "decoded"
    if "encrypted" in pkt:
        return "encrypted"
    if "hopLimit" in pkt or "rxSnr" in pkt:
        return "routing"
    return "unbekannt"


def handle_packet(pkt: dict):
    """Verarbeitet ein Paket abhängig von der Kategorie."""
    typ = classify_packet(pkt)

    if typ == "nodeinfo":
        print("Paket-Typ: NodeInfo")
        return

    if typ == "decoded":
        decoded = pkt.get("decoded") or {}
        port = decoded.get("portnum")
        print(f"Paket-Typ: Decoded (Port={port})")
        return

    if typ == "encrypted":
        ch = pkt.get("channel")
        print(f"Paket-Typ: Verschlüsselt (Channel={ch})")
        return

    if typ == "routing":
        snr = pkt.get("rxSnr")
        hops = pkt.get("hopLimit")
        print(f"Routing-Paket: SNR={snr}, Hops={hops}")
        return

    print("Unbekanntes Paket erkannt.")


def _find_telemetry_dict(pkt: dict):
    """
    Versucht, Telemetriedaten in verschiedenen Strukturen zu finden.
    Rückgabe: dict oder None
    """
    if not isinstance(pkt, dict):
        return None

    telemetry = pkt.get("telemetry")
    if isinstance(telemetry, dict):
        return telemetry

    decoded = pkt.get("decoded")
    if isinstance(decoded, dict):
        telemetry = decoded.get("telemetry")
        if isinstance(telemetry, dict):
            return telemetry

        payload = decoded.get("payload")
        if isinstance(payload, dict):
            telemetry = payload.get("telemetry")
            if isinstance(telemetry, dict):
                return telemetry

    return None


def handle_air_util(pkt: dict):
    """Analysiert airUtilTx-Werte und speichert sie in einer CSV-Datei."""
    try:
        telemetry = _find_telemetry_dict(pkt)
        if not telemetry:
            return

        metrics = telemetry.get("deviceMetrics") or telemetry.get("localStats")
        if not isinstance(metrics, dict):
            return

        air_value = metrics.get("airUtilTx")
        if air_value is None:
            return

        ts = int(time.time())
        dt = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")

        with open("airutil.csv", "a", encoding="utf-8") as f:
            f.write(f"{dt};{ts};{air_value}\n")

        print(f"airUtilTx erkannt: {air_value}")

    except Exception:
        pass


try:
    for raw_line in process.stdout:
        line = raw_line.strip()
        if not line:
            continue

        # Versuche JSON/Python-Struktur aus der Zeile zu extrahieren
        braced = find_balanced_braced_substring(line)
        pkt = try_parse_substring(braced) if braced else None

        # Falls ein strukturiertes Paket erkannt wurde
        if pkt is not None:
            # Paket als JSON protokollieren
            try:
                packet_fh.write(json.dumps(pkt, ensure_ascii=False) + "\n")
                packet_fh.flush()
            except Exception:
                pass

            # Klassifizierung und Telemetrie-Analyse
            handle_packet(pkt)
            handle_air_util(pkt)

            # Nodeinfo und eindeutige Nodes erfassen
            node_info = extract_node_key_and_summary(pkt)
            if node_info:
                key, summary = node_info
                if key not in unique_nodes:
                    unique_nodes[key] = summary
                    write_unique_nodes_file()
                    print(f"Neuer Node: {key} | {summary}")
                else:
                    print(f"Bekannter Node: {key} | {summary}")
            else:
                print("Paket (Text):")
                print(json.dumps(pkt, ensure_ascii=False))

            continue

        # Falls keine Struktur erkannt wurde, air_util_tx aus Text extrahieren
        m = re.search(r"air_util_tx:\s*([0-9.]+)", line)
        if m:
            air_value = float(m.group(1))
            ts = int(time.time())
            dt = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
            with open("airutil.csv", "a", encoding="utf-8") as f:
                f.write(f"{dt};{ts};{air_value}\n")
            print(f"air_util_tx (TEXT): {air_value}")
            continue

        # Unterdrückt Debug-Logs
        if any(p.search(line) for p in IGNORE_PATTERNS) or re.search(r"\bDEBUG\b", line, re.IGNORECASE):
            continue

        # Zeigt relevante Textzeilen an
        if "Connected to" in line:
            print(line)
        elif re.search(r"\bPacket\b|\bfrom\b|RX:|TX:", line, re.IGNORECASE):
            print(line)

except KeyboardInterrupt:
    print("\nStopped by user.")
finally:
    try:
        write_unique_nodes_file()
    except Exception:
        pass
    try:
        packet_fh.close()
    except Exception:
        pass
    try:
        process.terminate()
        time.sleep(0.2)
        process.kill()
    except Exception:
        pass
