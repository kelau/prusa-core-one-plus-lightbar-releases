
- Added private browser and container factory-installation tooling that downloads release firmware when needed while keeping factory provisioning assets out of the public OTA repository.
- Added a self-contained standalone factory-installer bundle with a validated manifest and merged ESP32-C3 image; incomplete bundles now fail with a clear error before serving.
- Made the standalone PowerShell launcher respond promptly to Ctrl+C and reliably release its listening port.
- Kept the yellow Setup AP scanner smooth while captive-portal and web requests are active by rendering it from a preemptive 20 ms task on the single-core ESP32-C3.
- Fixed the five-press diagnostic showcase being hidden by the startup ramp or Setup AP scanner on an unconfigured device; normal AP indication resumes after diagnostics stop.

