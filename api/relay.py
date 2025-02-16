import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Relay pin numbers (replace these with the actual GPIO pins you are using)
relay_pins = [26]  # GPIO pin for the relay (example)

# Set the relay pins as outputs
for pin in relay_pins:
    GPIO.setup(pin, GPIO.OUT)

# Function to turn on all relays
def turn_on_all_relays():
    for pin in relay_pins:
        GPIO.output(pin, GPIO.HIGH)  # Set pin HIGH to turn on relay

# Function to turn off all relays
def turn_off_all_relays():
    for pin in relay_pins:
        GPIO.output(pin, GPIO.LOW)  # Set pin LOW to turn off relay

# Example of turning relays on and off
try:
    print("Turning on all relays")
    turn_on_all_relays()
    time.sleep(5)  # Keep relays on for 2 seconds
    
    print("Turning off all relays")
    turn_off_all_relays()
    time.sleep(20)  # Keep relays off for 2 seconds
except Exception as error:
    print(error)
finally:
    GPIO.cleanup()  # Clean up GPIO settings
