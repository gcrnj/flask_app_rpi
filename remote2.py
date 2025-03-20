from flask import Flask, jsonify
import threading
from sensors import async_py

app = Flask(__name__)

# Global variable to store initial data
initial_data = {}

def start_sensors():
    global initial_data
    initial_data = async_py.run_sensors_in_background()

@app.route('/start', methods=['GET'])
def start():
    sensor_thread = threading.Thread(target=start_sensors, daemon=True)
    sensor_thread.start()
    return jsonify({"message": "Sensors started", "initial_data": initial_data})

@app.route('/status', methods=['GET'])
def get_status():
    return jsonify(initial_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
