import requests
import json
import os

# Set up authentication headers
headers = {
    "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
    "Accept": "application/vnd.github.v3+json"
}

# Define the repository and base URL for API requests
repo_owner = "your_username"
repo_name = "your_repo"
base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"

# Get a list of all workflow runs in the repository
workflow_runs_url = f"{base_url}/actions/runs"
response = requests.get(workflow_runs_url, headers=headers)
response_json = json.loads(response.content)
workflow_runs = response_json["workflow_runs"]
    
# Delete each workflow run one by one
for workflow_run in workflow_runs:
    workflow_run_id = workflow_run["id"]
    delete_url = f"{workflow_runs_url}/{workflow_run_id}"
    response = requests.delete(delete_url, headers=headers)
    if response.status_code == 204:
        print(f"Deleted workflow run {workflow_run_id}")
    else:
        print(f"Failed to delete workflow run {workflow_run_id} with status code {response.status_code}")
