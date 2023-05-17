import json
from urllib import response
import requests, os
              
class GH:        
    def __init__(self, logging=None):
        OWNER="totosan"
        REPO="GitHubIntegrationDWX"
        runid="{0}"
        self.logging = logging
        self.listOfRuns = []
        self.cancel_url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs/{runid}/cancel"
        self.blank_run_url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs"
        self.pendings = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs/{runid}/pending_deployments"
        self.starter_url = f"https://api.github.com/repos/{OWNER}/{REPO}/dispatches"
        
        self.token = str(os.getenv('TOKEN',''))
        self.gh_headers={
                        'Authorization': f'token {self.token}',
                        'Accept': 'application/vnd.github.v3+json'
                        }
    def log(self, msg):
        if self.logging:
            self.logging.debug(msg)
        else:
            print(msg)
            
    def approve(self):
        for runid in self.listOfRuns:
            res = requests.get(self.pendings.format(runid), headers=self.gh_headers)
            pendings = res.json()
            env_id = pendings[0]["environment"]["id"]
            body = {"environment_ids":[env_id], "state":"approved", "comment":"looks good"}
            print(json.dumps(body))
            res = requests.post(self.pendings.format(runid), headers=self.gh_headers, json=body)
            if(res.ok):
                print("Approval sent")
            else:
                print("issues with sending approval")

    def reject(self):
        for runid in self.listOfRuns:
            res = requests.get(self.pendings.format(runid), headers=self.gh_headers)
            pendings = res.json()
            env_id = pendings[0]["environment"]["id"]
            body = {"environment_ids":[env_id], "state":"rejected", "comment":"Oh dear, I cannot do that."}
            print(json.dumps(body))
            res = requests.post(self.pendings.format(runid), headers=self.gh_headers, json=body)
            if(res.ok):
                print("Rejection sent")
            else:
                print("issues with sending rejection")
        
    def cancel(self):
        try:
            for i in self.listOfRuns:
                self.log(f"canceling {i}")
                res = requests.post(self.cancel_url.format(i), headers=self.gh_headers)
                if(res.ok):
                    self.listOfRuns.remove(i)
                else:
                    self.log(f"issues with canceling {i}: {res.json()}")
        except Exception as e:
            self.log(f"Exception {e}")

    def startWF(self, isRing):
        if not isRing:
            body={'event_type':'on_deployer','client_payload':{"Experiment":"True"}}
        else:
            body={'event_type':'on_deployer_ring','client_payload':{"Experiment":"True"}}
        res = requests.post(url=self.starter_url, headers=self.gh_headers, json=body)
        if res.ok:
            return True
        else:
            print(res.json())
            return False
        
    def getCurrentRun(self):
        try:
            self.log(f"Sending request to: {self.blank_run_url}")
            res = requests.get(url=self.blank_run_url + "?status=", headers=self.gh_headers)
            res.raise_for_status()

            try:
                self.log("Parsing response JSON...")
                wfs = res.json()
            except ValueError as e:
                self.log(f"Error parsing JSON: {e}")
                return self.listOfRuns

            # filter the runs to only the ones that are waiting
            wfs["workflow_runs"] = list(filter(lambda x: x["status"] == "waiting", wfs["workflow_runs"]))

            if len(wfs["workflow_runs"]) > 0:
                # runs found
                self.log("Waiting runs found:")
                for i in wfs["workflow_runs"]:
                    runid = i["id"]
                    self.log(f"Run ID: {runid}")
                    if runid not in self.listOfRuns:
                        self.listOfRuns.append(runid)
                        self.log(f"New run added: {runid}")
                        # self.lcd.setText_norefresh(f'Run is waiting')
                        # self.log("run is waiting", self.GREEN)
            elif len(self.listOfRuns) > 0:
                self.listOfRuns.clear()
                self.log("No waiting runs found. Cleared list.")
                # self.log("no runs waiting", self.RED)
            self.log(f"Runs in list: {self.listOfRuns}")
        except requests.exceptions.RequestException as e:
            self.log(f"Error on GH call: {e}")

        return self.listOfRuns




