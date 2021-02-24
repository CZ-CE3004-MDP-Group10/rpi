import asyncio
import serial

from configs import ArduinoConfigs

class Arduino:
    def __init__(self):
        self.serial = serial.Serial() 
        self.serial.port = ArduinoConfigs.SERIAL_PORT
        self.serial.baudrate = ArduinoConfigs.BAUD_RATE
        self.serial.write_timeout = ArduinoConfigs.WRITE_TIMEOUT
        print("Arduino (INSTANTIATED)")

    def isConnected(self):
        try:
            return self.serial.isOpen()
        except:
            return False

    def connect(self):
        while self.isConnected == False:
            try:
                self.serial.open()
                print(f"Arduino (CONNECTED) to {self.serial.port}")
                self.connected = True
            except Exception as e:
                print(e)

    def disconnect(self):
        self.serial.close()
        print(f"Arduino (DISCONNECTED)")

    def read(self):
        try:
            message = self.serial.readline().decode("utf-8").strip()
            if len(message) > 0 :
                print(f"Arduino (MESSAGE-FROM):{message}")
                return message
        except serial.SerialException:
            self.disconnect()
        except Exception as e:
            print(f"Arduino (ERROR) read():{e}")
        return None

    def write(self, message):
        try:
            print(f"Arduino (MESSAGE-TO): {message}")
            self.serial.write(message.encode("utf-8"))
        except serial.SerialException:
            self.disconnect()
        except Exception as e:
            print(f"Arduino (ERROR) write():{e}")

                    