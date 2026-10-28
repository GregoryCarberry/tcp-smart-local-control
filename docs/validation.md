# Results, evidence and remaining work

## Verified by direct observation or user-confirmed testing

| Check | TCP Plug 2 | TCP Plug 1 |
| --- | --- | --- |
| Device reachable over local TCP/6668 | Yes | Yes |
| Protocol 3.1 `status()` | Yes | Yes |
| DPS 1 identifies relay state | Yes | Yes |
| Candidate key associated with the correct device record | Yes | Yes |
| TinyTuya local encrypted relay control | **PASS**, off/on physically observed | **PASS**, user confirmed |
| Original pairing retained | Yes | Yes |
| Works as LocalTuya switch in Home Assistant | **PASS**, tested from phone | **PASS**, user confirmed |

For TCP Plug 2, the original TCP Smart app was open during a *separate* TinyTuya test and its icon tracked the relay's off/on transition. **This did not establish whether the vendor app learned the change through LAN, cloud notifications or polling.**

## Open questions — not completion criteria

1. **Offline operation:** preserve LAN connectivity and selectively block internet access to a test plug via the existing firewall. Compare HA switching, status updates, vendor-app behaviour and reconnection. Record rules and rollback. *Not performed yet.*
2. **Latency:** compare controlled repetitions of vendor-app and Home Assistant commands. Define start and end events and account for phone UI and Wi-Fi variability. Perceived improvements have not yet been benchmarked.
3. **Firmware variation:** test other hardware/firmware revisions individually before claiming compatibility.
4. **Weekly timer scheduling and offline behaviour:** investigate where recurring schedules execute and whether the confirmed DPS 2 countdown completes with cloud connectivity blocked. DPS 2 has now been identified for TCP Plug 2; see experiment below.

## Countdown datapoint experiment — 28 October 2026

**Verified on TCP Plug 2 only:** DPS 1 is the relay's Boolean state; **DPS 2 is the OEM app's countdown-to-toggle value, in seconds**. This replaces the earlier “unknown datapoint” status. No claim is made for other firmware or for TCP Plug 1 without testing.

A Windows TinyTuya read-only monitor polled `status()` approximately every 10 seconds while the original TCP Smart Android app controlled the countdown. Observed data (local clock):

| Time | DPS 1 | DPS 2 | Event |
| --- | --- | --- | --- |
| 17:52:36 | true | 18000 | Accidental five-hour timer (5 × 3600 s) |
| 17:53:07 | true | 17970 | Reported value down by 30 s |
| 17:53:28 | true | 17940 | Reported value down by another 30 s |
| 17:53:38 | true | 0 | Five-hour timer cancelled in OEM app |
| 17:53:59 | true | 300 | Five-minute timer set |
| 17:54:29 | true | 270 | Countdown reported in 30 s steps |
| 17:55:10 | false | 0 | **Manual cancellation/relay action in app**; NOT evidence of five-minute expiry |
| 17:59:11 | false | 0 | Separate one-minute test; no timer |
| 17:59:32 | false | 60 | One-minute countdown begun |
| 18:00:03 | false | 30 | Reported remaining countdown |
| 18:00:34 | true | 0 | **Unassisted expiry**: relay toggled ON and countdown reset |
| 18:00:44 | true | 0 | Post-expiry state stable |

The *reported* remaining value stepped by 30 seconds in these observations; the test does not establish the internal timer's clock resolution or whether the device needs internet access to complete a countdown. Weekly scheduling location (device versus cloud) is **not yet tested**. The OEM app initiated the timer; this test did not write to DPS 2 using TinyTuya.

**Connection troubleshooting:** Windows could reach plug TCP/6668 (`Test-NetConnection` succeeded), but the monitor initially returned TinyTuya `901 Network Error: Unable to Connect` while Home Assistant's LocalTuya integration was operating the plug. Disabling the individual HA device did not restore TinyTuya reads. Temporarily stopping the HA Docker container restored DPS reads immediately. This strongly implicates competing local controller connections but is not proof of precise root cause. The user was instructed to restart HA and re-enable the disabled plug; **successful restoration was not confirmed in this record**. No pairing, key or network configuration was changed.

## Suggested evidence for eventual screenshots

- HA dashboard with **two working switch entities**, cropped to omit network addresses and other devices.
- A photo of the physical setup if it does not reveal identifying details.
- A short, anonymised demonstration of Python status output and toggling, without credentials or device IDs.
- No screenshot of the Home Assistant LocalTuya **device key configuration form** unless the credential field is fully masked and the original image is deleted from publication assets.
