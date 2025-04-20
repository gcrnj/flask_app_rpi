from flask import Blueprint, request, jsonify, send_file
from firebase_admin import firestore, storage
from datetime import datetime, timezone, timedelta
import requests
import os

if __name__ == '__main__':
    from ai import get_growth_stage
else:
    from api.ai import get_growth_stage
db = firestore.client()
devices_ref = db.collection('devices')
bucket = storage.bucket()  # Use actual bucket name

photosAPI = Blueprint('photos', __name__)


PH_TZ = timezone(timedelta(hours=8))

@photosAPI.route("/<device_id>/upload-file", methods=["POST"])
def upload_file(device_id):
    print(device_id)
    """Upload a file to Firebase Storage and return its public URL."""

    if 'photo' not in request.files:
        print("❌ No file part in request")  # Debugging log
        return jsonify({"error": "No file part"}), 400

    file = request.files['photo']

    if file.filename == '':
        print("❌ No selected file")  # Debugging log
        return jsonify({"error": "No selected file"}), 400

    try:
        # Get current date and time
        if 'time' in request.form:
            print('upload-file: Got time') 
            now = datetime.fromisoformat(request.form['time'])
        else:
            print('upload-file: Using now time')
            now = datetime.now(PH_TZ)
        date_str = now.strftime("%Y-%m-%d")  # e.g., 2025-03-09
        time_str = now.strftime("%H-%M-%S")     # e.g., 14-30 (24-hour format)

        # Define the storage path
        blob_path = f"captured_photos/{device_id}/{date_str}/{time_str}.jpg"

        # Upload file to Firebase Storage
        blob = bucket.blob(blob_path)
        blob.upload_from_file(file, content_type="image/jpeg")

        # Make the file publicly accessible
        blob.make_public()

        return jsonify({
            "photo": {
            "message": "File uploaded successfully",
            "file_path": blob_path,
            "public_url": blob.public_url
        }})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@photosAPI.route("/<device_id>/list-files", methods=["GET"])
def list_files(device_id):
    """List all uploaded files for a device grouped by date with custom metadata."""
    try:
        prefix = f"captured_photos/{device_id}/"  # Only fetch files inside this folder
        blobs = bucket.list_blobs(prefix=prefix)

        # Dictionary to store files grouped by date
        files_by_date = {}

        for blob in blobs:
            # Extract the path parts
            path_parts = blob.name.split('/')
            if len(path_parts) < 3:
                continue  # Skip invalid paths

            date_folder = path_parts[2]  # Get the date (YYYY-MM-DD)
            file_name = path_parts[3] if len(path_parts) > 3 else None  # HH-MM.jpg

            if file_name:
                # Fetch metadata for the blob
                blob.reload()  # Refresh metadata

                # Get file metadata
                file_size = f"{blob.size / (1024 * 1024):.2f} MB" if blob.size else "0 MB"
                content_type = blob.content_type or "unknown"
                creation_time = blob.time_created.isoformat() if blob.time_created else "unknown"
                last_updated = blob.updated.isoformat() if blob.updated else "unknown"
                download_url = blob.generate_signed_url(expiration=3600)  # 1-hour signed URL

                # Get custom metadata
                custom_metadata = blob.metadata or {}  # Dictionary of custom metadata

                # Initialize date group if not exists
                if date_folder not in files_by_date:
                    files_by_date[date_folder] = []

                # Append file metadata to the list
                files_by_date[date_folder].append({
                    "file_name": file_name,
                    "file_url": blob.public_url,
                    "file_size": file_size,
                    "content_type": content_type,
                    "creation_time": creation_time,
                    "last_updated": last_updated,
                    "download_url": download_url,
                    "custom_metadata": custom_metadata  # Include custom metadata
                })

        return jsonify({
            "device_id": device_id,
            "photos": files_by_date
        })
    except Exception as e:
        print(f"❌ Error: {str(e)}")  # Debugging log
        return jsonify({"error": str(e)}), 500

@photosAPI.route("/<device_id>/capture", methods=["GET"])
def capture_photo(device_id):
    from sensors import camera
    now = datetime.now(PH_TZ)
    date_str = now.strftime("%Y-%m-%d")  # e.g., 2025-03-09
    time_str = now.strftime("%H-%M-%S")  # e.g., 14-30 (24-hour format)

    # Firebase Storage base path
    base_blob_path = f"captured_photos/{device_id}/{date_str}"

    # Capture the image and get AI results
    
    # Save the image
    healths, stages, captured_paths, port_numbers = camera.get_ai_results(device_id)

    if not any(captured_paths):  # all are None
        return jsonify({'error': 'Cannot capture camera'}), 500

    results = []
    failed_upload_url = f"http://localhost:5000/failed-uploads/{device_id}/failed_upload"

    for i, captured_path in enumerate(captured_paths):
        if captured_path is None:
            continue

        try:
            captured_path = os.path.abspath(captured_path)  # Ensure absolute path
            blob_path = f"{base_blob_path}/{time_str}-{i}.jpg"

            # Generate metadata
            metadata = {
                "device_id": device_id,
                "health_status": healths[i],
                "growth_stage": stages[i],
                "timestamp": now.isoformat(),
                "camera": port_numbers[i]
            }

            # Upload to Firebase
            bucket = storage.bucket()
            blob = bucket.blob(blob_path)

            with open(captured_path, "rb") as image_file:
                blob.upload_from_file(image_file, content_type="image/jpeg")

            # Set metadata
            blob.metadata = metadata
            blob.patch()

            # Make the image public and get URL
            blob.make_public()
            image_url = blob.public_url

            results.append({
                "image_url": image_url,
                "metadata": metadata
            })

        except Exception as e:
            print(f"Upload failed for camera_{i}: {e}")
            try:
                with open(captured_path, "rb") as image_file:
                    failed_upload_response = requests.post(
                        failed_upload_url,
                        files={'file': image_file},
                        data={'type': 'photo'}
                    )
                    print(f'failed_upload_response = {failed_upload_response.text}')
            except Exception as inner_e:
                print(f"Failed to send to failed upload endpoint: {inner_e}")

    return jsonify(results if results else {"error": "All uploads failed"}), 200 if results else 500
