import asyncio
import time
from multiprocessing import Process, Value, Queue, Manager

from commands import *
from arduino import Arduino
from algorithm import Algorithm
from android import Android

class Main:
    def __init__(self):
        self.arduino = Arduino()
        self.algorithm = Algorithm()
        self.android = Android()
        # instantiate computer vision module

        self.write_queue = Manager().Queue()

        self.read_arduino_process = Process(target=self.read_arduino).start()
        self.read_algorithm_process = Process(target=self.read_algorithm).start()
        self.read_android_process = Process(target=self.read_android).start()
        
        # self.write_target = Process(target=self.write_target)

    # def start(self):
    #     try:
    #         self.read_arduino_process.start()
    #         self.read_algorithm_process.start()
    #         self.read_android_process.start()

    #     except Exception as e:
    #         print(e)

    def read_arduino(self):
        while True:
            raw_message = None
            if self.arduino.isConnected == False:
                self.arduino.connect()
            try:
                raw_message = self.arduino.read()
                if raw_message is None:
                    continue
                for message in raw_message.splitlines():
                    if len(message) <= 0:
                        continue
            except KeyboardInterrupt:
                print(f"Arduino (KEYBOARD INTERRUPT)")
                self.arduino.disconnect()
            except Exception as e:
                print(f"read_arduino:{str(e)}")
                break    

    def read_algorithm(self):
        while True:
            raw_message = None
            if self.algorithm.isConnected == False:
                self.algorithm.connect()
            try:
                raw_message = self.algorithm.read()
                if raw_message is None:
                    continue
                self.write_queue.put_nowait(raw_message)
            except KeyboardInterrupt:
                print(f"Algorithm (KEYBOARD INTERRUPT)")
                self.algorithm.disconnect_client()
                self.algorithm.disconnect_server()
            except Exception as e  :
                print(f'read_algorithm:{e}')
                break

    def read_android(self):
        while True:
            raw_message = None
            if self.android.isConnected == False:
                self.android.connect()
            try:
                raw_message = self.android.read()
                if raw_message is None:
                    continue
                self.write_queue.put_nowait(raw_message)
            except KeyboardInterrupt:
                print(f"Android (KEYBOARD INTERRUPT)")
                self.android.disconnect_client()
                self.android.disconnect_server()
            except Exception as e  :
                print(f'read_android:{e}')
                break

    def write_target(self):
        while True:
            try:
                if not self.write_queue.empty():
                    message = self.write_queue.get_nowait()
                    i =  message.split(SEPERATOR)
                    if i[0] == Header.ARDUINO:
                        if self.arduino.isConnected == True:
                            self.arduino.write(i)
                        else:
                            print("Arduino (WRITE) fail, not connected")
                    elif i[0] == Header.ALGORITHM:
                        if self.algorithm.isConnected == True:
                            self.algorithm.write(i)
                        else:
                            print("Algorithm (WRITE) fail, not connected")
                    elif i[0] == Header.ANDROID:
                        if self.android.isConnected == True:
                            self.android.write(i)
                        else:
                            print("Android (WRITE) fail, not connected")
                    else:
                        print("HEADER INFO WRONG")
            except KeyboardInterrupt:
                print(f"Writing (KEYBOARD INTERRUPT)")
            except Exception as e:
                print(f"write_target:{e}")
                break




if __name__ == "__main__":
    main = Main()
    # main.start()
    main.write_target()



    # async def connect(self):
    #     await asyncio.gather(
    #         self.arduino.connect(),
    #         self.android.connect(),
    #     )

    # async def readArduino(self):
    #     while True:
    #         message = await self.arduino.read()
    #         if message is None:
    #             return None

    # async def writeArduino(self):
    #     while True:
    #         self.arduino.write("test {self.i}")
    #         self.i += 1
    #         time.sleep(1)

    # loop = asyncio.get_event_loop()
    # loop.run_forever(main.readArduino()) 
    # asyncio.run(main.connect())
    # _thread.start_new_thread(main.writeArduino)
    # _thread.start_new_thread(main.readArduino)

    
            # await asyncio.gather(
            #     self.arduino.connect(),
            #     self.algorithm.connect(),
            # )