import asyncio
import time
import _thread

from arduino import Arduino
from android import Android

class Main:
    def __init__(self):
        self.arduino = Arduino()
        # self.android = Android()
        self.i = 0
        # instantiate computer vision module

    # async def connect(self):
    #     await asyncio.gather(
    #         self.arduino.connect(),
    #         self.android.connect(),
    #     )
    def connect(self):
        self.arduino.connect(),
        # self.android.connect(),
    
    def readArduino(self):
        while True:
            try:
                message = self.arduino.read()
                # print("from arduino: {message}")
                if message is None:
                    return None
            except Exception as e:
                print(e)

    def writeArduino(self):
        i = 0
        while True:
            self.arduino.write()
            i += 1
            time.sleep(1)

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


if __name__ == "__main__":
    main = Main()
    main.connect()
    # loop = asyncio.get_event_loop()
    # loop.run_forever(main.readArduino()) 
    # asyncio.run(main.connect())
    # _thread.start_new_thread(main.writeArduino)
    # _thread.start_new_thread(main.readArduino)
    
    # main.writeArduino()
    main.readArduino()

