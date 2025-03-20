from sensors import soil_moisture as moisture_py, valve as valve_py, pump as pump_py, temp_humid as temperature_py, growlight as growlight_py
import time
import sys
import threading

validMaxTemperature = 28
validMinTemperature = 33

def run_sensors(should_get_first_data):
    time.sleep(0.5)
    soilMoisture1 = 0
    soilMoisture2 = 0
    soilMoisture3 = 0
    isPumpOn = False
    isGrowLightOn = False
    start_time = time.time()  # Record the start time

    growlight_done = False
    water_pump_done = False
    fan_done = False


    
    while not growlight_done or not water_pump_done or not fan_done:
        # ==========================================================
        # ================ GROWLIGHT AND DHT11  ======================
        # ==========================================================

        print("/////Checking DHT11 & Growlight")

        temperature, humidity = temperature_py.get_temp_humid()
        print(f'Got {temperature} / {humidity}')

        # TEMPERATURE 28 - 33
        if temperature == None:
            print("Error temperature")
        elif temperature < 28:
            # Turn on growlight
            print(f'Temperature {temperature} is too low. Turning on growlight.')
            isGrowLightOn = True
            growlight_py.turn_on_growlight()
        elif temperature > 33:
            # Turn off growlight
            growlight_done = True
            print(f'Temperature {temperature} is too high. Turning off growlight.')
            growlight_py.turn_off_growlight()
        else:
            growlight_done = True
            print(f'Temperature {temperature} is just right.')
        
        # HUMIDITY 50 - 80
        if temperature == None:
            print('Error in humidity')
        elif humidity > 80:
            fan_done = True


        # ====================================================================
        # =================== PUMP AND SOIL MOISTURE =========================
        # ====================================================================
        print("///// Start PUMP AND SOIL MOISTURE")
        moisture1 = moisture_py.get_from_pot(1)
        moisture2 = moisture_py.get_from_pot(2)
        moisture3 = moisture_py.get_from_pot(3)
        print(f"Moisture1 = {moisture1}")
        print(f"Moisture2 = {moisture2}")
        print(f"Moisture3 = {moisture3}")
        print("///// Done PUMP AND SOIL MOISTURE")

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

        isValve1On = False
        isValve2On = False
        isValve3On = False
        
        # ===================================================================
        # ===================== WATER PUMP AND VALVES 1-3 ===================
        # ===================================================================
        if not water_pump_done:
            # Soil Moisture 1 and  Valve 1
            if moisture1 <= 3.6 and moisture1 > 2.7:
                isValve1On = True
                valve_py.turn_valve_on(1)
            else:
                valve_py.turn_valve_off(1)

            # Valve 2
            if moisture2 <= 3.6 and moisture2 > 2.7:
                isValve2On = True
                valve_py.turn_valve_on(2)
            else:
                valve_py.turn_valve_off(2)

            # Valve 3
            if moisture3 <= 3.6 and moisture3 > 2.7:
                isValve3On = True
                valve_py.turn_valve_on(3)
            else:
                valve_py.turn_valve_off(3)
            
            # Turn or off Pump
            if isValve1On or isValve2On or isValve3On:
                isPumpOn = True
                pump_py.turn_on()
                print("Pump is On")
            else:
                pump_py.turn_off()
                print("Pump is Off")
                water_pump_done = True

        print("\\\\")

        isWindows = sys.platform == "win32"
        elapsed_time = time.time() - start_time
        print(f"Elapsed Time: {elapsed_time:.2f} seconds")

        if should_get_first_data:
            print('Returning initial_data')
            return {
                'water_distributed': isPumpOn,
                'moisture1': moisture1,
                'moisture2': moisture2,
                'moisture3': moisture3,
                'temperature': temperature,
                'humidity': humidity,
                'light': isGrowLightOn
            }
        else:
            print('Not returning initial_data')


        print('\n===================\n')
        time.sleep(2)

        

def run_sensors_in_background():
    initial_data = run_sensors(True)
    sensor_thread = threading.Thread(target=run_sensors, args=(False,), daemon=True)
    sensor_thread.start()
    return initial_data

if __name__ == '__main__':
    print('Run in remote2.py')