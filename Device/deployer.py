#!/usr/bin/env python
import time
import asyncio
from lcd import LCD
from deployerService import DeployerService
import RPi.GPIO as GPIO
from datetime import datetime

lcd = LCD()
dpSvc = DeployerService()

CANCEL_BTN = 12
APPROVE_BTN = 10
START_BTN = 16
SWITCH = 18

#             0        1         2
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
counter = 0
isTerminator = False


def setup_hardware():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(CANCEL_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(APPROVE_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(START_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


if __name__ == "__main__":
      setup_hardware()
      lcd.setRGB(dpSvc.NEUTRAL.R, dpSvc.NEUTRAL.G, dpSvc.NEUTRAL.B)
      while True:
            if GPIO.input(CANCEL_BTN) == GPIO.HIGH:
                  R, G, B = colors[0]
                  if(isTerminator):
                      dpSvc.cancel()
                  else:
                      dpSvc.reject()
            if GPIO.input(APPROVE_BTN) == GPIO.HIGH:
                R, G, B = colors[1]
                dpSvc.approve()
            if GPIO.input(START_BTN) == GPIO.HIGH:
                R, G, B = colors[2]
                dpSvc.start()
            if GPIO.input(SWITCH) == GPIO.HIGH:
                isTerminator = True
            else:
                isTerminator = False

            lst = dpSvc.getCurrentRun()
            time.sleep(0.2)
