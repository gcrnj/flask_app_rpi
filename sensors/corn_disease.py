# corn_disease.py

import cv2
import base64
import numpy as np
import requests
import time

ROBOFLOW_API_KEY = "J18GrT2BmnD5IvuVHqia"
ROBOFLOW_MODEL_ID = "corn-grayleafspot2/22"
ROBOFLOW_SIZE = 416
upload_url = f"https://detect.roboflow.com/{ROBOFLOW_MODEL_ID}?api_key={ROBOFLOW_API_KEY}&format=json"

def get_health(ret, full_res_frame):
    print("[INFO] Capturing image from webcam...")
    if not ret:
        print("[ERROR] Failed to capture image.")
        return None

    print("[INFO] Resizing and encoding image...")
    resized_for_model = cv2.resize(full_res_frame, (ROBOFLOW_SIZE, ROBOFLOW_SIZE))
    retval, buffer = cv2.imencode('.jpg', resized_for_model)
    img_base64 = base64.b64encode(buffer).decode('utf-8')

    print("[INFO] Sending to Roboflow...")
    try:
        response = requests.post(upload_url, data=img_base64, headers={
            "Content-Type": "application/x-www-form-urlencoded"
        })
    except Exception as e:
        print(f"[ERROR] Request failed: {e}")
        return None

    if response.status_code != 200:
        print(f"[ERROR] API Error: {response.status_code}")
        return None

    predictions = response.json().get("predictions", [])

    if not predictions:
        print("[INFO] No corn leaf detected.")
        return "Unlabeled"

    original_height, original_width = full_res_frame.shape[:2]
    x_scale = original_width / ROBOFLOW_SIZE
    y_scale = original_height / ROBOFLOW_SIZE

    classes_detected = set()

    print("[INFO] Drawing predictions...")
    for pred in predictions:
        x = int(pred["x"] * x_scale)
        y = int(pred["y"] * y_scale)
        w = int(pred["width"] * x_scale)
        h = int(pred["height"] * y_scale)

        x1 = x - w // 2
        y1 = y - h // 2
        x2 = x + w // 2
        y2 = y + h // 2

        class_name = pred["class"]
        confidence = pred["confidence"]
        classes_detected.add(class_name)

        color = (0, 255, 0) if class_name.lower() == "healthy" else (0, 0, 255)

        cv2.rectangle(full_res_frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(full_res_frame, f"{class_name} ({confidence:.2f})", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

    if "Healthy" in classes_detected and len(classes_detected) == 1:
        classification = "healthy"
    else:
        classification = "unhealthy"

    cv2.putText(full_res_frame, f"Classification: {classification}", (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    print("[INFO] Displaying result...")
    # cv2.imshow("Corn Disease Detection", full_res_frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return classification


if __name__ == '__main__':
    import camera
    ret, frame, image_path = camera.get_image(0, 'Zg6XgWqdztP3bDwquu51')
    print(image_path)
    health = get_health(ret, frame)
    print(health)
