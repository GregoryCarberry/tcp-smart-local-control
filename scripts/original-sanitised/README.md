# Original investigation scripts — sanitised archive

These four scripts originated during the October 2026 TCP Smart troubleshooting investigation. Their real device identifiers and network addresses have been replaced by placeholders. They have **not** been rerun or verified against the original emulator after sanitisation.

**Naming:** TCP Plug 1 denotes the device formerly attached to a USB hub (original IoT address ending in .100). TCP Plug 2 denotes the device formerly attached to a lamp (original IoT address ending in .101). Neither accessory name is used in the public filenames and scripts. The numeric names are consistent identifiers, not a recommended operating order.

- `tcp-smart-memory-probe.py`: historical narrow mapped-memory probe
- `tcp-smart-device-record-probe.py`: historical search around remembered offsets
- `tcp-smart-key-candidate-check.py`: historical device-record correlation and optional local-only save
- `tcp-smart-lan-switch-test.py`: original physical relay validation, with public-facing target description corrected to TCP Plug 1 to match its original device constants

**Not ready to run as supplied:** The placeholder values are deliberately invalid. Historical heap offsets are session-dependent. Physical switching affects mains-connected equipment and an attempted restoration can fail. Use only in an authorised lab and never test on critical loads.

The scripts remain archival artefacts; the reconstructed, opt-in testing example under `examples/` is separate.
