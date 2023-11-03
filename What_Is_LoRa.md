LoRa is a wireless modulation technique derived from Chirp Spread Spectrum (CSS) technology. It encodes information on radio waves using chirp pulses - similar to the way dolphins and bats communicate! LoRa modulated transmission is robust against disturbances and can be received across great distances.

LoRa is ideal for applications that transmit small chunks of data with low bit rates. Data can be transmitted at a longer range compared to technologies like WiFi, Bluetooth or ZigBee. These features make LoRa well suited for sensors and actuators that operate in low power mode.

LoRa can be operated on the license free sub-gigahertz bands, for example, 868 MHz, and 433 MHz. It also can be operated on 2.4 GHz to achieve higher data rates compared to sub-gigahertz bands, at the cost of range. These frequencies fall into ISM bands that are reserved internationally for industrial, scientific, and medical purposes.



LoRa (from long range) is a proprietary radio technology that is owned by Semtech. It is designed for long-range (e.g., 10km), low-bandwidth (i.e., measured in Kbps), low-power communication, primarily for internet of things (IoT) networks.

LoRa defines the physical layer that controls how the radio signals are modulated. Specifically, LoRa uses chirp spread spectrum (CSS) to encode information.

LoRa operates in a license-free, sub-gigahertz frequency band (i.e., under 1GHz or 1000MHz), but each frequency varies from region to region due to regulatory requirements. If you’re buying a LoRa device, make sure you pick one tuned to the correct frequency band for your region.

China - 470-510MHz and 779-787MHz
Europe - 863–870MHz (typically 868MHz)
India - 865–867 MHz (typically 865MHz)
Japan - 920-923MHz
USA - 902–928 MHz (typically 915MHz)
South America - 915–928 MHz (typically 915 or 923MHz)

Why LoRa?

LoRa tries to bridge the gap between current communication technologies, like WiFi, Bluetooth, and cellular (4G/5G).

BILD:
https://www.thethingsnetwork.org/docs/lorawan/what-is-lorawan/bandwidth-vs-range.png


LoRa is useful for long-range, low-bandwidth, low-power communication, which is perfect for IoT devices. Some examples include:

a water sensor in a well in a remote location
a factory with hundreds of smoke alarms that all need to communicate
a large nature preserve trying to track animal migration
a natural gas provider needing to monitor each customer’s meter for usage
a weather station that only occasionally needs to transmit information


LoRa and LoRaWAN

LoRaWAN builds on top of LoRa to define the communication protocol and system architecture.

It’s important to note that you can use LoRa without using LoRaWAN. Other LoRa-based networks (that are not LoRaWAN) include Helium, The Things Network, Disaster.radio, and Meshtastic.

Meshtastic

Meshtastic builds on LoRa (not LoraWAN) to produce a decentralized mesh network. Features include:

Text-based, encrypted communication
No phone required (e.g., you can use a computer with the right hardware), but there are iOS and Android applications
Decentralization
Great battery life
Optional GPS location sharing
Open-source software
Unlike the traditional cellular network, each end-user device (e.g., phone, laptop, etc…) connects to a LoRa radio running Meshtastic, and all LoRa radios running Meshtastic can mesh together. Messages are relayed through LoRa radios until they reach their destination.

BILD BEISPIEL
https://loganmarchione.com/2023/05/lora-and-meshtastic/20230510_003.png



LORA RANGE(1300KM):

https://www.gsm-modem.de/M2M/m2m-faq/lpwan-range-comparision-nb-iot-lorawan-sigfox/