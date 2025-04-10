from enum import Enum

#5, 6, 16, 17, 22, 23, 24, 25, 26, 27

class Cpio(Enum):
    Growlight = 21 #in6 #gpio 40
    Pump = 26
    Vavle1 = 19
    Vavle2 = 13
    Vavle3 = 5
    Moisture1 = 23
    Moisture2 = 24
    Moisture3 = 25
    temp_humid = 17 
    SDA1 = 2
    SCL1 = 3
    Fan = 22