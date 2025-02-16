import time
import growlight
count = 0

while True:
    temperature = 31.8 if count < 15 else 32.5
    if temperature < 32:
        growlight.turn_on_growlight()
        print(f"Temperature {temperature} is too low. Turning on growlight.")
    else:
        growlight.turn_off_growlight()
        print(f"Temperature {temperature} is too high. Turning off growlight.")

    
    count = (count + 1)  # Reset after 6 iterations (5 times 32.7, 1 time 33.3)
    time.sleep(2)
