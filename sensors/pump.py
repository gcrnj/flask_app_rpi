import cpio
import RPi.GPIO as GPIO

PUMP_PIN = cpio.Cpio.Pump

def get_pump_status() -> bool:
    return True

def turn_on():
    GPIO.output(PUMP_PIN, GPIO.LOW)  # Activate relay (pump ON)
    print("Pump turned on")

def turn_off():
    GPIO.output(PUMP_PIN, GPIO.HIGH)  # Activate relay (pump ON)
    print("Pump turn off")