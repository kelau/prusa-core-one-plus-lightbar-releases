
- Moved Effect priority under Show advanced.
- Replaced the monolithic preset catalogue with a bounded index and one independently loadable file per preset.
- Added 64 KiB index and 4 KiB preset limits, a 200-preset cap, request timeouts, strict client-side schema/range/path/duplicate validation, and SHA-256 integrity verification before applying downloaded colours.
- Serialized preset publication and made each preset/index update an atomic Git commit.
- Pinned the GitHub publishing Action to an immutable commit.

