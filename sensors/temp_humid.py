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
            a = 1
            #print(f"Setting GPIO mode: {mode}")

        def cleanup(self):
            cleanup = True

        def setup(self, pin, mode):
            a = 1
            #print(f"Setting up GPIO pin {pin} as {mode}")

        def output(self, pin, value):
            a = 1
            #print(f"Setting GPIO pin {pin} to {value}")

    GPIO = FakeGPIO()

    class FakeDHT:
        temperature = 25
        humidity = 25
        def __init__(self, sensor, pin):
            self.temperature = 25.0  # Dummy temperature value
            self.humidity = 50.0  # Dummy humidity value
    adafruit_dht = type("adafruit_dht", (), {"DHT11": None})
    board = type("board", (), {"D5": "D5"})
    sensor = FakeDHT(adafruit_dht.DHT11, board.D5)
    board = FakeBoard()
else:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    import dht11
    import board

    if  __name__ == '__main__':
        import cpio
    else:
        from . import cpio

    pin = cpio.Cpio.Temperature.value
    sensor = dht11.DHT11(pin = pin)



def get_temp_humid() -> float | float:
    temperature = 0
    humidity = 0

    failedRounds = 0

    while temperature == 0 or humidity == 0 or failedRounds == 10:
        print(f'temperature and humidity is {temperature} and {humidity}')
        try:
            result = sensor.read()
            temperature = result.temperature
            humidity = result.humidity
            print(f'get_temp_humid = {temperature} / {humidity}')
            time.sleep(.5)
        except RuntimeError as error:
            print(f"Error: {error}, retrying...")
            time.sleep(1)
        except Exception as error:
            print(f"Error: {error}, retrying...")
            time.sleep(1)
        failedRounds += 1
        
    return temperature, humidity


if __name__ == '__main__':
    print(get_temp_humid())