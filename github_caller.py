from ctypes.wintypes import PINT
import requests, os
from github import Workflow,Github

class GH:
    def __init__(self):
        OWNER="totosan"
        REPO="GitHubIntegrationDWX"

        self.listOfRuns = []
        self.cancel_url = "https://api.github.com/repos/totosan/GitHubIntegrationDWX/actions/runs/{0}/cancel"
        self.blank_run_url = "https://api.github.com/repos/totosan/GitHubIntegrationDWX/actions/workflows/blank.yml/runs"
        self.run_url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/runs"
        self.token = str(os.getenv('TOKEN',''))
        self.gh_headers={
                        'Authorization': f'token {self.token}',
                        'Accept': 'application/vnd.github.v3+json'
                        }

    def cancel(self):
        for i in self.listOfRuns:
            res = requests.post(self.cancel_url.format(i), headers=self.gh_headers)
            if(res.ok):
                print(f"canceled run_id: {i}")
                self.listOfRuns.remove(i)
            
    def getCurrentRun(self):
        res = requests.get(url=self.blank_run_url+"?status=waiting", headers=self.gh_headers)
        wfs = res.json()
        if len(wfs["workflow_runs"]) > 0:
            for i in wfs["workflow_runs"]:
                runid = i["id"]
                if not runid in self.listOfRuns:
                    self.listOfRuns.append(runid)
                    print(runid)
        elif(len(self.listOfRuns)>0):
            self.listOfRuns.clear()
            print("cleared list")