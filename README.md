# Masters Research Project: Middleware-Based Sensor Data Abstraction in SDVs

## Overview

This project demonstrates a real-time sensor data abstraction pipeline for Software-Defined Vehicles (SDVs), using a Raspberry Pi and a Laptop. Raw image data is transmitted via DDS (on Pi) and Zenoh (on Laptop), semantically abstracted using Kuksa Databroker and Vehicle Signal Specification (VSS), and used for AI-based object detection.

## Technologies Used

- **DDS** (Fast DDS - C++) for real-time data exchange on Raspberry Pi  
- **Zenoh** (Python) for laptop-side communication  
- **Kuksa Databroker** for semantic vehicle signal management  
- **Vehicle Signal Specification (VSS)** for standard signal tree  
- **YOLOv5/YOLOv8** for object detection (Ultralytics)  
- **Python, C++, Docker, OpenCV, gRPC**

---

## Repository Structure

```
middleware-abstraction/
├── RPi/                       # Raspberry Pi pipeline implementation
│   ├── dds_rpi_publisher/     # C++ publisher that captures and sends JPEG image via DDS
│   ├── dds_rpi_subscriber/    # C++ DDS subscriber and Python script to forward image to Kuksa
│   │   ├── send_to_kuksa.py   # Forwards DDS image to Kuksa Databroker via gRPC
│   ├── detect_from_kuksa.py   # YOLOv5 object detection on image received from Kuksa
│   ├── run_rpi_pipeline.sh    # Orchestrates full pipeline in separate terminals
│   ├── vss/                   # Contains customized VSS tree (`vss_release_4.0.json`)
│   ├── vss_sync/              # Script to sync VSS signals between RPi and Laptop
│   └── README.md              # Documentation for Raspberry Pi pipeline
│
├── Laptop/                    # Laptop pipeline implementation
│   ├── publisher.py           # Captures webcam image, encodes and publishes over Zenoh
│   ├── subscriber.py          # Receives image from Zenoh, decodes, and saves locally
│   ├── send_image_to_kuksa.py # Sends saved image to Kuksa Databroker via gRPC
│   ├── detect_from_kuksa.py   # Performs object detection on Kuksa image signal
│   ├── laptop_sync.py         # Syncs VSS values from Laptop to RPi and vice versa
│   ├── run_laptop_pipeline.sh # Orchestrates full pipeline for Laptop
│   └── README.md              # Documentation for Laptop pipeline
│
└── README.md                  # Overall repository-level documentation
```

## How the System Works

* The Raspberry Pi and Laptop both capture image frames using onboard cameras.
* Each device publishes the image via a lightweight middleware protocol (DDS on RPi, Zenoh on Laptop).
* A subscriber on each device receives the image, optionally saves it, and forwards it to the Kuksa Databroker using a custom VSS signal tree.
* The object detection application retrieves the image signal from Kuksa, processes it, and publishes back the object count to another VSS signal.
* A sync script may optionally be used to exchange VSS signals between the two devices to ensure each can access the other's data.

## Kuksa Databroker

The Kuksa Databroker is run using Docker and requires an updated `vss_release_4.0.json` file. This file must be placed under:

```
<kuksa-databroker-repo>/data/vss-core/vss_release_4.0.json
```

It must contain the following custom signals:

* `Vehicle.Camera.RPi.Image`
* `Vehicle.Camera.RPi.ObjectCount`
* `Vehicle.Camera.Laptop.Image`
* `Vehicle.Camera.Laptop.ObjectCount`

This edited VSS file should replace the original in both the Raspberry Pi and Laptop pipelines to ensure consistent VSS structure.

All paths are defined in accordance with the COVESA Vehicle Signal Specification.

## Requirements

* Docker (for running Kuksa Databroker and CLI)
* Python 3.8+
* OpenCV, NumPy, Kuksa-client, YOLO (Ultralytics), Zenoh
* CMake + g++ (for compiling RPi DDS publisher/subscriber)

## Python Environment

All Python-based components were executed in a dedicated virtual environment:

```bash
source ~/kuksa_venv/bin/activate
```

Ensure this environment is created and activated before running the scripts. The `kuksa_venv` folder is not included in this repository.

## Running the Pipelines

Use `run_rpi_pipeline.sh` or `run_laptop_pipeline.sh` from their respective directories. Each script opens 7 terminal windows and launches the components in sequence.

## Evaluation

* Measured latency (DDS-to-Kuksa, detection loop)

* Object count consistency across devices

* Real-time VSS signal sync via gRPC

## Documentation

* All formal documents related to this research are in folder "Documentation".

## Notes

* DDS was used for Raspberry Pi due to its lightweight C++ integration.
* Zenoh was used on the Laptop for rapid testing and publish-subscribe functionality.
* The system design ensures abstraction of raw sensor data through VSS.
* All components are modular and can be adapted for other sensors or platforms.

