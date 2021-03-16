import socket
from picamera import PiCamera
import datetime
import os

class ImageCV:
    def __init__(self):
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_ip = "192.168.10.1"
        self.port = 50001
        self.server_sock.bind((self.server_ip, self.port))
        self.server_sock.listen(1)

        self.client_sock = None
        self.clientInfo = None
        self.is_connected = False

        self.buffer = b''
        print("CVIMAGE (INSTANTIATED)")

        self.camera = PiCamera()
        self.camera.resolution = (1024, 768)
        current_time = datetime.datetime.now().strftime("%d_%m_%y_%H:%M:%S")
        self.img_dir = f'0cv/captured_images/{current_time}'
        os.makedirs(self.img_dir)
        self.img_name_ctr = 1


        
    def isConnected(self):
        return self.is_connected

    def read(self):
        try:
            message = self.client_sock.recv(1024)
            if len(message) > 0:
                print(f"CVIMAGE (MESSAGE-FROM): {message}")
                return message.decode()
        except socket.error:
            print("CVIMAGE read disconnect client")
            self.disconnect_client()
        except Exception as e:
            print(f"CVIMAGE (ERROR) read():{e}")
        return None
    
    def write(self, message):
        try:
            print(f"CVIMAGE (MESSAGE-TO): {message}")
            self.client_sock.send(message.encode('utf-8'))
        except socket.error:
            self.disconnect_client()
        except Exception as e:
            print(f"CVIMAGE (ERROR) write():{e}")

    def take_image(self, coordinate):
        ""
        
        ""
        img_name = f"{self.img_name_ctr}{coordinate}"
        self.camera.capture(f"{self.img_dir}/{img_name}.jpg")
        print(f"CVIMAGE (take_image) image {img_name} captured")
        self.img_name_ctr += 1
        return img_name

    def send_image(self, img_name):
        try:
            file_size = str(os.path.getsize(f"{self.img_dir}/{img_name}.jpg"))
            print(f"{img_name} - {file_size}")
            self.write(f"{img_name}|{file_size}")
            file = open(f"{self.img_dir}/{img_name}.jpg",'rb')
            l = file.read(1024)
            while(l):
                self.client_sock.send(l)
                l = file.read(1024)
            file.close()
            print(f'CVIMAGE (send_image) File Sent')
            
        except socket.error:
            print("CVIMAGE (ERROR) send_image disconnect client")
            # self.disconnect_client()
        except Exception as e:
            print(f"CVIMAGE (ERROR) send_image():{e}")

    def connect(self):
        try:
            print(f"CVIMAGE (WAITING) at {self.server_ip}")
            if self.client_sock is None:
                self.client_sock, self.client_address = self.server_sock.accept()
                self.is_connected = True
                print(f"CVIMAGE (CONNECTED) to {self.client_address} {self.client_sock}")
        except KeyboardInterrupt:
            print(f"CVIMAGE (KEYBOARD INTERRUPT)")
            self.disconnect_server()
        except Exception as e:
            print(f"CVIMAGE (ERROR) connect():{e}")

    def disconnect_client(self):
        self.client_sock.close()
        self.client_sock = None
        self.is_connected = False
        print("CVIMAGE (CLIENT DISCONNECTED)")

    def disconnect_server(self):
        self.server_sock.close()
        print("CVIMAGE (SERVER DISCONNECTED)")