# Home Assistant integration — verified configuration

**Status: confirmed working on both plugs, 24 October 2026.** This records what was done in one installation, not a guarantee for all TCP-branded firmware revisions.

## Server architecture

- Existing Home Assistant **Container** deployment running on a Debian host under Docker Compose.
- HA and the two TCP Smart plugs were on separately routed home-lab and IoT VLANs.
- The host could communicate with the plugs' local API over **TCP port 6668** before changing HA.
- No cloud API credentials were configured for the LocalTuya integration.

## Implementation

1. Check Home Assistant is running and whether `config/custom_components` already contains other integrations.
2. Obtain the [LocalTuya](https://github.com/rospogrigio/localtuya) integration using its documented manual-installation approach. Install its `custom_components/localtuya` directory in HA's persistent configuration; restart **only Home Assistant**, not the whole server.
3. In **Settings → Devices & services → Add integration**, select **LocalTuya**.
4. On the cloud configuration screen, choose **Do not configure a Cloud API account**.
5. From the integration's device configuration, choose to add a device manually if discovery doesn't cross VLANs.
6. For each plug, enter its own private local key, its LAN address and device identifier. Choose **protocol 3.1**.
7. Choose entity platform **Switch** and map **ID / DPS 1** to the relay. For the TCP Plug 2 this was the detected Boolean state. Do **not** assign DPS 2 to current, consumption or voltage without confirming its function.
8. Test both states and physical switching. The TCP Plug 2 was specifically tested from the Home Assistant UI on the owner's phone. The TCP Plug 1 was subsequently reported working too.

The device credentials were entered privately through Home Assistant's UI. The original local-key JSON file was **not transferred** to the Debian host.

## Configuration fields (sanitised)

| Field | TCP Plug 2 | TCP Plug 1 |
| --- | --- | --- |
| Friendly name | TCP Plug 2 | TCP Plug 1 |
| LAN address | Private / omitted | Private / omitted |
| Device ID | Private / omitted | Private / omitted |
| Local key | Private / omitted | Private / omitted |
| Protocol | 3.1 | 3.1 |
| Entity | Switch | Switch |
| Relay DPS | 1 | 1 |
| Other DPS measurements | Unconfigured | Unconfigured |

## Operational notes

- Stop the vendor app while pairing/configuring in LocalTuya if simultaneous sessions cause issues. The original app was deliberately stopped during the initial setup.
- Secure your HA configuration/backups appropriately: local keys are credentials even when they are not submitted to a cloud API.
- If a future factory reset/re-pair rotates a key, existing HA configuration may need updating.
- The *command path* was local. A deliberate **internet-block test has not been done**, so do not infer every aspect of the original application or device behaviour is offline-independent.
- No measured comparison was done for app vs Home Assistant response latency.

### DPS 2 countdown control (28 October 2026)

TCP Plug 2 has DPS 2 configured as a LocalTuya Number entity (minimum 0, maximum 18000, increment 1; restore-last-value and passive-entity options off). It displays OEM countdown changes. Home Assistant's number.set_value with 60 did not start the timer even though the action completed. Direct localtuya.set_dp writing integer 60 to DPS 2 did start it, and the relay toggled after the countdown expired. This was verified by the user. The reason the Number write failed has not been diagnosed. No dashboard script or cancellation-by-zero action has yet been tested. The user confirmed Home Assistant and the Standing Lamp entity were restored after investigation.
