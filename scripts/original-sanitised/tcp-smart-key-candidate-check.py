#!/usr/bin/env python3
"""Read-only inspection of TCP Smart's emulator heap for JSON device records.

Never prints or uploads key material.  By default saves nothing.  --save
writes a private local file ONLY if both local keys are unambiguously paired
with their known device IDs in the SAME JSON object.

Requirements: Python 3, adb in PATH, rooted Android Studio emulator-5554,
TCP Smart logged in and running.  Nothing is written on the emulator.
"""

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys

PACKAGE = "com.tcp.smart"
DEVICES = {
    "<USB_HUB_DEVICE_ID>": ("USB hub", "<USB_HUB_IP>"),
    "<STANDING_LAMP_DEVICE_ID>": ("Standing lamp", "<STANDING_LAMP_IP>"),
}
PAGE = 4096
# Smallest previously scanned window containing all 4 JSON localKey matches.
REGION_START = 25_591_808
REGION_END = 25_726_976
KEY_PATTERN = re.compile(rb'"localKey"\s*:\s*"([^"\\\x00]{16})"')
KEY_FIELD_NAMES = ("localKey",)
ID_FIELD_NAMES = ("devId", "gwId", "deviceId", "id", "virtualId")


def adb(*args, timeout=30):
    done = subprocess.run(
        ["adb", "-e", *args], capture_output=True, timeout=timeout,
        check=False,
    )
    if done.returncode:
        error = done.stderr.decode("utf-8", "replace").strip()
        raise RuntimeError(f"ADB error ({done.returncode}): {error[:200]}")
    return done.stdout


def extract_same_object_pair(whole_region, match_pos, raw_key):
    """Only returns ID if SAME parsed JSON dictionary has both key and ID.

    Scan candidate start braces preceding the match.  raw_decode permits
    unrelated trailing heap bytes and won't expose them via stdout.
    """
    lower = max(0, match_pos - 24_576)
    prefix = whole_region[lower:match_pos]
    opens = [lower + m.start() for m in re.finditer(rb"\{", prefix)]
    found = set()
    key = raw_key.decode("utf-8", "replace")

    # Scan from the closest braces backwards, capped for predictable runtime.
    for brace in reversed(opens[-350:]):
        raw = whole_region[brace:min(len(whole_region), brace + 65536)]
        text = raw.decode("utf-8", "replace")
        try:
            obj, finish = json.JSONDecoder().raw_decode(text)
        except (ValueError, RecursionError):
            continue
        # The parsed JSON must actually span this exact localKey occurrence.
        if brace + len(text[:finish].encode("utf-8", "replace")) <= match_pos:
            continue

        def visit(item):
            if isinstance(item, dict):
                if item.get("localKey") == key:
                    ids = {item.get(f) for f in ID_FIELD_NAMES if isinstance(item.get(f), str)}
                    found.update(ids.intersection(DEVICES))
                for value in item.values():
                    visit(value)
            elif isinstance(item, list):
                for value in item:
                    visit(value)

        visit(obj)
        if found:
            break
    return found


def scan(data):
    records = []
    for index, m in enumerate(KEY_PATTERN.finditer(data), start=1):
        key_bytes = m.group(1)
        value_len = len(key_bytes)
        pair = extract_same_object_pair(data, m.start(), key_bytes)
        nearest = []
        for device_id, (name, _) in DEVICES.items():
            positions = [p.start() for p in re.finditer(re.escape(device_id.encode()), data)]
            if positions:
                closest = min(abs(p - m.start()) for p in positions)
                nearest.append((closest, name))
        nearest.sort()
        nearest_label = (
            f"{nearest[0][1]} ({nearest[0][0]} bytes away)"
            if nearest and nearest[0][0] <= 4096 else "none within 4 KiB"
        )
        print(f"Candidate {index}: offset {REGION_START + m.start():,}, "
              f"key length {value_len}, "
              f"same JSON object: {', '.join(DEVICES[d][0] for d in sorted(pair)) or 'unconfirmed'}, "
              f"nearest ID: {nearest_label}")
        records.append((pair, key_bytes.decode("utf-8", "strict")))
    return records


def save_if_confirmed(records):
    assignments = {device_id: set() for device_id in DEVICES}
    for pair, key in records:
        # Reject ambiguous grouping; never infer mapping solely by proximity.
        if len(pair) == 1:
            assignments[next(iter(pair))].add(key)
    if not all(len(keys) == 1 for keys in assignments.values()):
        print("Not saved: couldn't match one unique key to EACH plug within the same JSON object.")
        return 1
    private = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "TCP-Smart"
    private.mkdir(parents=True, exist_ok=True)
    dest = private / "device-local-keys.json"
    payload = {DEVICES[dev_id][0]: {"device_id": dev_id,
               "ip": DEVICES[dev_id][1], "protocol": "3.1",
               "local_key": next(iter(assignments[dev_id]))}
               for dev_id in DEVICES}
    # Refuse overwrite to avoid replacing valid existing keys unexpectedly.
    try:
        with dest.open("x", encoding="utf-8") as out:
            json.dump(payload, out, indent=2)
            out.write("\n")
    except FileExistsError:
        print("Not saved: destination already exists; no file was overwritten.")
        return 1
    print("Saved two candidate keys locally in:", dest)
    print("This file contains device credentials. Do NOT upload it or paste its contents here.")
    print("A live TinyTuya 3.1 control test is still required to verify them.")
    return 0


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--save", action="store_true",
                     help="Save only if BOTH keys have unambiguous JSON-object matches")
    args = cli.parse_args()

    pid = adb("shell", "pidof", PACKAGE).decode().strip()
    if not pid.isdecimal():
        print("TCP Smart not running. Open it on the emulator and retry.")
        return 1
    maps = adb("shell", f"cat /proc/{pid}/maps")
    heap_map = next((x for x in maps.splitlines() if b"dalvik-main space" in x), None)
    if heap_map is None:
        print("Dalvik main heap mapping not found.")
        return 1
    addresses = heap_map.split()[0].split(b"-", 1)
    start = int(addresses[0], 16)
    length = int(addresses[1], 16) - start
    if REGION_END > length:
        print("Recorded region no longer fits this heap; stop and re-map offsets.")
        return 1
    if (start + REGION_START) % PAGE or REGION_END % PAGE:
        print("Memory read bounds not page-aligned. Stopping.")
        return 1
    page_count = (REGION_END - REGION_START) // PAGE
    command = (f"dd if=/proc/{pid}/mem bs={PAGE} "
               f"skip={(start + REGION_START)//PAGE} count={page_count} 2>/dev/null")
    block = adb("exec-out", "sh", "-c", command, timeout=40)
    if len(block) != REGION_END - REGION_START:
        print("Short memory read; app may have restarted. No output saved.")
        return 1

    print("TCP Smart PID:", pid)
    print("Memory read: 132 KiB; matches reported WITHOUT displaying values.\n")
    records = scan(block)
    print("\nJSON candidates found:", len(records))
    print("No raw memory or secret values printed or saved by default.")
    if args.save:
        return save_if_confirmed(records)
    print("If both names show 'same JSON object', you can rerun with --save.")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print("Error:", exc)
        sys.exit(1)
