import abc

class iLCDDisplay(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def setRGB(self, r, g, b):
        pass
    
    @abc.abstractmethod
    def setText(self, text):
        pass
    
    @abc.abstractmethod
    def setText_norefresh(self, text):
        pass
    
    @abc.abstractmethod
    def create_char(self, location, pattern):
        pass
