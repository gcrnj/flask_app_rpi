import sys
import time

# Check platform (Windows = use dummy; Raspberry Pi = real sensor)
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
            print("Cleaning up GPIO")

        def setup(self, pin, mode):
            print(f"Setting up GPIO pin {pin} as {mode}")

        def output(self, pin, value):
            print(f"Setting GPIO pin {pin} to {value}")

    GPIO = FakeGPIO()

    class FakeDHT:
        temperature = 25.0
        humidity = 50.0

        def __init__(self, sensor, pin):
            self.temperature = 25.0
            self.humidity = 50.0

    adafruit_dht = type("adafruit_dht", (), {"DHT11": None})
    board = type("board", (), {"D17": "D17"})  # Dummy pin for Windows
    DHT_SENSOR = FakeDHT(adafruit_dht.DHT11, board.D17)
    board = FakeBoard()

else:
    # On Raspberry Pi - use real GPIO and DHT11 sensor
    import RPi.GPIO as GPIO
    import adafruit_dht
    import board

    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()
    GPIO.setup(20, GPIO.OUT)  # Optional: control valve or other component

    # Update this to the correct GPIO pin: GPIO17 = pin 11
    DHT_SENSOR = adafruit_dht.DHT11(board.D17)


def get_temp_humid() -> tuple[float | None, float | None]:
    temperature = None
    humidity = None
    retries = 0
    while (temperature is None or humidity is None) and retries < 10:
        try:
            temperature = DHT_SENSOR.temperature
            humidity = DHT_SENSOR.humidity
            print(f"Attempt {retries+1}: Temp={temperature}, Humidity={humidity}")
        except RuntimeError as error:
            print(f"RuntimeError: {error}, retrying...")
        except Exception as error:
            print(f"Other error: {error}, retrying...")
        time.sleep(1)
        retries += 1

    print(f'Final reading: Temp = {temperature}°C, Humidity = {humidity}%')
    return temperature, humidity


if __name__ == '__main__':
    get_temp_humid()
