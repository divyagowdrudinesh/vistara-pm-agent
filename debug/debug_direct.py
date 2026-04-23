import requests

EMAIL = "your_email@example.com"
API_TOKEN = "PASTE_YOUR_TOKEN_HERE"
BASE_URL = "https://your-instance.atlassian.net"

auth = (EMAIL, API_TOKEN)
headers = {"Accept": "application/json"}

url = f"{BASE_URL}/rest/api/3/issue/VAI-15"
response = requests.get(url, auth=auth, headers=headers)
print(f"Issue GET: {response.status_code}")

url2 = f"{BASE_URL}/rest/api/3/issue/VAI-15/comment"
response2 = requests.get(url2, auth=auth, headers=headers)
print(f"Comment GET: {response2.status_code}")