Maximal 500mW ERP  (1)  
P(dBm) = 10 ⋅ log10( P(mW) / 1mW)  
P(dBm) = 10 ⋅ log10( P(500mW) / 1mW)  
P(dBm) = 26.9897000434   
P(dBm) = 27dBm   


(1) https://www.bundesnetzagentur.de/DE/Fachthemen/Telekommunikation/Frequenzen/Grundlagen/Frequenzplan/frequenzplan-node.html  
(Stand März 2022) Eintrag 251004 (Frequenznutzungsbedingungen)

Max EIRP / ERP	+16 dBm (40 mW) / +14 dBm (25 mW)
This is the power radiated by the isotropic antenna / half-wave dipole antenna (not the transmitter power)
https://www.thethingsnetwork.org/docs/lorawan/regional-parameters/





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


Zusammenfassung:

Das Link-Budget definiert die max. Reichweite in einenm LoRa Funk Netzr.
Der Spreading Faktor und somit die Reichweite eines Senders hängen von den Ausbreitungsbedingungen ab. LoRa hat dabei den ADR Mechanismus eingeführt und regelt damit die Reichweiten der Sender.
Die Rx-Empfindlichkeit hängt von Signal-Rausch-Verhältnis (SNR), Rauschfaktor (NF) und Bandbreite (BW) ab.

Line of Sight tool
https://www.heywhatsthat.com
