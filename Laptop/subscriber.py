import cv2
import base64
import numpy as np
import zenoh
import threading
import signal
import sys
import os

shutdown_event = threading.Event()
last_image = None
lock = threading.Lock()
z = None

# Force path to /tmp so WSL scripts can read it
SAVE_PATH = "/home/aniket-barve/zenoh_share/laptop_image.jpg"

def signal_handler(sig, frame):
    print("\n[Signal] Stopping subscriber...")
    shutdown_event.set()
    if z:
        z.close()
        cv2.destroyAllWindows()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)


def callback(sample):
    global last_image
    try:
        b64 = bytes(sample.payload).decode()
        img_bytes = base64.b64decode(b64)
        npimg = np.frombuffer(img_bytes, dtype=np.uint8)
        frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        with lock:
            last_image = frame
            cv2.imwrite(SAVE_PATH, frame)
            print(f" Image saved to {SAVE_PATH}")
    except Exception as e:
        print("[Callback error]:", e)


def main():
    global z
    cfg = zenoh.Config()
    z = zenoh.open(cfg)
    z.declare_subscriber("demo/cam/image", callback)
    print("Zenoh subscriber started. Press CTRL+C to stop.")

    while not shutdown_event.is_set():
        with lock:
            if last_image is not None:
                print("Image received")
                key = cv2.waitKey(1)
                if key == 27:  # ESC to stop
                    signal_handler(None, None)
                    break

if __name__ == "__main__":
    main()
