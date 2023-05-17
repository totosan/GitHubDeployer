#!/usr/bin/env python
import time
import asyncio
from lcd import LCD
from deployerService import DeployerService
import RPi.GPIO as GPIO
from datetime import datetime
from rotaryEncoder import RotaryEncoder

lcd = LCD()
dpSvc = DeployerService(lcd=lcd)
loop = None
timer = None

CANCEL_BTN = 12
APPROVE_BTN = 10
START_BTN = 16
SWITCHa = 18
SWITCHb = 22

#             0        1         2
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
counter = 0
isTerminator = False
bouncetime = 100
e1 = None
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
    global isTerminator
    try:
        switchState = GPIO.input(SWITCHa)
        print(f'SWITCH IS {GPIO.input(SWITCHa)}')
        if switchState == 0:
            isTerminator = True
        else:
            isTerminator = False
            
        lst = dpSvc.getCurrentRun()
        if isTerminator:
            lcd.setRGB(dpSvc.YELLOW.R, dpSvc.YELLOW.G, dpSvc.YELLOW.B)
    except Exception as e:
        print(e)
        
def valueChanged(value, direction):
    if(value >= 50):
        print(f"value of rotary: {value}")
        # display a progress as # symbol that has a full length of 16 chars
        # where a value of 50 is 16th char
        # so each step is 50/16 = 3.125
        lcd.setText(f"{'#' * int(value/3.125)}")
        dpSvc.simulate(value)
        e1.resetValue()


def setup_hardware():
    print("init hardware")
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(CANCEL_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(APPROVE_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(START_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(SWITCHa, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


def button_pushed(_):
    global isTerminator
    guard = False
    if(loop is None):
        print("no loop")
        return
    
    if not guard:
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

def switchToggled(_):
    global isTerminator
    print(f'toggled {GPIO.input(SWITCHa)}')
    if GPIO.input(SWITCHa) == GPIO.HIGH:
        #isTerminator = not isTerminator
        if (not isTerminator):
            isTerminator = True
            print("Terminator")
            lcd.setText("Terminator")
        else:
            isTerminator = False
            print("Automator")
            lcd.setText("Automator")
    else:
        print("Turned OFF")
    return

    
def exit_handler():
    print('closed loop')
    GPIO.cleanup()
    loop.close()

if __name__ == "__main__":
    setup_hardware()
    lcd.setRGB(dpSvc.YELLOW.R, dpSvc.YELLOW.G, dpSvc.YELLOW.B)
    time.sleep(1)
    lcd.setRGB(dpSvc.NEUTRAL.R, dpSvc.NEUTRAL.G, dpSvc.NEUTRAL.B)
    
    try:
        timer = Timer(1,timeout_callback)
        e1 = RotaryEncoder(35, 37, GPIO, callback=valueChanged)
        
        GPIO.add_event_detect(CANCEL_BTN, GPIO.RISING, callback=button_pushed, bouncetime=bouncetime)    
        GPIO.add_event_detect(APPROVE_BTN, GPIO.RISING, callback=button_pushed, bouncetime=bouncetime)    
        GPIO.add_event_detect(START_BTN, GPIO.RISING, callback=button_pushed, bouncetime=bouncetime)    
        GPIO.add_event_detect(SWITCHa, GPIO.RISING, callback=switchToggled, bouncetime=500)    
        #GPIO.add_event_detect(SWITCHb, GPIO.FALLING, callback=switchToggled, bouncetime=bouncetime)    
            
        loop = asyncio.get_event_loop()
        loop.run_forever()
    finally:
        exit_handler()
