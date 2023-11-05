# Die ersten Schritte

## Hardware identifizieren oder auswählen

_Vorweg, Geräte nur mit angeschlossener Antenne einschalten! Anderenfalls kann das Gerät sich im schlimmsten Fall selber zerstören._

Meshtastic wird offiziell nur von bestimmten Geräten welche ein LoRa Modul innehaben supportet.

Es ist darauf zu achten, dass jedes Gerät welches im Meshnetz betrieben werden soll auf der _gleichen_ Frequenz arbeitet. Hier gibt es unterschiede!

Ohne Amateurfunklizenz kann man die in Deutschland freien Frequenzbänder 433 MHz und 868MHz, auf welchen Lora operiert, ohne Lizenzkosten nutzen.

Solange WLAN Verbindung zu einem Device nicht notw. ist und Bluetooth  ausreicht, sollte ein nRF52 Chip gewählt werden, da diese energieffizienter als ESP32 Chips und einfacher zu flashen sind.

Eine Liste mit unterstützer Hardware findet sich hier:

https://meshtastic.org/docs/supported-hardware/


##  Serial Treiber
### ESP32
Einen für das eigene Betriebssystem passenden Treiber auf folgender Seite identifizieren, herunterladen und Installieren:

https://meshtastic.org/docs/getting-started/serial-drivers
### nRF52
nRF52 Chips benötigen normalerweise _keinen_ Serial Treiber. Sie benutzen einen UF2 bootloader, welche das Gerät als USB-Stick vom Betriebssystem erkennen lassen.

_Auf keinen Fall folgenden USB geräte treiber herunterladen, es sei denn es wird UF2 support benötigt_

https://meshtastic.org/docs/getting-started/serial-drivers/nrf52

## Firmware Flashen

### ESP32
https://meshtastic.org/docs/getting-started/flashing-firmware/esp32/
### nRF52
https://meshtastic.org/docs/getting-started/flashing-firmware/nrf52/
