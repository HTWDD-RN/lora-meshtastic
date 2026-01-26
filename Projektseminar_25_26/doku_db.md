# Datenbank
Der Sniffer speichert alle empfangenen Daten in eine SQLite-Datenbank.  
Diese beinhaltet zwei Tabellen, je nachdem, über welchen Mechanismus die Pakete empfangen wurden.

## `packets`
In der Tabelle `packets` werden alle Pakete gespeichert, welche über das normale Interface der Meshtastic-Firmware empfangen wurden (L3 Sniffer).  
Pakete werden also nur ein Mal abgespeichert, unabhängig davon, wie oft sie tatsächlich empfangen wurden.  
Zusätzlich wurden die Pakete hier von der Firmware entschlüsselt, sofern die nötigen Schlüssel vorhanden waren. Es wird nicht weiter versucht, zusätzliche Kanäle mit dem Standardschlüssel zu entschlüsseln.

### Spalten

Spalte      |   Bedeutung
------------|-------------
time        | Epoch-time des Empfangs auf dem Host, in ms
id          | Nummer des Paketes, nicht zwingend einzigartig
from        | Absender
to          | Zieladresse, 4294967295 (0xffffffff) für Broadcast
rxTime      | Epoch-time des Empfangs laut Firmware, in s
hopStart    | maximal erlaubte Anzahl an Hops
hopLimit    | verbliebene Anzahl erlaubter Hops, `NULL` wenn 0
transport   | `TRANSPORT_LORA` wenn das Paket über LoRa empfangen wurde, `NULL`, wenn es nur von der Firmware generiert wurde (z.B. Telemetrie)
rxSnr       | Signal-Rausch-Abstand, mit dem das Paket empfangen wurde
rxRssi      | Feldstärke, mit der das Paket empfangen wurde
channel     | Kanalhash des Paketes (nur, wenn es nicht entschlüsselt werden konnte), siehe [Hashgenerierung](https://github.com/meshtastic/firmware/blob/143e1d1a0d0014332b1aa44222329f74a2df2455/src/mesh/Channels.cpp#L34)
relayNode   | Knoten, welcher zuletzt das Paket weitergeleitet hatte, oder welcher es zunächst weiterleiten soll; LSB der Adresse
priority    | Priorität des Paketes, wird nicht über LoRa übertragen
encrypted   | ob das Paket noch verschlüsselt ist oder entschlüsselt werden konnte
port        | Port/Anwendung, für den/die das Paket bestimmt ist
payload     | Nutzdaten des Paketes. Bei entschlüsselten Paketen die rohen Daten (Typ variiert je nach Port), bei verschlüsselten Rohdaten als base64

## `rawpackets`
In der Tabelle `rawpackets` werden alle Pakete gespeichert, welche direkt vor weiterer Verarbeitung ausgegeben wurden (L2 Sniffer).  
Pakete können wiederholt auftreten, wenn diese mehrfach empfangen wurden.  
Unabhängig vom Channel-Hash wird versucht, alle Pakete mit dem Standardschlüssel zu entschlüsseln.  
Empfangene Pakete werden nicht mit einer Prüfsumme geprüft, es können also auch abgeschnittene oder fehlerhafte Pakete enthalten sein.

### Spalten

Spalte      |   Bedeutung
------------|-------------
time        | Epoch-time des Empfangs auf dem Host, in ms
id          | Nummer des Paketes, nicht zwingend einzigartig
from        | Absender
to          | Zieladresse, 4294967295 (0xffffffff) für Broadcast
hopStart    | maximal erlaubte Anzahl an Hops
hopLimit    | verbliebene Anzahl erlaubter Hops
hash        | Kanalhash des Paketes, siehe [Hashgenerierung](https://github.com/meshtastic/firmware/blob/143e1d1a0d0014332b1aa44222329f74a2df2455/src/mesh/Channels.cpp#L34)
relayNode   | Knoten, welcher zuletzt das Paket weitergeleitet hatte
wantack     | ob das `want_ack` (Empfangsbestätigungswunsch) Flag im Header gesetzt war
nexthop     | LSB der Adresse des Knotens, welcher zunächst das Paket weiterleiten soll
mqtt        | `mqtt` Flag im Header
port        | Port/Anwendung, für den/die das Paket bestimmt ist
payload     | Nutzdaten des Paketes. Wenn das Paket entschlüsselt und dekodiert werden konnte das entschlüsselte Payload (ohne Portnummer), sonst das komplette verschlüsselte Payload
decrypt     | Ergebnis des Entschlüsselungsversuches mit dem Standardschlüssel, unabhängig vom Erfolg dessen
rssi        | Feldstärke, mit der das Paket empfangen wurde
snr         | Signal-Rausch-Abstand, mit dem das Paket empfangen wurde
