import asyncio
import serial
import time

from configs import ArduinoConfigs

class Arduino:
    def __init__(self):
        self.serial = serial.Serial() 
        self.serial.port = ArduinoConfigs.SERIAL_PORT
        self.serial.baudrate = ArduinoConfigs.BAUD_RATE
        self.serial.write_timeout = ArduinoConfigs.WRITE_TIMEOUT
        self.connected = False
        print("Arduino object instantiated")
    def connect(self):
        while self.connected == False:
            try:
                self.serial.open()
                self.connected = True
                print("Arduino USB connection established")
            except Exception as e:
                print(e)
                time.sleep(1)

    def disconnect(self):
        try:
            if self.serial is not None:
                self.serial.close()
                self.connected = False
        except Exception as e:
            print(e)

    def read(self):
        try:
            message = self.serial.readline().strip()
            print(f"From arduino:{message}")
            if len(message) > 0 :
                return message
        except Exception as e:
            print(e)
        return None

    def write(self, message):
        try:
            print(f"To arduino:{message}")
            self.serial.write(message)
        except Exception as e:
            print(e)

                    