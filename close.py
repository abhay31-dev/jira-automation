#!/usr/bin/env python3
import os
import json
from requests.auth import HTTPBasicAuth
import requests
from dotenv import load_dotenv

# --------------------------
# Load Jira credentials
# --------------------------
load_dotenv()
EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN")
DOMAIN = os.getenv("JIRA_DOMAIN")

if not all([EMAIL, API_TOKEN, DOMAIN]):
    print("❌ Missing environment variables. Check .env file.")
    exit()

# --------------------------
# Functions
# --------------------------

def add_comment(issue_key, comment_text):
    """Add a comment to a Jira issue."""
    url = f"https://{DOMAIN}/rest/api/3/issue/{issue_key}/comment"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    payload = json.dumps({
        "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [{"type": "text", "text": comment_text}]
                }
            ]
        }
    })

    response = requests.post(
        url, headers=headers, data=payload, auth=HTTPBasicAuth(EMAIL, API_TOKEN)
    )

    if response.status_code == 201:
        print("✅ Comment added successfully!")
    else:
        print(f"❌ Failed to add comment: {response.status_code}")
        print(response.text)

def get_transitions(issue_key):
    """Fetch all possible transitions for the issue."""
    url = f"https://{DOMAIN}/rest/api/3/issue/{issue_key}/transitions"
    headers = {"Accept": "application/json"}

    response = requests.get(url, headers=headers, auth=HTTPBasicAuth(EMAIL, API_TOKEN))
    if response.status_code != 200:
        print(f"❌ Failed to fetch transitions: {response.status_code}")
        print(response.text)
        return []

    data = response.json()
    return data.get("transitions", [])

def close_issue(issue_key):
    """Transition the issue to a 'Done' / 'Closed' status."""
    transitions = get_transitions(issue_key)
    if not transitions:
        print("❌ No transitions found for this issue.")
        return

    # Look for common close transitions
    close_transition = None
    for t in transitions:
        name = t.get("name", "").lower()
        if "done" in name or "close" in name or "resolved" in name:
            close_transition = t
            break

    if not close_transition:
        print("❌ No suitable 'Close/Done' transition found.")
        print("Available transitions:")
        for t in transitions:
            print(f"- {t['name']} (ID: {t['id']})")
        return

    # Perform transition
    url = f"https://{DOMAIN}/rest/api/3/issue/{issue_key}/transitions"
    payload = {"transition": {"id": close_transition["id"]}}
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    response = requests.post(
        url, headers=headers, data=json.dumps(payload),
        auth=HTTPBasicAuth(EMAIL, API_TOKEN)
    )

    if response.status_code == 204:
        print(f"✅ Issue {issue_key} has been successfully closed!")
    else:
        print(f"❌ Failed to close issue: {response.status_code}")
        print(response.text)

# --------------------------
# Interactive
# --------------------------
print("=== 🔵 Jira Close Issue with Comment ===\n")
issue_key = input("Enter Jira ISSUE KEY (example: SRE-1): ").strip()
comment_text = input("Enter comment to add before closing: ").strip()

# Step 1: Add comment
add_comment(issue_key, comment_text)

# Step 2: Close issue
close_issue(issue_key)

