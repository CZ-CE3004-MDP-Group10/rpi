import asyncio
import bluetooth

class Android:
    def __init__(self):
        print("Android object instantiated")
        # self.client_sock
        self.server_sock = bluetooth.BluetoothSocket()
        self.UUID = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
        self.port = 8
        self.status = 0

        self.server_sock.bind(("", self.port))
        self.server_sock.listen()
        bluetooth.advertise_service(
                sock = self.server_sock,
                name = "bluetooth-server-group10",
                service_id = self.UUID,
                service_classes = [self.UUID, bluetooth.SERIAL_PORT_CLASS],
                profiles = [bluetooth.SERIAL_PORT_PROFILE]
                )

    def connect(self):
        try:
            print("a")
        except Exception as e:
            print(e)