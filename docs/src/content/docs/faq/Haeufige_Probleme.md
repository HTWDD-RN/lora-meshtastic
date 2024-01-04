---
title: Häufige Probleme
---
## Kommunikation zum Device funktioniert nicht (Linux)

1. Die Gerät-Datei `/dev/ttyUSB0` gehört der Nutzergruppe `dialout`. Damit der Nutzer Schreibrechte erhalten kann, muss er zur Gruppe hinzugefügt werden:

    ```bash
    sudo adduser <user-name> dialout
    logout
    ```

    Der Nutzer muss sich ausloggen und wieder einloggen, damit er in der Gruppe enthalten ist.

2. Prüfen, ob das Kabel zwischen Computer und Gerät auch wirklich Daten übertragen kann.

3. USB-C &rarr; USB-C funktioniert manchmal nicht. Dies könnte an einem Fehler bei USB-C Power Delivery liegen. Adapter USB-C &rarr; USB-A schafft Abhilfe.
