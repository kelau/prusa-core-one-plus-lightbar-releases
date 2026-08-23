
- Replaced GitHub-account-dependent colour preset submissions with an anonymous, rate-limited Cloudflare Worker API.
- Added a free-text description to community presets and migrated individual preset documents to schema 2 and the catalogue to schema 3.
- Added a stable pseudonymous hardware ID derived from the ESP32 eFuse without publishing its raw identity.
- Highlighted presets submitted by the current lightbar as **Your preset**.
- Added strict Worker-side validation, bounded request sizes, integrity hashes, a D1 submission queue, and a scheduled GitHub catalogue publisher authenticated with short-lived Actions OIDC.

