
- Added connection diagnostics with Wi-Fi strength, IP, last successful poll age, failure count and reason.
- Replaced the independent browser lighting simulation with sampled RGB/RGBW values from the device output, with bounded, non-overlapping requests.
- Added individual 20-second effect tests, including PrusaLink loss, with automatic return to printer status.
- Added portable JSON configuration backup and validated restore. Secrets are omitted by default; sensitive maintenance uses the OTA password or a recent physical BOOT press.
- Delayed OTA image acceptance until 60 seconds of healthy main-loop operation, added crash-loop safe mode and verified previous-slot rollback.
- Extended colour presets with optional unfilled-bar mode/colour while retaining compatibility with existing presets.

