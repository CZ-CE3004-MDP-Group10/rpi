import asyncio
import bluetooth
import os
from configs import AndroidConfigs

class Android:
    def __init__(self):
        os.system("sudo hciconfig hci0 piscan")
        self.server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.port = bluetooth.PORT_ANY
        self.server_sock.bind(("", self.port))
        self.server_sock.listen(1)
        bluetooth.advertise_service(
                sock = self.server_sock,
                name = AndroidConfigs.BT_NAME,
                service_id = AndroidConfigs.UUID,
                service_classes = [AndroidConfigs.UUID, bluetooth.SERIAL_PORT_CLASS],
                profiles = [bluetooth.SERIAL_PORT_PROFILE]
                )
        
        self.client_sock = None
        print("Android (INSTANTIATED)")

    def isConnected(self):
        if self.client_sock == None:
            return False
        return True

    def connect(self):
        try:
            os.system("sudo hciconfig hci0 piscan")
            print(f"Android (WAITING) start advertising")
            if self.client_sock == None:
                print(f"Android (WAITING) on RFCOMM port {self.port}")
                self.client_sock, self.client_address = self.server_sock.accept()
                print(f"Android (CONNECTED) to {self.client_sock.getpeername} @ {self.client_address}")
            os.system("sudo hciconfig hci0 noscan")
            print(f"Android (CONNECTED) stop advertising")
        except Exception as e:
            print(f"Android (ERROR) connect():{e}")

    def disconnect_client(self):
        if self.client_sock != None:
            self.client_sock.close()
            self.client_sock = None
            print("Android (CLIENT DISCONNECTED)")

    def disconnect_server(self):
        if self.server_sock != None:
            self.server_sock.close()
            print("Android (SERVER DISCONNECTED)")

    def read(self):
        try:
            message = self.client_sock.recv(AndroidConfigs.BUFFER_SIZE)
            if len(message) > 0 :
                print(f"Android (MESSAGE-FROM): {message}")
                return message.decode("utf-8").strip()
            else:
                self.disconnect_client()
            message = None
        except Exception as e:
            self.disconnect_client()
            print(f"Android (ERROR) read():{e}")
        return None

    def write(self, message):
        try:
            print(f"Android (MESSAGE-TO): {message}")
            self.client_sock.send(message.encode("utf-8"))
        except Exception as e:
            self.disconnect_client()
            print(f"Android (ERROR) write():{e}")
    
# if __name__ == "__main__":
#     main = Android()
#     main.connect()
#     i = 0 
#     while i<10:
#         main.write(f"Write to bluetooth slave {i}\n")
#         i += 1
#     main.disconnect()
    
