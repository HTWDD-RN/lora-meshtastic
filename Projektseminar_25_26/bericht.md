# Meshtastic Netzstabilität (für Notfallkommunikation)
Ziel war es, die Netzqualität und -stabilität eines Meshtasticnetzes zu beurteilen und gegebenenfalls Verbesserungsmöglichkeiten zu finden,
spezifisch in Hinsicht auf die Nutzung zur Notfallkommunikation, wenn andere Kommunikationsmittel ausgefallen sind.

Um die Nutzung und eventuelle Probleme des Meshes sinnvoll beurteilen zu können, wurde der Datenverkehr mit Hilfe eines Sniffers aufgezeichnet.

## Sniffer
Die PC-Seite des Sniffers befindet sich in `sniffer.py`.

### L3 Sniffer
Zuerst wurde ein Sniffer auf dem Layer 3 eingesetzt. Mit diesem können keine Informationen direkt über das flooding des Meshtastic-Protokols
gewonnen werden, sondern nur über die generelle Nutzung des Meshes.  
Dazu wurde ein Meshtastic-Knoten über die serielle Schnittstelle angeschlossen und alle empfangenen Pakete zur späteren Auswertung in einer Datenbank gespeichtert.

Auffällig hierbei war, dass ca. 40% der empfangenen Nachrichten verschlüsselt und auch nicht entschlüsselbar waren. Dies sind Nachrichten auf nicht offenen Kanälen, bei denen sich nicht direkt weitere Aussagen über den Inhalt treffen lassen. 
Weitere 30% der Nachrichten waren für die Anwendung `POSITION_APP` bestimmt, gefolgt von 13% `NODEINFO_APP` und 12% `TELEMETRY_APP`.

