mit einem Link Budget von 150dBm (Einstellung = long fast, mit 17dBm transmit Power und 1,5dBi Antenne) lässt sich unter optimalen Bedingungen(nir freiraumdämpfing) eine Distanz von bis zu 800km Überwinden

Im Weltraum können Funksignale tatsächlich viel weiter reisen. Aber nun zurück zu Realität, in der die Sichtlinie eine größere Rolle spielt.
Mit 1,7m höhe ist es möglich 4,7km weit zu sehen. Aufgrund der Tatsache, dass die Welt eine Kugel ist.   
Der Horizont ist aber nur eine Begrenzung einer Radiowelle. Die quasioptische Ausbreitung gilt für Radiowellen im sub-GHz Bereich.

Im nächsten Schritt betrachten wir die Wellenausbreitung mit dem Hata-Okumura-Modell (Hata-Modell).

Das Hata-Modell verwendet verschiedene Begriffe uin der Dämpfungsformel, um zwischen verschiedenen Landnutzungen zu unterscheiden, von ländlicher bis zu dicht besiedelten Region.  
Hata-Ausbreitungsformel  
D=69,55+36,26log(f)-13,82log(h_s)+[44,9-6,55log(h_s)*log(d)-K]
mit:  
d=Entfernung zwischen Sender und Empfänger  
hS=Höhe der Senderantenne  
hR=Empfängerantennenhöhe  
K=Konstatne für den Stadttyp und die Gebäude  
Nicht entwickelt: K = 4,78 × (log(f2) – log(f) + 40,94  
Vorort: K = 2 × log(f/28)2 + 5,4  
Kleinstadt: K = (1,1 × log(f) – 0,7) × hR – (1,56 × log(f) – 0,8)  
Großstadt, f < 300 MHz: K = 8,29 × (log(1,54 × hR))2 – 1,1  
Großstadt, f > 300 MHz: K = 3,2 × (log(11,7555 × hR))2 – 4,97  
f = Übertragungsfrequenz  
Für die folgende Reichweitenanalyse wird eine Dämpfung von 20 dB für das Eindringen in Gebäude und ein Verlust von 8 dB für Fading angenommen. Das bedeutet, dass es an die Bedingungen für Sender innerhalb von Gebäuden angepasst ist. Der Link-Budget wird daher um 28 dB reduziert um die Abdeckung in dicht bebauten Umgebungen zu vergleichen.  

Link Budget: 154  
Range Hata Open: 35,3km  
Range Hata City: 5,2km  
Range City(-28dB loss): 0,85km  
Line of sight: 22,7km  

Das Hata-Modell beachtet keine Line of Sight, deswegen habe ich die Höhe der Antenne des Senders auf 25Meter festgelegt, da die die übliche Antennenhöhe einer LTE-Antenne im innerstädtischem Gebiet darstellt.  
Hata Open bedeutet, dass sich nichts zwischen der Sender und Empfengerantenne befindet. Die Radiowelle wird nur durch die Freifeld-Dämpfung und die Erdoberfläche abgeschwächt. Daher sind die im obigen Tableu angegebene Reichweite von 35,3km theoretische Werte. Die Sichlinie begrenzt die Reichweite auf 22,7km.  
Das einfache Hata-Modell unterscheidet nicht zwischen Wasseroberflächen, Wiesen, Ackerland oder offenen Flächen mit geringer Vegetation.

Fazit: Das Hata-Modell kennt keine Erdkrümmung und ist nur eine erste Näherung. Als Gegencheck sollte immer eine Sichtlinie beachtet werden. Um genauere Werte zu erreichen kann das Longley-Rice-Modell verwendet werden.

Channelsetting: Long Range / Fast  	
Alt Channelname: Long Fast  
Data Rate: 1.07 kbps (default)	  
SPreading Factor/ Symbols: 11 / 2048	  
Coding Rate: 4/5	  
Bandwith: 250	  

transmit Power: 17dBm    
Antenna gain: 1,5dBi  
RX sensitivity: -136dBm  
RX antenna: 0dBi  
Link Budget: 150dB  


WiFi LoRa 32 v3 (SX1262 Lora Chip)  
P(dBm) = 21dBm +-1dBm  
Max Receiving sensitivity = -136dBm@SF12 BW=125KHz

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


Let's consider a simplified example of a LoRa link budget for a point-to-point communication link. Please note that real-world scenarios are more complex and involve additional factors, but this example should provide a basic understanding:

1. **Transmit Power (Tx Power):** Let's assume the transmitter has a power output of 20 dBm.

2. **Frequency (f):** Assume a frequency of 868 MHz.

3. **Distance (d):** Let's consider a communication distance of 2 kilometers.

4. **Antenna Gains (Gt and Gr):** Assume both the transmitter and receiver antennas have a gain of 2 dBi.

5. **Free Space Path Loss (Lp):** Using the free space path loss formula:

   \[ Lp = 20 \log_{10}(d) + 20 \log_{10}(f) + L_{FS} \]

   \[ Lp = 20 \log_{10}(2) + 20 \log_{10}(868 \times 10^6) + 20\log_{10}\left(\frac{4\pi}{c}\right) \]

   Here, \(c\) is the speed of light. The result will be the path loss in dB.

6. **Received Power (Rx Power):** Plug the values into the link budget equation:

   \[ \text{Rx Power} = \text{Tx Power} + \text{Tx Antenna Gain} - \text{Path Loss} + \text{Rx Antenna Gain} \]

   Substitute the values and calculate the received power.

The calculated received power should be compared with the receiver's sensitivity specification. If the received power is higher than the sensitivity threshold, the link is expected to work under the specified conditions.

Keep in mind that this is a simplified example, and in a real-world scenario, additional factors such as atmospheric conditions, interference, and fading effects should be considered for a more accurate link budget analysis.
