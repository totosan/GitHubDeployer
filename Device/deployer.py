#!/usr/bin/env python
import time
import asyncio
from lcd import LCD
from deployerService import DeployerService
import RPi.GPIO as GPIO
from datetime import datetime
from encoder import Encoder

lcd = LCD()
dpSvc = DeployerService()
loop = None
timer = None

CANCEL_BTN = 12
APPROVE_BTN = 10
START_BTN = 16
SWITCH = 18

#             0        1         2
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
counter = 0
isTerminator = False
bouncetime = 500


class Timer:
    def __init__(self, timeout, callback):
        self._timeout = timeout
        self._callback = callback
        self._task = asyncio.ensure_future(self._job())

    async def _job(self):
        while True:
            await asyncio.sleep(self._timeout)
            await self._callback()

    def cancel(self):
        self._task.cancel()


async def timeout_callback():
    lst = dpSvc.getCurrentRun()
    if isTerminator:
        lcd.setRGB(dpSvc.YELLOW.R, dpSvc.YELLOW.G, dpSvc.YELLOW.B)

def valueChanged(value, direction):
    if(value == 50):
        print(f"value of rotary: {value}")
        dpSvc.simulate(value)


def setup_hardware():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(CANCEL_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(APPROVE_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(START_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def button_pushed(_):
    global isTerminator
    if(loop is None):
        print("no loop")
        return
    if GPIO.input(CANCEL_BTN) == GPIO.HIGH:
        print("Cancel")
        if(isTerminator):
            loop.call_soon_threadsafe(dpSvc.cancel())
        else:
            loop.call_soon_threadsafe(dpSvc.reject())
        return
            
    if GPIO.input(APPROVE_BTN) == GPIO.HIGH:
        print("Approve")
        loop.call_soon_threadsafe(dpSvc.approve())
        return

    if GPIO.input(START_BTN) == GPIO.HIGH:
        print("Start")
        loop.call_soon_threadsafe(dpSvc.start(isTerminator))
        return

    if GPIO.input(SWITCH) == GPIO.HIGH:
        isTerminator = not isTerminator
        if (isTerminator):
            print("Terminator")
            lcd.setText("Terminator")
        else:
            print("Automator")
            lcd.setText("Automator")
        return

def exit_handler():
    print('closed loop')
    GPIO.cleanup()
    loop.close()

if __name__ == "__main__":
    setup_hardware()
    lcd.setRGB(dpSvc.NEUTRAL.R, dpSvc.NEUTRAL.G, dpSvc.NEUTRAL.B)

    try:
        timer = Timer(1,timeout_callback)
        e1 = Encoder(35, 37, GPIO, callback=valueChanged)
        
        GPIO.add_event_detect(CANCEL_BTN, GPIO.RISING, callback=button_pushed, bouncetime=bouncetime)    
        GPIO.add_event_detect(APPROVE_BTN, GPIO.RISING, callback=button_pushed, bouncetime=bouncetime)    
        GPIO.add_event_detect(START_BTN, GPIO.RISING, callback=button_pushed, bouncetime=bouncetime)    
        GPIO.add_event_detect(SWITCH, GPIO.BOTH, callback=button_pushed, bouncetime=bouncetime)    

        loop = asyncio.get_event_loop()
        loop.run_forever()
    finally:
        exit_handler()
