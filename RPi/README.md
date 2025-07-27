# Raspberry Pi Pipeline for Sensor Data Abstraction

This directory contains the complete implementation of the Raspberry Pi side of the sensor data abstraction pipeline. It includes data capture, DDS-based transmission, integration with Kuksa Databroker using VSS, and object detection.

## Directory Overview

```
RPi/
├── dds_rpi_publisher/        # C++ DDS publisher for JPEG image frames
├── dds_rpi_subscriber/       # DDS subscriber and script to forward data to Kuksa
├── detect_from_kuksa.py      # Object detection script that reads from Kuksa
├── run_rpi_pipeline.sh       # Script to launch the full pipeline
├── vss/                      # Contains the VSS JSON file used by Kuksa
├── vss_sync/                 # Optional utilities for VSS signal syncing
```

## Running the Full Pipeline

To start the entire pipeline from DDS publishing to object detection, run the following script:

```bash
bash run_rpi_pipeline.sh
```

This script opens seven terminal windows to launch:

1. Kuksa Databroker (via Docker)
2. Kuksa CLI (via Docker)
3. DDS Publisher (C++)
4. DDS Subscriber
5. Python script to forward DDS data to Kuksa
6. Object detection script reading from Kuksa
7. VSS Sync script

## DDS Publisher

Location: `dds_rpi_publisher/`

Contains the C++ application that captures image frames and publishes them using Fast DDS. The DDS message format is defined in `RawImageMsg.hpp` and `RawImageMsgPubSubTypes.hpp`. A compiled binary `dds_rpi_publisher` is also included.

Before building, ensure you have Fast DDS and Fast CDR installed. You can follow the official installation steps here:
[https://fast-dds.docs.eprosima.com/en/stable/installation/sources/sources\_linux.html](https://fast-dds.docs.eprosima.com/en/stable/installation/sources/sources_linux.html)

To build manually:

```bash
cd dds_rpi_publisher
cmake .
make
./dds_rpi_publisher
```

## DDS Subscriber and Forwarding to Kuksa

Location: `dds_rpi_subscriber/`

This folder includes the subscriber logic and the script responsible for forwarding image data to the Kuksa Databroker. The main Python script, `send_to_kuksa.py`, reads a base64-encoded JPEG image from a specified file path and writes it to a VSS signal using gRPC. By default, the script monitors `/tmp/rpi_image.jpg`, which should be continuously updated by the DDS subscriber. This path can be modified in the script if needed, but it must match the output path used by the subscriber.

The [kuksa-databroker](https://github.com/eclipse-kuksa/kuksa-databroker) runs in a Docker container, but its repository was cloned locally to access configuration examples and signal files. The included file `vss_release_4.0.json` contains the required custom signals and must be used to replace the default `vss.json` in the `data/vss-core/` directory before starting the container.

## Object Detection

Script: `detect_from_kuksa.py`

This script reads image data from the Kuksa Databroker using the VSS signal `Vehicle.Camera.RPi.Image`, decodes the image, and performs object detection.

## VSS Tree and Signal Definitions

Located in `vss/vss_release_4.0.json`.

Includes custom VSS signals such as:

* `Vehicle.Camera.RPi.Image`: for transmitting the image (string, base64 encoded)
* `Vehicle.Camera.RPi.ObjectCount`: for storing the number of detected objects (integer)

This file is mounted into Kuksa Databroker on startup.

## VSS Sync Script

Location: `vss_sync/rpi_sync.py`

This script continuously synchronizes VSS signal values between the Raspberry Pi and the Laptop. It reads the image and object count values from the local Kuksa Databroker and writes them to the corresponding signals on the Laptop's Databroker, and vice versa. This allows both devices to have consistent access to each other's sensor data.

The script is included as part of the full pipeline and is automatically launched by `run_rpi_pipeline.sh` in the seventh terminal window.

## Notes

* The `.idl` file used to generate the DDS message types, `RawImageMsg.idl`, is included in the project directory alongside the generated header and source files.
* The folder assumes you have Docker, g++, cmake, and Python 3 installed with required libraries.
* All components were tested on Raspberry Pi OS in a real-time capture and inference setting.


