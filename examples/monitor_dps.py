#!/usr/bin/env python3
"""Read-only Tuya LAN datapoint monitor for devices you own or administer.

Requires: pip install tinytuya
Prompts for connection details and never saves or prints the local key.
No switching commands are issued. Ctrl+C stops polling.
"""

import argparse
import getpass
import time

import tinytuya


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--interval", type=float, default=10, help="Seconds between readings (default: 10)")
    args = parser.parse_args()
    if args.interval <= 0:
        parser.error("--interval must be positive")

    device_id = input("Device ID: ").strip()
    address = input("Device LAN IP/hostname: ").strip()
    version = input("Protocol version [3.1]: ").strip() or "3.1"
    local_key = getpass.getpass("Local key (hidden): ")
    if not all((device_id, address, local_key)):
        parser.error("Device ID, LAN address and local key are required")

    device = tinytuya.OutletDevice(
        dev_id=device_id,
        address=address,
        local_key=local_key,
        version=float(version),
    )
    device.set_socketTimeout(5)
    device.set_socketRetryLimit(1)
    print("Monitoring datapoints (read-only). Press Ctrl+C to stop.")

    try:
        while True:
            result = device.status()
            now = time.strftime("%H:%M:%S")
            if isinstance(result, dict) and isinstance(result.get("dps"), dict):
                print(now, result["dps"], flush=True)
            elif isinstance(result, dict):
                # Do not dump raw responses: they can contain device information.
                print(now, "Status error", result.get("Err", "unknown"), flush=True)
            else:
                print(now, "Unexpected status response", flush=True)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")


if __name__ == "__main__":
    main()
