import asyncio
import serial
class Arduino:
    def __init__(self):
        self.serial = serial.Serial() 
        self.serial.port = "/dev/ttyACM0"
        self.serial.baudrate = 115200
        self.serial.write_timeout = 0
        self.status = 0
        print("Arduino object instantiated")
    def connect(self):
        try:
            self.serial.open()
            print("Arduino USB connection established")
            self.status = 1
        except Exception as e:
            print(e)