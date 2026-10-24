# Security, boundaries and public-release checklist

This project investigates **personally owned smart plugs** through a user-controlled test environment. It does not require compromising a third-party account, rooting an everyday handset or distributing a proprietary OEM APK.

## Keep private

- Real 16-character local keys, TCP Smart account credentials, session tokens, local-key JSON backups and exported application preferences/databases.
- Emulator memory dumps, device-record excerpts, and unreviewed diagnostic output.
- Full device IDs, MAC addresses, private LAN addresses, wireless SSIDs, VLAN administration credentials or screenshots revealing them.
- Signed OEM APK binaries and original proprietary firmware.
- Home Assistant `.storage` and other private configuration or backup files; logs may accidentally contain credentials.

## Redaction and checks

- Review **all files** before pushing; `.gitignore` helps but cannot protect against intentionally staged tracked files.
- Do not publish actual network config or firewall exports from the home lab.
- Never assume a masked credential in a screenshot is safe if the underlying image still contains visible text. Crop/redact in an image editor and inspect the exported file.
- If a key is accidentally published, deleting a commit is not a sufficient response: rotate/re-pair affected devices as appropriate and purge exposed histories where possible.
- New devices may have different firmware/protocol/key behaviour; do not claim one method works universally.

## Scope of code in this repo

The included Python example is **reconstructed and sanitised**, with no Android app instrumentation or runtime-dump tools. The investigation document explains the real decisions and findings, including unsuccessful approaches, without pretending that the example is a bit-for-bit copy of the original working scripts.

## Before opening a public GitHub repo

- [x] No recovered local keys in included files
- [x] No original OEM APK or emulator data included
- [x] Private network addresses and device identifiers omitted
- [x] Direct Home Assistant integration verified for both devices
- [ ] Review any future screenshots carefully
- [ ] Decide licence terms for code and documentation
- [ ] Optional additional tests clearly labelled as unperformed
