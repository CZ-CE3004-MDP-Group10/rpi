import asyncio
from bluetooth import *
from configs import AndroidConfigs

class Android:
    def __init__(self):
        print("Android (INSTANTIATED)")
        self.client_sock == None
        self.server_sock = bluetooth.BluetoothSocket()
        self.UUID = AndroidConfigs.UUID
        self.port = bluetooth.PORT_ANY
        
        self.server_sock.bind(("", self.port))
        self.server_sock.listen(1)
        bluetooth.advertise_service(
                sock = self.server_sock,
                name = AndroidConfigs.BT_NAME,
                service_id = self.UUID,
                service_classes = [self.UUID, bluetooth.SERIAL_PORT_CLASS],
                profiles = [bluetooth.SERIAL_PORT_PROFILE]
                )
        
        self.connected = False
        print(f"Android (WAITING) on RFCOMM port {self.port}")

    def connect(self):
        while self.client_sock == None:
            try:
                self.client_sock, address = self.server_sock.accept()
                print(f"Android (CONNECTED) to {self.client_sock.getpeername} @ {address}")
                self.connected = True
            except Exception as e:
                self.disconnect()
                print(e)

    def disconnect(self):
        try:
            if self.client_sock != None:
                self.client_sock.close()
                self.client_sock = None
            print(f"Android (DISCONNECTED)")
            self.connected = False
        except Exception as e:
            print(e)

    def read(self):
        try:
            message = self.client_sock.recv(AndroidConfigs.BUFFER_SIZE).strip()
            print(f"Android (MESSAGE-FROM): {message}")
            if len(message) > 0 :
                return message            
        except Exception as e:
            print(e)
        return None
            
    def write(self, message):
        try:
            print(f"Android (MESSAGE-TO): {message}")
            self.client_sock.send(message.encode("utf-8"))
        except Exception as e:
            print(e)
    