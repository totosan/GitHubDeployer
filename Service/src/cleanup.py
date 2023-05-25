import requests
import datetime
import os

# Set up authentication
# replace ### by token
headers = {
    "Authorization": f"Bearer {os.getenv('TOKEN','')}",
    "Accept": "application/vnd.github.v3+json"
}

# Set the retention period to 90 days ago
retention_period = datetime.datetime.utcnow() - datetime.timedelta(minutes=1)

# Retrieve the workflows in the repository
response = requests.get(
    "https://api.github.com/repos/totosan/GitHubIntegrationDWX/actions/workflows",
    headers=headers
)

try:
    workflows = response.json()["workflows"]
except KeyError:
    print("No workflows found")
    workflows = []
    
# Loop through each workflow and delete old runs
for workflow in workflows:
    workflow_id = workflow["id"]
    response = requests.get(f"https://api.github.com/repos/totosan/GitHubIntegrationDWX/actions/workflows/{workflow_id}/runs",headers=headers)
    runs = response.json()["workflow_runs"]
    for run in runs:
        run_id = run["id"]
        created_at = datetime.datetime.fromisoformat(run["created_at"][:-1])
        if created_at < retention_period:
            response = requests.delete(
                f"https://api.github.com/repos/totosan/GitHubIntegrationDWX/actions/runs/{run_id}",
                headers=headers
            )
            if response.status_code == 204:
                print(f"Deleted run {run_id}")
            else:
                print(f"Failed to delete run {run_id} ({response.status_code} {response.reason})")
