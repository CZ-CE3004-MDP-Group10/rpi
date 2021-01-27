import asyncio
import time
from multiprocessing import Process, Value, Queue, Manager

from arduino import Arduino
# from android import Android
from algorithm import Algorithm

class Main:
    def __init__(self):
        self.arduino = Arduino()
        self.algorithm = Algorithm()
        # self.android = Android()
        # instantiate computer vision module

        self.manager = Manager()
        self.write_queue = self.manager.Queue()

        self.read_arduino_process = Process(target=self.read_arduino)
        self.read_algorithm_process = Process(target=self.read_algorithm)
        # self.read_android_process = Process(target=self.read_android)
        self.write_target = Process(target=self.write_target)

    def start(self):
        try:
            self.arduino.connect()
            self.algorithm.connect()
            # self.android.connect()
            
            self.read_arduino_process.start()
            # self.read_android_process.start()
            # self.write_android_process.start()

            self.write_target.start()
        except Exception as e:
            print(e)

    def read_arduino(self):
        while True:
            try:
                raw_message = self.arduino.read()
                if raw_message is None:
                    continue
                # for message in raw_message.splitlines():
                #     if len(message) <= 0:
                #         continue
                self.write_queue.put_nowait(raw_message)
            except Exception as e:
                print(f"read_arduino:{e}")
                break    

    def read_algorithm(self):
        while True:
            try:
                raw_message = self.algorithm.read()
                if raw_message is None:
                    continue                
                self.write_queue.put_nowait(raw_message)
                
            except Exception as e  :
                print(f'read_algorithm:{e}')
                break

    def write_target(self):
        while True:
            try:
                if not self.write_queue.empty():
                    message = self.write_queue.get_nowait()
                    print(message)
                    self.arduino.write(message)
                    # self.algorithm.write(message)
                    # self.android.write(message)
            except Exception as e:
                print(f"write_target:{e}")




if __name__ == "__main__":
    main = Main()
    main.start()
    main.readArduino()



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