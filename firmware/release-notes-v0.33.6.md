
- Added a bounded nearby-network scan on the Network page. Scan replaces the SSID text field with a signal-sorted dropdown, collapses duplicate SSIDs, identifies secured/open networks, and retains manual entry for hidden networks.
- Added wildcard DNS and Android, Apple, and Windows captive-portal probes so joining the setup AP opens `http://192.168.4.1` automatically; DNS and the AP shut down cleanly after station Wi-Fi connects.
- Added verified SVG and 1080×1080 PNG Wi-Fi QR assets for the open `CORE-One-Lightbar` setup network.
- Updated the standalone factory launcher to select beta, stable, or exact private GitHub releases, verify the merged image size and SHA-256 digest, cache it atomically, and fall back safely for offline use without exposing GitHub credentials to the browser.

