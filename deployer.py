#!/usr/bin/env python
import time
from lcd import LCD
from github_caller import GH
import RPi.GPIO as GPIO
from datetime import datetime

lcd = LCD()
gh = GH()

#             0        1         2
colors = [(255,0,0),(0,255,0),(0,0,255)]
counter=0


if __name__=="__main__":
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    R = 128
    G = 128
    B = 128
    while True:
      if GPIO.input(10) == GPIO.HIGH:
        R,G,B = colors[counter]
        gh.cancel()
      gh.getCurrentRun()

      lcd.setText_norefresh(f'Zeit UTC:{str(datetime.now().time())}')
      lcd.setRGB(R,G,B)
      time.sleep(0.2)
