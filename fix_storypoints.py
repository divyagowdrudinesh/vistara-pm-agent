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

# All Epic 2 stories with their correct story points
stories = {
    "VAI-15": 8,
    "VAI-16": 3,
    "VAI-17": 3,
    "VAI-18": 2,
    "VAI-19": 2,
    "VAI-20": 1,
    "VAI-21": 1,
    "VAI-22": 3
}

for issue_key, story_points in stories.items():
    url = f"{BASE_URL}/rest/api/3/issue/{issue_key}"
    payload = {
        "fields": {
            "customfield_10037": story_points
        }
    }
    response = requests.put(url, headers=headers, auth=auth, data=json.dumps(payload))
    if response.status_code == 204:
        print(f"Updated {issue_key} with {story_points} story points.")
    else:
        print(f"Failed to update {issue_key}. Status code: {response.status_code}, Response: {response.text}")