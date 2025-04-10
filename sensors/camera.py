import cv2
from datetime import datetime, timezone, timedelta
import sys
import time
if __name__ == '__main__':
    import corn_disease, corn_growth
else:
    from sensors import corn_disease, corn_growth
# Open the webcam (0 is the default camera)
PH_TZ = timezone(timedelta(hours=8))

def get_file_name(camera, device_id):
    # Save the image
    timestamp = datetime.now(PH_TZ).strftime('%Y%m%d-%H%M%S')
    file_name = f"api/static/{device_id}-{timestamp}-{camera}.jpg"
    return file_name

def get_image(web_cam, device_id):
    """
    Captures an image.
    
    Returns:
    ret, frame, image_path
    """
    video = cv2.VideoCapture(web_cam)
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

    time.sleep(0.1)
    for _ in range(5):
        video.read()

    ret, frame = video.read()
    video.release()
    
    if not ret:
        print("[ERROR] Failed to capture image from webcam.")
        return None, None, None

    image_path = get_file_name(web_cam, device_id)
    cv2.imwrite(image_path, frame)
    return ret, frame, image_path
    
def get_ai_results(device_id):
    cameras = [0, 1, 2]
    healths = []
    stages = []
    paths = []
    for port_number in cameras:
        ret, frame, image_path = get_image(port_number, device_id)
        health = corn_disease.get_health(ret, frame)
        stage = corn_growth.get_stage(ret, frame, image_path)
        healths.append(health)
        stages.append(stage)
        paths.append(image_path)
        time.sleep(0.5)
    return healths, stages, paths, cameras
if __name__ == '__main__':
    device_id = 'Zg6XgWqdztP3bDwquu51'
    healths, stages, paths, cameras = get_ai_results(device_id)
    print(healths)
    print(stages)
    print(paths)
    print(cameras)