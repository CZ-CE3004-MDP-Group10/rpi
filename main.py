import asyncio

from arduino import Arduino
from android import Android

class Main:
    def __init__(self):
        self.arduino = Arduino()
        self.android = Android()
        # instantiate computer vision module

    # async def connect(self):
    #     await asyncio.gather(
    #         self.arduino.connect(),
    #         self.android.connect(),
    #     )
    def connect(self):
        self.arduino.connect(),
        self.android.connect(),

if __name__ == "__main__":
    main = Main()
    # asyncio.run(main.connect())
