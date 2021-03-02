import asyncio
import time
from multiprocessing import Process, Value, Queue, Manager
from multiprocessing.managers import BaseManager

from commands import *
from arduino import Arduino
from algorithm import Algorithm
from android import Android
from cvimage import ImageCV

class Main:
    def __init__(self):
        self.write_queue = Manager().Queue()

        BaseManager.register('Arduino',Arduino)
        BaseManager.register('Algorithm',Algorithm)
        BaseManager.register('Android',Android)
        BaseManager.register('ImageCV', ImageCV)
        manager = BaseManager()
        manager.start()
        shared_ard = manager.Arduino()
        shared_alg = manager.Algorithm()
        shared_and = manager.Android()
        shared_icv = manager.ImageCV()
        
        p1 = Process(target=self.read_algorithm, args=[shared_alg])
        p1.start()
        p2 = Process(target=self.read_arduino, args=[shared_ard])
        p2.start()
        p3 = Process(target=self.read_android, args=[shared_and])
        p3.start()
        p4 = Process(target=self.read_imagecv, args=[shared_icv])
        p4.start()
        p5 = Process(target=self.write_target, args=(shared_ard, shared_alg, shared_and))
        p5.start()
        p5.join()

    def read_arduino(self, arduino):
        while True:
            raw_message = None
            if arduino.isConnected() == False:
                arduino.connect()
            else:
                try:
                    raw_message = arduino.read()
                    if raw_message is None:
                        continue
                    for message in raw_message.splitlines():
                        if len(message) <= 0:
                            continue
                    self.write_queue.put(raw_message)
                except KeyboardInterrupt:
                    print(f"Arduino (KEYBOARD INTERRUPT)")
                    arduino.disconnect()
                except Exception as e:
                    print(f"read_arduino:{str(e)}")
                    break    

    def read_algorithm(self, algorithm):
        while True:
            raw_message = None
            if not algorithm.isConnected():
               algorithm.connect()
            else:
                try:
                    raw_message = algorithm.read()
                    if raw_message is None:
                        continue
                    self.write_queue.put(raw_message)
                except KeyboardInterrupt:
                    print(f"Algorithm (KEYBOARD INTERRUPT)")
                    algorithm.disconnect_client()
                    algorithm.disconnect_server()
                except Exception as e  :
                    print(f'read_algorithm:{e}')
                    break

    def read_android(self, android):
        while True:
            raw_message = None
            if android.isConnected() == False:
                android.connect()
            else:
                try:
                    raw_message = android.read()
                    if raw_message is None:
                        continue
                    self.write_queue.put_nowait(raw_message)
                except KeyboardInterrupt:
                    print(f"Android (KEYBOARD INTERRUPT)")
                    android.disconnect_client()
                    android.disconnect_server()
                except Exception as e  :
                    print(f'read_android:{e}')
                    break

    def read_imagecv(self, imagecv):
        while True:
            raw_message = None
            if not imagecv.isConnected():
               imagecv.connect()
            else:
                try:
                    raw_message = imagecv.read()
                    if raw_message is None:
                        continue
                    elif raw_message.decode("utf-8").strip() == "CV|TAKIMG":
                        imagecv.take_image()
                    # self.write_queue.put(raw_message)
                except KeyboardInterrupt:
                    print(f"Imagecv (KEYBOARD INTERRUPT)")
                    imagecv.disconnect_client()
                    imagecv.disconnect_server()
                except Exception as e  :
                    print(f'Imagecv:{e}')
                    break

    def write_target(self, arduino, algorithm, android, imagecv):
        print("Write Process (CALLED)")
        while True:
            try:
                if not self.write_queue.empty():
                    message = self.write_queue.get()
                    i =  message.split(SEPERATOR)
                    if i[0] == "ARD":
                        if arduino.isConnected() == True:
                            arduino.write(message)
                        else:
                            pass
                            # self.write_queue.put(message)
                            print("Arduino (WRITE) fail, not connected, reconnecting Arduino now...")
                            # arduino.connect()
                    elif i[0] == "ALG":
                        if algorithm.isConnected() == True:
                            algorithm.write(message)
                        else:
                            # self.write_queue.put(message)
                            print("Algorithm (WRITE) fail, not connected, reconnecting Algorithm now...")
                            # algorithm.connect()
                    elif i[0] == "AND":
                        if android.isConnected == True:
                            android.write(message)
                        else:
                            self.write_queue.put(message)
                            print("Android (WRITE) fail, not connected, reconnecting Android now...")
                    # elif i[0] == "CV":
                        # if imagecv.isConnected == True:
                        #     imagecv.write(message)
                        # else:
                        #     self.write_queue.put(message)
                        #     print("Android (WRITE) fail, not connected, reconnecting Android now...")
                    else:
                        print("HEADER INFO WRONG")
            except KeyboardInterrupt:
                print(f"Writing (KEYBOARD INTERRUPT)")
            except Exception as e:
                print(f"write_target:{e}")
                break


if __name__ == "__main__":
    main = Main()
    # main.write_target()
    while True: 
        pass