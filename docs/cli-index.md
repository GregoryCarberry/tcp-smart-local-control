# CLI source inventory and publication status

The original 224-position conversation transcript yielded **64 fenced code/command/output blocks**, including Bash, PowerShell, YAML, JSON and terminal output.

## Now published

- [Recovered non-sensitive CLI excerpts](recovered-cli-safe-excerpts.md) — **37** of the **64** blocks, redacted and attributed to their original conversation turns.
- [Home Assistant Docker Compose configuration](../config/homeassistant/compose.example.yml) — extracted from conversation turn 060.
- [Source provenance and limitations](source-provenance.md).
- [CLI investigation journal](cli-command-journal.md) — explanatory examples, some reconstructed and labelled accordingly.
- [Local switch check example](../examples/local_switch_check.py) — reconstructed, not the original file.

## Still private / for manual review

The other **27** blocks were excluded from the public excerpt collection by a conservative filtering pass (sensitive emulator or credential-related commands and miscellaneous output). Exclusion does **not** imply every one is unsafe.

Four original Python source files were recovered separately. Their names are `tcp-smart-memory-probe.py`, `tcp-smart-device-record-probe.py`, `tcp-smart-key-candidate-check.py`, and `tcp-smart-lan-switch-test.py`. They will be uploaded manually by the owner after checking identifiers and correcting the LAN-test naming discrepancy.

No real device IDs, private local keys or original memory dumps should be committed to the public repository. The raw conversation archive remains private. See the provenance document for limitations.
