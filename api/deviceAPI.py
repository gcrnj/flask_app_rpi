from flask import Blueprint, request, jsonify
from firebase_admin import firestore
from sensors import soil_moisture
from sensors import temp_humid
from datetime import datetime, timezone, timedelta
from flask import request
import requests
from sensors import async_py

db = firestore.client()
devices_ref = db.collection('devices')

deviceAPI = Blueprint('deviceAPI', __name__)
PH_TZ = timezone(timedelta(hours=8))

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
    print("/register")
    try:
        print("adding device")
        # Reference to the Firestore document
        new_device_ref = devices_ref.add({
            "createdAt": firestore.SERVER_TIMESTAMP,
            "ownerId": [],
            "deviceName": "Main System"
            })
        print("added successfully")

        return jsonify({"message": "Device registered successfully", "device_id": new_device_ref[1].id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
# GET - DEVICES
@deviceAPI.route('/find/<device_id>', methods=['GET'])
def get_device(device_id):
    try:
        device_doc = devices_ref.document(device_id).get()
        if device_doc.exists:
            device_data = device_doc.to_dict()
            device_data['device_id'] = device_doc.id  # Add document ID to JSON
            return jsonify(device_data), 200
        else:
            return jsonify({"error": "Device not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@deviceAPI.route('/edit/<device_id>', methods=['PATCH'])
def edit_device_name(device_id):
    try:
        data = request.get_json()
        new_name = data.get('deviceName')

        if not new_name:
            return jsonify({"error": "Missing 'deviceName' in request body"}), 400

        device_ref = devices_ref.document(device_id)
        device_doc = device_ref.get()

        if device_doc.exists:
            device_ref.update({"deviceName": new_name})
            return jsonify({"message": "Device name updated successfully"}), 200
        else:
            return jsonify({"error": "Device not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET - SOIL MOISTURE
@deviceAPI.route('/<device_id>/soil_moisture', methods=['GET'])
def get_soil_moisture(device_id):
    try:
        # Retrieve query parameters
        start_str = request.args.get('start')
        end_str = request.args.get('end')
        water_distributed = request.args.get('water_distributed')
        print(f'water_distributed {water_distributed}')
        print('get_soil_moisture')
        print(f'args = From {start_str} ; To {end_str}')

        readings_ref = devices_ref.document(device_id).collection('moisture_readings')

        # Convert start and end to UTC datetime
        try:
            if start_str:
                start = datetime.fromisoformat(start_str).replace(tzinfo=PH_TZ)
            else:
                start = None

            if end_str:
                end = datetime.fromisoformat(end_str).replace(tzinfo=PH_TZ)
            else:
                end = None
        except ValueError:
            return jsonify({"error": "Invalid date format. Use ISO 8601 format."}), 400

        query = readings_ref

        if start:
            query = query.where("time", ">=", start)  # ✅ Still use positional arguments
        if end:
            query = query.where("time", "<=", end)  # ✅ Still use positional arguments
        if water_distributed is not None:
            print(f"Not none but {water_distributed}")
            query = query.where("water_distributed", "==", water_distributed == 'true')  # ✅ Still use positional arguments
        else:
            print("none")

        # Get filtered readings
        readings = query.stream()

        # Convert the dictionary structure into a list with IDs included
        moisture_data = [
            {
                "id": reading.id,
                **reading.to_dict(),
                "time": reading.to_dict()["time"].astimezone(PH_TZ).isoformat()  # Convert UTC to UTC+8
            }
            for reading in readings
        ]

        print(moisture_data)

        if moisture_data:
            return jsonify(moisture_data), 200
        else:
            return jsonify({"error": "No data found in the date range."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# CREATE - SOIL MOISTURE and TEMPERATURE
@deviceAPI.route('/<device_id>/soil_moisture', methods=['POST'])
def add_temperature(device_id):
    try:
        # Get request data
        try:
            data = async_py.run_sensors()
        except Exception as e:
            return jsonify({"error": f"Error in asunc_py {e}"}), 400

        
        # time = data.get("time")
        water_distributed = data["water_distributed"]  # Default to False if not provided
        moisture1 = data['moisture1']
        moisture2 = data['moisture2']
        moisture3 = data['moisture3']
        temperature = data['temperature']
        humidity = data['humidity']
        print(f'Got data: {data}')

        if water_distributed is None:
            return jsonify({"error": "Missing required field: water_distributed"}), 400
        if moisture1 is None:
            return jsonify({"error": "Missing required field: moisture1"}), 400
        if moisture2 is None:
            return jsonify({"error": "Missing required field: moisture2"}), 400
        if moisture3 is None:
            return jsonify({"error": "Missing required field: moisture3"}), 400
        if temperature is None:
            return jsonify({"error": "Missing required field: temperature"}), 400
        if humidity is None:
            return jsonify({"error": "Missing required field: humidity"}), 400
        

        # Reference to the moisture_readings subcollection
        readings_ref = devices_ref.document(device_id).collection("moisture_readings")

        # Add a new document with auto-generated ID

        # Convert string time to datetime object

        date_time = datetime.now(PH_TZ)

        post_data = {
            "moisture1": moisture1,
            "moisture2": moisture2,
            "moisture3": moisture3,
            "temperature": temperature,
            "humidiity": humidity,
            "time": date_time,
            "water_distributed": water_distributed
        }
        new_doc_ref = readings_ref.add(post_data)
        added_post_data = post_data

        # Check if the document was added successfully
        post_data['type'] = 'soil_moisture'
        post_data['time'] = date_time.isoformat()
        if new_doc_ref:
            print('Doc Added successfully')
            doc_id = ''
            try:
                doc_id = new_doc_ref[1].id
            except:
                doc_id = '...' 
            return jsonify({
                'doc_id': doc_id,
                "message": f"Soil Moisture 1 ({moisture1}), Soil Moisture 2 ({moisture2}), Soil Moisture 3 ({moisture3}), Temperature({temperature}) and Humidity ({humidity}) added successfully",
                'added_post_data': added_post_data
                }), 200
        else:
            failed_upload_respones  = call_failed_uploads(device_id, post_data)
            print(f'Response {failed_upload_respones.json()}')
            return jsonify({'error': 'Failed to upload data'}), 502
    except Exception as e:
        failed_upload_respones  = call_failed_uploads(device_id, post_data)
        print(f'Response {failed_upload_respones.json()}') 
        return jsonify({"error": f'Exception in add_temperature: {str(e)}'}), 501
    
def call_failed_uploads(device_id, post_data, photo):
    return requests.post(
                f"http://localhost:5000/failed-uploads/{device_id}/failed_upload",
                json=post_data,
                headers={
                    'Content-Type': 'application/json'
                }
            )