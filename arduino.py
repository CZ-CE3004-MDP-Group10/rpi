import asyncio
import serial
import time

class Arduino:
    def __init__(self):
        self.serial = None 
        self.serial.port = "/dev/ttyACM0"
        self.serial.baudrate = 115200
        self.serial.write_timeout = 0
        self.status = 0
        print("Arduino object instantiated")
    def connect(self):
        self.serial = serial.Serial() 
        while(self.status == 0):
            try:
                self.serial.open()
                print("Arduino USB connection established")
                self.status = 1
            except Exception as e:
                print(e)
                time.sleep(1)

    def disconnect(self):
        try:
            if self.serial is not None:
                self.serial.close()
                self.serial = None
        except Exception as e:
            print(e)

    def read(self):
        try:
            message = self.serial.readline().strip()
            print("from arduino: {message}")
            if len(message) > 0 :
                return message
        except Exception as e:
            print(e)
        return None

    def write(self, message):
        try:
            self.serial.write(message)
            print("to arduino: {message}")
        except Exception as e:
            print(e)

                    