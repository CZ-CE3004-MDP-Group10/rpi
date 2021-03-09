import socket
from picamera import PiCamera
import datetime
import os
import buffer

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
        self.time = datetime.datetime
        self.img_dir = '../0cv/captured_images/'
        self.img_name = 'image'

    def isConnected(self):
        return self.is_connected

    def read(self):
        try:
            message = self.client_sock.recv(1024).decode("utf-8")
            if len(message) > 0:
                print(f"PiCamera (MESSAGE-FROM): {message}")
                return message
            else:
                self.disconnect_client()
            message = None
        except socket.error:
            print("PiCamera read disconnect client")
            self.disconnect_client()
        except Exception as e:
            print(f"PiCameraorithm (ERROR) read():{e}")
        return None

    def take_image(self):
        # to do - take pic and save to directory in rpi
        image_name = f"{self.img_dir}{self.img_name}.jpg"
        self.camera.capture(image_name)
        print(f"take_image: {image_name} captured")
        return image_name

    def send_image(self,image_name):
        try:
            sbuf = buffer.Buffer(sock)
            sbuf.put_utf8(image_name)
            file_size = os.path.getsize(image_name)
            sbuf.put_utf8(str(file_size))

            self.client_sock.send(f"{self.image_name}|{file_size}".encode())

            with open(image_name, 'rb') as f:
                # remaining = file_size
                # while True:
                #     bytes_read = f.read(1024)
                #     if not bytes_read:
                #         break
                #     self.client_sock.sendall(bytes_read)
                sbuf.put_bytes(f.read())

                print(f"{image_name} sent")


            self.disconnect_client()
        except socket.error:
            print("PiCamera (ERROR) send_image disconnect client")
            self.disconnect_client()
        except Exception as e:
            print(f"PiCamera (ERROR) send_image():{e}")

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

