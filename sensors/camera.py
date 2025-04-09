import cv2
from datetime import datetime, timezone, timedelta
import sys
# Open the webcam (0 is the default camera)
PH_TZ = timezone(timedelta(hours=8))

def capture_image(device_id):
    if sys.platform == 'win32':
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(0)
    # Check if the webcam is opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        release(cap)
        return None
    else:
        # Capture a single frame
        ret, frame = cap.read()
        release(cap)
        if ret:
            # Save the image
            timestamp = datetime.now(PH_TZ).strftime('%Y%m%d-%H%M%S')
            file_name = f"api/static/{device_id}-{timestamp}.jpg"
            isSuccess = cv2.imwrite(file_name, frame)
            print(f'{isSuccess} - {file_name}')
            return file_name
        else:
            print("Error: Could not capture image.")
            return None

def release(cap):

    # Release the camera
    cap.release()

    # Close all OpenCV windows (not needed for this script but useful in GUI apps)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    print(capture_image('Zg6XgWqdztP3bDwquu51'))