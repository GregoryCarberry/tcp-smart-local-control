#!/usr/bin/env python3
"""Validate TCP Smart Standing lamp local key with one reversible LAN toggle.

Reads existing private key JSON from %LOCALAPPDATA%/TCP-Smart/device-local-keys.json.
Does not print, transmit externally, or save local keys. Uses direct TCP to
<STANDING_LAMP_IP> on the LAN with TinyTuya 3.1. Does not touch USB hub plug.
"""

import json
import os
from pathlib import Path
import sys
import time

try:
    import tinytuya
except ImportError:
    print("TinyTuya is missing. Install: py -m pip install --user tinytuya")
    sys.exit(2)

DEVICE_NAME = "USB hub"
EXPECTED_DEVICE_ID = "<USB_HUB_DEVICE_ID>"
EXPECTED_IP = "<USB_HUB_IP>"
SECRET_PATH = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "TCP-Smart" / "device-local-keys.json"


def status_bool(device):
    response = device.status()
    if not isinstance(response, dict):
        raise RuntimeError("Status returned an unexpected response")
    dps = response.get("dps")
    if not isinstance(dps, dict) or type(dps.get("1")) is not bool:
        raise RuntimeError("DPS 1 relay state missing or invalid")
    return dps["1"]


def label(state):
    return "ON" if state else "OFF"


def main():
    try:
        with SECRET_PATH.open("r", encoding="utf-8") as f:
            records = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print(f"Could not open saved private JSON ({type(e).__name__}). Expected: {SECRET_PATH}")
        return 2

    record = records.get(DEVICE_NAME) if isinstance(records, dict) else None
    if not isinstance(record, dict):
        print("Standing lamp entry missing in saved JSON; no action taken.")
        return 2

    if (record.get("device_id") != EXPECTED_DEVICE_ID or
            record.get("ip") != EXPECTED_IP or
            str(record.get("protocol")) != "3.1"):
        print("Unexpected Standing lamp device ID, IP or protocol; no action taken.")
        return 2
    key = record.get("local_key")
    if not isinstance(key, str) or len(key) != 16:
        print("Standing lamp key is not a 16-character string; no action taken.")
        return 2

    device = tinytuya.OutletDevice(
        dev_id=EXPECTED_DEVICE_ID,
        address=EXPECTED_IP,
        local_key=key,
        version=3.1,
    )
    device.set_socketTimeout(3)
    device.set_socketRetryLimit(1)

    print("Direct LAN test: Standing lamp (<STANDING_LAMP_IP>), protocol 3.1")
    print("USB hub will not be contacted. No keys will be shown.")

    try:
        original = status_bool(device)
    except Exception as e:
        print(f"Could not read initial state ({type(e).__name__}); no switching attempted.")
        return 1

    print(f"Original Standing lamp state: {label(original)}")
    target = not original
    print(f"Attempting {label(target)} for approximately 2 seconds, then restoring {label(original)}...")

    # Once attempted, always issue a restoration command even if an exception
    # occurs, in case the switch did change before a response was lost.
    changed = False
    try:
        device.set_status(target, switch=1)
        time.sleep(2)
        observed = status_bool(device)
        changed = observed == target
        print(f"Observed after command: {label(observed)}")
    except Exception as e:
        print(f"Toggle/verification encountered {type(e).__name__}.")
    finally:
        try:
            device.set_status(original, switch=1)
            time.sleep(1)
            final_state = status_bool(device)
            print(f"Restored state: {label(final_state)}")
            restored = final_state == original
        except Exception as e:
            print(f"WARNING: Restoration couldn't be verified ({type(e).__name__}).")
            print("Check the lamp using TCP Smart and restore manually if necessary.")
            restored = False

    if changed and restored:
        print("PASS: Standing lamp responded to local encrypted control and was restored.")
        return 0
    if restored:
        print("NOT CONFIRMED: Lamp is in its original state but local switching wasn't verified.")
    else:
        print("WARNING: Final state not confirmed. Please check lamp in the TCP Smart app.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
