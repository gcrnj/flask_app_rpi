import RPi.GPIO as GPIO
import adafruit_dht
import board
import time


DHT_SENSOR = adafruit_dht.DHT11(board.D27)

while True:
    try:
        temperature = DHT_SENSOR.temperature
        humidity = DHT_SENSOR.humidity
        print(f"Temp: {temperature}C  Humidity: {humidity}%")
    except RuntimeError as error:
        print(f"Error: {error}, retrying...")
    except Exception as error:
        DHT_SENSOR.exit()
        raise error
    
    time.sleep(2)  # Wait 2 seconds before next reading
