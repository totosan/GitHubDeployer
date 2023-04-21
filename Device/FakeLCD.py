from iLCDDisplay import iLCDDisplay

# create a fake from the interface iLCDDisplay

class FakeLCD(iLCDDisplay):
    def setRGB(self, r, g, b):
        print("setRGB: r = " + str(r) + ", g = " + str(g) + ", b = " + str(b))
    
    def setText(self, text):
        print("setText: " + text)
    
    def setText_norefresh(self, text):
        print("setText_norefresh: " + text)
    
    def create_char(self, location, pattern):
        print("create_char: location = " + str(location) + ", pattern = " + str(pattern))