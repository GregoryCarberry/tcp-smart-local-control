# Recovered CLI excerpts (safe subset)

Historical snippets extracted from the rendered shared conversation; these are not a single runnable script. Identifiers and private addresses are redacted. Other, more sensitive emulator/key-recovery commands remain in the private review archive pending separate review.

## Conversation turn 22 — PowerShell

```PowerShell
ping <PRIVATE_IP>
ping <PRIVATE_IP>
```

## Conversation turn 60 — Bash

```Bash
ssh yoga@<PRIVATE_IP>
```

## Conversation turn 60 — Bash

```Bash
docker compose version
free -h
df -h /home/yoga
ss -ltn '( sport = :8123 )'
```

## Conversation turn 60 — Bash

```Bash
mkdir -p ~/docker/homeassistant/config
cd ~/docker/homeassistant
```

## Conversation turn 60 — Bash

```Bash
nano compose.yml
```

## Conversation turn 60 — YAML

```YAML

services:
  homeassistant:
    container_name: homeassistant
    image: ghcr.io/home-assistant/home-assistant:stable
    restart: unless-stopped
    stop_grace_period: 60s
    network_mode: host

    environment:
      TZ: Europe/London

    volumes:
      - ./config:/config
      - /etc/localtime:/etc/localtime:ro
```

## Conversation turn 60 — Bash

```Bash
docker compose config
```

## Conversation turn 60 — Bash

```Bash
docker compose up -d
```

## Conversation turn 60 — Bash

```Bash
docker compose ps
```

## Conversation turn 60 — Bash

```Bash
docker logs --tail 50 homeassistant
```

## Conversation turn 74 — Bash

```Bash

python3 - <<'PY'
import socket

for ip in ["<PRIVATE_IP>", "<PRIVATE_IP>"]:
    try:
        with socket.create_connection((ip, 6668), timeout=3):
            print(f"{ip}: TCP 6668 OPEN")
    except OSError as e:
        print(f"{ip}: No connection ({e})")
PY
```

## Conversation turn 76 — Bash

```Bash
mkdir -p ~/venvs
python3 -m venv ~/venvs/tinytuya
~/venvs/tinytuya/bin/pip install tinytuya
```

## Conversation turn 76 — Bash

```Bash
~/venvs/tinytuya/bin/python -m tinytuya scan 15 \
  -force <PRIVATE_IP>/32 <PRIVATE_IP>/32 \
  -no-broadcasts
```

## Conversation turn 92 — Bash

```Bash
python3 - <<'PY'
import socket

with socket.create_connection(("<PRIVATE_IP>", 6668), timeout=3):
    print("Connected successfully")
PY
```

## Conversation turn 110 — Bash

```Bash

~/venvs/tinytuya/bin/python - <<'PY'
import tinytuya

plugs = [
    ("TCP plug 1", "<DEVICE_ID_REDACTED>", "<PRIVATE_IP>"),
    ("TCP Plug 2", "<DEVICE_ID_REDACTED>", "<PRIVATE_IP>")
]

for name, device_id, ip in plugs:
    print(f"\n--- {name} ({ip}) ---")
    try:
        plug = tinytuya.OutletDevice(
            dev_id=device_id,
            address=ip,
            local_key="",
            version=3.1
        )
        plug.set_socketTimeout(3)
        print(plug.status())
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
PY
```

## Conversation turn 110 — JSON

```JSON
{
  "dps": {
    "1": true,
    "2": 0
  }
}
```

## Conversation turn 112 — PowerShell

```PowerShell
adb version
```

## Conversation turn 114 — PowerShell

```PowerShell
adb devices -l
```

## Conversation turn 114 — PowerShell

```PowerShell
adb shell pm path com.tcp.smart
```

## Conversation turn 116 — PowerShell

```PowerShell

# Create a working directory
$dest = "$env:USERPROFILE\Desktop\TCP-Smart-APK"
New-Item -ItemType Directory -Force -Path $dest | Out-Null

# Retrieve both APK components directly from the phone
adb shell pm path com.tcp.smart | ForEach-Object {
    $remote = ($_ -replace '^package:', '').Trim()
    if ($remote) {
        adb pull $remote $dest
    }
}

# Check the extracted files
Get-ChildItem $dest | Select-Object Name, Length
```

