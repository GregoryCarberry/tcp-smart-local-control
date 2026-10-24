# Changelog

## 2026-10-24 — Home Assistant integration completed

- TCP Plug 2 and TCP Plug 1 both reported working as LocalTuya switch entities via the Debian Home Assistant Container deployment.
- DPS 1 selected for the relay; Tuya protocol 3.1; no Tuya cloud API account configured.
- Original TCP Smart app pairing preserved. Optional cloud-isolation/latency checks left for follow-up.

## 2026-10-21 — Direct LAN control verified

- Recovered per-device local-key candidates from an inspectable, user-controlled Android emulator after other methods failed.
- Correlated candidates with the appropriate device records; locally validated encrypted switching for both plugs using Python and TinyTuya.
- Original OEM app visibly reflected a separate local switch test on the TCP Plug 2.

## 2026-10-20 — Initial investigation

- Identified TCP/6668 accessibility and local protocol 3.1 status readings.
- Began OEM app/APK investigation after confirming keyless reads did not provide encrypted switching.

## Starter repository package

- Documentation prepared and a **reconstructed, sanitised** test example added. This changelog records historical project activity; it does not claim these example files were committed or used on the original dates.
