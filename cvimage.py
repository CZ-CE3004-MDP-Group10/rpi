import socket
from picamera import PiCamera

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
        print("PiCamera (INSTANTIATED)")

        self.camera = PiCamera()
        self.camera.resolution = (1024, 768)

    def isConnected(self):
        return self.is_connected

    def read(self):
        try:
            message = self.client_sock.recv(1024)
            if len(message) > 0:
                print(f"PiCamera (MESSAGE-FROM): {message}")
                if message.decode("utf-8").strip() == "CV|TAKIMG":
                    self.take_image()
            else:
                self.disconnect_client()
            message = None
        except socket.error:
            print("PiCamera read disconnect client")
            self.disconnect_client()
        except Exception as e:
            print(f"AlgPiCameraorithm (ERROR) read():{e}")
        return None


    def take_image(self, no_pic=1):
        label = "image_name"
        image_directory = './captured_images/'
        while 0 < no_pic:
            # to do - take pic and save to directory in rpi
            image_name = f"{image_directory}{label}_{no_pic}.jpg"
            self.camera.capture(image_name)
            print(f"Image: {image_name} captured")
            no_pic = no_pic + 1
            self.send_image(image_name)


    def send_image(self,image_name):
        #open file
        f = open(image_name, 'rb')
        image_file = f.read(1024)
        while image_file:
            print("sending image")
            self.server_sock.send(image_file)
            image_file.read(1024)
        f.close()


    def connect(self):
        try:
            print(f"PiCamera (WAITING) at {self.server_ip}")
            if self.client_sock is None:
                self.client_sock, self.client_address = self.server_sock.accept()
                self.is_connected = True
                print(f"PiCamera (CONNECTED) to {self.client_address} {self.client_sock}")
        except KeyboardInterrupt:
            print(f"PiCamera (KEYBOARD INTERRUPT)")
            self.disconnect_server()
        except Exception as e:
            print(f"PiCamera (ERROR) connect():{e}")


    def disconnect_client(self):
        self.client_sock.close()
        self.client_sock = None
        self.is_connected = False
        print("PiCamera (CLIENT DISCONNECTED)")


    def disconnect_server(self):
        self.server_sock.close()
        print("PiCamera (SERVER DISCONNECTED)")

