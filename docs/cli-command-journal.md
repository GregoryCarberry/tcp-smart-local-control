# CLI investigation journal — TCP Smart local control

This is a working command reference for the October 2026 investigation, **not an exact terminal transcript**. The original conversation establishes which tools and operations were performed, but the complete original shell history and source code are not available in this repository.

**Provenance key:** **Recorded** = operation and/or command fragment independently recoverable from the October chat history; **Illustrative** = sanitised command sequence recreated to document the method, *not claimed to have been executed verbatim*. Replace placeholder package names, addresses and paths locally. Never publish device IDs, 16-character local keys, APKs, app data, captures or RAM dumps.

## 1. Network and protocol checks

**Recorded:** Both devices accepted TCP connections on port **6668** across the trusted-to-IoT VLAN boundary. TinyTuya **3.1** returned relay status (DPS **1**) even when the key supplied for a status request was empty. That established *read* access, not permission to send encrypted switch commands.

**Illustrative** reachability check from Linux:

```bash
python3 - <<'PY'
import socket
host = input("Plug IP (private): ").strip()
try:
    with socket.create_connection((host, 6668), timeout=3):
        print("TCP/6668 reachable")
except OSError as exc:
    print(f"Connection failed: {exc}")
PY
```

**Illustrative** status-only test (replace the placeholders *locally*):

```python
import tinytuya

plug = tinytuya.OutletDevice(
    dev_id="<DEVICE_ID>",
    address="<PRIVATE_PLUG_IP>",
    local_key="",
)
plug.set_version(3.1)
print(plug.status())  # DPS 1: boolean relay state
```

The repository's [existing LAN-check example](../examples/local_switch_check.py) is a separate **reconstruction**, not an original forensic script.

## 2. Android device and OEM APK inspection

**Recorded command fragments:** `adb devices -l` and `adb shell pm path`. The signed OEM APK and an ABI split were obtained and installed into an Android Studio Android 14 / API 34 emulator. The actual daily-use phone was not rooted. The logged-in emulator app showed both existing plugs.

**Illustrative** session:

```powershell
adb devices -l
adb shell pm list packages | findstr /i "tcp"
adb shell pm path <OEM_PACKAGE_NAME>
# Paths returned by pm path are specific to the installed version:
adb pull /data/app/<REDACTED>/base.apk .\private\base.apk
# Split packages require their matching splits; values below are placeholders.
adb install-multiple .\private\base.apk .\private\split_config.arm64_v8a.apk
```

The OEM package name and filenames must come from the local `pm path` output. They must **not** be copied from this example. APK inspection exposed Tuya/ThingClips SDK references including `DeviceBean` and `getLocalKey()`, but did not expose each account-specific key.

## 3. Frida investigation — unsuccessful

**Recorded:** Frida was installed/tested against the rooted emulator. Attaching to the OEM app consistently terminated it, including attempts without a custom instrumentation script. No root cause was established.

**Illustrative** diagnosis commands:

```powershell
adb devices -l
frida-ps -U
frida -U -n <RUNNING_OEM_PROCESS_NAME>
# In another terminal, investigate an app crash (do not publish logs unchanged):
adb logcat -d > .\private\emulator-logcat.log
```

The attach command above demonstrates the diagnostic approach; its exact arguments are **not verified as the original invocation**. Do not present the Frida crash as proven anti-tamper behaviour.

## 4. Rooted-emulator memory and device-record analysis

**Recorded original Python script names:**

- `tcp-smart-memory-probe.py` — bounded mapped-memory probe around a relevant Dalvik heap area.
- `tcp-smart-device-record-probe.py` — sought device-associated records rather than isolated `localKey` strings.
- `tcp-smart-key-candidate-check.py` — checked that candidates belonged to the same parsed device record as the corresponding ID.
- An additional physical LAN-switch test — confirmed encrypted switching worked against the two owned plugs.

These are **not** reproduced here because the actual script bodies have not been recovered verbatim. Generating new scripts under those names and claiming they are the original source would falsify the project history.

The documented investigative sequence was: inspect process mappings on a user-controlled emulator; confine read-only inspection to a relevant memory area; look for known device IDs and `localKey` fields; reject unattached string hits; correlate keys and IDs within the **same JSON object**; validate candidates on the physical devices. Sensitive values and raw process data stayed private.

## 5. Physical LAN validation with TinyTuya

**Recorded:** Candidate keys were validated independently with Python/TinyTuya. Both plugs accepted encrypted commands. The standing-lamp test restored its initial power state; the OEM app also reflected the external change. A local key was required for encrypted on/off commands.

Use [`examples/local_switch_check.py`](../examples/local_switch_check.py) for a **sanitised reconstruction** of the final status/toggle test:

```bash
python -m pip install -r requirements.txt
python examples/local_switch_check.py
# Changes physical power only when explicitly requested:
python examples/local_switch_check.py --toggle
```

Do not test by switching power to a computer, NAS or other device that must remain on.

## 6. Home Assistant / LocalTuya on the Debian Yoga

**Recorded command fragments:** `cd ~/docker/homeassistant` and `docker compose ps`. The October conversation also records a `curl`/`tar` manual installation of LocalTuya **v5.2.5**, followed by a restart of **Home Assistant only**. The complete original installation command block was not recovered verbatim.

**Illustrative** checks and restart, from the existing deployment directory:

```bash
cd ~/docker/homeassistant
docker compose ps
ls -ld ./config/custom_components ./config/custom_components/localtuya
# Once the custom integration is present in the persistent config:
docker compose restart homeassistant
docker compose ps
```

The Compose service name may differ; confirm it from `docker compose ps` before using the restart command. For the actual recorded settings, read [Home Assistant configuration](home-assistant.md): both devices, protocol **3.1**, switch entity **DPS 1**, no Tuya Cloud API configuration, pairing preserved.

## 7. What remains to recover

The genuinely original `.py` files, complete ADB/Frida/PowerShell command transcript and the actual LocalTuya download command block are **not yet preserved in this repository**. Obtain them from the original chat export or local shell/script files, redact them, then commit them with precise original-vs-adapted labels. Avoid claiming this reference is an exhaustive transcript.

**Status:** this journal preserves a useful, reproducible troubleshooting reference while keeping the archival gap visible.
