import firebase_admin
from firebase_admin import credentials, messaging, firestore
from dataclasses import dataclass
from typing import List
from datetime import datetime, timezone, timedelta

@dataclass
class UserDevice:
    tokens: List[str]
    name: str
    userId: str

# Load Firebase credentials
cred = credentials.Certificate("api/firebase_key2.json")
firebase_admin.initialize_app(cred, {"storageBucket": "project-corntrack.firebasestorage.app"})  # Ensure correct bucket name

db = firestore.client()
PH_TZ = timezone(timedelta(hours=8))


def get_device_tokens(device_id):
    """Fetch the device owner's tokens from Firestore."""
    device_ref = db.collection("devices").document(device_id)
    device_doc = device_ref.get()

    if device_doc.exists:
        owner_ids = device_doc.to_dict().get("ownerId", [])  # Ensure it's a list
        user_devices = []

        for owner_id in owner_ids:
            user_ref = db.collection("users").document(owner_id)
            user_doc = user_ref.get()
            if user_doc.exists:
                user_data = user_doc.to_dict()
                user_devices.append(UserDevice(
                    tokens=user_data.get("fcm_tokens", []),
                    name=user_data.get("firstName", ""),
                    userId=user_doc.id
                ))

        return user_devices if user_devices else []

    return []


def send_push_notification(device_id, post_data):
    """Fetch tokens dynamically and send push notifications."""
    final_message = generate_notification_message(post_data)
    user_devices: List[UserDevice] = get_device_tokens(device_id)
    if not user_devices:
        print("Error: No valid tokens found for the device.")
        return

    messages = []
    for user in user_devices:
        title = f"Hello, {user.name}! Corntrack Update!"
        body = message
        for token in user.tokens:
            messages.append(messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                token=token,
            ))
            print(f'Sending to: {user.name}\n')
            print(f'Tokens: {user.tokens}\n')
            print(f'Message:\n {message}\n')
        add_notification_to_firebase(user.userId, title, body)

    response = messaging.send_each(messages)  # Send to multiple tokens
    print(f"Successfully sent messages: {response}")
    
    # Logging successful and failed responses
    for idx, resp in enumerate(response.responses):
        if resp.success:
            print(f"Message {idx + 1} sent successfully!")
        else:
            print(f"Message {idx + 1} failed: {resp.exception}")

    print(f"Total messages sent: {response.success_count}/{len(messages)}")


def add_notification_to_firebase(user_id, title, body):
    """Add a notification entry to Firestore under users/{user_id}/notifications."""
    notifications_ref = db.collection("users").document(user_id).collection("notifications")
    notifications_ref.add({
        "title": title,
        "body": body,
        "time": datetime.now(PH_TZ),
        "is_read": False
    })



def generate_notification_message(post_data):
    # {
    #         "moisture1": moisture1,
    #         "moisture2": moisture2,
    #         "moisture3": moisture3,
    #         "temperature": temperature,
    #         "humidiity": humidity,
    #         "time": date_time,
    #         "water_distributed": water_distributed
    #     }
    # post_data['type'] = 'soil_moisture'
    # post_data['time'] = date_time.isoformat()def generate_notification_message(post_data):
    messages = []
    moisture1 = post_data['moisture1']
    moisture2 = post_data['moisture2']
    moisture3 = post_data['moisture3']
    temperature = post_data['temperature']
    humidity = post_data['humidiity']
    time = post_data['date_time']
    water_distributed = post_data['water_distributed']

    valves_triggered = []

    if water_distributed:
        messages.append("Water was distributed ✅")

    if 2.7 < moisture1 <= 3.6:
        valves_triggered.append("Valve 1")
    if 2.7 < moisture2 <= 3.6:
        valves_triggered.append("Valve 2")
    if 2.7 < moisture3 <= 3.6:
        valves_triggered.append("Valve 3")

    if valves_triggered:
        messages.append(f"Activated Valves: {', '.join(valves_triggered)}")

    messages.append(f"Temperature: {temperature}°C | Humidity: {humidity}%")

    # Example Usage
    return "\n".join(messages)

if __name__ == '__main__':
    post_data = {
        "moisture1": 3.0,
        "moisture2": 4.0,
        "moisture3": 2.5,
        "temperature": 26,
        "humidiity": 60,
        "date_time": "2025-03-20 10:30 AM",
        "water_distributed": True
    }
    message = generate_notification_message(post_data)
    if message:
        tokens = send_push_notification('Zg6XgWqdztP3bDwquu51', message)



