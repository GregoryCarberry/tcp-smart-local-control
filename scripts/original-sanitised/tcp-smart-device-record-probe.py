#!/usr/bin/env python3
"""Read-only TCP Smart emulator memory probe near previously found device IDs.

No raw memory, credentials or local keys are saved or printed.
Requires Windows adb in PATH; run while TCP Smart is open in API 34 emulator.
"""

import re
import subprocess
import sys

PACKAGE = 'com.tcp.smart'
DEVICE_IDS = {
    b'<TCP_PLUG_1_DEVICE_ID>': 'TCP Plug 1 (.100)',
    b'<TCP_PLUG_2_DEVICE_ID>': 'TCP Plug 2 (.101)',
}
# Previous offsets relative to the start of the Dalvik main heap.
OFFSETS = (
    265104, 20737336, 20740012, 20926350, 20939341,
    22069928, 22079308, 25295820, 25442398, 25442612,
    25519312, 25660184,
)
PAGE = 4096
MARGIN = 65536
FIELD_NAMES = ('localKey', 'local_key', 'devId', 'gwId', 'uuid', 'productId')
JSON_KEY = re.compile(rb'"localKey"\s*:\s*"([^"\x00]{1,128})"')


def adb(*args):
    result = subprocess.run(['adb', '-e', *args], stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, timeout=45, check=False)
    if result.returncode:
        err = result.stderr.decode('utf-8', 'replace').strip()
        raise RuntimeError(f'ADB returned {result.returncode}: {err[:240]}')
    return result.stdout


def aligned_down(n):
    return n // PAGE * PAGE


def aligned_up(n):
    return (n + PAGE - 1) // PAGE * PAGE


def windows(heap_size):
    spans = sorted(
        (max(0, aligned_down(offset - MARGIN)),
         min(heap_size, aligned_up(offset + MARGIN)))
        for offset in OFFSETS if 0 <= offset < heap_size
    )
    merged = []
    for lo, hi in spans:
        if merged and lo <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], hi))
        else:
            merged.append((lo, hi))
    return merged


def main():
    pid = adb('shell', 'pidof', PACKAGE).decode('utf-8', 'replace').strip()
    if not pid.isdecimal():
        print('TCP Smart is not running. Open it in the emulator before trying again.')
        return 1
    mappings = adb('shell', f'cat /proc/{pid}/maps')
    mapped = next((line for line in mappings.splitlines() if b'dalvik-main space' in line), None)
    if not mapped:
        print('Could not find the Dalvik main heap. Stop here.')
        return 1
    a, b = mapped.split()[0].split(b'-', 1)
    start, end = int(a, 16), int(b, 16)
    print(f'TCP Smart PID: {pid}; Dalvik heap starts at 0x{start:x}')
    print('Searching small regions around device-ID matches (no secrets shown or saved).\n')

    seen = {label: 0 for label in DEVICE_IDS.values()}
    total_key_fields = 0
    total_json_keys = 0
    for index, (lo, hi) in enumerate(windows(end-start), start=1):
        pages = (hi - lo) // PAGE
        cmd = (f'dd if=/proc/{pid}/mem bs={PAGE} '
               f'skip={(start+lo)//PAGE} count={pages} 2>/dev/null')
        data = adb('exec-out', 'sh', '-c', cmd)
        if len(data) != hi-lo:
            print(f'Region {index}: could only read {len(data)} of {hi-lo} bytes; stopping.')
            return 1
        matches = {label: data.count(device_id) for device_id, label in DEVICE_IDS.items()}
        for label, n in matches.items():
            seen[label] += n
        fields = {}
        for name in FIELD_NAMES:
            raw = name.encode('ascii')
            # Look for both ASCII/UTF-8 and UTF-16LE field labels, not values.
            n = data.count(raw) + data.count(name.encode('utf-16le'))
            if n:
                fields[name] = n
        json_lens = [len(m.group(1)) for m in JSON_KEY.finditer(data)]
        total_key_fields += fields.get('localKey', 0) + fields.get('local_key', 0)
        total_json_keys += len(json_lens)
        device_summary = ', '.join(f'{label}: {cnt}' for label, cnt in matches.items() if cnt) or 'none'
        field_summary = ', '.join(f'{name}: {n}' for name, n in fields.items()) or 'none'
        print(f'Region {index} (offsets {lo:,}–{hi:,}, {(hi-lo)//1024} KiB):')
        print(f'  known device IDs: {device_summary}')
        print(f'  nearby field labels: {field_summary}')
        print(f'  JSON localKey value lengths: {json_lens or "none"}')

    print('\nSummary:')
    print('  ' + ', '.join(f'{name}: {count} occurrence(s)' for name, count in seen.items()))
    print(f'  localKey labels: {total_key_fields}; JSON key-value candidates: {total_json_keys}')
    print('No key values or raw memory were displayed or saved. Share this output only.')
    if sum(seen.values()) == 0:
        print('Note: old offsets no longer contain device IDs; app memory layout may have changed.')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except FileNotFoundError:
        print('adb was not found on PATH.')
    except subprocess.TimeoutExpired:
        print('ADB timed out; is the emulator still running?')
    except Exception as exc:
        print(f'Probe failed: {exc}')
    sys.exit(1)
