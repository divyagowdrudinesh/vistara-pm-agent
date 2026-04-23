import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN")
BASE_URL = os.getenv("JIRA_BASE_URL")

auth = (EMAIL, API_TOKEN)
headers = {"Accept": "application/json"}

# Step 1: Get ALL fields from Jira to find story point fields
print("=== Finding all story point related fields ===\n")
url = f"{BASE_URL}/rest/api/3/field"
response = requests.get(url, auth=auth, headers=headers)
fields = json.loads(response.text)

for field in fields:
    name = field["name"].lower()
    if "point" in name or "estimate" in name or "story" in name:
        print(f"  Name: {field['name']}")
        print(f"  ID:   {field['id']}")
        print(f"  Type: {field.get('schema', {}).get('type', 'unknown')}")
        print()

# Step 2: Check VAI-15 values for those fields
print("=== VAI-15 current values ===\n")
url2 = f"{BASE_URL}/rest/api/3/issue/VAI-15"
response2 = requests.get(url2, auth=auth, headers=headers)
data = json.loads(response2.text)

for field in fields:
    name = field["name"].lower()
    if "point" in name or "estimate" in name or "story" in name:
        field_id = field["id"]
        value = data["fields"].get(field_id, "NOT IN RESPONSE")
        print(f"  {field['name']} ({field_id}) = {value}")