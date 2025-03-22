from flask import Flask, send_file, jsonify
import pandas as pd
import matplotlib
matplotlib.use("Agg")  # Fix RuntimeError: main thread is not in main loop
import matplotlib.pyplot as plt
from firebase_admin import db, firestore
from flask import Blueprint, request, jsonify
from datetime import timezone, timedelta
import base64
import io

db = firestore.client()

graphsAPI = Blueprint('graphs', __name__)
PH_TZ = timezone(timedelta(hours=8))

def fetch_data_from_firebase(device_id):
    """Fetch moisture readings from Firebase for a given device ID."""
    ref = db.collection(f"devices/{device_id}/moisture_readings")
    docs = ref.stream()

    data = []
    for doc in docs:
        doc_data = doc.to_dict()
        doc_data["time"] = pd.to_datetime(doc_data["time"])  # Convert time to datetime
        data.append(doc_data)

    if not data:
        return None

    return pd.DataFrame(data)

def generate_graph(df, moisture_id):
    """Generate the graph and return it as a Base64 string."""
    plt.figure(figsize=(8, 5))
    plt.plot(df["time"], df[moisture_id], marker="o", label="Moisture")
    plt.plot(df["time"], df["temperature"], marker="s", label="Temperature", linestyle="dashed")
    plt.plot(df["time"], df["humidiity"], marker="^", label="Humidity", linestyle="dotted")

    plt.xlabel("Date")
    plt.ylabel("Values")
    plt.title("Soil Moisture, Temperature & Humidity Trends")
    plt.legend()
    plt.grid(True)

    # Save the image to a BytesIO stream
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format="png")
    plt.close()
    
    img_buffer.seek(0)
    return base64.b64encode(img_buffer.read()).decode("utf-8")

def generate_conclusion(df, moistureId: str):
    """Generate a non-technical conclusion based on the data using a specified moisture sensor."""
    
    # Ensure the provided moistureId exists in the DataFrame
    if moistureId not in df.columns:
        return f"Error: {moistureId} is not a valid column."

    avg_moisture = df[moistureId].mean()
    avg_temp = df["temperature"].mean()
    avg_humidity = df["humidiity"].mean()  # Corrected column name

    # Moisture assessment
    if avg_moisture > 2.7:
        moisture_comment = "The soil is often too dry. Increase watering frequency."
    elif avg_moisture < 2:
        moisture_comment = "The soil is often too wet. Reduce watering to avoid root rot."
    else:
        moisture_comment = "Moisture levels are balanced. Keep monitoring!"

    # Temperature assessment
    if avg_temp < 28:
        temp_comment = "Temperature is quite low. Increase grow light exposure."
    elif avg_temp > 33:
        temp_comment = "Temperature is quite high. Consider shading or cooling methods."
    else:
        temp_comment = "Temperature is within a good range."

    # Humidity assessment
    if avg_humidity < 50:
        humidity_comment = "Humidity is low. The soil might dry faster, so adjust watering."
    elif avg_humidity > 80:
        humidity_comment = "Humidity is high. The corn might die."
    else:
        humidity_comment = "Humidity levels are good for plant growth."

    # Check if all conditions are optimal
    if (
        2 <= avg_moisture <= 2.7 and
        28 <= avg_temp <= 33 and
        50 <= avg_humidity <= 80
    ):
        efficiency_comment = "Plant is growing efficiently."
    else:
        efficiency_comment = ""

    return f"{moisture_comment}\n{temp_comment}\n{humidity_comment}\n{efficiency_comment}".strip()


@graphsAPI.route("/get-graph/<device_id>", methods=["GET"])
def get_graph(device_id):
    """API endpoint to return multiple graphs and conclusions based on moisture sensors."""

    # Get moistureIds from query parameters, defaulting to ["moisture1"] if not provided
    moisture_ids = request.args.get("moistureId", "moisture1").split(",")

    # Validate moistureIds
    valid_moisture_ids = {"moisture1", "moisture2", "moisture3"}
    invalid_ids = [m_id for m_id in moisture_ids if m_id not in valid_moisture_ids]

    if invalid_ids:
        return jsonify({"error": f"Invalid moistureId(s): {', '.join(invalid_ids)}"}), 400

    df = fetch_data_from_firebase(device_id)
    if df is None:
        return jsonify({"error": "No data found for this device"}), 404

    # Generate results for each moistureId
    results = []
    for moisture_id in moisture_ids:
        graph_base64 = generate_graph(df, moisture_id)
        conclusion = generate_conclusion(df, moisture_id)
        
        results.append({
            "moisture_id": moisture_id,
            "graph_base64": graph_base64,
            "conclusion": conclusion
        })

    return jsonify({
        "device_id": device_id,
        "data": results
    })