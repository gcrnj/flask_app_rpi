import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)  # or busnum=21

# Initialize ADS1115
ads = ADS.ADS1115(i2c)

# Read from channel A0
chan = AnalogIn(ads, ADS.P0)

while True:
    print(f"Raw ADC Value: {chan.value}, Voltage: {chan.voltage:.2f}V")
    time.sleep(1)

