---
title: Example Guide
description: A guide in my new Starlight docs site.
---
# Aufgetretene Probleme mit Lösungen
## ESP32 : Linux: Ubuntu : Kommunikation zwischen Device und Computer funktioniert nicht
1. Das Gerät /dev/ttyUSB0 hat eine Gruppe: dialout. Der User muss der dialoutgruppe hinzugefügt werden. //
sudo adduser USER_NAME dialout //
USER_NAME muss sich jetzt ausloggen und wieder einloggen damit die Änderung in Kraft tritt.
2. Prüfen ob das Kabel zwischen Computer und Gerät auch wirklich Daten übertragen kann!
3. USB-C -> USB-C funktioniert nicht. Adapter USB-C:USB-A schafft abhilfe (Anscheinend funktioniert Power Delivery bei meinem Device nicht)