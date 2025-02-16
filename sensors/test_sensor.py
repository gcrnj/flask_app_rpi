from time import sleep
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
while True:
        try:        
                # Initialize I2C bus
                i2c = busio.I2C(board.SCL, board.SDA)  # or busnum=21

                # Initialize ADS1115
                ads = ADS.ADS1115(i2c)
                ads.gain = 1  # Set gain to �4.096V


                # Read from channel A0
                channel0 = AnalogIn(ads, ADS.P0)
                channel1 = AnalogIn(ads, ADS.P1)
                channel2 = AnalogIn(ads, ADS.P2)
                channel3 = AnalogIn(ads, ADS.P3)

                # # while True:
                # #     print(f"Raw ADC Value: {chan.value}, Voltage: {chan.voltage:.2f}V")
                print(f"First Pot: {channel0.value}, {channel0.voltage:.2f}V")
                print(f"Second Pot: {channel1.value}, {channel1.voltage:.2f}V")
                print(f"Third Pot: {channel2.value}, {channel2.voltage:.2f}V")
                print(f"Fourth Pot: {channel3.value}, {channel3.voltage:.2f}V")
                print("===========================\n")

        except Exception as e:
                print(e)
                
        sleep(2)
