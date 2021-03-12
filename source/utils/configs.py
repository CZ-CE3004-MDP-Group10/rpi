class ArduinoConfigs:
    SERIAL_PORT = "/dev/ttyUSB0"
    BAUD_RATE = 115200
    WRITE_TIMEOUT = 1
    # ttyUSB0
    # idProduct = "0002"
    # idProduct = "9514"
    # idProduct = "7523"
    # idVendor = "0424"
    # idVendor = "1d6b"


class AlgorithmConfigs:
    SERVER_IP = '192.168.10.1'
    SERVER_PORT = 30000
    BUFFER_SIZE = 1024

class AndroidConfigs:
    # reset bluetooth -> hciconfig hci0 reset
    # RPI BT MAC: B8:27:EB:1A:B3:54
    # ANDROID MAC: CC:46:4E:E1:D1:AD
    # UUID = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    UUID ="00001101-0000-1000-8000-00805f9b34fb"
    BT_NAME = "MDP-group10"
    BUFFER_SIZE = 1024
    # SDP_CHANNEL = 19 set to any now