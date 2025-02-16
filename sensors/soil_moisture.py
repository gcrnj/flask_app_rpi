from time import sleep
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn



def get_from_pot(pot_number: int) -> int | None:

    try:
        i2c = busio.I2C(board.SCL, board.SDA)  # or busnum=21

        # Initialize ADS1115
        ads = ADS.ADS1115(i2c)
        ads.gain = 1  # Set gain to �4.096V

        # Read from channel A0
        # channel0 = AnalogIn(ads, ADS.P0)
        # channel1 = AnalogIn(ads, ADS.P1)
        # channel2 = AnalogIn(ads, ADS.P2)
        # channel3 = AnalogIn(ads, ADS.P3)
        match pot_number:
            case 1:
                return AnalogIn(ads, ADS.P1).value
            case 2:
                return AnalogIn(ads, ADS.P2).value
            case 3:
                return AnalogIn(ads, ADS.P3).value
        return None  # Return None instead of a string
    except Exception as e:
        return None
