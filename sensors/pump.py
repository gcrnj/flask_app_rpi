import cpio
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)  # Use BCM numbering
PUMP_PIN = cpio.Cpio.Pump.value
GPIO.setup(PUMP_PIN, GPIO.OUT)  # Set grow light pin as output because you are sending signals to it

def get_pump_status() -> bool:
    return True

def turn_on():
    GPIO.setup(PUMP_PIN, GPIO.OUT)  # Set grow light pin as output because you are sending signals to it
    GPIO.output(PUMP_PIN, GPIO.LOW)  # Activate relay (pump ON)
    print("Pump turned on")

def turn_off():
    GPIO.setup(PUMP_PIN, GPIO.OUT)  # Set grow light pin as output because you are sending signals to it
    GPIO.output(PUMP_PIN, GPIO.HIGH)  # Activate relay (pump ON)
    print("Pump turn off")