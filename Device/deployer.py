#!/usr/bin/env python
import time
from lcd import LCD
from deployerService import DeployerService
import RPi.GPIO as GPIO
from datetime import datetime

lcd = LCD()
dpSvc = DeployerService()

#             0        1         2
colors = [(255,0,0),(0,255,0),(0,0,255)]
counter=0


if __name__=="__main__":
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    CANCEL_BTN=12
    APPROVE_BTN=10
    START_BTN=16
    GPIO.setup(CANCEL_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(APPROVE_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(START_BTN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    R = 128
    G = 128
    B = 128
    lcd.setRGB(R,G,B)
    while True:
      if GPIO.input(CANCEL_BTN) == GPIO.HIGH :
        R,G,B = colors[0]
        dpSvc.cancel()
      if GPIO.input(APPROVE_BTN) == GPIO.HIGH:
        R,G,B = colors[1]
        dpSvc.approve()
      if GPIO.input(START_BTN) == GPIO.HIGH:
        R,G,B = colors[2]
        dpSvc.start()
        
      lst=dpSvc.getCurrentRun()
      time.sleep(0.2)
