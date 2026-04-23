# ============================================================
# CREATE EPIC 4 — PARTNER COLLEGE WORKSHOPS & INDUSTRY PLACEMENT PIPELINE
# Creates 10 stories, subtasks, acceptance criteria,
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

# --- Authentication and headers ---
auth = (EMAIL, API_TOKEN)
headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# --- Constants ---
BOARD_ID = 100
EPIC_KEY = "VAI-4"
STORY_POINTS_FIELD = "customfield_10037"


# --- Reusable functions (same as Epic 3) ---

def create_issue(summary, issue_type, description="", story_points=0, epic_key=None, parent_key=None):
    url = f"{BASE_URL}/rest/api/3/issue"
    fields = {
        "project": {"key": config.PROJECT_KEY},
        "summary": summary,
        "issuetype": {"name": issue_type},
        "description": {
            "version": 1,
            "type": "doc",
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
        fields[STORY_POINTS_FIELD] = story_points
    if epic_key:
        fields["parent"] = {"key": epic_key}
    if parent_key:
        fields["parent"] = {"key": parent_key}
    payload = {"fields": fields}
    response = requests.post(url, data=json.dumps(payload), auth=auth, headers=headers)
    return response

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
    response = requests.post(url, data=json.dumps(payload), auth=auth, headers=headers)
    return response

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

def assign_to_sprint(sprint_id, issue_keys):
    url = f"{BASE_URL}/rest/agile/1.0/sprint/{sprint_id}/issue"
    payload = {"issues": issue_keys}
    response = requests.post(url, data=json.dumps(payload), auth=auth, headers=headers)
    return response


# ============================================================
# STEP 1: Create Sprints 8 and 9
# ============================================================
print("=== Creating Sprints ===\n")

s8_response = create_sprint(
    "Sprint 8 — Partners & Plan",
    "2022-09-01T09:00:00.000+05:30",
    "2023-01-31T18:00:00.000+05:30",
    "Snappy Lime and Sripada partnerships formalized, workshop curriculum designed, RG Institute collaboration confirmed"
)
s8_data = json.loads(s8_response.text)
SPRINT_8_ID = s8_data["id"]
print(f"  Sprint 8 created | ID: {SPRINT_8_ID}")

s9_response = create_sprint(
    "Sprint 9 — Deliver & Convert",
    "2023-02-01T09:00:00.000+05:30",
    "2023-03-31T18:00:00.000+05:30",
    "3-day and 6-day workshops delivered, conversion offer launched, 17 enrolments secured, placement outcomes tracked"
)
s9_data = json.loads(s9_response.text)
SPRINT_9_ID = s9_data["id"]
print(f"  Sprint 9 created | ID: {SPRINT_9_ID}")

# ============================================================
# STEP 1B: Update Epic 4 name and description
# ============================================================
print("\n=== Updating Epic 4 ===\n")

epic_url = f"{BASE_URL}/rest/api/3/issue/{EPIC_KEY}"
epic_payload = {
    "fields": {
        "summary": "Partner College Workshops & Industry Placement Pipeline",
        "description": {
            "version": 1,
            "type": "doc",
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": "Planning and delivery of 3-day and 6-day animation workshops at RG Institute of Commerce and Management, formalization of industry placement partnerships with Sripada Studios and Snappy Lime, workshop-to-enrolment conversion tracking, and placement outcome documentation. Covers workshop curriculum design (Adobe Photoshop, Premiere Pro, Autodesk Maya), tiered pricing (Rs. 299/499), 15-day conversion offer execution, and partnership ROI measurement."
                        }
                    ]
                }
            ]
        }
    }
}
epic_response = requests.put(epic_url, data=json.dumps(epic_payload), auth=auth, headers=headers)
if epic_response.status_code == 204:
    print("  Epic 4 updated — name and description changed")
else:
    print(f"  Epic 4 update FAILED: {epic_response.status_code} — {epic_response.text[:100]}")

# ============================================================
# STEP 2: Define all 10 stories
# ============================================================

