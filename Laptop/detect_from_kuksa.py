import base64
import numpy as np
import cv2
import time
from kuksa_client.grpc import VSSClient, Datapoint
from ultralytics import YOLO

SIGNAL_PATH = "Vehicle.Camera.Laptop.Image"
DETECTION_SIGNAL = "Vehicle.Camera.Laptop.ObjectCount"

def decode_base64_image(encoded_str):
    try:
        img_bytes = base64.b64decode(encoded_str)
        img_array = np.frombuffer(img_bytes, dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        print("Error decoding image:", e)
        return None

def main():
    print("[Kuksa] Loading YOLO model...")
    model = YOLO("yolov8n.pt")  # Or yolov5s.pt
    print("[Kuksa] Model loaded!")

    last_image_data = None  # To skip duplicate images

    with VSSClient("localhost", 55555) as client:
        print("[Kuksa] Starting detection loop from signal...")
        while True:
            value = client.get_current_values([SIGNAL_PATH])
            dp = value.get(SIGNAL_PATH)

            if dp is None or dp.value is None:
                print("Waiting for image data from Kuksa...")
                time.sleep(0.01)
                continue

            # Skip if image data hasn't changed
            if dp.value == last_image_data:
                time.sleep(0.01)
                continue
            last_image_data = dp.value

            img = decode_base64_image(dp.value)
            if img is None:
                print("Decode failed. Waiting...")
                time.sleep(0.01)
                continue

            # Run object detection
            results = model.predict(img, imgsz=320, conf=0.3, save=False)

            for r in results:
                annotated = r.plot()
                obj_count = len(r.boxes)
                print(f"Objects detected: {obj_count}")

                # Show the image with bounding boxes
                cv2.imshow("Kuksa Detection", annotated)
                key = cv2.waitKey(1)
                if key == 27:  # ESC key
                    print("ESC pressed. Exiting.")
                    cv2.destroyAllWindows()
                    return

                # Send result back to Kuksa
                client.set_current_values({
                    DETECTION_SIGNAL: Datapoint(obj_count)
                })

            time.sleep(0.01)

if __name__ == "__main__":
    main()
