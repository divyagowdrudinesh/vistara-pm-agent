import requests
import json
import os
from dotenv import load_dotenv
import config 

load_dotenv()
EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN")
BASE_URL = os.getenv("JIRA_BASE_URL")

auth = (EMAIL, API_TOKEN)
headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
}

def create_issue(summary, issue_type, description="", story_points=0, epic_key=None, parent_key=None):
    url = f"{BASE_URL}/rest/api/3/issue"

    fields = {
        "project": {"key": config.PROJECT_KEY},
        "summary": summary,
        "issuetype": {"name": issue_type},
        "description": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": description if description else " "
                        }
                    ]
                }
            ]
        }
    }

    if story_points:
        fields["customfield_10016"] = story_points

    if epic_key:
        fields["parent"] = {"key": epic_key}

    if parent_key:
        fields["parent"] = {"key": parent_key}

    payload = {"fields": fields}

    response = requests.post(url, headers=headers, auth=auth, data=json.dumps(payload))
    return response

if __name__ == "__main__":
    print("Starting Vistara Agent — Epic 2 Stories...")

    stories = [
        {
            "summary": "Extract curriculum content — all 7 programmes via 1-1 sessions with Chethan Kumar",
            "points": 8,
            "description": "As a PM responsible for brochure accuracy, I need to extract and validate all curriculum content directly from head faculty so that the brochure reflects what Vistara actually delivers — not aspirational content.",
            "subtasks": []
        },
        {
            "summary": "Draft design brief and brief external designer",
            "points": 3,
            "description": "As a PM managing external vendor output, I need to produce a complete design brief before any design work begins so that revision cycles are minimised and the designer has unambiguous direction.",
            "subtasks": []
        },
        {
            "summary": "Review Draft 1 — technical content accuracy sign-off by Chethan Kumar",
            "points": 3,
            "description": "As head faculty, I need to review Draft 1 for technical accuracy so that no incorrect software names, tool versions, or module titles appear in the published brochure.",
            "subtasks": []
        },
        {
            "summary": "Review Draft 1 — visual quality and layout sign-off by PM",
            "points": 2,
            "description": "As PM, I need to review Draft 1 for visual hierarchy, consistency, and completeness so that consolidated feedback to the designer is single-pass and unambiguous.",
            "subtasks": [
                "Consolidate VAI-17 and VAI-18 feedback into single revision brief document"
            ]
        },
        {
            "summary": "Incorporate revision feedback — designer produces Draft 2",
            "points": 2,
            "description": "As PM managing the vendor relationship, I need to ensure all consolidated feedback is actioned in Draft 2 so that Director review proceeds without further design iteration.",
            "subtasks": []
        },
        {
            "summary": "Director final approval — Dinesh G K sign-off on Draft 2",
            "points": 1,
            "description": "As PM, I need Director sign-off before any printing or distribution begins so that the institute is not exposed to content errors in a publicly distributed document.",
            "subtasks": []
        },
        {
            "summary": "Receive and archive final print-ready and digital PDF files from designer",
            "points": 1,
            "description": "As PM, I need to receive, verify, and archive all final design files so that print production and digital distribution can begin without delay and source files are preserved for future updates.",
            "subtasks": [
                "Confirm print vendor has received print-ready PDF"
            ]
        },
        {
            "summary": "Distribute brochure via Snappy Lime — digital and print channels activated",
            "points": 3,
            "description": "As PM responsible for go-to-market execution, I need to confirm distribution through all channels so that the brochure reaches prospective students before the next enrolment window opens.",
            "subtasks": []
        }
    ]

    for story in stories:
        print(f"\nCreating story: {story['summary'][:50]}...")
        
        response = create_issue(
            summary=story["summary"],
            issue_type=config.STORY_ISSUE_TYPE,
            description=story["description"],
            story_points=story["points"],
            epic_key="VAI-2"
        )
        
        if response.status_code == 201:
            story_data = json.loads(response.text)
            story_key = story_data["key"]
            print(f"✅ Created: {story_key}")
            
            for subtask_summary in story["subtasks"]:
                print(f"   Creating subtask: {subtask_summary[:50]}...")
                sub_response = create_issue(
                    summary=subtask_summary,
                    issue_type=config.SUBTASK_ISSUE_TYPE,
                    description="",
                    story_points=0,
                    parent_key=story_key
                )
                if sub_response.status_code == 201:
                    sub_data = json.loads(sub_response.text)
                    print(f"   ✅ Subtask created: {sub_data['key']}")
                else:
                    print(f"   ❌ Subtask failed: {sub_response.text}")
        else:
            print(f"❌ Story failed: {response.text}")

    print("\nAgent run complete.")