stories = [
    # --- SPRINT 8 STORIES (4 stories) ---
    {
        "summary": "Formalize Snappy Lime hiring collaboration agreement",
        "points": 3,
        "sprint": 8,
        "description": "As PM responsible for building industry partnerships, I need to formalize the hiring collaboration with Snappy Lime so that Vistara students have a documented pipeline for animation, ad production, and digital content projects — strengthening both placement credibility and revenue through outsourced work.",
        "criteria": (
            "Acceptance Criteria:\n"
            "1. Partnership terms defined — hiring collaboration scope covering animation, company ads, festival message animations, digital content\n"
            "2. Institute's interests documented — student exposure, project pipeline, placement credibility\n"
            "3. Partner expectations captured — practical production quality standards, delivery timelines expected from students\n"
            "4. Formal collaboration letter issued by Snappy Lime — CEO Manjunath Hegde and Director Abhishek JH sign-off\n"
            "5. Relationship maintenance plan agreed — ongoing coordination cadence between Vistara and Snappy Lime"
        ),
        "subtasks": []
    },
    {
        "summary": "Formalize Sripada Studios official placement partner agreement",
        "points": 3,
        "sprint": 8,
        "description": "As PM building a placement pipeline for graduating students, I need to formalize Sripada Studios as official placement partner so that students have a structured internship-to-employment pathway and the institute can credibly market placement support to prospective enrolments.",
        "criteria": (
            "Acceptance Criteria:\n"
            "1. Placement partnership terms agreed — internship 2-3 months with stipend, evaluation, full-time conversion pathway\n"
            "2. Recruitment process documented — intern onboarding, performance assessment criteria, conversion to probation\n"
            "3. Scope of partnership defined — video editing, animation, design, digital media placement opportunities\n"
            "4. Official placement partner letter signed by P V Phani Srivatsa (CEO, Sripada Studios)\n"
            "5. Student profile sharing process agreed — top priority sharing of profiles for placement shortlisting\n"
            "6. Partnership communicated to students and faculty — placement pipeline visible in programme marketing"
        ),
        "subtasks": ["Draft student profile sharing template for Sripada Studios shortlisting process"]
    },
    {
        "summary": "Design workshop curriculum and pricing model for partner colleges",
        "points": 3,
        "sprint": 8,
        "description": "As PM responsible for workshop product design, I need to define the curriculum, format, and pricing for partner college workshops so that there is a standardized, repeatable workshop model ready for delivery at RG Institute and future college partners.",
        "criteria": (
            "Acceptance Criteria:\n"
            "1. Two workshop tiers defined — 3-day (Rs. 299) and 6-day (Rs. 499)\n"
            "2. 3-day curriculum finalized — Adobe Photoshop + Autodesk Maya covering logo design, product packaging, photo manipulation, 3D modelling, environment design, motion graphics, color correction\n"
            "3. 6-day curriculum finalized — adds Adobe Premiere Pro covering video editing, news layout animation, masking and transition, social media video creation\n"
            "4. Pricing covers costs — course material soft-copies, software access, faculty time accounted for\n"
            "5. Content topics mapped to industry relevance — AI, product design, social media content, interior/exterior design, wedding photo/video editing, cinematic color grading\n"
            "6. Curriculum approved by Chethan Kumar (Head Faculty) and Director"
        ),
        "subtasks": []
    },
    {
        "summary": "Establish RG Institute partnership and schedule first workshop",
        "points": 2,
        "sprint": 8,
        "description": "As PM coordinating external college partnerships, I need to formalize the collaboration with RG Institute of Commerce and Management so that workshop dates, lab access, and student registration logistics are confirmed before the first delivery.",
        "criteria": (
            "Acceptance Criteria:\n"
            "1. RG Institute partnership agreed — collaboration terms confirmed with college administration\n"
            "2. Lab access secured — computer lab hours and software availability confirmed via Sunil (on-ground logistics)\n"
            "3. First workshop dates locked — February 2023 batch scheduled\n"
            "4. Student registration process defined — batch sizes confirmed (50 students for 3-day split into 2 batches of 25, 30 students for 6-day)\n"
            "5. Co-branded workshop flier produced — Vistara + RG Institute branding, content details, pricing, registration info"
        ),
        "subtasks": ["Coordinate with Sunil to confirm lab hours and infrastructure readiness at RG Institute"]
    },

    # --- SPRINT 9 STORIES (6 stories) ---
    {
        "summary": "Deliver 3-day workshop batch at RG Institute — 50 students",
        "points": 3,
        "sprint": 9,
        "description": "As PM managing workshop execution, I need to ensure the 3-day workshop is delivered smoothly across 2 batches of 25 students each so that attendees receive the full curriculum experience and Vistara's brand credibility at RG Institute is established.",
        "criteria": (
            "Acceptance Criteria:\n"
            "1. Both batches delivered — 2 batches of 25 students each completed the 3-day programme\n"
            "2. Full curriculum covered — Adobe Photoshop and Autodesk Maya modules delivered as per plan\n"
            "3. Course materials distributed — soft-copies and software access provided to all 50 students\n"
            "4. Faculty delivery confirmed — Chethan Kumar (lead) assisted by Sunil\n"
            "5. Student feedback collected — post-workshop satisfaction survey or verbal feedback documented\n"
            "6. No logistical disruptions — lab access, software, and AV worked without P1 issues"
        ),
        "subtasks": []
    },
    {
        "summary": "Deliver 6-day workshop batch at RG Institute — 30 students",
        "points": 5,
        "sprint": 9,
        "description": "As PM managing extended workshop delivery, I need to ensure the 6-day workshop is delivered successfully so that students experience the full Photoshop + Premiere Pro + Maya pipeline and are primed for conversion to Vistara's longer programmes.",
        "criteria": (
            "Acceptance Criteria:\n"
            "1. Single batch of 30 students completed the 6-day programme\n"
            "2. Full curriculum covered — Adobe Photoshop, Adobe Premiere Pro, and Autodesk Maya modules delivered\n"
            "3. Extended content delivered — video editing, news layout animation, social media video creation in addition to 3-day content\n"
            "4. Course materials and software access provided to all 30 students\n"
            "5. Faculty delivery confirmed — Chethan Kumar (lead) assisted by Sunil\n"
            "6. Student feedback collected and documented"
        ),
        "subtasks": []
    },
    {
        "summary": "Launch 15-day conversion offer for workshop attendees",
        "points": 2,
        "sprint": 9,
        "description": "As PM driving enrolment conversion, I need to launch a time-bound discount offer for workshop attendees so that the conversion window is structured with clear incentives tiered by programme duration.",
        "criteria": (
            "Acceptance Criteria:\n"
            "1. Discount tiers finalized and approved by Director — 10% off 6-month, 15% off 1-year and under-2-year, 25% off 2-year, 50% off 2+ year courses\n"
            "2. Offer communicated to all 80 workshop attendees — via WhatsApp, in-person announcement, or printed handout\n"
            "3. 15-day validity window set — clear deadline communicated\n"
            "4. Registration process ready — enrolment forms and payment process available for immediate conversion\n"
            "5. Conversion tracking initiated — spreadsheet or tracker set up to monitor sign-ups by course and workshop batch"
        ),
        "subtasks": []
    },
    {
        "summary": "Track workshop-to-enrolment conversions and report outcomes",
        "points": 3,
        "sprint": 9,
        "description": "As PM responsible for measuring workshop ROI, I need to track and report all conversions from workshop attendees to enrolled students so that the workshop model's effectiveness is quantified and future college partnership decisions are data-driven.",
        "criteria": (
            "Acceptance Criteria:\n"
            "1. 6-day batch conversions documented — 13 enrolments (7 for 6-month, 5 for 1-year, 1 for 3-year)\n"
            "2. 3-day batch conversions documented — 4 enrolments (all 6-month)\n"
            "3. Total conversion rate calculated — 17 out of 80 attendees (21.25%)\n"
            "4. Revenue impact estimated — enrolment fees collected minus discount amounts\n"
            "5. Conversion breakdown by programme duration prepared for Director review\n"
            "6. Recommendations documented — what drove conversion, what blocked it, improvements for next workshop cycle"
        ),
        "subtasks": ["Prepare conversion report with course-wise breakdown for Director review meeting"]
    },
    {
        "summary": "Track placement outcomes via Sripada Studios and Snappy Lime pipelines",
        "points": 3,
        "sprint": 9,
        "description": "As PM managing industry partnerships end-to-end, I need to track placement outcomes across both Sripada Studios and Snappy Lime so that partnership ROI is documented and placement credibility can be marketed to prospective students.",
        "criteria": (
            "Acceptance Criteria:\n"
            "1. Snappy Lime project pipeline documented — end-to-end animation work, company ads, festival message animations handled by Vistara students\n"
            "2. Sripada Studios placement outcomes tracked — 1-year and 2-year students receiving internship/placement offers, all 3-year students placed (minimum internship offers)\n"
            "3. Placement data organized by programme duration — which programmes produced placement-ready students\n"
            "4. Partnership health assessed — any gaps, escalations, or improvements needed\n"
            "5. Outcomes summarized for use in marketing materials and programme brochures"
        ),
        "subtasks": []
    },
    {
        "summary": "Retrospective — workshop model evaluation and future college expansion plan",
        "points": 2,
        "sprint": 9,
        "description": "As PM driving programme growth strategy, I need to evaluate the workshop model's success and plan the expansion to additional partner colleges so that Vistara has a repeatable outreach-to-enrolment pipeline ready for BIET and GMIT in 2024.",
        "criteria": (
            "Acceptance Criteria:\n"
            "1. Workshop model evaluated — cost, effort, conversion rate, student feedback assessed\n"
            "2. RG Institute relationship reviewed — what worked, what to improve for repeat workshops\n"
            "3. Sept 2023 repeat workshop confirmed — same format, dates tentatively locked with RG Institute\n"
            "4. 2024 repeat cycle planned — Feb and Sept 2024 slots identified\n"
            "5. Future college expansion roadmap drafted — BIET and GMIT targeted for 2026 workshop rollout (pending solidified presence)\n"
            "6. Retrospective findings documented in Confluence"
        ),
        "subtasks": []
    }
]


