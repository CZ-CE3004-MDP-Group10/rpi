import asyncio
import time
from multiprocessing import Process, Value, Queue, Manager
from multiprocessing.managers import BaseManager

from commands import *
from arduino import Arduino
from algorithm import Algorithm
from android import Android

# class ShareManager(BaseManager):
#     pass

# ShareManger.register('arduino',Arduino)
# ShareManger.register('algorithm',Algorithm)
# ShareManger.register('android',Android)

class Main:
    def __init__(self):
        # self.arduino = Arduino()
        # self.algorithm = Algorithm()
        # self.android = Android()
        # instantiate computer vision module
        self.write_queue = Manager().Queue()

        # self.manager = ShareManager()
        # self.manager.start()

        BaseManager.register('Arduino',Arduino)
        BaseManager.register('Algorithm',Algorithm)
        BaseManager.register('Android',Android)
        manager = BaseManager()
        manager.start()
        shared_ard = manager.Arduino()
        shared_alg = manager.Algorithm()
        shared_and = manager.Android()
        
        p1 = Process(target=self.read_algorithm, args=[shared_alg])
        p1.start()
        p2 = Process(target=self.read_arduino, args=[shared_ard])
        p2.start()
        p3 = Process(target=self.read_android, args=[shared_and])
        p3.start()
        p4 = Process(target=self.write_target, args=(shared_ard, shared_alg, shared_and))
        p4.start()
        p4.join()

        # self.read_arduino_process = Process(target=self.read_arduino).start()
        # self.read_algorithm_process = Process(target=self.read_algorithm, args=(self.algorithm, self.write_queue)).start()
        # self.read_android_process = Process(target=self.read_android).start()
        # self.write_target = Process(target=self.write_target, args=(self.algorithm,self.write_queue)).start()

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

    def write_target(self, arduino, algorithm, android):
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
                            self.write_queue.put(message)
                            print("Arduino (WRITE) fail, not connected, reconnecting Arduino now...")
                            arduino.connect()
                    elif i[0] == "ALG":
                        if algorithm.isConnected() == True:
                            algorithm.write(message)
                        else:
                            self.write_queue.put(message)
                            print("Algorithm (WRITE) fail, not connected, reconnecting Algorithm now...")
                            algorithm.connect()
                    elif i[0] == "AND":
                        if android.isConnected == True:
                            android.write(message)
                        else:
                            self.write_queue.put(message)
                            print("Android (WRITE) fail, not connected, reconnecting Android now...")
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