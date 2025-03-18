import sys
import time

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

if  __name__ == '__main__':
    import cpio
else:
    from . import cpio

GPIO.setmode(GPIO.BCM)  # Use BCM numbering
VALVE1 = cpio.Cpio.Vavle1.value
VALVE2 = cpio.Cpio.Vavle2.value
VALVE3 = cpio.Cpio.Vavle3.value

def set_output_bcms():
    GPIO.setup(VALVE1, GPIO.OUT)  # Set valve pins as output
    GPIO.setup(VALVE2, GPIO.OUT)
    GPIO.setup(VALVE3, GPIO.OUT)

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
    GPIO.output(gpio, GPIO.LOW)  # Activate relay (valve ON)
    print(f"Valve {pot_number} turned on")

def turn_valve_off(pot_number):
    set_output_bcms()
    gpio = get_cpio_from_pot(pot_number)
    print(f"Pot {pot_number}, BCM {gpio} turning off...")
    GPIO.output(gpio, GPIO.HIGH)  # Deactivate relay (valve OFF)
    print(f"Valve {pot_number} turned off")

if __name__ == '__main__':
    turn_valve_off(1)
    turn_valve_off(2)
    turn_valve_off(3)
    while True:
        from time import sleep
        turn_valve_on(1)
        sleep(1)
        turn_valve_on(2)
        sleep(1)
        turn_valve_on(3)
        sleep(2)

        turn_valve_off(1)
        sleep(1)
        turn_valve_off(2)
        sleep(1)
        turn_valve_off(3)
        sleep(2)