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

sprints_to_create = [
    {
        "name": "Sprint 4 — Content & Design",
        "startDate": "2024-08-01T09:00:00.000+05:30",
        "endDate": "2024-08-14T18:00:00.000+05:30",
        "goal": "Content extracted from all 7 programmes, design brief delivered to external designer, Draft 1 in production",
        "originBoardId": 100
    },
    {
        "name": "Sprint 5 — Review & Launch",
        "startDate": "2024-08-15T09:00:00.000+05:30",
        "endDate": "2024-09-20T18:00:00.000+05:30",
        "goal": "Draft 2 approved by Director, final files archived, Snappy Lime distribution confirmed",
        "originBoardId": 100
    }
]

url = f"{BASE_URL}/rest/agile/1.0/sprint"

for sprint in sprints_to_create:
    response = requests.post(url, data=json.dumps(sprint), auth=auth, headers=headers)
    if response.status_code == 201:
        sprint_data = json.loads(response.text)
        print(f"  Created: {sprint_data['name']} | ID: {sprint_data['id']}")
    else:
        print(f"  FAILED: {response.status_code} - {response.text}")