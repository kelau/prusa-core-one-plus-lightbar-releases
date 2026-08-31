
- Fixed the embedded offline Seeq Default preset so loading it now sets both Idle and Startup to `#d13800` as intended.
- Added Seeq vendor, manufacturer, product, model, firmware and pseudonymous serial identity to HTTP mDNS TXT records and structured device metadata.
- Added Seeq model identity to configuration backups and factory-installer manifests. The configurable mDNS/DHCP hostname continues to provide the network-visible device name without altering or spoofing the hardware MAC address.

