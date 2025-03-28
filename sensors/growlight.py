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

        def input(self, pin):
            print(f"Setting GPIO pin {pin} to input")

    GPIO = FakeGPIO()
else:
    import RPi.GPIO as GPIO

# GPIO.cleanup()  # Reset any previous GPIO settings
# Set up GPIO
growlight_gpio_bus = cpio.Cpio.Growlight.value

def get_growlight_status() -> bool:
    state = GPIO.input(growlight_gpio_bus)  # Read GPIO pin state
    return state == GPIO.LOW  # True if HIGH (ON), False if LOW (OFF)

def turn_on_growlight():
    GPIO.setmode(GPIO.BCM)  # Use BCM numbering
    GPIO.setup(growlight_gpio_bus, GPIO.OUT)  # Set grow light pin as output because you are sending signals to it
    GPIO.output(growlight_gpio_bus, GPIO.LOW)  # Set GPIO pin to HIGH to turn on the grow light

def turn_off_growlight():
    GPIO.setmode(GPIO.BCM)  # Use BCM numbering
    GPIO.setup(growlight_gpio_bus, GPIO.OUT)  # Set grow light pin as output because you are sending signals to it
    GPIO.output(growlight_gpio_bus, GPIO.HIGH)  # Set GPIO pin to HIGH to turn on the grow light

if __name__ == '__main__':
    from time import sleep
    while True:
        print('Turn on GL')
        turn_on_growlight()
        sleep(2)
        print('Turn off GL')
        turn_off_growlight()
        sleep(2)