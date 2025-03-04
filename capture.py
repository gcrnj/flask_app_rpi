from picamera2 import Picamera2
import time

picam2 = Picamera2()
picam2.start()
time.sleep(2)  # Allow time for the camera to adjust
picam2.capture_file("capture.jpg")
print("Photo captured!")