Daran ist erkennbar, dass ein nicht unwesentlicher Teil des Datenverkehrs aus automatisch gesendeten Paketen besteht.
Je nach Anwendung (hier betrachtet Notfallkommunikation) werden diese Daten nicht zwingend benötigt, konkurrieren aber zusammen mit den gewünschten Nutzdaten um Kanalzeit.
[Um diesem Problem entgegenzuwirken wird bereits das Sendeinterval dieser Pakete standardmäßig an die Anzahl der gesehenen Nodes angepasst.](https://meshtastic.org/de/docs/overview/mesh-algo/#regular-broadcast-intervals)  
An dieser Stelle ergibt sich eine Verbesserungsmöglichkeit, indem das Senden und weiterverteilen von Paketen von diesen Anwendungen mehr an die Netzauslastung angepasst wird.

Die Anzahl aktiver Nodes ist ein Indiz für die Netzauslastung, jedoch kein sonderlich aktuelles, und ein lokal beschränktes.  
Die Auslastung an anderen Orten, welche die Pakete durch Weiterleitung erreichen, wird gebenenfalls nicht beachtet. 
Eine Möglichkeit dies zu verbessern wäre die Einführung eines Prioritätsfelds in Paketen. Damit könnte, auch bei verschlüsselten Paketen, die Reichweite eines Paketes an die jeweils lokale Auslastung angepasst werden, indem Pakete mit geringerer Priorität ab einer gewissen Kanalauslastung nicht, oder besser seltener, weitergeleitet werden.
Damit sollten weiterhin hohe Reichweiten mit vielen Hops nutzbar sein, ohne in Gebieten mit vielen Knoten das Netz zu stark zu überlasten.  
Dies ist jedoch ohne breaking Changes am Protokoll derzeit schwierig umsetzbar, da im Header keine Felder frei sind, und bei verschlüsselten Paketen die Protobufs nicht zugänglich sind.

In einer abgeschwächten Variante ließe sich dies umsetzen, indem das hop Limit nicht statisch festgelegt wird, sondern variabel ist und indirekt für Prioritäten genutzt wird. Je nach Anwendungsfall können dann gerade `NODEINFO_APP`, `TELEMETRY_APP` und `POSITION_APP`, wenn diese überhaupt aktiv sind, mit einem geringeren hop Limit, um trotzdem eine höhere Reichweite zu haben zu einem gewissen Anteil zufällig aber auch mit dem normalen hop Limit gesendet werden.
Für Textkommunikation kann dies dazu führen, dass es länger dauert, bis ein bestimmter Node von einem anderen Node gesehen wird, die Nachrichten selbst wären jedoch nicht beeinträchtigt.
Hierbei ist es wichtig, zufällig zu entscheiden, ob das normale oder herabgesetzte hop Limit genutzt wird, da es sonst dazu kommen kann, dass zu einem Zeitpunkt viele Nodes immer wieder mit hohem hop Limit senden. Dies wäre zwar weiterhin nicht unmöglich, jedoch sollten die Nodes nicht synchronisiert bleiben, wodurch dies nur zu einem kurzzeitigen Problem wird.  
Dieses Verfahren wäre auch mit älterer Firmware abwärtskompatibel.

Das in Firmwareversion 2.7.15 (beta) `TELEMETRY_APP` standardmäßig deaktiviert wurde weißt auch darauf hin, dass diese Anwendung viel Datenverkehr mit meist begrenztem Nutzen erzeugt. Das Problem ist somit real und auch den Entwicklern bekannt.


### L2 Sniffer
Da der Layer 3 Sniffer nur Informationen über die Nutzung des Netzes und zusätzlich nur wenige Informationen über die Übertragung zwischen Knoten liefert (abgesehen vom letzten relay-Knoten), wurde der Sniffer um einen Layer 2 Sniffer erweitert.

Hierfür musste die Firmware angepasst werden, um sämtliche empfangene LoRa-Pakete mit dem korrekten Syncword über die serielle Schnittstelle auszugeben. Die Patches sind in `sniffer_firmware.diff` zu finden und wurden auf Commit `17cd8308` angewandt.
Die Pakete wurden anschließend dekodiert, versucht, mit dem Standardschlüssel für Meshtastic zu entchlüsseln, und ebenfalls in einer Datenbank abgespeichert.

Mit Hilfe dieser Daten lässt sich zu einem gewissen Grad prüfen, wie gut das managed flooding Verfahren in der Praxis funktioniert. 
Um so wenig Kanalzeit wie möglich zu verschwenden sollte jedes Paket idealerweise nur ein Mal vorkommen, durch die Weiterleitungen kommt es jedoch vor, dass Pakete mehrfach empfangen werden. Wenn Pakete sehr oft empfangen werden, deutet dies entweder auf ein ungünstiges Mesh hin, da mehr Knoten als scheinbar nötig die Pakete wiederholen, oder auf eine gute Lage des Empfängers, weshalb dieser besonders viele Wiederholungen empfangen kann. Das hop Limit kann hierüber weiter Aufschluss geben. Im Idealfall wird ein Paket genau zwei mal empfangen, wobei das hop Limit um eins dekrementiert wurde.

Durchschnittlich wurde ein Paket am Teststandort 1.22 mal, bereinigt von Paketen, welche nicht weitergeleitet werden können und auch nicht wurden, 1.27 mal empfangen. Mehrfach empfangene Pakete wurden dabei durchschnittlich 2.1 mal empfangen.
Beide dieser Werte deuten auf keine am Standort erkennbaren großen Probleme in der Konfiguration anderer Knoten oder ein schlecht aufgebautes Netz hin. Doppelter Empfang eines Paketes sind vermutlich das Originalpaket oder eine Wiederholung und eine darauf folgende Wiederholung, welche für die meisten Rollen eine weitere Wiederholung unterdrückt.  
An einem zentraler gelegenen Standort wurden Pakete durchschnittlich (bereinigt) 1.96 mal empfangen, was fast dem Idealwert entspricht, mehrfach empfangene Pakete jedoch 2.92 mal, öfter als ideal. Um beurteilen zu können, ob dies nur durch eine gute Lage oder durch ein suboptimales Netz der Fall ist, ist weitere Auswertung nötig.

### weitere Auswertung
Um mehr Informationen über die Nutzung des Netzes zu bekommen wurde versucht, an Hand der Paketlänge auf den Inhalt zu schließen.
Hierfür wurden zuerst die entschlüsselten Pakete nach Port und Länge gruppiert. Pakete des gleichen Ports treten hierbei mit sehr unterschiedlichen Längen auf, und Pakete unterschiedlicher Ports können die gleiche Länge haben, womit sich über die Länge keine sonderlich guten Rückschlüsse auf den Inhalt ziehen lassen. Tendentiell sind `POSITION_APP` und `TELEMETRY_APP` Pakete jedoch eher kürzer, wogegen `NODEINFO_APP` eher länger ist.  
Insgesamt zeigen die verschlüsselten und entschlüsselten Pakete jedoch eine ähnliche Verteilung der Paketlängen, womit sich vermuten lässt, dass sich auch bei der Häufigkeit der Portnummern eine ähnliche Verteilung ergibt.

## Positionsabhängige Netzqualität
Als ein Indikator für die Netzqualität wurde die Standardabweichung des Hop Counts von empfangenen Nachrichten einzelner Nodes je relay Node gewählt. Diese deutet auf die Stabilität der Routen hin, wobei nach angegebenem relay Node getrennt werden muss, da Pakete oft genug mehrfach empfangen werden und dies das Ergebnis verfälschen würde (wenn Pakete von einem Node immer über relay 1 und relay 2 mit jeweils gleichem hop Count empfangen werden scheint die Route zwar stabil zu sein, der Hop Count der empfangenen Pakete unterscheidet sich aber in den meisten Fällen, womit ein Zusammenfassen zu einem fälschlich schlechten Ergebnis führen kann).
Eine hohe Standardabweichung bedeutet nicht zwingend, dass ein verwendeter Teil des Netzes schlecht ist. Wenn Routen von fest installierter Infrastruktur, welche idealerweise an günstigen Orten mit hoher Reichweite installiert ist, bedient werden, sollten diese jedoch relativ stabil sein, wogegen von normalen, teilweise beweglichen Clients abgedeckte Routen mit sich mit höherer Wahrscheinlichkeit ändern, und bei ungünstiger platzierten Nodes mehr Rebroadcasts und somit auch mehr Kanalzeit benötigt werden. Aus diesem Grund werden stabile Routen, und damit stabile Hop Counts, als günstig gewertet.  

Die durchschnittliche Standardabweichung pro relay Node kann, wenn der von einem Relay bediente Bereich bekannt ist, einen groben Anhaltspunkt für die Qualität des Netzes in den entsprechenden Himmelsrichtungen vom Empfänger aus geben. Da das Einzugsgebiet von relays jedoch relativ groß ist und je nach Position nicht sonderlich viele verschiedene Relays häufig genutzt werden, sind diese Daten nicht sonderlich genau und schwieriger auszuwerten.
Um einen genaueren Überblick zu erhalten wurden alle Nodes, von welchen mindestens ein Mal ein Positionspaket empfangen wurde, auf einer Karte mit ihrer durchschnittlichen Standardabweichung (Durchschnitt über die Werte getrennt nach angegebenem Relay) als Heatmap dargestellt, um eventuelle problematische Bereiche einfach erkennen zu können. Dies wurde mit dem Skript `hop_var.py` realisiert.  
Aus den gesammelten Daten konnten dabei jedoch keine sinnvollen Informationen gewonnen werden, je näher die Nodes am Sniffer positioniert waren, desto instabiler war deren Hop Count.  
Dies lässt sich dadurch erklären, dass bei nahe gelegenen Nodes eher Rebroadcasts, welche nicht von weniger dicht verteilter Infrastruktur stammen, noch empfangen werden, wogegen bei weiter entfernten Nodes Pakete, welche über stabile Infrastruktur weitergeleitet wurden, eine bessere Chance haben, überhaupt noch empfangen zu werden. Bewegliche Nodes haben ebenfalls durch ihre Bewegung instabile Routen, was das Ergebnis verfälscht.  
Da sich nur feststellen lässt, dass ein Node sich bewegt, wenn er mehrere verschiedene Positionen sendet, aber sich nicht mit sicherheit sagen lässt, dass sich ein Node nicht bewegt, ist das Filtern der Daten nach nur stationären Nodes nicht vollständig möglich.  
Trotz des imperfekten Filterns bleiben nicht genug Daten übrig, um sinnvoll Aussagen treffen zu können, dieser Ansatz ist somit leider hier nicht praktikabel.

Eine weitere Möglichkeit wäre, in Zukunft Hop Counts statt nach Node nur nach Position zu werten, wobei dies nur mit Positionspaketen sinnvoll ist. Damit könnten auch Daten von mobilen Nodes verwendet werden. Auch die Genauigkeit der Position wurde bisher nicht beachtet, was die Daten etwas verfälscht.
