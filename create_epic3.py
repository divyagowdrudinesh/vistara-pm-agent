# ============================================================
# CREATE EPIC 3 — CINEMOTSAVA 2025
# Creates 14 stories, subtasks, acceptance criteria,
# 2 sprints, and assigns stories to sprints
# ============================================================

import requests
import json
import os
from dotenv import load_dotenv
import config

# --- Load secrets from .env file ---
load_dotenv()
EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN")
BASE_URL = os.getenv("JIRA_BASE_URL")

# --- Authentication and headers for all API calls ---
auth = (EMAIL, API_TOKEN)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# --- Constants used throughout the script ---
BOARD_ID = 100                          # VAI board ID (from find_sprints.py)
EPIC_KEY = "VAI-3"                      # Epic 3 already exists in Jira
STORY_POINTS_FIELD = "customfield_10037"  # Correct field ID for Story Points


# ============================================================
# FUNCTION: Create a Jira issue (story, subtask, or epic)
# ============================================================
def create_issue(summary, issue_type, description="", story_points=0, epic_key=None, parent_key=None):
    url = f"{BASE_URL}/rest/api/3/issue"

    # Build the base fields every issue needs
    fields = {
        "project": {"key": config.PROJECT_KEY},
        "summary": summary,
        "issuetype": {"name": issue_type},
        "description": {                        # ADF Level 1: document
            "version": 1,
            "type": "doc",
            "content": [                        # ADF Level 2: list of paragraphs
                {
                    "type": "paragraph",        # ADF Level 3: one paragraph
                    "content": [                # ADF Level 4: list of text runs
                        {
                            "type": "text",     # ADF Level 5: actual words
                            "text": description if description else " "
                        }
                    ]
                }
            ]
        }
    }

    # Conditionally add optional fields
    if story_points:                            # Stories have points, subtasks don't
        fields[STORY_POINTS_FIELD] = story_points
    if epic_key:                                # Stories need a parent epic
        fields["parent"] = {"key": epic_key}
    if parent_key:                              # Subtasks need a parent story
        fields["parent"] = {"key": parent_key}

    # Wrap in the structure Jira expects and send
    payload = {"fields": fields}
    response = requests.post(url, data=json.dumps(payload), auth=auth, headers=headers)
    return response


