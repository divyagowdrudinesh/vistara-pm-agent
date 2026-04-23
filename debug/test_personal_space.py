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

# Get space info by key (personal space keys start with ~)
print("=== Searching for personal space ===\n")
url = f"{BASE_URL}/wiki/rest/api/space?limit=100"
response = requests.get(url, auth=auth, headers=headers)
data = json.loads(response.text)

for space in data.get("results", []):
    print(f"  Key: {space['key']} | ID: {space['id']} | Type: {space.get('type')} | Name: {space['name']}")