import cv2
import time
import base64
import zenoh

def main():
    cam = cv2.VideoCapture(2)
    if not cam.isOpened():
        print("Cannot access camera")
        return

    cfg = zenoh.Config()               
    z = zenoh.open(cfg)               
    pub = z.declare_publisher("demo/cam/image")

    while True:
        ret, frame = cam.read()
        if not ret:
            break
        _, jpeg = cv2.imencode(".jpg", frame)
        b64 = base64.b64encode(jpeg.tobytes()).decode()
        pub.put(b64)
        print("Image published")
        time.sleep(0.2)

if __name__ == "__main__":
    main()
