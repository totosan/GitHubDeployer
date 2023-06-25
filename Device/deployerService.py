import requests, os, json
from FakeLCD import FakeLCD

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
        self.NEUTRAL=Color(128,128,128)
        self.YELLOW=Color(244,130,37)
        
        if(not lcd):
            lcd = FakeLCD()
        self.lcd = lcd
        self.listOfRuns = []
        self.start_url = "https://deployer-app.whitebeach-e0296232.westeurope.azurecontainerapps.io/start-run"
        self.simulate_url = "https://deployer-app.whitebeach-e0296232.westeurope.azurecontainerapps.io/simulate"
        self.reject_url = "https://deployer-app.whitebeach-e0296232.westeurope.azurecontainerapps.io/reject-run?runid={0}"
        self.approve_url = "https://deployer-app.whitebeach-e0296232.westeurope.azurecontainerapps.io/approve-run?runid={0}"
        self.cancel_url = "https://deployer-app.whitebeach-e0296232.westeurope.azurecontainerapps.io/cancel-run?runid={0}"
        self.blank_run_url = "https://deployer-app.whitebeach-e0296232.westeurope.azurecontainerapps.io/all-running-runs?all=true"

        self.rotary = False
        # init custom characters
        [self.lcd.create_char(i,DeployerService.CUSTOM_CHARS[i]) for i in range(0,len(DeployerService.CUSTOM_CHARS))]
        
    def log(self, text, color):
        print(text)
        self.lcd.setText_norefresh(f'{text}')
        R,G,B=color.Get()
        self.lcd.setRGB(R,G,B)
        
    def cancel(self):
        for i in self.listOfRuns:
            res = requests.post(self.cancel_url.format(i))
            if(res.ok):
                self.log("canceling...",self.RED)
                self.listOfRuns.remove(i)
            print(res.content)
            
    def approve(self):
        for i in self.listOfRuns:
            res = requests.post(self.approve_url.format(i))
            if(res.ok):
                self.log("approving...",self.GREEN)
                self.listOfRuns.remove(i)
    
    def start(self, isRing):
        body={'isTerminator':isRing}
        print(body)
        res = requests.post(url=self.start_url, json=body)
        if res.ok:
            print("started")
            self.log("started WF", self.YELLOW)
        else:
            print("not started")
            self.log("NOT started", self.YELLOW)

    def simulate(self, value):
        self.rotary = True
        print(f"value of rotary: {value}")
        # display a progress as # symbol that has a full length of 16 chars
        # where a value of 50 is 16th char
        # so each step is 50/16 = 3.125        
        self.log(f"{'#' * int(value/3.125)}",self.NEUTRAL)
        if(value >= 50):
            try:
                for i in self.listOfRuns:
                    body = {'RunId':i,'Command':"CPU",'Value': value}
                    print(f'{body}')
                    res = requests.post(url=self.simulate_url, json=body)
                    if res.ok:
                        self.log("High CPU", self.RED)
            except Exception as ex:
                print(ex)
            self.rotary = False
            return True
        self.rotary = False
        return False
                        
    def reject(self):
        for i in self.listOfRuns:
            res = requests.post(self.reject_url.format(i))
            if(res.ok):
                self.log("Rejected...",self.RED)
                self.listOfRuns.remove(i)
            
    def getCurrentRun(self):
        if(self.rotary):
            return 
        res = requests.get(url=self.blank_run_url)
        if(res.ok):
            wfs = res.json()
            if len(wfs) > 0:
                # runs found
                self.listOfRuns.clear()
                k = 0
                for i in wfs["runId"]:
                    runid = i
                    state = str(wfs["runStatus"][k])
                    self.listOfRuns.append(runid)
                    self.log(f"{len(self.listOfRuns)} runs \n{state}",self.BLUE)
                    k = k+1
        if(len(self.listOfRuns)==0):
            self.log("no runs waiting",self.NEUTRAL)

        return self.listOfRuns
