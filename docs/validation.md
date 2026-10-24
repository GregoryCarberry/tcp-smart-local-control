# Results, evidence and remaining work

## Verified by direct observation or user-confirmed testing

| Check | TCP Plug 2 (TCP Plug 2) | TCP Plug 1 (TCP Plug 1) |
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
4. **Unknown datapoint:** investigate DPS 2 only if useful; do not label it as an electrical sensor without evidence.

## Suggested evidence for eventual screenshots

- HA dashboard with **two working switch entities**, cropped to omit network addresses and other devices.
- A photo of the physical setup if it does not reveal identifying details.
- A short, anonymised demonstration of Python status output and toggling, without credentials or device IDs.
- No screenshot of the Home Assistant LocalTuya **device key configuration form** unless the credential field is fully masked and the original image is deleted from publication assets.
