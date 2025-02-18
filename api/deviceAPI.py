from flask import Blueprint, request, jsonify
from firebase_admin import firestore
from sensors import soil_moisture
from datetime import datetime

db = firestore.client()
devices_ref = db.collection('devices')

deviceAPI = Blueprint('deviceAPI', __name__)

# All Devices
# Todo - Remove - vulneribility issue
@deviceAPI.route('/', methods=['GET'])
def get_devices():
    try:
        devices = devices_ref.stream()  # Get all documents in the collection
        device_list = {doc.id: doc.to_dict() for doc in devices}
        return jsonify(device_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# CREATE - DEVICE
@deviceAPI.route('/register', methods=['POST'])
def register_device():
    try:
        # Reference to the Firestore document
        new_device_ref = devices_ref.add({
            "createdAt": firestore.SERVER_TIMESTAMP,
            "ownerId": "",
            "deviceName": "Main System"
            })

        return jsonify({"message": "Device registered successfully", "device_id": new_device_ref[1].id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET - DEVICES
@deviceAPI.route('/find/<device_id>', methods=['GET'])
def get_device(device_id):
    try:
        device_doc = devices_ref.document(device_id).get()
        if device_doc.exists:
            return jsonify(device_doc.to_dict()), 200
        else:
            return jsonify({"error": "Device not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get - SOIL MOISTURE
@deviceAPI.route('/<device_id>/soil_moisture', methods=['GET'])
def get_soil_moisture(device_id):
    try:
        readings_ref = devices_ref.document(device_id).collection('moisture_readings')
        readings = readings_ref.stream()

        # Convert the dictionary structure into a list with IDs included
        moisture_data = [
            {"id": reading.id, **reading.to_dict()} for reading in readings
        ]

        if moisture_data:
            return jsonify(moisture_data), 200
        else:
            return jsonify({"error": "No soil moisture readings found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

from flask import request

# CREATE - SOIL MOISTURE
@deviceAPI.route('/<device_id>/soil_moisture', methods=['POST'])
def add_temperature(device_id):
    try:
        # Get request data
        try:
            data = request.get_json()
        except Exception as e:
            return jsonify({"error": "Missing required field: Pot and Time"}), 400

        pot = data.get("pot")
        time = data.get("time")


        if pot is None:
            return jsonify({"error": "Missing required field: Pot"}), 400
        if time is None:
            return jsonify({"error": "Missing required field: Time"}), 400
        
        moisture = soil_moisture.get_from_pot(pot)

        # Reference to the moisture_readings subcollection
        readings_ref = devices_ref.document(device_id).collection("moisture_readings")

        # Add a new document with auto-generated ID
        date_time = datetime.strptime(time, "%a, %d %b %Y %H:%M:%S %Z")

        new_doc_ref = readings_ref.add({
            "pot": pot,
            "moisture": moisture,
            "time": date_time,
        })

        return jsonify({"message": "Temperature added successfully", "id": new_doc_ref[1].id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
