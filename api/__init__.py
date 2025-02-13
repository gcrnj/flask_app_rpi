from flask import Flask
from firebase_admin import credentials, initialize_app

# Initialize Firebase
cred = credentials.Certificate("api/firebase_key.json")
default_app = initialize_app(cred)

def create_app():
    app = Flask(__name__)

    from .deviceAPI import deviceAPI  

    app.register_blueprint(deviceAPI, url_prefix='/devices')
    return app
