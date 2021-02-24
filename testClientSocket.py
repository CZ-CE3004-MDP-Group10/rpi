import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("192.168.10.1",101))

movement = ("w1", "a2","s5","w10")
try:
    for i in movement:
        message = "ARD"+"|"+i
        message = message.encode("utf-8")
        sock.send(message)
        # sock.sendall(message)
        print(message)
        time.sleep(5)
    sock.close()
    # while True:
    #     message  = sock.recv(1024).decode("utf-8")
    #     if message != None:
    #         print(message)
    #     message = None
finally:
    sock.close()