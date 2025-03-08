from flask import Blueprint, request, jsonify
from firebase_admin import firestore
from sensors import soil_moisture
from sensors import temp_humid
from datetime import datetime, timezone, timedelta
from flask import request

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
            "ownerId": "",
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
        pots = request.args.getlist('pots', type=int)  # Get list of pots
        water_distributed = request.args.get('water_distributed')
        print(f'water_distributed {water_distributed}')
        print('get_soil_moisture')
        print(f'args = From {start_str} ; To {end_str} ; Pots {pots}')

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
        if pots:
            query = query.where("pot", "in", pots)  # ✅ Still use positional arguments
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
            return jsonify({"error": "No soil moisture readings found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# CREATE - SOIL MOISTURE and TEMPERATURE
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
        water_distributed = data.get("water_distributed", False)  # Default to False if not provided
        print(f'water_distributed {water_distributed}')

        if pot is None:
            return jsonify({"error": "Missing required field: Pot"}), 400
        if time is None:
            return jsonify({"error": "Missing required field: Time"}), 400
        
        moisture = soil_moisture.get_from_pot(pot)
        temperature, humidity = temp_humid.get_temp_humid()

        # Reference to the moisture_readings subcollection
        readings_ref = devices_ref.document(device_id).collection("moisture_readings")

        # Add a new document with auto-generated ID

        # Convert string time to datetime object

        date_time = datetime.now(PH_TZ)
        print(f'Adding Pot {pot} ; Time {date_time}')

        new_doc_ref = readings_ref.add({
            "pot": pot,
            "moisture": moisture,
            "temperature": temperature,
            "humidiity": humidity,
            "time": date_time,
            "water_distributed": water_distributed
        })

        return jsonify({"message": f"Soil Moisture ({moisture}), Temperature({temperature}) and Humidity ({humidity}) added successfully", "id": new_doc_ref[1].id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
