import RPi.GPIO as GPIO
import cpio


GPIO.cleanup()  # Reset any previous GPIO settings
# Set up GPIO
GPIO.setmode(GPIO.BCM)  # Use BCM numbering
growlight_gpio_bus = cpio.Cpio.Growlight.value
GPIO.setup(growlight_gpio_bus, GPIO.OUT)  # Set grow light pin as output because you are sending signals to it

def get_growlight_status() -> bool:
    state = GPIO.input(growlight_gpio_bus)  # Read GPIO pin state
    return state == GPIO.LOW  # True if HIGH (ON), False if LOW (OFF)

def turn_on_growlight():
    GPIO.output(growlight_gpio_bus, GPIO.LOW)  # Set GPIO pin to HIGH to turn on the grow light

def turn_off_growlight():
    GPIO.output(growlight_gpio_bus, GPIO.HIGH)  # Set GPIO pin to HIGH to turn on the grow light


turn_off_growlight()
print(get_growlight_status())