# Laptop Pipeline for Sensor Data Abstraction

This directory contains the complete implementation of the Laptop-side sensor data abstraction pipeline. It captures webcam images, transmits them using Zenoh, forwards them to Kuksa Databroker, and performs object detection.

## Directory Structure

```
Laptop/
├── publisher.py              # Captures webcam image and publishes via Zenoh
├── subscriber.py             # Receives image, saves to file
├── send_image_to_kuksa.py    # Sends image to Kuksa Databroker
├── detect_from_kuksa.py      # Performs object detection on image from Kuksa
├── run_laptop_pipeline.sh    # Launches all components in terminal windows
├── laptop_sync.py            # Syncs VSS signals between Laptop and RPi
```

## Running the Full Pipeline

Launch the entire system with:

```bash
bash run_laptop_pipeline.sh
```

This script opens seven terminal windows that execute:

1. Kuksa Databroker
2. Kuksa CLI
3. `publisher.py` – captures image from webcam and sends via Zenoh
4. `subscriber.py` – receives image from Zenoh and saves to file
5. `send_image_to_kuksa.py` – sends image file to Kuksa
6. `detect_from_kuksa.py` – detects objects from Kuksa image signal
7. `laptop_sync.py` – optional script for syncing signals between Laptop and RPi

## VSS Signal

The pipeline uses the following custom signals in the VSS tree:

* `Vehicle.Camera.Laptop.Image` (string): base64-encoded JPEG image
* `Vehicle.Camera.Laptop.ObjectCount` (int): number of detected objects

These signals must be defined in the `vss_release_4.0.json` file provided to the Kuksa Databroker. Replace the default file in the Kuksa Databroker’s data directory with the one used for this project.

## Image Flow and Paths

* Webcam images are captured and published to Zenoh (`demo/cam/image`)
* Subscriber saves images to: `/home/aniket-barve/zenoh_share/laptop_image.jpg`
* `send_image_to_kuksa.py` reads from the same path and sends to Kuksa
* `detect_from_kuksa.py` reads the signal from Kuksa, runs detection, and writes result back

## Component Descriptions

### publisher.py

Captures webcam frames, encodes them to JPEG and then base64, and publishes to Zenoh topic `demo/cam/image`.

### subscriber.py

Receives the Zenoh messages, decodes the base64-encoded JPEG image, and saves it to the specified path.

### send\_image\_to\_kuksa.py

Monitors the saved image file. When a new image is available, it encodes it to base64 and sends it to Kuksa Databroker.

### detect\_from\_kuksa.py

Retrieves the image signal from Kuksa Databroker, decodes it, and performs object detection using YOLOv8. The detected object count is sent back to Kuksa.

### laptop\_sync.py

Fetches VSS signals from the local Kuksa Databroker and syncs them to the Raspberry Pi Databroker, and vice versa.

## Python Environment

All scripts were executed within a dedicated Python virtual environment named `kuksa_venv`. This environment should include all necessary dependencies such as:

* kuksa-client
* ultralytics
* opencv-python
* numpy
* zenoh-py

To activate the environment:

```bash
source ~/kuksa_venv/bin/activate
```

Make sure this environment is set up before running any of the scripts.

## Dependencies and Setup

Before running the pipeline, ensure that the following repositories and tools are set up:

* Clone [kuksa-databroker](https://github.com/eclipse-kuksa/kuksa-databroker) into your home directory.
* Install Rust and build the Databroker using `cargo build`.
* Install Docker to run the Kuksa CLI container.
* Install the Zenoh Python client using `pip install eclipse-zenoh`.

## Notes

* All paths such as image storage and signal names are hardcoded in scripts and should be changed if adapting to another system.
* This setup was tested on Ubuntu with Zenoh, Docker, Python 3.9, and a USB webcam.
* The same edited `vss_release_4.0.json` file must be used in both Laptop and RPi pipelines.

