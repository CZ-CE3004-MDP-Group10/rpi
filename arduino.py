import asyncio
import serial

from configs import ArduinoConfigs

class Arduino:
    def __init__(self):
        self.serial = serial.Serial() 
        self.serial.port = ArduinoConfigs.SERIAL_PORT
        self.serial.baudrate = ArduinoConfigs.BAUD_RATE
        self.serial.write_timeout = ArduinoConfigs.WRITE_TIMEOUT
        self.connected = False
        print("Arduino (INSTANTIATED)")

    def connect(self):
        while self.connected == False:
            try:
                self.serial.open()
                self.connected = True
                print("Arduino (CONNECTED) to {self.serial.port}")
            except Exception as e:
                print(e)

    def disconnect(self):
        try:
            if self.serial is not None:
                self.serial.close()
                self.connected = False
                print(f"Android (DISCONNECTED)")
            
        except Exception as e:
            print(e)

    def read(self):
        try:
            message = self.serial.readline().strip()
            print(f"Arduino (MESSAGE-FROM):{message}")
            if len(message) > 0 :
                return message
        except Exception as e:
            print(e)
        return None

    def write(self, message):
        try:
            print(f"Arduino (MESSAGE-TO): {message}")
            self.serial.write(message.encode("utf-8"))
        except Exception as e:
            print(e)

                    