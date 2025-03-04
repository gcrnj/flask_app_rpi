from time import sleep
import sys

# Handle platform-specific imports
if sys.platform == "win32":
    print("Running on Windows - Using dummy hardware modules")

    class FakeBoard:
        SCL = "SCL"
        SDA = "SDA"

    class FakeADS:
        P0 = "P0"
        P1 = "P1"
        P2 = "P2"
        P3 = "P3"

    class FakeAnalogIn:
        def __init__(self, ads, pin):
            self.voltage = 2.5  # Return a dummy value

    class FakeI2C:
        def __init__(self, scl, sda):
            print(f"Initializing Fake I2C on {scl}, {sda}")

    board = FakeBoard()
    ADS = FakeADS()
    AnalogIn = FakeAnalogIn
    busio = FakeI2C  # Mock I2C

else:
    import busio
    import board  # Import actual board module on Raspberry Pi
    import adafruit_ads1x15.ads1115 as ADS
    from adafruit_ads1x15.analog_in import AnalogIn

def get_from_pot(pot_number: int):
    try:
        i2c = busio.I2C(board.SCL, board.SDA)  # Initialize I2C
        ads = ADS.ADS1115(i2c)
        ads.gain = 1  # Set gain to ±4.096V

        match pot_number:
            case 1:
                return AnalogIn(ads, ADS.P1).voltage
            case 2:
                return AnalogIn(ads, ADS.P2).voltage
            case 3:
                return AnalogIn(ads, ADS.P3).voltage
        return 0  # If invalid pot_number
    except Exception as e:
        print(f"Error reading sensor: {e}. Returning 0 for pot {pot_number}")
        return 0

### Soil Moisture Voltage Ranges ###
# Dry Soil: 3.4V – 5.0V
# Moist Soil: 1.5V – 3.5V
# Wet Soil: 0.0V – 1.4V