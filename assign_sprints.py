import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN")
BASE_URL = os.getenv("JIRA_BASE_URL")

auth = (EMAIL, API_TOKEN)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

assignments = {
    170: ["VAI-15", "VAI-16"],
    171: ["VAI-17", "VAI-18", "VAI-19", "VAI-20", "VAI-21", "VAI-22"]
}

for sprint_id, issues in assignments.items():
    url = f"{BASE_URL}/rest/agile/1.0/sprint/{sprint_id}/issue"
    payload = {
        "issues": issues
    }
    response = requests.post(url, data=json.dumps(payload), auth=auth, headers=headers)
    if response.status_code == 204:
        print(f"  Sprint {sprint_id} — assigned {issues}")
    else:
        print(f"  Sprint {sprint_id} FAILED: {response.status_code} - {response.text}")

        