# ============================================================
# STEP 3: Create all stories, subtasks, and acceptance criteria
# ============================================================
print("\n=== Creating Stories ===\n")

sprint_8_keys = []
sprint_9_keys = []

for story in stories:
    # --- Create the story under Epic 4 ---
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

        # --- Track sprint assignment ---
        if story["sprint"] == 8:
            sprint_8_keys.append(story_key)
        else:
            sprint_9_keys.append(story_key)

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
                issue_type="Sub-task",
                parent_key=story_key
            )
            if st_response.status_code == 201:
                st_data = json.loads(st_response.text)
                print(f"           Subtask: {st_data['key']} — {subtask_summary[:50]}")
            else:
                print(f"           Subtask FAILED: {st_response.status_code} — {st_response.text[:100]}")

    else:
        print(f"  FAILED: {story['summary'][:50]} — {response.status_code} {response.text[:100]}")


# ============================================================
# STEP 4: Assign stories to sprints
# ============================================================
print("\n=== Assigning to Sprints ===\n")

s8_assign = assign_to_sprint(SPRINT_8_ID, sprint_8_keys)
if s8_assign.status_code == 204:
    print(f"  Sprint 8 — {len(sprint_8_keys)} stories assigned")
else:
    print(f"  Sprint 8 FAILED: {s8_assign.status_code}")

s9_assign = assign_to_sprint(SPRINT_9_ID, sprint_9_keys)
if s9_assign.status_code == 204:
    print(f"  Sprint 9 — {len(sprint_9_keys)} stories assigned")
else:
    print(f"  Sprint 9 FAILED: {s9_assign.status_code}")

print("\n=== Epic 4 — Partner College Workshops & Industry Placement Pipeline — COMPLETE ===")