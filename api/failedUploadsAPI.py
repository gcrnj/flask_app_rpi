from flask import Blueprint, request, jsonify
import json
import os
from datetime import datetime, timezone, timedelta
import uuid
from datetime import datetime

failedUploads = Blueprint('failedUploads', __name__)
PH_TZ = timezone(timedelta(hours=8))
FAILED_UPLOADS_FILE = 'failed_uploads.json'
UPLOAD_FOLDER = 'uploads'  # Folder to store failed photos

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

@failedUploads.route('/<device_id>/failed_upload', methods=['POST'])
def add_failed_upload_endpoint(device_id):
    """API endpoint to add a failed upload entry for a specific device."""
    
    if 'type' not in request.form:
        return jsonify({"error": "Missing 'type' parameter"}), 400

    upload_type = request.form['type']

    if upload_type == 'photo':
        if 'file' not in request.files:
            return jsonify({"error": "Missing file"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"error": "No selected file"}), 400
        
        # Generate a filename in the format <device_id>-YYYYMMDD-HHMMSS.png
        timestamp = datetime.now(PH_TZ).strftime('%Y%m%d-%H%M%S')
        file_extension = file.filename.rsplit('.', 1)[-1].lower()  # Get file extension
        filename = f"{device_id}-{timestamp}.{file_extension}"
        
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)  # Save file

        data = {
            "type": "photo",
            "file": file_path,
            "time": datetime.now(PH_TZ).isoformat()
        }

    else:
        # Handle JSON payload for sensor data
        data = request.json
        if not data:
            return jsonify({"error": "Invalid data"}), 400

        data["time"] = datetime.now(PH_TZ).isoformat()

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
