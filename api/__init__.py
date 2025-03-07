from flask import Flask
from firebase_admin import credentials, initialize_app
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current file
cred_path = os.path.join(BASE_DIR, "firebase_key.json")  # Construct absolute path
print(cred_path)
cred = credentials.Certificate(cred_path)  # Use absolute path

# Initialize Firebase
default_app = initialize_app(cred)

def create_app():
    app = Flask(__name__)

    from .deviceAPI import deviceAPI 
    from .photosAPI import photosAPI 

    app.register_blueprint(deviceAPI, url_prefix='/devices')
    app.register_blueprint(photosAPI, url_prefix='/photos')
    return app
