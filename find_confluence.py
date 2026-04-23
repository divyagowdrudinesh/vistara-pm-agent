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

# Try v1 API with all space types including personal
print("=== All Spaces via v1 API (includes personal) ===\n")
url = f"{BASE_URL}/wiki/rest/api/space?type=personal&limit=50"
response = requests.get(url, auth=auth, headers=headers)
data = json.loads(response.text)

for space in data.get("results", []):
    print(f"  Key: {space['key']} | ID: {space['id']} | Type: {space.get('type')} | Name: {space['name']}")

# Also try global spaces
print("\n=== Global Spaces via v1 API ===\n")
url2 = f"{BASE_URL}/wiki/rest/api/space?type=global&limit=50"
response2 = requests.get(url2, auth=auth, headers=headers)
data2 = json.loads(response2.text)

for space in data2.get("results", []):
    print(f"  Key: {space['key']} | ID: {space['id']} | Type: {space.get('type')} | Name: {space['name']}")