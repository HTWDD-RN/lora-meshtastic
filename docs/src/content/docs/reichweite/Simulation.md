---
title: Simulation
description: Experimente zmit der Simulationssoftware Meshtasticator.
sidebar:
  order: 51
---

Um ein Meshtastic Netzwerk zu simulieren braucht man einen Linux PC, da der [Meshtasticator](https://github.com/GUVWAF/Meshtasticator) die [Meshtastic Linux Anwendung](https://meshtastic.org/docs/software/linux-native/) verwendet.

Um den Simulator einzurichten haben wir eine Ubuntu-VM verwendet. Folgende Pakete müssen mit apt installiert werden:
- git
- python3-tk
- python3-pip
- python3-venv
- gpiod
- libgpiod
- gpiod
- libgpiod-dev
- libgpiod2
- libyaml-cpp-dev
- libbluetooth-dev

Danach muss man das [Meshtasticator](https://github.com/GUVWAF/Meshtasticator) und das [Meshtastic-Firmware](https://github.com/meshtastic/firmware) Repository herunterladen.
Um die Firmware zu compilieren benötigt man den Platformio, das kann man mit apt installieren, ist dann aber veraltet. Deshalb einfach mit `pip install platformio` das tool installieren und danach ~/.local/bin zur PATH-Variable der Shell hinzufügen. Dann kann mit `pio run --environment native` die Firmware mit [Portduino](https://github.com/meshtastic/framework-portduino) als Linux-Programm bauen. Die Schritte können auf einem Desktopsystem natürlich auch in Visual Studio Code mit dem Platformio-Plugin getätigt werden. Im Ordner firmware/.pio/build/native findet man danach das compilierte Programm.
Damit der Meshtasticator die gewünschten Anordnungen simulieren kann, muss die ausführbare Datei program einfach in den Meshtasticator-Ordner kopiert werden. Nachdem man dann mit `python3 -m venv venv` und `source venv/bin/activate` eine neue Python-Umgebung in dem Meshtasticator Ordner erstellt hat, müssen mit `pip3 install -r requirements.txt` noch alle Abhängigkeiten installiert werden.
