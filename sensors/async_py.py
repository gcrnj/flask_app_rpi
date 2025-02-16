import asyncio
import soil_moisture as moisture_py, valve as valve_py, pump as pump_py, temp_humid as temperature_py, growlight as growlight_py
import time

validMaxTemperature = 28
validMinTemperature = 33

async def run_sensors():
    await asyncio.sleep(2)

    running_pumps = []
    isLightOn = False

    while True:
        #============= DHT11 & Growlight
        print("/////Checking DHT11 & Growlight")
        temperature, humidity = temperature_py.get_temp_humid()
        growlight_status =  growlight_py.get_growlight_status()
        if temperature == None:
            print("Error temperature")
        elif temperature < 28:
            # Turn on growlight
            print(f'Temperature {temperature} is too low. Turning on growlight.')
            growlight_py.turn_on_growlight()
        elif temperature > 27:
            # Turn off growlight
            print(f'Temperature {temperature} is too high. Turning off growlight.')
            growlight_py.turn_off_growlight()
        else:
            print(f'Temperature {temperature} is just right. Growlight: {growlight_status}')

        #============= Soil Moisture, Pump & Solenoid Valve
        print("/////Checking Soil Moisture, Pump & Solenoid Valve")
        pumpStatus = pump_py.get_pump_status()
        moisture1 = moisture_py.get_from_pot(1)
        moisture2 = moisture_py.get_from_pot(2)
        moisture3 = moisture_py.get_from_pot(3)
        valve1 = valve_py.get_valve_status(1)
        valve2 = valve_py.get_valve_status(2)
        valve3 = valve_py.get_valve_status(3)
        
        if pumpStatus == 1:
            # pump is off
            shouldTurnPumpOn = False

            # Soil Moisture 1 and  Valve 1
            if moisture1:
                valve_py.turn_valve_on(1)
                shouldTurnPumpOn = True
            else:
                valve_py.turn_valve_off(1)

            # Valve 2
            if moisture2:
                valve_py.turn_valve_on(2)
                shouldTurnPumpOn = True
            else:
                valve_py.turn_valve_off(2)

            # Valve 3
            if moisture3:
                valve_py.turn_valve_on(3)
                shouldTurnPumpOn = True
            else:
                valve_py.turn_valve_off(3)
            
            time

            # Turn or off Pump
            if shouldTurnPumpOn:
                pump_py.turn_on()
                print("Pump is On")
            else:
                pump_py.turn_off()
                print("Pump is Off")

        # Delay
        time.sleep(2)
        print("\\\\")
    






asyncio.run(run_sensors())

