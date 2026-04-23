import requests
import json
import os
from dotenv import load_dotenv
import config

load_dotenv()
auth = (os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN"))
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}
url = f"{os.getenv('JIRA_BASE_URL')}/rest/api/3/issue"

subtasks = [("VAI-18", "Consolidate VAI-17 and VAI-18 feedback into single revision brief document"),
    ("VAI-21", "Confirm print vendor has received print-ready PDF")
]

for parent_key, summary in subtasks:
    payload = {
        "fields": {
            "project": {"key": config.PROJECT_KEY},
            "summary": summary,
            "issuetype": {"name": "Sub-task"},
            "parent": {"key": parent_key},
        }
    }
    
    r = requests.post(url, headers=headers, auth=auth, data=json.dumps(payload))
    if r.status_code == 201:
        print(f"Successfully created sub-task for {parent_key}: {json.loads(r.text)['key']}")
    else:
        print(f"Failed to create sub-task for {parent_key}: {r.status_code} - {r.text}")