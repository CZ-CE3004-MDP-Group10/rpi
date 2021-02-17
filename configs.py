class ArduinoConfigs:
    SERIAL_PORT = "/dev/ttyACM0"
    BAUD_RATE = 115200
    WRITE_TIMEOUT = 0

class AlgorithmConfigs:
    SERVER_IP = '192.168.10.1'
    SERVER_PORT = 101
    BUFFER_SIZE = 1024

class AndroidConfigs:
    # reset bluetooth -> hciconfig hci0 reset
    # MAC: B8:27:EB:1A:B3:54
    UUID = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    BT_NAME = "MDP-group10"
    BUFFER_SIZE = 1024