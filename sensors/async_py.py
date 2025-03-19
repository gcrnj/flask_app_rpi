from sensors import soil_moisture as moisture_py, valve as valve_py, pump as pump_py, temp_humid as temperature_py, growlight as growlight_py
import time
import sys

validMaxTemperature = 28
validMinTemperature = 33

def run_sensors():
    time.sleep(0.5)
    temp = 0
    humid = 0
    isValve1On = False
    isValve2On = False
    isValve3On = False
    soilMoisture1 = 0
    soilMoisture2 = 0
    soilMoisture3 = 0
    isPumpOn = False
    isGrowLightOn = False
    isAPICalled = False
    start_time = time.time()  # Record the start time


    
    while not isAPICalled:
        #============= DHT11 & Growlight
        print("/////Checking DHT11 & Growlight")
        temperature, humidity = temperature_py.get_temp_humid()
        print(f'Got {temperature} / {humidity}')
        if temperature != None:
            print("/////DHT11 & Growlight None")
            temp = temperature
            humid = humidity
        # growlight_status =  growlight_py.get_growlight_status()
        if temperature == None:
            print("Error temperature")
        elif temperature < 28:
            # Turn on growlight
            print(f'Temperature {temperature} is too low. Turning on growlight.')
            isGrowLightOn = True
            growlight_py.turn_on_growlight()
        elif temperature > 27:
            # Turn off growlight
            print(f'Temperature {temperature} is too high. Turning off growlight.')
            growlight_py.turn_off_growlight()
        else:
            print(f'Temperature {temperature} is just right.')

        #============= Soil Moisture, Pump & Solenoid Valve
        print("/////Checking Soil Moisture, Pump & Solenoid Valve")
        moisture1 = moisture_py.get_from_pot(1)
        print(f"Moisture1 = {moisture1}")
        moisture2 = moisture_py.get_from_pot(2)
        print(f"Moisture2 = {moisture2}")
        moisture3 = moisture_py.get_from_pot(3)
        print(f"Moisture3 = {moisture3}")
        valve1 = valve_py.get_valve_status(1)
        valve2 = valve_py.get_valve_status(2)
        valve3 = valve_py.get_valve_status(3)
        print("/////Done getting the data")

        ### Dry Soil: 3.4V – 5.0V
    
        ### Moist Soil: 1.5V – 3.5V
        ### Wet Soil: 0.0V – 1.4V
        ### None 3.2-3.6V

        # Findings:
        # AIR / SNO SOIL - 3.65 & 3.87
        # Dry Soil - 3.45
        # Moist Soil = 2.6-2.7
        # Wet Soil - 1.95-1.98
        # Water - 2.07 - 2.15


         # Findings:
        # AIR / SNO SOIL - 3.7-3.8
        # Dry Soil - 3.6
        # Moist Soil = 2.6-2.7
        # Wet Soil - 2.2
        # Water - 2.07 - 2.15


        ### Dry Soil / Air → Lower capacitance → Higher voltage output
        ### Moist Soil → Higher capacitance → Lower voltage output
        

        if moisture1 != 777:
            soilMoisture1 = moisture1
        if moisture2 != 777:
            soilMoisture2 = moisture2
        if moisture3 != 777:
            soilMoisture3 = moisture3

        # pump is off
        shouldTurnPumpOn = False

        # Soil Moisture 1 and  Valve 1
        if moisture1 <= 3.6 and moisture1 > 2.7:
            isValve1On = True
            valve_py.turn_valve_on(1)
            shouldTurnPumpOn = True
        else:
            valve_py.turn_valve_off(1)

        # Valve 2
        if moisture2 <= 3.6 and moisture2 > 2.7:
            isValve2On = True
            valve_py.turn_valve_on(2)
            shouldTurnPumpOn = True
        else:
            valve_py.turn_valve_off(2)

        # Valve 3
        if moisture3 <= 3.6 and moisture3 > 2.7:
            isValve3On = True
            valve_py.turn_valve_on(3)
            shouldTurnPumpOn = True
        else:
            valve_py.turn_valve_off(3)
        
        # Turn or off Pump
        if shouldTurnPumpOn:
            isPumpOn = True
            pump_py.turn_on()
            print("Pump is On")
        else:
            pump_py.turn_off()
            print("Pump is Off")

        print("\\\\")

        isWindows = sys.platform == "win32"
        elapsed_time = time.time() - start_time
        print(f"Elapsed Time: {elapsed_time:.2f} seconds")

        if (temp != 0 and humid != 0 and soilMoisture1 != 0 and soilMoisture2 != 0 and soilMoisture3 != 0 and not isAPICalled) or isWindows:
            # Call API
            isAPICalled = True
            return {
                'water_distributed': isPumpOn,
                'moisture1': moisture1,
                'moisture2': moisture2,
                'moisture3': moisture3,
                'temperature': temperature,
                'humidity': humidity,
                'light': isGrowLightOn
            }
        time.sleep(0.5)
        








def run():
    print('')
    # asyncio.run(run_sensors())
