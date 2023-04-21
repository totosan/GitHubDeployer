import time,sys
from iLCDDisplay import iLCDDisplay
import smbus
import RPi.GPIO as GPIO
rev = GPIO.RPI_REVISION
if rev == 2 or rev == 3:
    bus = smbus.SMBus(1)
else:
    bus = smbus.SMBus(0)

class LCD(iLCDDisplay):
    # this device has two I2C addresses
    def __init__(self):
        self.DISPLAY_RGB_ADDR = 0x62
        self.DISPLAY_TEXT_ADDR = 0x3e

    # set backlight to (R,G,B) (values from 0..255 for each)
    def setRGB(self,r,g,b):
        bus.write_byte_data(self.DISPLAY_RGB_ADDR,0,0)
        bus.write_byte_data(self.DISPLAY_RGB_ADDR,1,0)
        bus.write_byte_data(self.DISPLAY_RGB_ADDR,0x08,0xaa)
        bus.write_byte_data(self.DISPLAY_RGB_ADDR,4,r)
        bus.write_byte_data(self.DISPLAY_RGB_ADDR,3,g)
        bus.write_byte_data(self.DISPLAY_RGB_ADDR,2,b)

    # send command to display (no need for external use)
    def textCommand(self,cmd):
        bus.write_byte_data(self.DISPLAY_TEXT_ADDR,0x80,cmd)

    # set display text \n for second line(or auto wrap)
    def setText(self,text):
        self.textCommand(0x01) # clear display
        time.sleep(.05)
        self.textCommand(0x08 | 0x04) # display on, no cursor
        self.textCommand(0x28) # 2 lines
        time.sleep(.05)
        count = 0
        row = 0
        for c in text:
            if c == '\n' or count == 16:
                count = 0
                row += 1
                if row == 2:
                    break
                self.textCommand(0xc0)
                if c == '\n':
                    continue
            count += 1
            bus.write_byte_data(self.DISPLAY_TEXT_ADDR,0x40,ord(c))

    #Update the display without erasing the display
    def setText_norefresh(self, text):
        self.textCommand(0x02) # return home
        time.sleep(.05)
        self.textCommand(0x08 | 0x04) # display on, no cursor
        self.textCommand(0x28) # 2 lines
        time.sleep(.05)
        count = 0
        row = 0
        while len(text) < 32: #clears the rest of the screen
            text += ' '
        for c in text:
            if c == '\n' or count == 16:
                count = 0
                row += 1
                if row == 2:
                    break
                self.textCommand(0xc0)
                if c == '\n':
                    continue
            count += 1
            bus.write_byte_data(self.DISPLAY_TEXT_ADDR,0x40,ord(c))

    # Create a custom character (from array of row patterns)
    def create_char(self, location, pattern):
        """
        Writes a bit pattern to LCD CGRAM

        Arguments:
        location -- integer, one of 8 slots (0-7)
        pattern -- byte array containing the bit pattern, like as found at
                https://omerk.github.io/lcdchargen/
        """
        location &= 0x07 # Make sure location is 0-7
        self.textCommand(0x40 | (location << 3))
        bus.write_i2c_block_data(self.DISPLAY_TEXT_ADDR, 0x40, pattern)