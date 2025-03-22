from flask import Flask
from flask_cors import CORS
from firebase_admin import credentials, initialize_app
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current file
cred_path = os.path.join(BASE_DIR, "firebase_key.json")  # Construct absolute path
print(cred_path)
cred = credentials.Certificate(cred_path)  # Use absolute path

# Initialize Firebase
default_app = initialize_app(cred, {
    'storageBucket': 'project-corntrack.firebasestorage.app'  # Replace with your actual bucket name
})

def create_app():
    app = Flask(__name__, static_folder='uploads')
    CORS(app)

    from .deviceAPI import deviceAPI 
    from .photosAPI import photosAPI
    from .failedUploadsAPI import failedUploads as failedUploadsAPI
    from .qrCodeAPI import qrCodeAPI
    from .graphsAPI import graphsAPI

    app.register_blueprint(deviceAPI, url_prefix='/devices')
    app.register_blueprint(photosAPI, url_prefix='/photos')
    app.register_blueprint(failedUploadsAPI, url_prefix='/failed-uploads')
    app.register_blueprint(qrCodeAPI, url_prefix='/qrcode')
    app.register_blueprint(graphsAPI, url_prefix='/graphs')
    return app
