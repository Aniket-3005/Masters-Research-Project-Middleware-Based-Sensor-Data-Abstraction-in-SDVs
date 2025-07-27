import base64
import cv2
import numpy as np
import time
from kuksa_client.grpc import VSSClient, Datapoint
from ultralytics import YOLO

# Kuksa VSS signal paths
SIGNAL_PATH = "Vehicle.Camera.RPi.Image"
DETECTION_SIGNAL_PATH = "Vehicle.Camera.RPi.ObjectCount"

# Base64 decode function
def decode_base64_image(encoded_str):
    try:
        img_bytes = base64.b64decode(encoded_str)
        img_array = np.frombuffer(img_bytes, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        print("Error decoding base64 image:", e)
        return None

def main():
    model = YOLO("yolov5n.pt")

    with VSSClient("localhost", 55555) as client:
        print("Starting detection loop from Kuksa...")
        while True:
            try:
                value = client.get_current_values([SIGNAL_PATH])
                dp = value.get(SIGNAL_PATH)

                if dp is None or dp.value is None:
                    print("No image data in signal. Waiting...")
                    time.sleep(0.1)
                    continue

                encoded_img = dp.value
                img = decode_base64_image(encoded_img)
                if img is None:
                    print("Could not decode image. Skipping.")
                    time.sleep(0.1)
                    continue

                # Run object detection
                results = model.predict(img, imgsz=320, save=False, conf=0.3)

                for r in results:
                    annotated = r.plot()
                    obj_count = len(r.boxes)

                    # Send detection count to Kuksa
                    client.set_current_values({
                        DETECTION_SIGNAL_PATH: Datapoint(obj_count)
                    })
                    print(f"Detected {obj_count} objects and sent to Kuksa")

                    # Display result
                    cv2.imshow("YOLO Detection from VSS Image", annotated)
                    if cv2.waitKey(33) & 0xFF == ord('q'):
                        break

                time.sleep(0.1)

            except Exception as e:
                print("Error in detection loop:", e)
                time.sleep(0.1)

if __name__ == "__main__":
    main()
