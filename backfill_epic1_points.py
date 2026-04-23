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

# Epic 1 stories with proposed story points
stories = {
    "VAI-3": 5,
    "VAI-4": 3,
    "VAI-5": 5,
    "VAI-6": 3,
    "VAI-7": 5,
    "VAI-8": 3,
    "VAI-9": 5,
    "VAI-10": 3,
    "VAI-11": 2,
    "VAI-12": 3
}

print("=== Backfilling Epic 1 story points ===\n")

for issue_key, points in stories.items():
    url = f"{BASE_URL}/rest/api/3/issue/{issue_key}"
    payload = {
        "fields": {
            "customfield_10037": points
        }
    }
    response = requests.put(url, data=json.dumps(payload), auth=auth, headers=headers)

    if response.status_code == 204:
        print(f"  {issue_key} = {points} points SET")
    else:
        print(f"  {issue_key} FAILED: {response.status_code} - {response.text[:100]}")

# Quick check — fetch all VAI-15 to VAI-22 (Epic 2 stories) for current points
print("\n=== Checking Epic 2 story points ===\n")
for i in range(15, 23):
    issue_key = f"VAI-{i}"
    url = f"{BASE_URL}/rest/api/3/issue/{issue_key}"
    response = requests.get(url, auth=auth, headers=headers)
    data = json.loads(response.text)
    points = data["fields"].get("customfield_10037", "None")
    print(f"  {issue_key} = {points} points")