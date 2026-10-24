#!/usr/bin/env python3
"""Read-only, narrow memory probe for the user's TCP Smart Android emulator.

Examines up to 32 KiB around each of four pre-observed 'localKey' string
matches in the running app's Dalvik heap. Reads binary data in-memory over
ADB; displays only match counts, candidate value LENGTHS and device-ID presence.
It never outputs the candidate keys or saves a memory dump.
"""

import re
import subprocess
import sys

APP = "com.tcp.smart"
OFFSETS = (54375896, 62105800, 65083424, 65176840)
DEVICES = {
    b"<USB_HUB_DEVICE_ID>": "USB hub (.100)",
    b"<STANDING_LAMP_DEVICE_ID>": "Standing lamp (.101)",
}
JSON_FIELD = re.compile(rb'"localKey"\s*:\s*"([^"\x00]{1,128})"')


def adb(*args):
    result = subprocess.run(
        ["adb", "-e", *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=30,
    )
    if result.returncode:
        raise RuntimeError(
            f"ADB returned {result.returncode}: "
            + result.stderr.decode("utf-8", "replace")[:300]
        )
    return result.stdout


def main():
    try:
        pid = adb("shell", "pidof", APP).decode().strip()
        if not pid or not pid.isdecimal():
            print("TCP Smart is not currently running. Open it in the emulator.")
            return 1

        mappings = adb("shell", f"cat /proc/{pid}/maps")
        line = next((ln for ln in mappings.splitlines() if b"dalvik-main space" in ln), None)
        if line is None:
            print("Dalvik main heap not found. Stop here and share this message.")
            return 1
        memory_range = line.split(None, 1)[0].decode()
        start_hex, end_hex = memory_range.split("-", 1)
        heap_start, heap_end = int(start_hex, 16), int(end_hex, 16)
        print(f"Running TCP Smart PID: {pid}")
        print(f"Dalvik main heap: 0x{heap_start:x} - 0x{heap_end:x}")
        print("Checking four small windows; no secrets will be printed or saved.\n")

        for i, offset in enumerate(OFFSETS, 1):
            absolute = heap_start + offset
            if not heap_start <= absolute < heap_end:
                print(f"Match {i}: offset outside current heap (app layout changed).")
                continue
            # Capture 8 KiB preceding and up to 24 KiB beyond each match.
            window_start = max(heap_start, ((absolute - 8192) // 4096) * 4096)
            window_end = min(heap_end, window_start + 8 * 4096)
            pages = (window_end - window_start) // 4096
            command = (
                f"dd if=/proc/{pid}/mem bs=4096 "
                f"skip={window_start // 4096} count={pages} 2>/dev/null"
            )
            payload = adb("exec-out", "sh", "-c", command)
            count = len(re.findall(rb"localKey", payload))
            candidates = JSON_FIELD.findall(payload)
            # Report only device labels and candidate key lengths, never key data.
            found = [label for dev_id, label in DEVICES.items() if dev_id in payload]
            lengths = sorted({len(value) for value in candidates})
            print(
                f"Match {i} (offset {offset:,}): "
                f"field occurrences={count}, "
                f"JSON key-value pairs={len(candidates)}, "
                f"value lengths={lengths or 'none'}, "
                f"nearby known devices={', '.join(found) if found else 'none'}"
            )
        print("\nFinished. Share the text above only; it contains no key values.")
        return 0
    except FileNotFoundError:
        print("ADB not found on PATH; run this from the same PowerShell as earlier.")
    except subprocess.TimeoutExpired:
        print("ADB timed out. Check the emulator is responsive.")
    except Exception as exc:
        print("Probe failed:", str(exc))
    return 1


if __name__ == "__main__":
    sys.exit(main())
