from flask import Blueprint, request, jsonify, send_file, abort
import json
import os
from datetime import datetime, timezone, timedelta
import requests

failedUploads = Blueprint('failedUploads', __name__)
PH_TZ = timezone(timedelta(hours=8))
FAILED_UPLOADS_FILE = 'failed_uploads.json'
UPLOAD_FOLDER = 'api\\static'  # Folder to store failed photos

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def ensure_failed_uploads_file():
    """Ensure that failed_uploads.json exists."""
    if not os.path.exists(FAILED_UPLOADS_FILE):
        with open(FAILED_UPLOADS_FILE, 'w') as file:
            json.dump({}, file)  # Initialize with an empty dict

def add_failed_upload(device_id, entry):
    """Add a new failed upload entry to failed_uploads.json."""
    ensure_failed_uploads_file()
    
    with open(FAILED_UPLOADS_FILE, 'r+') as file:
        try:
            data = json.load(file)
            if not isinstance(data, dict):
                data = {}
        except json.JSONDecodeError:
            data = {}
        
        if device_id not in data:
            data[device_id] = []
        
        data[device_id].append(entry)
        
        file.seek(0)
        json.dump(data, file, indent=4)

# Assuming these are defined somewhere
PH_TZ = None  # Set your timezone here

failedUploads = Blueprint('failedUploads', __name__)

@failedUploads.route('/<device_id>/failed_upload', methods=['POST'])
def add_failed_upload_endpoint(device_id):
    """API endpoint to add a failed upload entry for a specific device."""
    
    
    # Handling file uploads
    if request.form.get('type') == 'photo':
        #print(f'g={request.files['file']}')
        if 'file' not in request.files:
            return jsonify({"error": "Missing file"}), 400
        
        file = request.files['file'] # Failing
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        timestamp = datetime.now(PH_TZ).strftime('%Y%m%d-%H%M%S')
        file_extension = file.filename.rsplit('.', 1)[-1].lower()
        filename = file.filename
        data = {}
        file_path = ''
        try:
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            data = {
                "type": "photo",
                "file": file_path,
                "time": datetime.now(PH_TZ).isoformat()
            }
        except FileNotFoundError as e:
            return jsonify({"error": f'{file_path} - {e.strerror}'}), 400
    
    # Handling JSON payloads (e.g., sensor data)
    elif request.is_json:
        data = request.json
        if not data or data.get('type') != 'soil_moisture':
            return jsonify({"error": "Invalid or missing 'type' parameter"}), 400
    else:
        return jsonify({"error": "Missing 'type' parameter"}), 400
    
    add_failed_upload(device_id, data)
    
    return jsonify({"message": "Failed upload recorded", "data": data}), 201

@failedUploads.route('/<device_id>/failed_upload', methods=['GET'])
def get_all_failed_uploads(device_id):
    """API endpoint to get all failed uploads for a specific device."""
    ensure_failed_uploads_file()
    
    with open(FAILED_UPLOADS_FILE, 'r') as file:
        try:
            data = json.load(file)
            if not isinstance(data, dict):
                data = {}
        except json.JSONDecodeError:
            data = {}
    
    device_data = data.get(device_id, [])
    
    return jsonify({device_id: device_data}), 200

@failedUploads.route('/uploads/<filename>', methods=['GET'])
def get_failed_uploaded_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename).removeprefix('api\\')
    print('file_path2')
    print(file_path)

    return send_file(file_path, mimetype='image/png')

@failedUploads.route('/<device_id>/upload', methods=['POST'])
def uploadFailedUploads(device_id):
    """API endpoint to manually trigger re-upload of failed uploads by calling PhotosAPI and DeviceAPI."""
    ensure_failed_uploads_file()
    print('ensure_failed_uploads_file')
    with open(FAILED_UPLOADS_FILE, 'r+') as file:
        try:
            print('try ensure_failed_uploads_file')
            data = json.load(file)
            if not isinstance(data, dict):
                data = {}
        except json.JSONDecodeError as e:
            print(f'ex ensure_failed_uploads_file - {e}')
            data = {}
    print(device_id)
    print(data)
    if device_id not in data or not data[device_id]:
        return jsonify({"message": "No failed uploads to process"}), 200
    
    failed_uploads = data[device_id]
    
    for upload in failed_uploads:
        if upload['type'] == 'photo':
            print('uploading photo...')
            uploadType = upload['type']
            uploadFile = upload['file']
            uploadTime = upload['time']
            print(f'uploadFailedUploads - {uploadType} - {uploadFile} - {uploadTime}')
            files = {
                'photo': open(upload['file'], 'rb'),  # Send photo as a file
            }
            data = {
                'time': upload['time']  # Send time as form data
            }
            response = requests.post(
                f"http://localhost:5000/photos/{device_id}/upload-file",
                files=files,
                data=data
            )
            if response.status_code == 200:
                print(f"✅ Photo re-uploaded: {upload['file']}")
            else:
                print(f"❌ {response.status_code} Failed to re-upload photo: {upload['file']}")
                return response.json()
        elif upload['type'] == 'soil_moisture':
            print('uploading soil_moisture...')
            response = requests.post(f"http://localhost:5000/devices/{device_id}/soil_moisture", json=upload)
            if response.status_code == 201:
                print("✅ Soil moisture data re-uploaded")
            else:
                print("❌ Failed to re-upload soil moisture data")
    
    # Clear failed uploads after processing
    data[device_id] = []
    with open(FAILED_UPLOADS_FILE, 'w') as file:
        json.dump(data, file, indent=4)
    
    return jsonify({"message": "Failed uploads processed successfully"}), 200
