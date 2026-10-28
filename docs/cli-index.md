# CLI source inventory and publication status

The original 224-position conversation transcript yielded **64 fenced code/command/output blocks**, including Bash, PowerShell, YAML, JSON and terminal output.

## Now published

- [Recovered non-sensitive CLI excerpts](recovered-cli-safe-excerpts.md) — **37** of the **64** blocks, redacted and attributed to their original conversation turns.
- [Home Assistant Docker Compose configuration](../config/homeassistant/compose.example.yml) — extracted from conversation turn 060.
- [Source provenance and limitations](source-provenance.md).
- [CLI investigation journal](cli-command-journal.md) — explanatory examples, some reconstructed and labelled accordingly.
- [Local switch check example](../examples/local_switch_check.py) — reconstructed, not the original file.
- [Read-only DPS monitor](../examples/monitor_dps.py) — sanitised adaptation of the private Windows monitor used in the 28 October 2026 countdown experiment; prompts for credentials instead of reading the original private JSON; no device switching.

## Remaining 27 blocks — reviewed and accounted for

All **27** remaining blocks have now been reviewed individually in [the disposition register](excluded-blocks-review.md). They remain in the private raw source archive; selected conclusions are documented publicly, without verbatim sensitive commands or trivial terminal outputs.

Four original Python source files have now been published in [scripts/original-sanitised](../scripts/original-sanitised/) using device-identifier placeholders. They are historical archival material and have not been revalidated against live devices.

No real device IDs, private local keys or original memory dumps should be committed to the public repository. The raw conversation archive remains private. See the provenance document for limitations.
