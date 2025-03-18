import sys

if  __name__ == '__main__':
    import cpio
else:
    from . import cpio

if sys.platform == "win32":
    print("Running on Windows - Using dummy GPIO")

    class FakeGPIO:
        BCM = "BCM"
        OUT = "OUT"
        LOW = "LOW"
        HIGH = "HIGH"

        def setmode(self, mode):
            print(f"Setting GPIO mode: {mode}")

        def setup(self, pin, mode):
            print(f"Setting up GPIO pin {pin} as {mode}")

        def output(self, pin, value):
            print(f"Setting GPIO pin {pin} to {value}")

    GPIO = FakeGPIO()
else:
    import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)  # Use BCM numbering
FAN_PIN = cpio.Cpio.Fan.value
GPIO.setup(FAN_PIN, GPIO.OUT)  # Set fan pin as output

def get_fan_status() -> bool:
    return True

def turn_on():
    GPIO.setup(FAN_PIN, GPIO.OUT)
    GPIO.output(FAN_PIN, GPIO.LOW)  # Activate relay (fan ON)
    print("Fan turned on")

def turn_off():
    GPIO.setup(FAN_PIN, GPIO.OUT)
    GPIO.output(FAN_PIN, GPIO.HIGH)  # Deactivate relay (fan OFF)
    print("Fan turned off")


if __name__ == '__main__':
    from time import sleep
    while True:
        turn_on()
        sleep(7)
        turn_off()
        sleep(7)