## Conversation turn 116 — PowerShell

```PowerShell
Compress-Archive -Path "$dest\*.apk" `
  -DestinationPath "$env:USERPROFILE\Desktop\TCP-Smart-APK.zip" -Force
```

## Conversation turn 118 — PowerShell

```PowerShell
# Where the script saved the files
Get-ChildItem "$env:USERPROFILE\Desktop\TCP-Smart*"

# Where Windows says your actual Desktop is
[Environment]::GetFolderPath('Desktop')
```

## Conversation turn 118 — PowerShell

```PowerShell
explorer.exe "$env:USERPROFILE\Desktop"
```

## Conversation turn 128 — PowerShell

```PowerShell

$apkDir = "$env:USERPROFILE\Desktop\TCP-Smart-APK"

# Confirm both APKs are present
Get-ChildItem "$apkDir\*.apk"

# Install both components together
adb -e install-multiple "$apkDir\base.apk" "$apkDir\split_config.arm64_v8a.apk"
```

## Conversation turn 128 — PowerShell

```PowerShell
adb -e shell pm path com.tcp.smart
```

## Conversation turn 132 — PowerShell

```PowerShell

adb -e shell "find /data/user/0/com.tcp.smart -maxdepth 2 -type f | head -80"
```

## Conversation turn 136 — PowerShell

```PowerShell

# Count log entries mentioning local keys,
# without displaying their potentially sensitive contents.
(
    adb -e logcat -d -v raw |
    Select-String -Pattern '(?i)local[_-]?key'
).Count

# Check whether SELinux is enforcing access restrictions
adb -e shell getenforce
```

## Conversation turn 150 — PowerShell

```PowerShell

# List files in TCP Smart's MMKV directory
adb -e shell "ls -lah /data/user/0/com.tcp.smart/files/thingmmkv"

# Inspect the other database-like file
adb -e shell "ls -lh /data/user/0/com.tcp.smart/files/database"
```

## Conversation turn 152 — PowerShell

```PowerShell

# Search for TCP Plug 1 device ID
adb -e shell "grep -arlF '<DEVICE_ID_REDACTED>' /data/user/0/com.tcp.smart/files/thingmmkv"

# Search for TCP Plug 2 device ID
adb -e shell "grep -arlF '<DEVICE_ID_REDACTED>' /data/user/0/com.tcp.smart/files/thingmmkv"
```

## Conversation turn 158 — PowerShell

```PowerShell
adb -e shell 'p=$(pidof com.tcp.smart); echo PID:$p; grep -m1 dalvik-main /proc/$p/maps'
```

## Conversation turn 166 — PowerShell

```PowerShell
py .\tcp-smart-device-record-probe.py
```

## Conversation turn 172 — PowerShell

```PowerShell
Test-NetConnection <PRIVATE_IP> -Port 6668
```

## Conversation turn 174 — PowerShell

```PowerShell
py -m pip install --user tinytuya
```

## Conversation turn 174 — PowerShell

```PowerShell
py .\tcp-smart-lan-switch-test.py
```

## Conversation turn 200 — Bash

```Bash
cd ~/docker/homeassistant

docker compose ps

if [ -d config/custom_components ]; then
    find config/custom_components -mindepth 1 -maxdepth 1 -type d -printf '%f\n'
else
    echo "No custom_components directory yet"
fi
```

## Conversation turn 202 — Bash

```Bash
cd ~/docker/homeassistant

curl -fL --retry 3 \
  -o /tmp/localtuya-v5.2.5.tar.gz \
  https://github.com/rospogrigio/localtuya/archive/refs/tags/v5.2.5.tar.gz

mkdir -p config/custom_components

tar -xzf /tmp/localtuya-v5.2.5.tar.gz \
  -C config/custom_components \
  --strip-components=2 \
  localtuya-5.2.5/custom_components/localtuya

test -f config/custom_components/localtuya/manifest.json \
  && echo "LocalTuya files installed successfully"
```

## Conversation turn 204 — Bash

```Bash
cd ~/docker/homeassistant
docker compose restart homeassistant
docker compose ps
```
