import requests
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

r = requests.get(f'{BASE_URL}/rest/api/3/issue/VAI-15/comment', auth=auth, headers=headers); 
print(f"EMAIL loaded: {EMAIL is not None}")
print(f"TOKEN loaded: {API_TOKEN is not None}")
print(f"TOKEN length: {len(API_TOKEN) if API_TOKEN else 0}")



print(r.status_code, r.text[:200])