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

# Try to create a test page in VAI space
url = f"{BASE_URL}/wiki/api/v2/pages"
payload = {
    "spaceId": "131075",
    "status": "current",
    "title": "TEST PAGE — DELETE ME",
    "parentId": "131181",
    "body": {
        "representation": "storage",
        "value": "<p>This is a test page created by the agent.</p>"
    }
}

response = requests.post(url, data=json.dumps(payload), auth=auth, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:500]}")