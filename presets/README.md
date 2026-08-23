# Community colour presets

The lightbar reads the bounded `index.json` from the public `prusa-core-one-plus-lightbar-releases` repository and downloads an individual file only when the user loads that preset. Every index entry includes a SHA-256 hash checked by the UI before use. The built-in **Seeq Default** preset is always available in firmware, even without internet access.

The device creates a GitHub issue containing the proposed preset. A serialized publishing workflow validates the schema, colour ranges, duplicate names, allowed characters, blocked terms, and 200-preset limit before atomically committing one preset file and the regenerated index. Invalid submissions are rejected.
