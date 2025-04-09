import sys
import time
if sys.platform == "win32":
    print("Running on Windows - Using dummy GPIO")

    class FakeBoard:
        SCL = "SCL"
        SDA = "SDA"
        D5 = "D5"
        D6 = "D6"

    class FakeGPIO:
        BCM = "BCM"
        OUT = "OUT"
        LOW = "LOW"
        HIGH = "HIGH"

        def setmode(self, mode):
            print(f"Setting GPIO mode: {mode}")

        def cleanup(self):
            cleanup = True

        def setup(self, pin, mode):
            print(f"Setting up GPIO pin {pin} as {mode}")

        def output(self, pin, value):
            print(f"Setting GPIO pin {pin} to {value}")

    GPIO = FakeGPIO()

    class FakeDHT:
        temperature = 25
        humidity = 25
        def __init__(self, sensor, pin):
            self.temperature = 25.0  # Dummy temperature value
            self.humidity = 50.0  # Dummy humidity value
    adafruit_dht = type("adafruit_dht", (), {"DHT11": None})
    board = type("board", (), {"D5": "D5"})
    DHT_SENSOR = FakeDHT(adafruit_dht.DHT11, board.D5)
    board = FakeBoard()
else:
    import RPi.GPIO as GPIO
    import adafruit_dht
    import board

    GPIO.cleanup()
    GPIO.setup(21, GPIO.OUT)  # Set valve pins as output
    DHT_SENSOR = adafruit_dht.DHT22(board.D21)

def get_temp_humid() -> float | float:
    temperature = None
    humidity = None
    while temperature is None or humidity is None:
        try:
            temperature = DHT_SENSOR.temperature
            humidity = DHT_SENSOR.humidity
            print(f'get_temp_humid = {temperature} / {humidity}')
            time.sleep(.5)
        except RuntimeError as error:
            print(f"Error: {error}, retrying...")
            time.sleep(1)
        except Exception as error:
            print(f"Error: {error}, retrying...")
            time.sleep(1)
    
    print(f'get_temp_humid = {temperature} / {humidity}')
    return temperature, humidity


if __name__ == '__main__':
    print(get_temp_humid())