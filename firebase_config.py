import firebase_admin
from firebase_admin import credentials, firestore, storage, auth

cred = credentials.Certificate("/firebase_key.json")
firebase_admin.initialize_app(cred, {
    'storageBucket': 'gs://project-corntrack.firebasestorage.app'  # Replace with your actual bucket name
})


# Firestore client
db = firestore.client()

# Storage bucket
bucket = storage.bucket()

