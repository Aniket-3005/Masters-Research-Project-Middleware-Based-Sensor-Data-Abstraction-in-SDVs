import base64
import os
import time
from kuksa_client.grpc import VSSClient, Datapoint

IMG_PATH = "/tmp/rpi_image.jpg"
SIGNAL_PATH = "Vehicle.Camera.RPi.Image"

def read_image_as_base64():
    try:
        with open(IMG_PATH, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except FileNotFoundError:
        print("Image not yet available.")
        return None

def main():
    print("Watching /tmp/rpi_image.jpg and sending to Kuksa...")
    last_mod_time = 0

    with VSSClient("localhost", 55555) as client:
        while True:
            if not os.path.exists(IMG_PATH):
                time.sleep(1)
                continue

            mod_time = os.path.getmtime(IMG_PATH)
            if mod_time != last_mod_time:
                last_mod_time = mod_time
                encoded = read_image_as_base64()
                if encoded:
                    client.set_current_values({
                        SIGNAL_PATH: Datapoint(encoded)
                    })
                    print("Sent updated image to Kuksa")

            time.sleep(0.5)

if __name__ == "__main__":
    main()
