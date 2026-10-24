# Original CLI and script provenance

The original investigation was recorded in a 224-position shared ChatGPT conversation. Its rendered-page extraction contains 64 fenced command, configuration and output blocks. Four Python files were subsequently recovered from the owner's local copies.

## Classification

- `docs/recovered-cli-blocks.md`: intended historical command excerpts, not one runnable shell script.
- `config/homeassistant/compose.example.yml`: original Home Assistant Container service configuration extracted from the conversation.
- `examples/local_switch_check.py`: separately reconstructed example already in this repository, **not** an original forensic script.
- The four separately recovered Python files are being reviewed and uploaded manually by the owner. They have not been published by this update.

The browser-based archive preserves rendered code, but cannot guarantee the original Markdown fence syntax. Images, attachments and original code file bytes were not all available from the shared page; the Python file bodies were recovered separately.

## Critical warning about the physical LAN-switch test

The uploaded `tcp-smart-lan-switch-test.py` contains a historical mismatch: its device constants identify the USB hub, while its prose and output messages refer to the standing lamp. Do not run it uncorrected. Confirm the target device and connected equipment before any physical switching tests.

## Sensitive material

The private source transcript must not be committed to this public repository. Do not commit recovered local keys, private device identifiers, personal IP addresses, APKs, logs or memory dumps. Scripts based on historical emulator heap offsets are environment-specific, not portable key-recovery tools.

The published documentation distinguishes successful checks from attempted and unsuccessful investigations. The original source files have not been re-executed during repository recovery.
