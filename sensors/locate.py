import smbus2

bus1 = smbus2.SMBus(1)
bus20 = smbus2.SMBus(20)
bus21 = smbus2.SMBus(20)
address = 0x48

def locateBus(busNumber):
    try:
        busNumber.write_byte(address, 0)
        print("ADS1115 detected at 0x48")
    except OSError:
        print("No device detected at 0x48")

print('Bus 1')
locateBus(bus1)
print('Bus 20')
locateBus(bus20)
print('Bus 21')
locateBus(bus21)