import socket

from configs import AlgorithmConfigs

class Algorithm:
    def __init__(self):
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_ip = AlgorithmConfigs.SERVER_IP
        self.port = AlgorithmConfigs.SERVER_PORT
        self.server_sock.bind((self.server_ip, self.port))
        self.server_sock.listen(1)

        self.client_sock = None
        self.client_ip = None
        self.connected = False
    def connect(self):
        while True:
            try:
                print('Establishing connection with Algorithm')
                if self.client_sock is None:
                    self.client_sock, self.address = self.server_sock.accept()
                    print(f'{self.address} has connected')
                    break
            except Exception as e:
                print(f"Connection with Algorithm failed:{e}")
                if self.client_sock is not None:
                    self.client_sock.close()
                    self.client_sock = None
            print("Retrying Algorithm connection...")

    def disconnect(self):
        try:
            if self.client_sock is not None:
                self.client_sock.close()
                self.client_sock = None
            print("Algorithm disconnected Successfully")
        except Exception as e:
            print(f"Algorithm disconnect failed:{e}")
    
    def read(self):
        try:
            message = self.client_sock.recv(AlgorithmConfigs.BUFFER_SIZE).strip()
            print(f"Algorithm (MESSAGE-FROM): {message}")
            if len(message) > 0:
                return message
        except Exception as e:
            print(f"Algorithm:{e}")
        return None

    def write(self, message):
        try:
            print(f"To Algorithm:{message}")
            self.client_sock.send(message)
        except Exception as e:
            print(f"Algorithm:{e}")