## Offline printer network

- Add an offline mode for installations without an existing Wi-Fi access point or internet connection.
- Keep the lightbar's `CORE-One-Lightbar` access point active so the printer can join it directly.
- Discover and poll PrusaLink over the local `192.168.4.x` network while normal status lighting remains active.
- Add guided setup in the Network page, including printer-side Wi-Fi and PrusaLink instructions.
- Ensure changing the offline-network option enables Save, and preserve the setting in configuration backups and diagnostics.

Online firmware updates, preset downloads, and NTP synchronization still require an internet-connected network.
