
- Fixed PrusaLink auto-detection accepting an unresolved mDNS address and displaying `0.0.0.0` as the printer host.
- Discovery now rejects unusable IPv4 addresses and falls back to the advertised `.local` hostname while mDNS address resolution is pending.
- Added a second API safeguard preventing an invalid discovery result from populating the Network page.

