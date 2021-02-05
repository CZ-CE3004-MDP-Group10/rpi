import socket

from configs import AlgorithmConfigs

class Algorithm:
    def __init__(self):
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = AlgorithmConfigs.SERVER_IP
        self.port = AlgorithmConfigs.SERVER_PORT
        self.server_sock.bind((self.server_ip, self.port))
        self.server_sock.listen(1)

        self.client_sock = None
        self.client_ip = None
        self.connected = False
        print("Algorithm (INSTANTIATED)")

    def connect(self):
        while True:
            try:
                print(f"Algorithm (WAITING) at {self.server_ip}")
                if self.client_sock is None:
                    self.client_sock, self.address = self.server_sock.accept()
                    print(f"Algorithm (CONNECTED) to {self.address}")
                    break
            except Exception as e:
                print(f"Connection with Algorithm failed:{e}")
                if self.client_sock is not None:
                    self.client_sock.close()
                    self.client_sock = None

    def disconnect(self):
        try:
            if self.client_sock is not None:
                self.client_sock.close()
                self.client_sock = None
            print("Algorithm (DISCONNECTED)")
        except Exception as e:
            print(f"Algorithm disconnect failed:{e}")
    
    def read(self):
        try:
            if self.client_sock != None:
                message = self.client_sock.recv(AlgorithmConfigs.BUFFER_SIZE).decode("utf-8").strip()
                if len(message) > 0:
                    print(f"Algorithm (MESSAGE-FROM): {message}")
                    return message
                message = None
        except Exception as e:
            print(f"Algorithm:{e}")
        return None

    def write(self, message):
        try:
            print(f"Algorithm (MESSAGE-TO): {message}")
            self.client_sock.send(message.encode("utf-8"))
        except Exception as e:
            print(f"Algorithm:{e}")

if __name__ == "__main__":
    main = Algorithm
    main.connect
    while True:
        main.read()