# ============================================================
# FUNCTION: Add a comment to a Jira issue
# ============================================================
def add_comment(issue_key, comment_text):
    url = f"{BASE_URL}/rest/api/3/issue/{issue_key}/comment"
    payload = {
        "body": {                               # Comments use "body" not "fields"
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
    response = requests.post(url, data=json.dumps(payload), auth=auth, headers=headers)
    return response


# ============================================================
# FUNCTION: Create a sprint on the VAI board
# ============================================================
def create_sprint(name, start_date, end_date, goal):
    url = f"{BASE_URL}/rest/agile/1.0/sprint"
    payload = {
        "name": name,
        "startDate": start_date,
        "endDate": end_date,
        "goal": goal,
        "originBoardId": BOARD_ID
    }
    response = requests.post(url, data=json.dumps(payload), auth=auth, headers=headers)
    return response


# ============================================================
# FUNCTION: Assign a list of issues to a sprint
# ============================================================
def assign_to_sprint(sprint_id, issue_keys):
    url = f"{BASE_URL}/rest/agile/1.0/sprint/{sprint_id}/issue"
    payload = {"issues": issue_keys}
    response = requests.post(url, data=json.dumps(payload), auth=auth, headers=headers)
    return response

# ============================================================
# STEP 1: Create Sprints 6 and 7
# ============================================================
print("=== Creating Sprints ===\n")

s6_response = create_sprint(
    "Sprint 6 — Plan & Logistics",
    "2025-01-06T09:00:00.000+05:30",
    "2025-01-31T18:00:00.000+05:30",
    "Event collaboration finalized, venue approved, flier distributed, all logistics confirmed"
)
s6_data = json.loads(s6_response.text)
SPRINT_6_ID = s6_data["id"]
print(f"  Sprint 6 created | ID: {SPRINT_6_ID}")

s7_response = create_sprint(
    "Sprint 7 — Execute & Review",
    "2025-02-01T09:00:00.000+05:30",
    "2025-02-28T18:00:00.000+05:30",
    "Cinemotsava executed, conversions tracked, retrospective completed"
)
s7_data = json.loads(s7_response.text)
SPRINT_7_ID = s7_data["id"]
print(f"  Sprint 7 created | ID: {SPRINT_7_ID}")


# ============================================================
# STEP 2: Define all 14 stories
# Each story is a dictionary with all its fields
# ============================================================

stories = [
    # --- SPRINT 6 STORIES (7 stories) ---
    {
        "summary": "Finalize event collaboration with Vishistaa Cine Journey",
        "points": 3,
        "sprint": 6,
        "description": "As PM coordinating an inter-organizational event, I need to formalize the collaboration with Vishistaa Cine Journey so that both partners have agreed on shared branding, competition format, and responsibilities before any public announcements.",
        "criteria": (
            "Acceptance Criteria:\n"
            "1. Partnership terms agreed — shared branding, cost-sharing, competition ownership documented\n"
            "2. Event format confirmed — Short Movie, Creative Reels competitions, Gaming events (PUBG, FreeFire)\n"
            "3. 5 prize categories finalized — Best Short Movie, Best Direction, Best Actor, Best Cinematographer, Best Editor\n"
            "4. Co-branding approved — both Vistara and Vishistaa logos confirmed for all collateral\n"
            "5. Collaboration agreement documented in Confluence"
        ),
        "subtasks": []
    },
    {
        "summary": "Secure venue approval from GMIT Principal and confirm event date",
        "points": 2,
        "sprint": 6,
        "description": "As PM responsible for event logistics, I need formal venue approval from the GMIT Principal so that the event date (February 12, 2025) is locked and all downstream planning can proceed with certainty.",
        "criteria": (
            "Acceptance Criteria:\n"
            "1. Principal approval received — written or verbal confirmation documented\n"
            "2. Event date locked — February 12, 2025 confirmed with no conflicts\n"
            "3. Venue logistics scoped — seating capacity, AV setup, power supply, parking confirmed\n"
            "4. Any venue-specific restrictions documented — noise limits, time constraints, setup/teardown windows"
        ),
        "subtasks": []
    },
    {
        "summary": "Define budget, registration fee, and competition structure",
        "points": 3,
        "sprint": 6,
        "description": "As PM managing event financials, I need to define the full budget, set the registration fee, and finalize competition categories so that all cost decisions are made before flier production begins.",
        "criteria": (
            "Acceptance Criteria:\n"
            "1. Budget estimated — all cost heads identified (venue, catering, prizes, printing, logistics)\n"
            "2. Registration fee set — Rs. 50 per participant, cost-covering model (no profit intent)\n"
            "3. Competition categories locked — Short Movie & Creative Reels, Gaming (PUBG & FreeFire)\n"
            "4. Prize categories confirmed — 5 awards as agreed with Vishistaa\n"
            "5. Break-even attendee count calculated — minimum registrations needed to cover costs"
        ),
        "subtasks": ["Calculate break-even analysis based on Rs. 50 fee vs estimated total costs"]
    },
    {
        "summary": "Finalize registration POCs and assign on-ground crew roles",
        "points": 2,
        "sprint": 6,
        "description": "As PM responsible for event execution, I need to assign registration points of contact and on-ground crew so that every attendee touchpoint and operational task has a named owner before the event goes public.",
        "criteria": (
            "Acceptance Criteria:\n"
            "1. Registration POCs assigned — Kiran Kumar C M and Imran Khan confirmed as Program Managers\n"
            "2. On-ground crew roles defined — registration desk, AV management, guest reception, competition coordination, refreshments\n"
            "3. Contact numbers published — POC details ready for flier inclusion\n"
            "4. Crew briefing scheduled — pre-event walkthrough date set"
        ),
        "subtasks": []
    },
    {
        "summary": "Plan entertainment, refreshments, and draft prize amounts",
        "points": 2,
        "sprint": 6,
        "description": "As PM managing vendor relationships and event experience, I need to finalize entertainment flow, book caterers, and draft prize amounts so that the event experience is planned end-to-end before execution week.",
        "criteria": (
            "Acceptance Criteria:\n"
            "1. Caterer identified and menu agreed — refreshments for estimated attendee count\n"
            "2. Entertainment schedule drafted — competition slots, breaks, award ceremony timing\n"
            "3. Draft prize amounts prepared — pending final adjustment based on registration count after Feb 7\n"
            "4. All vendor commitments confirmed with delivery dates"
        ),
        "subtasks": []
    },
    {
        "summary": "Produce and distribute event flier — print and digital",
        "points": 3,
        "sprint": 6,
        "description": "As PM responsible for event marketing, I need the event flier designed, printed, and distributed across physical and digital channels so that registrations begin by February 1 with full event details visible to the target audience.",
        "criteria": (
            "Acceptance Criteria:\n"
            "1. Flier content finalized — event name, date, competitions, prizes, registration fee, POC contacts, QR code\n"
            "2. Design approved by Director — Dinesh G K sign-off on visual and content\n"
            "3. Print copies produced and distributed — physical fliers at GM University, Vistara front desk, partner locations\n"
            "4. Digital version distributed — WhatsApp broadcast via Snappy Lime contact list\n"
            "5. Distribution completed by February 1, 2025"
        ),
        "subtasks": ["Get Director sign-off on final flier design before print production"]
    },
    {
        "summary": "Prepare course advertisement hoardings for event venue",
        "points": 2,
        "sprint": 6,
        "description": "As PM leveraging the event for enrolment conversion, I need course-specific advertisement hoardings produced and installed at the venue so that all attendees are exposed to Vistara's 7 programme offerings throughout the event day.",
        "criteria": (
            "Acceptance Criteria:\n"
            "1. All 7 courses represented — individual hoarding or banner per programme\n"
            "2. Hoardings produced — print-ready files sent to vendor, physical copies received\n"
            "3. Installation plan confirmed — hoardings placed and tree hangings installed by February 8\n"
            "4. Content accuracy verified — programme names, durations, and career outcomes match brochure"
        ),
        "subtasks": []
    },

    # --- SPRINT 7 STORIES (7 stories) ---
    {
        "summary": "Invite GMIT lecturers and HoDs as event attendees",
        "points": 1,
        "sprint": 7,
        "description": "As PM managing stakeholder engagement, I need to formally invite all GMIT college lecturers and Heads of Departments so that institutional buy-in is visible on event day and future academic collaboration is strengthened.",
        "criteria": (
            "Acceptance Criteria:\n"
            "1. Invitation list prepared — all relevant lecturers and HoDs identified\n"
            "2. Formal invitations sent by February 5 — physical or digital as appropriate\n"
            "3. RSVPs tracked — confirmed attendees documented\n"
            "4. Seating or recognition planned — HoDs acknowledged during event if attending"
        ),
        "subtasks": []
    },
    {
        "summary": "Invite industry partners as guests of honour",
        "points": 1,
        "sprint": 7,
        "description": "As PM managing external stakeholder relationships, I need to invite Snappy Lime and other industry partners as guests of honour so that the event has industry credibility and students see real placement pipeline connections.",
        "criteria": (
            "Acceptance Criteria:\n"
            "1. Snappy Lime invited as guest of honour — confirmation received\n"
            "2. Any additional industry contacts invited — Sripada Studios or other partners\n"
            "3. Guest introduction and speaking slot planned — brief acknowledgement during event\n"
            "4. Guest logistics confirmed — arrival time, parking, seating arranged"
        ),
        "subtasks": []
    },
    {
        "summary": "Finalize prize amounts based on registration count",
        "points": 1,
        "sprint": 7,
        "description": "As PM managing event budget, I need to finalize prize amounts after the registration deadline (Feb 7) so that prize distribution is confirmed before event day with no budget overrun.",
        "criteria": (
            "Acceptance Criteria:\n"
            "1. Final registration count documented — total participants confirmed after Feb 7 deadline\n"
            "2. Revenue calculated — registrations x Rs. 50\n"
            "3. Prize amounts finalized — allocated within budget after deducting venue, catering, printing costs\n"
            "4. Prize amounts communicated to event crew — judges and award presenters informed"
        ),
        "subtasks": []
    },
    {
        "summary": "Prepare event grounds and coordinate caterers — weekend setup",
        "points": 2,
        "sprint": 7,
        "description": "As PM responsible for on-ground readiness, I need the venue fully set up and caterers confirmed over the weekend (Feb 10-11) so that event day starts without any infrastructure or logistics delays.",
        "criteria": (
            "Acceptance Criteria:\n"
            "1. Venue setup completed — seating, stage, AV equipment, registration desk, signage all in place\n"
            "2. Course hoardings installed — all 7 programme advertisements visible at venue\n"
            "3. Caterer final confirmation — menu, quantity, delivery time locked\n"
            "4. AV dry run completed — projector, sound system, microphones tested\n"
            "5. On-ground crew walkthrough done — every team member knows their station and responsibilities"
        ),
        "subtasks": []
    },
    {
        "summary": "Execute Cinemotsava event day — Feb 12, 2025",
        "points": 5,
        "sprint": 7,
        "description": "As PM and sole event coordinator, I need to manage all on-ground operations on event day so that competitions run on schedule, guests are hosted professionally, and attendees have a seamless experience.",
        "criteria": (
            "Acceptance Criteria:\n"
            "1. Registration desk operational — attendee check-in running smoothly\n"
            "2. Competitions executed on schedule — Short Movie, Creative Reels, Gaming events completed\n"
            "3. Judges coordinated — scoring and winner selection completed without delays\n"
            "4. Guests of honour hosted — Snappy Lime and other guests received and acknowledged\n"
            "5. Prize distribution completed — all 5 categories awarded\n"
            "6. Refreshments served on time — caterer delivery matched attendee flow\n"
            "7. No P1 incidents — no major disruptions to event schedule"
        ),
        "subtasks": [
            "Manage competition judging and winner selection",
            "Coordinate guest of honour arrival, introduction, and hospitality"
        ]
    },
    {
        "summary": "Post-event analysis — track admission conversions across 7 courses",
        "points": 3,
        "sprint": 7,
        "description": "As PM responsible for measuring event ROI, I need to track how many event attendees converted to course admissions so that we can quantify Cinemotsava's impact on enrolment and justify future event investment.",
        "criteria": (
            "Acceptance Criteria:\n"
            "1. Conversion count documented — number of attendees who enrolled, broken down by course\n"
            "2. Non-conversion feedback collected — reasons documented from those who attended but didn't enrol\n"
            "3. Conversion rate calculated — attendees-to-admissions percentage\n"
            "4. Course-wise breakdown prepared — which of the 7 programmes attracted most conversions\n"
            "5. Findings summarized in Confluence for Director review"
        ),
        "subtasks": []
    },
    {
        "summary": "Post-event retrospective and next-event planning",
        "points": 2,
        "sprint": 7,
        "description": "As PM driving continuous improvement, I need to conduct a post-event retrospective with the team so that lessons learned are captured and actionable improvements are documented for the next Cinemotsava edition.",
        "criteria": (
            "Acceptance Criteria:\n"
            "1. Retrospective meeting conducted — PM, Director, Head Faculty, crew leads attended\n"
            "2. What went well documented — successful elements identified\n"
            "3. What could improve documented — gaps, delays, feedback themes captured\n"
            "4. Conversion blockers analysed — specific reasons why non-converting attendees didn't enrol\n"
            "5. Action items for next edition documented — with owners and target dates\n"
            "6. Retrospective summary published to Confluence"
        ),
        "subtasks": []
    }
]


# ============================================================
# STEP 3: Create all stories, subtasks, and acceptance criteria
# ============================================================
print("\n=== Creating Stories ===\n")

# These lists will collect issue keys for sprint assignment later
sprint_6_keys = []
sprint_7_keys = []

for story in stories:
    # --- Create the story under Epic 3 ---
    response = create_issue(
        summary=story["summary"],
        issue_type="Story",
        description=story["description"],
        story_points=story["points"],
        epic_key=EPIC_KEY
    )

    if response.status_code == 201:
        story_data = json.loads(response.text)
        story_key = story_data["key"]
        print(f"  {story_key} — {story['summary'][:50]}...")

        # --- Track which sprint this story belongs to ---
        if story["sprint"] == 6:
            sprint_6_keys.append(story_key)
        else:
            sprint_7_keys.append(story_key)

        # --- Add acceptance criteria as comment ---
        ac_response = add_comment(story_key, story["criteria"])
        if ac_response.status_code == 201:
            print(f"           AC comment added")
        else:
            print(f"           AC FAILED: {ac_response.status_code}")

        # --- Create subtasks if any ---
        for subtask_summary in story["subtasks"]:
            st_response = create_issue(
                summary=subtask_summary,
                issue_type="Subtask",
                parent_key=story_key
            )
            if st_response.status_code == 201:
                st_data = json.loads(response.text)
                print(f"           Subtask: {subtask_summary[:50]}")
            else:
                print(f"           Subtask FAILED: {st_response.status_code}")

    else:
        print(f"  FAILED: {story['summary'][:50]} — {response.status_code} {response.text}")


# ============================================================
# STEP 4: Assign stories to sprints
# ============================================================
print("\n=== Assigning to Sprints ===\n")

s6_assign = assign_to_sprint(SPRINT_6_ID, sprint_6_keys)
if s6_assign.status_code == 204:
    print(f"  Sprint 6 — {len(sprint_6_keys)} stories assigned")
else:
    print(f"  Sprint 6 FAILED: {s6_assign.status_code}")

s7_assign = assign_to_sprint(SPRINT_7_ID, sprint_7_keys)
if s7_assign.status_code == 204:
    print(f"  Sprint 7 — {len(sprint_7_keys)} stories assigned")
else:
    print(f"  Sprint 7 FAILED: {s7_assign.status_code}")

print("\n=== Epic 3 — Cinemotsava 2025 — COMPLETE ===")
