# Meshtastic Sniffer Project

## Protokollbeschreibung

Meshtastic nutzt **LoRa**, ein Funkprotokoll mit großer Reichweite, das in den meisten Regionen ohne zusätzliche Lizenzen oder Zertifizierungen verfügbar ist — im Gegensatz zum Amateurfunk.

Diese Funkgeräte sind so konzipiert, dass sie empfangene Nachrichten weiterleiten und dadurch ein **Mesh-Netzwerk** bilden. Dieses System stellt sicher, dass jedes Gruppenmitglied, einschließlich der am weitesten entfernten Personen, Nachrichten empfangen kann.

Zusätzlich können Meshtastic-Geräte mit einem einzigen Smartphone gekoppelt werden, sodass Freunde und Familie Nachrichten direkt an ein spezifisches Gerät senden können. Es ist wichtig zu beachten, dass jedes Gerät nur eine Verbindung zu einem Benutzer gleichzeitig unterstützen kann.

Die Pakete sind mit **AES256-CTR** verschlüsselt.

---

## Ausgangssituation

Als Hardware wurde ein **LilyGo T-Echo** Gerät verwendet, das auf dem **ESP32** basiert.

Das Gerät funktionierte ursprünglich korrekt. Nach der Installation einer aktuellen Firmware erhielt ich die Aufgabe, einen **Sniffer** zu implementieren.

Zu diesem Zeitpunkt funktionierten:

- Bluetooth-Verbindung mit dem Smartphone
- Anzeige auf dem Display
- Empfang und Weiterleitung von Mesh-Paketen
- Empfang von Telemetrie-Paketen (z. B. `airUtilTx`)

Mein Hauptziel war die **Nutzung des Geräts als Sniffer** mithilfe eines Python-Programms, das auch **Raw-Packets** sammelt.

---

## Firmware-Analyse und Debugging

Zur Analyse der Firmware verwendete ich:
`meshtastic --info`
`meshtastic --get ...`

Obwohl der Parameter `debugLogApiEnabled: false` gesetzt war, änderte sich das Verhalten nicht.

---

# Verbindungsprobleme & Fehlersuche

Im Verlauf der Fehlersuche wurden folgende Schritte durchgeführt:

1. Reboot über CLI
2. Firmware-Reflash
3. Gerät wurde danach als **neues Gerät** erkannt

Trotz korrekt installierter Treiber, sichtbarem **COM-Port** und funktionierendem Bluetooth war die **serielle Verbindung nicht mehr aktiv** (auch nicht mit `--port COM3`).

Es entstand eine klare Trennung:

* Bluetooth funktionierte
* Display funktionierte
* Mesh-Betrieb aktiv
* **Meshtastic-CLI-Kommandos nicht aktiv**

Daraus ergibt sich die Erkenntnis, dass die eingeschränkte Nutzbarkeit als Sniffer **nicht ausschließlich auf Hardware oder Firmware** zurückzuführen ist.

---

# Codeanalyse & Debugging

Eine nachträgliche Analyse zeigte, dass Teile meiner **Sniffer-Implementierung** nicht wie erwartet ausgeführt wurden.  
Dies könnte einen Teil der beobachteten Probleme erklären.

Unabhängig davon blieb die Einschränkung bestehen, dass `debugLogApiEnabled = false` gesetzt war, wodurch **kein Zugriff auf Debug-Logs** möglich war.

Die Arbeit führte zu einem besseren Verständnis der Grenzen zwischen:

* physikalischem Funkverkehr
* Firmware-Konfiguration
* Meshtastic-Protokollbetrieb
* API-Zugriff

---

# Entwicklung des Sniffer-Programms (Python)

Im Projekt wurde ein **Python-basiertes Sniffer-System** zur Analyse von **Meshtastic-Netzwerkpaketen** entwickelt.  
Die Implementierung entwickelte sich von einem einfachen **Live-Sniffer** zu einem **Offline-Analysetool** für Netzwerktopologie und Knotenstruktur.

---

## Phase 1: Live-Sniffer für Paketempfang

Ein einfacher Sniffer wurde implementiert, der sich direkt über die **serielle Schnittstelle** mit einem Meshtastic-Gerät verbindet und Pakete in Echtzeit über:
`meshtastic.receive` verarbeitet
Ziel war **Beobachtung und Debugging des Paketverkehrs.

---

## Phase 2: CLI-basierter Sniffer mit Logging

Das Skript `cli_sniffer_json.py` startet die **Meshtastic-CLI** über einen Subprozess:
`meshtastic --listen`
Die Konsolenausgabe wird kontinuierlich verarbeitet, JSON-/Dictionary-Strukturen erkannt und in Python-Objekte umgewandelt.

Eigene Parsing-Logik wurde implementiert:
`find_balanced_braced_substring`
`try_parse_substring`

---

## Phase 3: SQL-basierte Offline-Analyse

Die Datenspeicherung wurde auf eine **SQLite-Datenbank** umgestellt.  
Die Tabelle: `rawpackets` dient als persistente Grundlage für **Offline-Auswertungen**.

---

# Analyse-Skripte

## Analyse der Hop-Distanzen

Das Skript `meshtastic_hops.py` berechnet aus `hopStart` und `hopLimit` die geschätzte Hop-Distanz von Paketen.  
Es ermittelt statistische Kennwerte (Median, Mittelwert) pro Node.

Ergebnis:  
→ Abschätzung der **Netzwerktopologie** und relativen Node-Entfernung.

---

## Analyse der Node-Mobilität

Das Skript `node_mobility.py` nutzt die Anzahl von **POSITION_APP**-Paketen als Heuristik zur Abschätzung der Bewegungsaktivität.

Nodes mit vielen Positionsupdates werden als **potenziell mobil** klassifiziert.

---

## Erweiterte Telemetrie-Auswertung

Eine Telemetrie-Analyse identifiziert Telemetrie-Pakete und extrahiert insbesondere den Parameter:
`airUtilTx`, damit kann die **Kanalauslastung über längere Zeiträume** ausgewertet werden.

---

# Fehlerrobustheit & Datenqualität

Mehrere Verarbeitungsschritte sind durch `try/except` abgesichert, um:

* fehlerhafte Pakete zu überspringen
* Laufzeitabbrüche zu vermeiden

Dies erhöht die **Stabilität der Datenerfassung** in realen Funkumgebungen.

---

# Fazit

Die Arbeit zeigt, dass **Meshtastic** nicht nur als Kommunikationssystem, sondern auch als **Datenquelle für Netzwerkanalyse** genutzt werden kann.

Die Funktionalität eines **Sniffers** hängt nicht nur von der Hardware ab, sondern stark von:

* Firmware-Konfiguration
* API-Zugänglichkeit
* Datenverarbeitungslogik

Durch die Entwicklung der Sniffer- und Analysewerkzeuge entstand ein besseres Verständnis von:

* Mesh-Routing
* Hop-Distanzen
* Knotenmobilität
* Funkkanalauslastung



