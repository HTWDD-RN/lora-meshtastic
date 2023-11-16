mit einem Link Budget von 150dBm lässt sich unter optimalen Bedingungen(nir freiraumdämpfing) eine Distanz von bis zu 800km Überwinden


Maximal 500mW ERP  (1)  
P(dBm) = 10 ⋅ log10( P(mW) / 1mW)  
P(dBm) = 10 ⋅ log10( P(500mW) / 1mW)  
P(dBm) = 26.9897000434   
P(dBm) = 27dBm   


(1) https://www.bundesnetzagentur.de/DE/Fachthemen/Telekommunikation/Frequenzen/Grundlagen/Frequenzplan/frequenzplan-node.html  
(Stand März 2022) Eintrag 251004 (Frequenznutzungsbedingungen)





Radio link budget formula  
𝑃RX=𝑃TX+𝐺TX+𝐺RX−𝐿TX−𝐿FS−𝐿𝑃−𝐿RX  
PRX  = received power (dBm)  
PTX  = transmitter output power (dBm)  
GTX  = transmitter antenna gain (dBi)  
GRX  = receiver antenna gain (dBi)  
LTX  = transmit feeder and associated losses (feeder, connectors, etc.) (dB)  
LFS  = free space loss or path loss (dB)  
LP  = miscellaneous signal propagation losses (these include fading margin, polarization mismatch, losses associated with medium through which signal is travelling, other losses...) (dB)  
LRX  = receiver feeder and associated losses (feeder, connectors, etc.) (d)B  


Das Link-Budget, (Leistungsübertragungsbilanz) gibt die Qualität eines Funk-Übertragungskanals an.
Über ein einfaches Modell lässt sich das Link-Budget mittels Addition der Sendeleistung (Transmitter Power, Tx), der Empfängerempfindlichkeit (Receiver Power, Rx), des Antennengewinns und der Freiraumdämpfung (Free Space Path Loss, FSPL) errechnen.

FSPL (dB) = 20log10(d) + 20log10(f) – 147,55
FSPL = (4πd/λ)2 = (4πdf/c)2
FSPL = Free Space Path Loss (Freiraumdämpfung)
d = Abstand zwischen Tx und Rx in Metern
f = Frequenz in Hertz

Rx-Empfindlichkeit = -174 + 10log10(BW) + NF + SNR
BW = Bandbreite in Hz,
NF = Rauschfaktor in dB,
SNR = Signal-Rausch-Verhältnis (signal to noise ratio). Es gibt an, wie weit das Signal über
dem Rauschen liegen muss.

Material	Dämpfung (dB)
Glas (6mm)	0,8
Glas (13mm)	2
Holz (76mm)	2,8
Ziegelstein (89mm)	3,5
Ziegelstein (178mm)	5
Ziegelstein (267mm)	7
Beton (102mm)	12
Steinmauer (203mm)	12
Ziegelbeton (192mm)	14
Steinmauer (406mm)	17
Beton (203mm)	23
Stahlbeton (89mm)	27
Steinmauer (610mm)	28
Beton (305mm)	35


Zusammenfassung:

Das Link-Budget definiert die max. Reichweite in einenm LoRa Funk Netzr.
Der Spreading Faktor und somit die Reichweite eines Senders hängen von den Ausbreitungsbedingungen ab. LoRa hat dabei den ADR Mechanismus eingeführt und regelt damit die Reichweiten der Sender.
Die Rx-Empfindlichkeit hängt von Signal-Rausch-Verhältnis (SNR), Rauschfaktor (NF) und Bandbreite (BW) ab.

Zusammenfassung
Das Link-Budget gibt die maximale Reichweite eines LoRaWAN-Netzwerks vor.
Die Freiraumdämpfung beeinträchtigt die Reichweite. Durch die Verdopplung der Entfernung nimmt die Freiraumdämpfung um 6 dB zu.
Reflektionen und Brechungen der Funkwellen an Hindernissen und Boden beeinflussen Signalpegel und Reichweite. Im LoRaWAN-Netzwerk befindet sich eine Seite der Funkverbindung in der Regel in Bodennähe.
Hindernisse in der ersten Fresnelzone beeinflussen den Signalpegel auf der Rx-Seite und verkürzen die Reichweite.
SF-Werte und somit die Reichweite eines Senders hängen von den Ausbreitungsbedingungen ab. LoRaWAN erlaubt mittels ADR ein automatisches Netzmanagement und regelt damit die Reichweiten der Sender.
Die Rx-Empfindlichkeit hängt von Signal-Rausch-Verhältnis (SNR), Rauschfaktor (NF) und Bandbreite (BW) ab.

Line of Sight tool
https://www.heywhatsthat.com
