# maize_growth.py

import cv2
from inference_sdk import InferenceHTTPClient

ROBOFLOW_API_KEY = "mUHiIlSJOzpUNaF5KXib"
ROBOFLOW_MODEL_ID = "capstone-maize-growth-v2/2"

stage_mapping = {
    "Maize Growth Stage 1": "V3",
    "Maize Growth Stage 2": "V6",
    "Maize Growth Stage 3": "V9",
    "Maize Growth Stage 4": "V10",
    "Maize Growth Stage 5": "R1",
    "Unhealthy Leaf": "Unlabeled"
}

def get_stage(ret, frame, image_path):
    if not ret:
        print("[ERROR] Failed to capture image from webcam.")
        return None

    print("[INFO] Sending to Roboflow for growth stage inference...")
    try:
        client = InferenceHTTPClient(
            api_url="https://serverless.roboflow.com",
            api_key=ROBOFLOW_API_KEY
        )
        result = client.infer(image_path, model_id=ROBOFLOW_MODEL_ID)
    except Exception as e:
        print(f"[ERROR] Inference failed: {e}")
        return None

    predictions = result.get("predictions", [])
    if not predictions:
        print("[INFO] No maize growth stage detected.")
        return "Unlabeled"

    detected_stages = set()

    for pred in predictions:
        class_name = pred["class"]
        confidence = pred["confidence"]

        normalized_class = class_name.strip().title().replace("_", " ")
        mapped_label = stage_mapping.get(normalized_class, normalized_class)

        x = int(pred["x"])
        y = int(pred["y"])
        w = int(pred["width"])
        h = int(pred["height"])

        x1 = int(x - w / 2)
        y1 = int(y - h / 2)
        x2 = int(x + w / 2)
        y2 = int(y + h / 2)

        detected_stages.add(mapped_label)

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"{mapped_label} ({confidence:.2f})", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    summary_text = "Detected Stage(s): " + ", ".join(sorted(detected_stages))
    stage = list(detected_stages)[0] if detected_stages else "Unlabeled"

    cv2.putText(frame, summary_text, (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    print(f"[INFO] {summary_text}")
    print("[INFO] Displaying result...")
    cv2.imshow("Maize Growth Stage Detection", frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return stage

if __name__ == '__main__':
    import camera  # this should be your custom module
    ret, frame, image_path = camera.get_image(1, 'captured.jpg')  # change 1 to 0 if necessary
    stage = get_stage(ret, frame, image_path)
    print(f"[RESULT] Final Detected Stage: {stage}")
