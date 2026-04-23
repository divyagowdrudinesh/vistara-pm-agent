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

def add_comment(issue_key, comment_text):
    url = f"{BASE_URL}/rest/api/3/issue/{issue_key}/comment"
    payload = {
        "body": {
            "version": 1,
            "type": "doc",
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": comment_text
                        }
                    ]
                }
            ]
        }
    }
    response = requests.post(url, headers=headers, auth=auth, data=json.dumps(payload))
    return response

acceptance_criteria = {
    "VAI-15": (
        "Acceptance Criteria:\n"
        "1. All 7 programme module lists confirmed — Chethan Kumar verbally confirmed and PM documented\n"
        "2. Software stack per programme verified — Tool names match licensed versions in lab\n"
        "3. Career outcome titles validated — Cross-checked against Sripada Studios hiring roles\n"
        "4. AVP Term 2 guest faculty dependency flagged — Documented as risk in PRD and DACI\n"
        "5. Session notes published to Confluence — 1-1 Meeting page updated post each session"
    ),
    "VAI-16": (
        "Acceptance Criteria:\n"
        "1. Target audience defined — Students 18-25, aspirational tone documented\n"
        "2. Visual style specified — Dark background, cinematic, programme-specific imagery confirmed\n"
        "3. Format requirements locked — A4 portrait, print CMYK + digital RGB PDF confirmed\n"
        "4. Deliverables list agreed — 7 programme pages + cover + back cover listed\n"
        "5. Designer engagement confirmed — Designer has received brief and confirmed timeline"
    ),
    "VAI-17": (
        "Acceptance Criteria:\n"
        "1. All software names verified — No incorrect tool names on any of 7 pages\n"
        "2. Module titles match curriculum — Each page module list matches BOS syllabus\n"
        "3. Career outcomes realistic — No role listed that Sripada doesn't actually hire\n"
        "4. Feedback documented — Review notes added to Design Brief & Review Log in Confluence\n"
        "5. Formal sign-off given — Chethan Kumar adds comment 'Content Approved — CK' on this ticket"
    ),
    "VAI-18": (
        "Acceptance Criteria:\n"
        "1. Visual hierarchy checked on all 7 pages — Programme name, duration, career outcomes readable at a glance\n"
        "2. Brand consistency confirmed — Consistent colour palette, typography, logo placement\n"
        "3. Consolidated feedback document created — PM notes + Chethan Kumar notes combined into single revision brief\n"
        "4. Revision brief sent to designer — Designer has acknowledged and confirmed Draft 2 timeline"
    ),
    "VAI-19": (
        "Acceptance Criteria:\n"
        "1. All revision brief items addressed — PM checks each line of revision brief against Draft 2\n"
        "2. Software logos accurate — Correct Adobe, Autodesk, Houdini logos confirmed\n"
        "3. Career outcomes expanded — Each page shows 3+ role titles\n"
        "4. Draft 2 internally approved by PM — PM confirms ready for Director review\n"
        "5. Draft 2 file received — PDF in hand before VAI-20 begins"
    ),
    "VAI-20": (
        "Acceptance Criteria:\n"
        "1. Director has reviewed all 7 programme pages — Meeting or walkthrough completed\n"
        "2. Approval decision documented — Director adds comment or PM records decision on this ticket\n"
        "3. No unapproved changes after this point — Any post-approval changes require a new sign-off cycle"
    ),
    "VAI-21": (
        "Acceptance Criteria:\n"
        "1. Print-ready PDF received — High resolution, CMYK, confirmed printable\n"
        "2. Digital PDF received — Compressed, RGB, WhatsApp-shareable file size\n"
        "3. Source files received — Designer source files archived\n"
        "4. File naming convention applied — Files named: Vistara_Brochure_v3_Print_Sep2024.pdf\n"
        "5. Files stored in designated location — Confirmed accessible to Director and PM"
    ),
    "VAI-22": (
        "Acceptance Criteria:\n"
        "1. Digital PDF sent to Snappy Lime — Confirmed received and scheduled for distribution\n"
        "2. WhatsApp broadcast sent — Snappy Lime confirms send to contact list\n"
        "3. Print copies at GM University — Delivered and confirmed with SPOC\n"
        "4. Print copies at Vistara front desk — Available for walk-in enquiries\n"
        "5. Sripada Studios copy sent — Digital copy shared with placement contact\n"
        "6. Initial enquiry uptick noted — Any enrolment enquiries referencing brochure documented"
    )
}

print("=== Adding acceptance criteria as comments ===\n")

for issue_key, criteria in acceptance_criteria.items():
    response = add_comment(issue_key, criteria)
    if response.status_code == 201:
        print(f"Added acceptance criteria comment to {issue_key}.")
    else:
        print(f"Failed to add comment to {issue_key}. Status code: {response.status_code}, Response: {response.text}")