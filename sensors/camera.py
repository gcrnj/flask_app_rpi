import cv2

# Open the webcam (0 is the default camera)

def capture_image():
    cap = cv2.VideoCapture(0)
    # Check if the webcam is opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        release()
        return None
    else:
        # Capture a single frame
        ret, frame = cap.read()
        release(cap)
        if ret:
            # Save the image
            cv2.imwrite("captured_image.jpg", frame)
            return '../captured_image.jpg'
        else:
            print("Error: Could not capture image.")
            return None

def release(cap):

    # Release the camera
    cap.release()

    # Close all OpenCV windows (not needed for this script but useful in GUI apps)
    cv2.destroyAllWindows()