---
title: Simulation
description: Installieren der Simulationssoftware Meshtasticator.
sidebar:
  order: 30
---

Die Wartung vieler Meshtastic Nodes für den Zweck des Experimentierens mit der Software bzw. dem Protokoll kommt mit einem größeren Aufwand einher. Dafür kann sich eine Simulation besser eignen, um Resultate ohne Aufwand direkt beobachten zu können.

Mit der Software [Meshtasticator](https://github.com/GUVWAF/Meshtasticator) ist es möglich, ein Meshtastic Netzwerk zu simulieren. Diese basiert auf zwei vorherigen Simulatoren ([lora-network-simulator](https://github.com/lucagioacchini/lora-network-simulator) und [LoRaSim](https://mcbor.github.io/lorasim/)) und nutzt unterliegend die [Meshtastic Linux Anwendung](https://meshtastic.org/docs/software/linux-native/), weswegen die Verwendung eines Linux Betriebsystems Voraussetzung ist.

Wir haben den Simulator in einer Ubuntu-VM installiert. Einige Pakete mussten installiert werden.

```shell
sudo apt install git python3-tk python3-pip python3-venv \
  gpiod libgpiod gpiod libgpiod-dev \
  libgpiod2 libyaml-cpp-dev libbluetooth-dev
```

Danach musste man das [Meshtasticator](https://github.com/GUVWAF/Meshtasticator) und [Meshtastic-Firmware](https://github.com/meshtastic/firmware) Repository herunterladen.

Um die Firmware zu compilieren, benötigt man `PlatformIO`. Das Tool lässt sich mit dem System Paketmanager wie z.B. `apt` installieren, häufig bekommt man eine veraltete Version, da die Paketquellen der meisten Betriebsysteme nur langsam aktualisiert werden.

Deshalb empfehlen wir, den Paketmanager von Python zu nutzen:

```shell
pip install platformio
```

Der Installationspfad liegt in `~/.local/bin`, welcher nicht standardmäßig in der Systemvariable `PATH` enthalten sein kann. Falls der Befehl `pio` beim Aufruf nicht gefunden wird, reicht es aus, den Installiationspfad zum System-`PATH` hinzuzufügen:

```shell
export PATH="$HOME/.local/bin:$PATH"
```

Die Meshtastic Firmware, welche normalerweise für IoT Hardware kompiliert wird, kann auch nativ auf einem Linux Betriebsystem mithilfe von [Portduino](https://github.com/meshtastic/framework-portduino) ausgeführt werden.

Mit Environment-Parameter `native` baut PlatformIO die Firmware für ein Linux Betriebsystem.

```shell
pio run --environment native
```

:::tip
Die PlatformIO Extension für VSCode bietet eine praktische GUI, mit der die Befehle ausgeführt werden können.
:::

Das kompilierte Binary befindet sich dann im Ordner `firmware/.pio/build/native`.

Damit der Meshtasticator die gewünschten Anordnungen simulieren kann, muss die Binary in den Ordner von Meshtasticator kopiert werden.
Bevor die Abhängigkeiten von Meshtasticator installiert werden können, sollte in dem Ordner eine Python-Umgebung aktiviert werden:

```shell
python3 -m venv venv
source venv/bin/activate
```

```shell title="Installieren der Abhängigkeiten"
pip3 install -r requirements.txt
```
