#!/bin/bash

echo "Starting full RPi camera > DDS > Kuksa > Detection pipeline..."

# 1: Kuksa Databroker
x-terminal-emulator -T "Kuksa Databroker" -e bash -c \
"cd ~/kuksa-databroker && docker run --network host \
-v ./data/vss-core/vss_release_4.0.json:/data/vss.json \
ghcr.io/eclipse-kuksa/kuksa-databroker:main \
--insecure --metadata /data/vss.json"
sleep 3

# 2: Kuksa CLI
x-terminal-emulator -T "Kuksa CLI" -e bash -c \
"docker run -it --rm --network host ghcr.io/eclipse-kuksa/kuksa-databroker-cli:main --server localhost:55555"
sleep 3

# 3: RPi DDS Publisher
x-terminal-emulator -T "DDS Publisher" -e bash -c \
"cd ~/Middleware-abstraction/RPi/dds_rpi_publisher && ./dds_rpi_publisher"
sleep 3

# 4: RPi DDS Subscriber
x-terminal-emulator -T "DDS Subscriber" -e bash -c \
"cd ~/Middleware-abstraction/RPi/dds_rpi_subscriber && ./dds_rpi_subscriber"
sleep 3

# 5: Send to Kuksa
x-terminal-emulator -T "Send to Kuksa" -e bash -c \
"cd ~/Middleware-abstraction/RPi/dds_rpi_subscriber && python3 send_to_kuksa.py"
sleep 3

# 6: Object Detection
x-terminal-emulator -T "Detection" -e bash -c \
"cd ~/Middleware-abstraction/RPi && python3 detect_from_kuksa.py"
sleep 3

# 7: VSS Sync Script
x-terminal-emulator -T "VSS Sync" -e bash -c \
"cd ~/Middleware-abstraction/RPi/vss_sync && python3 rpi_sync.py"

