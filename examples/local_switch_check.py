#!/usr/bin/env python3
"""Sanitised, reconstructed TinyTuya status / local switching demonstration.

Read-only by default. --toggle requires explicit opt-in and attempts to restore
starting relay state. Test only equipment that can safely be power-cycled.

This is NOT the original 2026 memory-inspection/key-recovery script.
"""

from __future__ import annotations

import argparse
import getpass
import os
import sys
import time


def relay_state(result: object) -> bool:
    """Read the observed Boolean relay value from DPS 1, rejecting error payloads."""
    if not isinstance(result, dict):
        raise ValueError("Device did not return a status dictionary")
    dps = result.get("dps")
    if not isinstance(dps, dict) or type(dps.get("1")) is not bool:
        raise ValueError("DPS 1 is missing or not a Boolean relay state")
    return dps["1"]


def status(device) -> bool:
    return relay_state(device.status())


def confirm_state(device, desired: bool, tries: int = 5) -> bool:
    for attempt in range(tries):
        try:
            if status(device) is desired:
                return True
        except (ValueError, OSError):
            pass
        if attempt + 1 < tries:
            time.sleep(0.35)
    return False


def toggle_and_restore(device, delay: float) -> bool:
    original = status(device)
    opposite = not original
    print(f"Original relay state: {'ON' if original else 'OFF'}")
    print("Testing a temporary relay change. Power to the connected load will change.")
    attempted = False
    switched = False
    restored = False
    try:
        attempted = True
        device.set_status(opposite, 1)
        switched = confirm_state(device, opposite)
        print(f"Temporary switch verified: {switched}")
        time.sleep(delay)
    finally:
        if attempted:
            try:
                device.set_status(original, 1)
                restored = confirm_state(device, original)
            except Exception as exc:  # best-effort restoration even after earlier errors
                print(f"WARNING: restore command failed ({type(exc).__name__})", file=sys.stderr)
    if not restored:
        print("WARNING: original state NOT verified — check the physical plug now", file=sys.stderr)
        return False
    print(f"Original state restored: {'ON' if original else 'OFF'}")
    return switched


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--toggle", action="store_true", help="briefly change and restore physical relay")
    parser.add_argument("--hold", type=float, default=1.0, help="seconds in changed state (0–10; default 1)")
    args = parser.parse_args()
    if not 0 <= args.hold <= 10:
        parser.error("--hold must be between 0 and 10 seconds")

    device_id = os.environ.get("TUYA_DEVICE_ID") or input("Device ID (not printed): ").strip()
    address = os.environ.get("TUYA_DEVICE_IP") or input("Plug LAN IP / host: ").strip()
    key = os.environ.get("TUYA_LOCAL_KEY") or getpass.getpass("Device local key (hidden): ")
    if not device_id or not address or len(key) != 16:
        print("Missing device ID/address or unexpected key length", file=sys.stderr)
        return 2
    try:
        import tinytuya
    except ImportError:
        print("Please install dependencies: python -m pip install -r requirements.txt", file=sys.stderr)
        return 2

    plug = tinytuya.OutletDevice(dev_id=device_id, address=address, local_key=key, version=3.1)
    plug.set_socketTimeout(3)
    try:
        if args.toggle:
            ok = toggle_and_restore(plug, args.hold)
            print("PASS" if ok else "FAIL")
            return 0 if ok else 1
        print(f"Relay state: {'ON' if status(plug) else 'OFF'} (read only)")
        return 0
    except Exception as exc:
        print(f"Test failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        print("If a toggle was attempted, verify the physical relay state.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
