import RPi.GPIO as GPIO
import adafruit_dht
import board
import time


DHT_SENSOR = adafruit_dht.DHT11(board.D27)

def get_temp_humid() -> float | float:
    try:
        temperature = DHT_SENSOR.temperature
        humidity = DHT_SENSOR.humidity
        print(f"Temp: {temperature}C  Humidity: {humidity}%")
        DHT_SENSOR.exit()
        return temperature, humidity
    except RuntimeError as error:
        print(f"Error: {error}, retrying...")
        DHT_SENSOR.exit()
        return None, None
    except Exception as error:
        DHT_SENSOR.exit()
        print(f"Error: {error}, retrying...")
        return None, None
