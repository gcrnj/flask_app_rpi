from flask import Blueprint, request, jsonify
from firebase_admin import firestore

db = firestore.client()
user_Ref = db.collection('devices')

deviceAPI = Blueprint('deviceAPI', __name__)


@deviceAPI.route('/', methods=['GET'])
def get_devices():
    try:
        devices = user_Ref.stream()  # Get all documents in the collection
        device_list = {doc.id: doc.to_dict() for doc in devices}
        return jsonify(device_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
