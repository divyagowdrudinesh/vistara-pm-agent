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

# Try to access personal space directly by key
personal_space_key = "~71202063ae6eacef0546e2a30dde8a2a2159a6"

print("=== Attempt 1: Get space by key (v1 API) ===\n")
url = f"{BASE_URL}/wiki/rest/api/space/{personal_space_key}"
response = requests.get(url, auth=auth, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:300]}\n")

print("=== Attempt 2: Get pages in personal space (v1 API with CQL) ===\n")
url2 = f"{BASE_URL}/wiki/rest/api/content/search?cql=space.key=\"{personal_space_key}\"&limit=100"
response2 = requests.get(url2, auth=auth, headers=headers)
print(f"Status: {response2.status_code}")
data = json.loads(response2.text)
print(f"Results count: {len(data.get('results', []))}")
for page in data.get("results", [])[:20]:
    print(f"  ID: {page.get('id')} | Title: {page.get('title')}")