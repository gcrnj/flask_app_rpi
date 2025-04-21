import os
from datetime import datetime, timezone, timedelta
import firebase_admin
from firebase_admin import credentials, storage

# Initialize Firebase
cred = credentials.Certificate('api/firebase_key.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'project-corntrack.firebasestorage.app'  # Replace with your bucket
})

# Constants
DEVICE_ID = 'Zg6XgWqdztP3bDwquu51'
PH_TZ = timezone(timedelta(hours=8))
IMAGES_FOLDER = 'Images'
BUCKET = storage.bucket()

def extract_info_and_upload(local_file):
    try:
        # Example Firebase name: 2025-04-20/07-00-00-1.jpg
        filename = os.path.basename(local_file)  # e.g. 'img_1234.jpg'
        
        # You'll define how to map this file to date/time/port
        # For now, just simulate that mapping (change this part to fit your mapping logic)
        # Let's say you want to upload files sequentially, starting from 2025-04-20 07:00:00
        # and loop ports 0,1,2

        # You'll define this part outside:
        return filename  # for now just to test

    except Exception as e:
        print(f"[ERROR] Skipping file {local_file}: {e}")

def main():
    # Start timestamp for simulation (first image gets this, then +1hr each image)
    current_time = datetime(2025, 4, 20, 7, 0, tzinfo=PH_TZ)
    port_cycle = [0, 1, 2]
    port_index = 0

    # Get all files in the folder
    image_files = [os.path.join(IMAGES_FOLDER, f) for f in os.listdir(IMAGES_FOLDER)
                   if os.path.isfile(os.path.join(IMAGES_FOLDER, f)) and f.lower().endswith(('.jpg', '.jpeg', '.png'))]

    for local_path in sorted(image_files):  # sort to ensure consistent order
        date_str = current_time.strftime('%Y-%m-%d')
        time_str = current_time.strftime('%H-%M-%S')
        port = port_cycle[port_index]

        firebase_filename = f"{time_str}-{port}.jpg"
        firebase_path = f"captured_photos/{DEVICE_ID}/{date_str}/{firebase_filename}"

        metadata = {
            "device_id": DEVICE_ID,
            "health_status": "Unhealthy",
            "growth_stage": "R1",
            "timestamp": current_time.isoformat(),
            "camera": port
        }

        try:
            blob = BUCKET.blob(firebase_path)
            blob.upload_from_filename(local_path, content_type="image/jpeg")
            blob.metadata = metadata
            blob.patch()
            blob.make_public()
            image_url = blob.public_url
            print(f"[UPLOADED] {firebase_path} - {image_url}")
        except Exception as e:
            print(f"[ERROR] Failed to upload {local_path}: {e}")

        # Prepare for next image
        port_index = (port_index + 1) % 3
        if port_index == 0:
            current_time += timedelta(hours=1)

if __name__ == "__main__":
    main()
