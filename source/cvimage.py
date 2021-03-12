import socket
from picamera import PiCamera
import datetime
import os
import utils.buffer as buffer

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
        self.connbuf = None
        self.is_connected = False

        self.buffer = b''
        print("CVIMAGE (INSTANTIATED)")

        self.camera = PiCamera()
        self.camera.resolution = (1024, 768)
        self.time = datetime.datetime
        self.img_dir = '0cv/captured_images'
        self.img_name_ctr = 1


        
    def isConnected(self):
        return self.is_connected

    def read(self):
        try:
            # while b'\x00' not in self.buffer:
            #     data = self.sock.recv(1024)
            #     if not data:
            #         return ''
            #     self.buffer += data
            # # split off the string from the buffer.
            # data, _,self.buffer = self.buffer.partition(b'\x00')
            # return data.decode()

            message = self.connbuf.get_utf8()
            if len(message) > 0:
                print(f"CVIMAGE (MESSAGE-FROM): {message}")
                return message
        except socket.error:
            print("CVIMAGE read disconnect client")
            self.disconnect_client()
        except Exception as e:
            print(f"CVIMAGE (ERROR) read():{e}")
        return None
    
    def write(self, message):
        try:
            print(f"CVIMAGE (MESSAGE-TO): {message}")
            # self.sock.sendall(message.encode() + b'\x00')
            self.connbuf.put_utf8(message)
        except socket.error:
            self.disconnect_client()
        except Exception as e:
            print(f"CVIMAGE (ERROR) write():{e}")

    def take_image(self, coordinate):
        # take pic and save to directory in rpi
        img_name = f"{self.img_name_ctr}{coordinate}"
        self.camera.capture(f"{self.img_dir}/{img_name}.jpg")
        print(f"CVIMAGE (take_image) image {img_name} captured")
        self.img_name_ctr += 1
        return img_name

    def send_image(self, img_name):
        try:
            # send image name
            # self.sock.sendall(img_name.encode() + b'\x00')
            self.connbuf.put_utf8(img_name)
            print(f"CVIMAGE (send_image): {img_name}")
            # send image size
            image_size = os.path.getsize(f"{self.img_dir}/{img_name}.jpg")
            # self.sock.sendall(image_size.encode() + b'\x00')
            self.connbuf.put_utf8(str(image_size))
            print(f"CVIMAGE (send_image): {image_size}")
            # send image data
            with open(f"{self.img_dir}/{img_name}.jpg", 'rb') as f:
                # self.sock.sendall(f.read())
                self.connbuf.put_bytes(f.read())
            print(f'CVIMAGE (send_image) File Sent')
            
        except socket.error:
            print("CVIMAGE (ERROR) send_image disconnect client")
            self.disconnect_client()
        except Exception as e:
            print(f"CVIMAGE (ERROR) send_image():{e}")

    def connect(self):
        try:
            print(f"CVIMAGE (WAITING) at {self.server_ip}")
            if self.client_sock is None:
                self.client_sock, self.client_address = self.server_sock.accept()
                self.connbuf = buffer.Buffer(self.client_sock)
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