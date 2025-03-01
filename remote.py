import RPi.GPIO as GPIO
import time

RELAY_PIN = 16  # GPIO Bus16

GPIO.setmode(GPIO.BCM)
GPIO.setup(RELAY_PIN, GPIO.OUT)

try:
    print("Turning ON Water Pump")
    GPIO.output(RELAY_PIN, GPIO.HIGH)  # Activate relay (pump ON)
    time.sleep(5)  # Run pump for 5 seconds
    print("Turning OFF Water Pump")
    GPIO.output(RELAY_PIN, GPIO.LOW)  # Deactivate relay (pump OFF)
except KeyboardInterrupt:
    print("Process interrupted")
finally:
    GPIO.cleanup()
