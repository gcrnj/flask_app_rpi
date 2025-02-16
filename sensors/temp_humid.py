import RPi.GPIO as GPIO
import adafruit_dht
import board
import time


DHT_SENSOR = adafruit_dht.DHT11(board.D5)

def get_temp_humid() -> float | float:
    try:
        temperature = DHT_SENSOR.temperature
        humidity = DHT_SENSOR.humidity
        return temperature, humidity
    except RuntimeError as error:
        print(f"Error: {error}, retrying...")
        return None, None
    except Exception as error:
        print(f"Error: {error}, retrying...")
        return None, None

print(get_temp_humid())