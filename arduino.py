import asyncio
import serial
import os

from configs import ArduinoConfigs

class Arduino:
    def __init__(self):
        self.serial = serial.Serial() 
        self.serial.port = ArduinoConfigs.SERIAL_PORT
        self.serial.baudrate = ArduinoConfigs.BAUD_RATE
        self.serial.write_timeout = ArduinoConfigs.WRITE_TIMEOUT
        self.connected = False
        print("Arduino (INSTANTIATED)")
    
    def port_exists(self):
        try:
            os.stat(self.serial.port)
        except OSError:
            return False
        return True

    def isConnected(self):
        return self.connected

    def connect(self):
        while self.port_exists():
            try: 
                self.serial.open()
                print(f"Arduino (CONNECTED) to {self.serial.port}")
                self.connected = True
                break
            except Exception as e:
                print(e)

    def disconnect(self):
        self.serial.close()
        self.connected = False
        print(f"Arduino (DISCONNECTED)")

    def read(self):
        try:
            message = self.serial.readline().decode("utf-8").strip()
            if len(message) > 0 :
                print(f"Arduino (MESSAGE-FROM):{message}")
                return message
        # except serial.SerialException:
        #     self.disconnect()
        except Exception as e:
            print(f"Arduino (ERROR) read():{e}")
            self.disconnect()  # <<<<<<
        return None

    def write(self, message):
        try:
            print(f"Arduino (MESSAGE-TO): {message}")
            self.serial.write(message.encode("utf-8"))
        # except serial.SerialException:
        #     print("serial.SerialException")
        #     self.connect()
        except Exception as e:
            print(f"Arduino (ERROR) write():{e}")
            self.disconnect() # <<<<<<
            # self.connect()


                    