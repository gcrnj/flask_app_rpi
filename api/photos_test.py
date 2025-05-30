from flask import Flask, request, jsonify
import firebase_admin
from firebase_admin import credentials, storage
from datetime import datetime, timezone, timedelta

PH_TZ = timezone(timedelta(hours=8))

app = Flask(__name__)

# Initialize Firebase Admin SDK
cred = credentials.Certificate("api/firebase_key2.json")
firebase_admin.initialize_app(cred, {"storageBucket": "project-corntrack.firebasestorage.app"})  # Ensure correct bucket name

bucket = storage.bucket()


# @app.route("/get-download-url", methods=["GET"])
# def get_download_url():
#     blob = bucket.blob('gallery.png')

#     # Generate signed URL (valid for 1 hour)

#     expiration_time = datetime.now(PH_TZ) + timedelta(days=1)
#     url = blob.generate_signed_url(expiration=expiration_time)
#     return jsonify({"download_url": url})

# Upload {"photo": "file.jpg"}
@app.route("/<device_id>/upload-file", methods=["POST"])
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
        now = datetime.now(PH_TZ)
        date_str = now.strftime("%Y-%m-%d")  # e.g., 2025-03-09
        time_str = now.strftime("%H-%M")     # e.g., 14-30 (24-hour format)

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

@app.route("/<device_id>/list-files", methods=["GET"])
def list_files(device_id):
    """List all uploaded files for a device grouped by date."""
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
                file_url = blob.public_url  # Get public URL of the file
                if date_folder not in files_by_date:
                    files_by_date[date_folder] = []
                files_by_date[date_folder].append({
                    "file_name": file_name,
                    "file_url": file_url
                })

        return jsonify({
            "device_id": device_id,
            "photos": files_by_date
        })
    except Exception as e:
        print(f"❌ Error: {str(e)}")  # Debugging log
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
