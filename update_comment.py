import requests
from requests.auth import HTTPBasicAuth
import sys
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ---------- CONFIGURATION ----------
JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

if not (JIRA_DOMAIN and JIRA_EMAIL and JIRA_API_TOKEN):
    print("Missing .env variables! Ensure JIRA_DOMAIN, JIRA_EMAIL, and JIRA_API_TOKEN exist.")
    sys.exit(1)

JIRA_URL = f"https://{JIRA_DOMAIN}"
# -----------------------------------

def update_comment(issue_key, comment_id, new_text):
    url = f"{JIRA_URL}/rest/api/3/issue/{issue_key}/comment/{comment_id}"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # ADF format for Jira Cloud
    payload = json.dumps({
        "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "paragraph",
                    "content": [
                        {
                            "type": "text",
                            "text": new_text
                        }
                    ]
                }
            ]
        }
    })

    response = requests.put(
        url,
        headers=headers,
        data=payload,
        auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN)
    )

    if response.status_code == 200:
        print(f"Comment updated successfully! (ID: {comment_id})")
    else:
        print(f"Failed to update comment: {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python update_comment.py ISSUE_KEY COMMENT_ID \"Updated comment text\"")
        sys.exit(1)

    issue_key = sys.argv[1]
    comment_id = sys.argv[2]
    new_text = sys.argv[3]

    update_comment(issue_key, comment_id, new_text)

