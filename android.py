import asyncio
import bluetooth

from configs import AndroidConfigs

class Android:
    def __init__(self):
        print("Android object instantiated")
        # self.client_sock
        self.server_sock = bluetooth.BluetoothSocket()
        self.UUID = AndroidConfigs.UUID
        self.port = AndroidConfigs.PORT
        self.connected = False

        self.server_sock.bind(("", self.port))
        self.server_sock.listen()
        bluetooth.advertise_service(
                sock = self.server_sock,
                name = AndroidConfigs.BT_NAME,
                service_id = self.UUID,
                service_classes = [self.UUID, bluetooth.SERIAL_PORT_CLASS],
                profiles = [bluetooth.SERIAL_PORT_PROFILE]
                )

    def connect(self):
        try:
            print("a")
        except Exception as e:
            print(e)