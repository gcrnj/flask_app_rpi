import firebase_admin
from firebase_admin import credentials, firestore, storage, auth

cred = credentials.Certificate("/firebase_key.json")
firebase_admin.initialize_app(cred)


# Firestore client
db = firestore.client()

# Storage bucket
bucket = storage.bucket()

