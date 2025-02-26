###
### Dry Soil: 3.4V – 5.0V
### Moist Soil: 1.5V – 3.5V
### Wet Soil: 0.0V – 1.4V
###

def get_from_pot(pot_number) -> int | None:
    if pot_number not in range(1, 4):  # Fix range to include pot 3
        return None  # Return None instead of a string
    return 35  # Todo - Replace with real sensor data
