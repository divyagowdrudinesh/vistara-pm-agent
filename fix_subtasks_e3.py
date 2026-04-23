import requests
import json
import os
from dotenv import load_dotenv
import config

load_dotenv()

EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN")
BASE_URL = os.getenv("JIRA_BASE_URL")

auth = (EMAIL, API_TOKEN)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# Parent story key → list of subtask summaries
subtasks = {
    "VAI-27": ["Calculate break-even analysis based on Rs. 50 fee vs estimated total costs"],
    "VAI-30": ["Get Director sign-off on final flier design before print production"],
    "VAI-36": [
        "Manage competition judging and winner selection",
        "Coordinate guest of honour arrival, introduction, and hospitality"
    ]
}

print("=== Creating subtasks ===\n")

for parent_key, summaries in subtasks.items():
    for summary in summaries:
        url = f"{BASE_URL}/rest/api/3/issue"
        fields = {
            "project": {"key": config.PROJECT_KEY},
            "summary": summary,
            "issuetype": {"name": "Sub-task"},
            "parent": {"key": parent_key}
        }
        payload = {"fields": fields}
        response = requests.post(url, data=json.dumps(payload), auth=auth, headers=headers)

        if response.status_code == 201:
            data = json.loads(response.text)
            print(f"  {data['key']} — {summary[:50]} (parent: {parent_key})")
        else:
            print(f"  FAILED: {summary[:50]} — {response.status_code} {response.text}")