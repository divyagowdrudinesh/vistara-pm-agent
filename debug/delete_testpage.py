import requests
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN")
BASE_URL = os.getenv("JIRA_BASE_URL")

auth = (EMAIL, API_TOKEN)
headers = {"Accept": "application/json"}

url = f"{BASE_URL}/wiki/api/v2/pages/11075585"
response = requests.delete(url, auth=auth, headers=headers)
print(f"Status: {response.status_code}")
print(f"Response: {response.text[:200]}")