import requests, os
from lcd import LCD

class Color:
    def __init__(self, R=100,G=100,B=100) -> None:
        self.R=R
        self.G=G
        self.B=B
        
    def Get(self):
        return self.R,self.G,self.B
               
class DeployerService:
    
    CUSTOM_CHARS = [   
                        [0x0E,0x15,0x15,0x17,0x11,0x11,0x0E,0x00],
                        [0x04,0x0E,0x0E,0x04,0x1F,0x04,0x0E,0x1B],
                        [0x06,0x0F,0x06,0x04,0x0E,0x0D,0x04,0x06]
                    ]
        
    def __init__(self, lcd=None):
        self.RED = Color(100,0,0)
        self.GREEN=Color(0,100,0)
        self.BLUE=Color(0,0,100)
        
        if(not lcd):
            lcd = LCD()
        self.lcd = lcd
        self.listOfRuns = []
        self.cancel_url = "https://deployer-app.whitebeach-e0296232.westeurope.azurecontainerapps.io/cancel"
        self.blank_run_url = "https://deployer-app.whitebeach-e0296232.westeurope.azurecontainerapps.io"

        # init custom characters
        [self.lcd.create_char(i,GH.CUSTOM_CHARS[i]) for i in range(0,len(GH.CUSTOM_CHARS))]
        
    def log(self, text, color):
        self.lcd.setText_norefresh(f'{text}')
        R,G,B=color.Get()
        print(R,G,B)
        self.lcd.setRGB(R,G,B)
        
    def cancel(self):
        for i in self.listOfRuns:
            res = requests.post(self.cancel_url.format(i))
            if(res.ok):
                self.log("canceling...",self.RED)
                self.listOfRuns.remove(i)
            
    def getCurrentRun(self):
        res = requests.get(url=self.blank_run_url)
        if(res.ok):
            wfs = res.json()
            if len(wfs) > 0:
                # runs found
                for i in wfs:
                    runid = i
                    if not runid in self.listOfRuns:
                        self.listOfRuns.append(runid)
                        print(runid)
                        #self.lcd.setText_norefresh(f'Run is waiting')
                        self.log("run is waiting",self.GREEN)
                        
            elif(len(self.listOfRuns)>0):
                self.listOfRuns.clear()
                print("cleared list")
                self.log("no runs waiting",self.RED)
        return self.listOfRuns