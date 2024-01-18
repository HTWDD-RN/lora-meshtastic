---
title: Fazit
sidebar:
  order: 99
---

Meshtastic ist ein gut voranschreitendes Projekt, dass eine solide Software-Plattform für die Kommunikation zwischen LoRa-fähigen Geräten ermöglicht.

Damit aber Meshtastic als Katastrophennetz eingesetzt werden könnte, sind aktuell noch einige Hürden im Weg.

Für den Einsatz als Katastrophennetz müssten erstmal genug solcher Meshtastic- und LoRa-fähigen Geräte angeschafft werden, sodass ein zuverlässiges Mesh-Netzwerk innerhalb der Stadt aufgebaut werden könnte. Dies müsste am Besten mit einer Großbestellung geschehen, da sonst der Markt überlastet werden und die Preise steigen könnten.

Es müssten genug Geräte innerhalb der Stadt hoch positioniert werden, da die Reichweite von LoRa durch Gebäude wesentlich begrenzt ist. Nur bei freier Luftlinie sind Verbindungen über mehrere Kilometer möglich. Andere Funktechnologien mit mehr Sendeleistung, sind durch Gebäude weniger beeinträchtigt.
Aber im Katastrophenfall mit zusammengebrochener Infrastruktur (Black-Out), ist LoRa mit geringem Energieverbrauch besser geeignet.

Aktuell ist Meshtastic noch softwareseitig auf Netzwerke [mit bis zu 80 Nodes limitiert](https://meshtastic.org/docs/introduction#:~:text=the%20Meshtastic%20mesh%20can%20sustain%20up%20to%2080%20device%20nodes). Das reicht bei Weitem nicht, um den Raum Dresden vollständig abzudecken.
Das Protokoll scheint auch nicht für solche Mega-Meshes ausgelegt zu sein, was man am maximalen Hop Count von 7 erkennen kann. Ein limitierter Hop Count könnte eine weitreichende Zustellung verhindern.
