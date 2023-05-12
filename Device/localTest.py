
#!/usr/bin/env python
import time
import asyncio
import sys, select
import asyncio 

from FakeLCD import FakeLCD
from deployerService import DeployerService
from datetime import datetime
from Device.rotaryEncoder import RotaryEncoder

        
fakeLCD = FakeLCD()

# write a console menu, to chose three items from, while keeping the program running
# with asyncio 
async def main():
    deployerService = DeployerService(lcd=fakeLCD)
    while True:
        deployerService.getCurrentRun()
        # keep prints in console always on a specific line
        for i in range(0, 10):
            print("\033[F\033[K", end="")
        # print the menu

        print ("Choose an option:")
        print ("1. Start a new workflow")
        print ("2. Simulate high CPU")
        print ("3. Exit")
        # wait for user input
        choice = input("Enter your choice [1-3]: ")
        # if user input is 1, start a new workflow
        if choice == '1':
            deployerService.start(isRing=True)
        # if user input is 2, simulate high CPU
        if choice == '2':
            deployerService.simulate(value=100)
        # if user input is 3, exit the program
        if choice == '3':
            sys.exit()
        await asyncio.sleep(0.1)
  
asyncio.run(main())