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

PUMP_PIN = cpio.Cpio.Pump.value

def get_pump_status() -> bool:
    return True

def turn_on():
    GPIO.setmode(GPIO.BCM)  # Use BCM numbering
    GPIO.setup(PUMP_PIN, GPIO.OUT)  # Set grow light pin as output because you are sending signals to it
    GPIO.output(PUMP_PIN, GPIO.LOW)  # Activate relay (pump ON)
    print("Pump turned on")

def turn_off():
    GPIO.setmode(GPIO.BCM)  # Use BCM numbering
    GPIO.setup(PUMP_PIN, GPIO.OUT)  # Set grow light pin as output because you are sending signals to it
    GPIO.output(PUMP_PIN, GPIO.HIGH)  # Activate relay (pump ON)
    print("Pump turn off")

if __name__ == '__main__':
    from time import sleep
    while True:
        turn_on()
        sleep(1)
        turn_off()
        sleep(100)        