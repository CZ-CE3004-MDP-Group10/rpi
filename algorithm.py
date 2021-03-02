import socket

from configs import AlgorithmConfigs

class Algorithm:
    def __init__(self):
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # self.server_sock.setblocking(False)
        self.server_ip = AlgorithmConfigs.SERVER_IP
        self.port = AlgorithmConfigs.SERVER_PORT
        self.server_sock.bind((self.server_ip, self.port))
        self.server_sock.listen(1)

        self.client_sock = None
        self.clientInfo = None
        self.is_connected = False
        print("Algorithm (INSTANTIATED)")

    def isConnected(self):
        return self.is_connected

    def connect(self):
        try:
            print(f"Algorithm (WAITING) at {self.server_ip}")
            if self.client_sock is None:
                self.client_sock, self.client_address = self.server_sock.accept()
                self.is_connected = True
                print(f"Algorithm (CONNECTED) to {self.client_address} {self.client_sock}")
        except KeyboardInterrupt:
                print(f"Android (KEYBOARD INTERRUPT)")
                self.disconnect_server()
        except Exception as e:
            print(f"Algorithm (ERROR) connect():{e}")

    def disconnect_client(self):
        self.client_sock.close()
        self.client_sock = None
        self.is_connected = False
        print("Algorithm (CLIENT DISCONNECTED)")

    def disconnect_server(self):
        self.server_sock.close()
        print("Algorithm (SERVER DISCONNECTED)")
    
    def read(self):
        try:
            message = self.client_sock.recv(AlgorithmConfigs.BUFFER_SIZE)
            if len(message) > 0:
                print(f"Algorithm (MESSAGE-FROM): {message}")
                return message.decode("utf-8").strip()
            else:
                self.disconnect_client()
            message = None
        except socket.error:
            print("Algorithm read disconnect client")
            self.disconnect_client()
        except Exception as e:
            print(f"Algorithm (ERROR) read():{e}")
        return None

    def write(self, message):
        try:
            print(f"Algorithm (MESSAGE-TO): {message}")
            self.client_sock.send(message.encode("utf-8"))
        except socket.error:
            self.disconnect_client()
        except Exception as e:
            print(f"Algorithm (ERROR) write():{e}")