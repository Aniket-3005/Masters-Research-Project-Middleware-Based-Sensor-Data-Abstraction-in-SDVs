import os
import base64
import time
from kuksa_client.grpc import VSSClient, Datapoint

IMG_PATH = "/home/aniket-barve/zenoh_share/laptop_image.jpg"
SIGNAL_PATH = "Vehicle.Camera.Laptop.Image"

def read_image_as_base64():
    try:
        with open(IMG_PATH, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except FileNotFoundError:
        print("Image not yet available.")
        return None

def main():
    print("[Kuksa] Watching image and sending to Databroker...")
    last_mod_time = 0
    with VSSClient("localhost", 55555) as client:
        while True:
            if not os.path.exists(IMG_PATH):
                time.sleep(0.2)
                continue

            mod_time = os.path.getmtime(IMG_PATH)
            if mod_time != last_mod_time:
                last_mod_time = mod_time
                encoded = read_image_as_base64()
                if encoded:
                    client.set_current_values({SIGNAL_PATH: Datapoint(encoded)})
                    print("Image sent to Kuksa")
            time.sleep(0.2)

if __name__ == "__main__":
    main()
