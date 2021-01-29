import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("192.168.10.1",101))

i=0
try:
#     message = 'This is the message.  It will be repeated.'
#     sock.sendall(message.encode())

    # while True:
    #     data = sock.recv(1024)
    #     if data != None:
    #         print(data)
    #     data = None

    while i<10:
        message = "w"
        sock.sendall(message.encode())
        print(message)
        i += 1
        time.sleep(1)
        

finally:
    sock.close()