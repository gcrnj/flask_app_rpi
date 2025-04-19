import random
from datetime import datetime, timezone, timedelta
import time
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase Admin SDK
cred = credentials.Certificate('api/firebase_key.json')
firebase_admin.initialize_app(cred)

# Define Firestore reference
db = firestore.client()

# Define the timezone for the Philippines (PH_TZ)
PH_TZ = timezone(timedelta(hours=8))  # UTC+8 for the Philippines

# Helper function to generate data for each hour
def generate_soil_data_for_hour(current_time):
    # Randomize moisture levels between 2.0 and 4.3
    moisture1 = round(random.uniform(2.0, 4.3), 2)
    moisture2 = round(random.uniform(2.0, 4.3), 2)
    moisture3 = round(random.uniform(2.0, 4.3), 2)

    # Randomize temperature between 25.0 and 34.0
    temperature = round(random.uniform(25.0, 34.0), 2)

    # Randomize humidity between 50 and 80
    humidity = random.randint(50, 80)

    # Determine if water was distributed (if any moisture value is between 2.7 and 4.0)
    water_distributed = (2.7 <= moisture1 <= 4.0) or (2.7 <= moisture2 <= 4.0) or (2.7 <= moisture3 <= 4.0)

    # Prepare the data payload
    post_data = {
        "moisture1": moisture1,
        "moisture2": moisture2,
        "moisture3": moisture3,
        "temperature": temperature,
        "humidity": humidity,
        "time": current_time,
        "water_distributed": water_distributed
    }
    
    return post_data

# Function to upload data to Firestore
def upload_to_firestore(device_id, post_data):
    try:
        # Reference to the Firestore subcollection for soil moisture readings
        readings_ref = db.collection('devices').document(device_id).collection('moisture_readings')

        # Add data to Firestore
        new_doc_ref = readings_ref.add(post_data)

        # Print success message and document ID
        print(f"Data added with doc ID: {new_doc_ref[1].id}")
    except Exception as e:
        print(f"Error uploading to Firestore: {str(e)}")

# Main function to generate data from today to March 1, 2025
def main():
    # Set the current date (today) in the Philippines timezone
    current_date = datetime(2025, 4, 10, 15, 0, tzinfo=PH_TZ)  # Current date, now

    # Set the end date (March 1, 2025) in the Philippines timezone
    end_date = datetime(2025, 3, 1, 0, 0, tzinfo=PH_TZ)  # March 1, 2025, 00:00

    # Specify the device ID for storing data (you can modify it based on actual use)
    device_id = 'Zg6XgWqdztP3bDwquu51'

    # Iterate over the hours from current_date to March 1, 2025
    current_time = current_date

    while current_time >= end_date:
        # Generate data for the current hour
        post_data = generate_soil_data_for_hour(current_time)

        # Upload the data to Firestore
        upload_to_firestore(device_id, post_data)

        # Move to the previous hour
        current_time -= timedelta(hours=1)

        # Sleep for a short time (to prevent overwhelming resources in an example script)
        time.sleep(0.1)  # You can adjust or remove this in a real script

if __name__ == "__main__":
    main()
