import RPi.GPIO as GPIO
from . import cpio
import time

GPIO.setmode(GPIO.BCM)  # Use BCM numberingturn_valve_on
VALVE1 = cpio.Cpio.Vavle1.value
VALVE2 = cpio.Cpio.Vavle2.value
VALVE3 = cpio.Cpio.Vavle3.value

def set_output_bcms():
    GPIO.setup(VALVE1, GPIO.OUT)  # Set grow light pin as output because you are sending signals to it
    GPIO.setup(VALVE2, GPIO.OUT)  # Set grow light pin as output because you are sending signals to it
    GPIO.setup(VALVE3, GPIO.OUT)  # Set grow light pin as output because you are sending signals to it

def get_valve_status(pot_number) -> bool:
    return False

def get_cpio_from_pot(pot_number):
    if pot_number == 1:
        return VALVE1
    elif pot_number == 2:
        return VALVE2
    else:
        return VALVE3

def turn_valve_on(pot_number):
    set_output_bcms()
    gpio = get_cpio_from_pot(pot_number)
    print(f"Pot {pot_number} BCM {gpio} turning on...")
    GPIO.output(gpio, GPIO.LOW)  # Activate relay (pump ON)
    print(f"Valve {pot_number} turned on")
    
def turn_valve_off(pot_number):
    set_output_bcms()
    gpio = get_cpio_from_pot(pot_number)
    print(f"Pot {pot_number}, BCM {gpio} turning off...")
    GPIO.output(gpio, GPIO.HIGH)  # Activate relay (pump ON)
    print(f"Valve {pot_number} turned off")