# Community colour presets

The lightbar reads the bounded `index.json` from the public `prusa-core-one-plus-lightbar-releases` repository and downloads an individual file only when the user loads that preset. Every index entry includes its publication timestamp and a SHA-256 hash checked by the UI before use. Presets can be sorted by name, newest first, or oldest first. The built-in **Seeq Default** preset is always available in firmware, even without internet access.

The device submits a name, free-text description, colours, and pseudonymous ESP32-derived hardware ID to the anonymous Cloudflare Worker in `cloudflare/preset-api`. Users do not need GitHub accounts. The Worker validates and rate-limits submissions, then queues them in Cloudflare D1. An OIDC-authenticated scheduled workflow in the private source repository publishes one file per preset and rebuilds the public index using the existing releases deploy key. Cloudflare therefore holds no GitHub credential.

The hardware ID is a truncated SHA-256 digest derived from the ESP32 eFuse identity and a domain separator; the raw MAC/eFuse value is never published. It is used only to mark a device's own submissions in the UI and is not authentication.
