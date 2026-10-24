# Troubleshooting journey — from app-only control to a tested LAN path

This is a selective engineering record, not an exhaustive command transcript. It deliberately omits genuine credentials and private emulator data. Findings are distinguished from hypotheses.

## Requirements and constraints

- Keep two already-paired TCP Smart plugs operational in their original app.
- Do not factory reset, re-pair or modify the plugs' firmware.
- Do not root the actual Android phone.
- Prefer local control through Home Assistant on an existing Debian Docker host.
- Collect enough evidence for a portfolio case study without publishing secrets.

## Evidence gathered before key recovery

**Network reachability:** both plugs were present on an IoT VLAN; local **TCP/6668** accepted connections over the routed home-lab network. Packet capture supported identification of the communications in use. This was necessary, but not proof that encrypted commands would work.

**Protocol discovery:** TinyTuya's version **3.1** `status()` successfully returned a DPS dictionary even with an empty key. **DPS 1** was Boolean (the on/off relay). **DPS 2** was numeric zero, but its meaning was not proven. Reading state and commanding a relay were treated as distinct capabilities.

## Approaches attempted

| Investigation | Observed result | Decision |
| --- | --- | --- |
| Packet captures and TinyTuya scan/status | Connectivity and status established, key not revealed | Keep as diagnostic baseline |
| Inspect OEM APK and Tuya SDK references | Found code referring to `DeviceBean` and `getLocalKey()`; no account-specific key in APK | An app binary isn't the logged-in account's data |
| Investigate OEM cloud/developer-account linking | Compatibility/permissions uncertain for the branded TCP app | Did not base recovery on unverified linkage |
| Run actual OEM app in Android Studio emulator | App installed, logged in and showed both paired devices | Established a test environment without rooting physical phone |
| Frida process attachment | App terminated when attaching, including without any custom JS | Stop repeating the crash; alternative diagnostics |
| Inspect emulator's MMKV / SQLCipher-related storage | No simple plaintext device-key record established | Avoid inventing conclusions about encryption/storage |
| Read-only mapped-process-memory inspection | Found candidate JSON records associating device identifiers and 16-character values | Validate matches against actual hardware |

**Frida root cause:** not determined. An incompatibility in the emulated/translated environment was a possibility, **not a verified explanation**.

## The successful approach, with meaningful detail

1. Set up an **Android Studio Google APIs emulator (Android 14 / API 34, x86_64 with ARM translation)** with root access available via ADB. Install the original signed TCP Smart APK and its matching ABI split. Sign into the existing account and confirm both configured devices appear.
2. Confirm that **read-only access** to the emulator app's mapped process memory is technically possible while the app runs. Use process mapping metadata to identify a relevant Dalvik heap region rather than dumping every accessible process page.
3. Search small read-only regions for **known per-device identifiers** and field names such as `localKey` and `devId`. Field-name strings on their own are often metadata, *not* credential values — the earliest hits were false leads.
4. Where records occur close to the known identifiers, examine **JSON structure**, not just byte proximity. Locate 16-character candidate field values and correlate them with the corresponding device ID **inside the same parsed JSON object**. Some matches were ambiguous and intentionally rejected.
5. Store only the uniquely matched candidates in an **access-controlled, local-only file**. Report candidate counts and matching confidence without printing values or uploading raw data.
6. Validate each candidate with TinyTuya **protocol 3.1** from the LAN. A real key must enable encrypted relay control, not merely status polling. Briefly toggle the TCP Plug 2 and restore its starting state; repeat on the second plug when it is safe to disrupt connected loads.
7. Confirm Home Assistant can use the matched keys through **LocalTuya**, without requiring the Windows test machine or cloud API registration.

The step-by-step memory-inspection scripts used during investigation are **not included** in this repository: the working copies were tied to the emulator session and included sensitive context. Any publication of those tools should be a separately reviewed, sanitised and independently tested contribution rather than retroactively presenting a re-created script as an original artefact.

## Why this was worth doing

The original reset-and-re-pair route would have solved a device setup problem. This route answered a broader troubleshooting question: *Could I understand enough of the existing stack to preserve the working app and add direct local control?* The process involved forming hypotheses, observing evidence, ruling out unsupported assumptions and testing the result on the actual devices.
