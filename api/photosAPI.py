from flask import Blueprint, request, jsonify
from firebase_admin import firestore, storage
from datetime import datetime
import uuid

db = firestore.client()
devices_ref = db.collection('devices')

photosAPI = Blueprint('photos', __name__)
bucket = storage.bucket(name="your-bucket-name")  # Replace with your actual bucket name


@photosAPI.route('/<device_id>', methods=['GET'])
def get_photos(device_id):  
    device_doc = devices_ref.document(device_id).get()
    
    if not device_doc.exists:
        return jsonify({"error": "Device not found"}), 404

    photos_ref = devices_ref.document(device_id).collection('captured_photos')
    photos = photos_ref.stream()  # Fetch all documents in the 'photos' subcollection

    photo_list = []
    for photo in photos:
        photo_data = photo.to_dict()
        formatted_photo = {
            "refId": photo.id,  # Document ID as ref_id
            "path": photo_data.get("path", ""),  # Use default empty string if missing
            "time": photo_data.get("time", "")  # Ensure dateTime is included
        }
        photo_list.append(formatted_photo)

    return jsonify({"device_id": device_id, "photos": photo_list})


@photosAPI.route('/upload', methods=['POST'])
def upload():
    device_id = request.form.get('device_id')  # Get device_id from form data
    image = request.files.get('image')  # Get the uploaded file

    if not device_id or not image:
        return jsonify({"error": "Missing device_id or image"}), 400

    # Generate a unique filename
    file_ext = image.filename.split('.')[-1]  # Get file extension
    unique_filename = f"{uuid.uuid4()}.{file_ext}"

    # Upload file to Firebase Storage
    blob = bucket.blob(f"devices/{device_id}/captured_photos/{unique_filename}")
    blob.upload_from_file(image, content_type=image.content_type)
    blob.make_public()  # Make the file publicly accessible

    # Save metadata to Firestore
    photo_doc = {
        "path": blob.public_url,
        "dateTime": datetime.now(datetime.UTC).isoformat()
    }
    photo_ref = devices_ref.document(device_id).collection('photos').add(photo_doc)

    return jsonify({
        "message": "Photo added successfully.",
        "device_id": device_id,
        "photo": {
            "ref_id": photo_ref[1].id,  # Get the Firestore document ID
            "path": blob.public_url,
            "dateTime": photo_doc["dateTime"]
        }
    })


