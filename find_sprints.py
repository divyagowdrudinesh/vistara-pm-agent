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

# First, get the board ID for VAI project
url = f"{BASE_URL}/rest/agile/1.0/board"
response = requests.get(url, auth=auth, headers=headers)
boards = json.loads(response.text)

for board in boards["values"]:
    print(f"  Board: {board['name']} | ID: {board['id']}")

# VAI Board Id = 100
print("\n=== Sprints for VAI board ===\n")
url2 = f"{BASE_URL}/rest/agile/1.0/board/100/sprint"
response2 = requests.get(url2, auth=auth, headers=headers)
sprints = json.loads(response2.text)

for sprint in sprints["values"]:
    print(f"  {sprint['name']} | ID: {sprint['id']} | State: {sprint['state']}")

#  === Sprints for VAI board ===

#   Sprint 1 — Semester Pre-Launch | ID: 70 | State: closed
#   Sprint 2 — Enrolment & Launch | ID: 103 | State: closed
#   Sprint 3 — Semester Retrospect | ID: 104 | State: closed   