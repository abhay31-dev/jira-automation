import requests
from requests.auth import HTTPBasicAuth
import sys
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ---------- CONFIGURATION ----------
EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN")
DOMAIN = os.getenv("JIRA_DOMAIN")    # e.g., yourdomain.atlassian.net
JIRA_URL = f"https://{DOMAIN}"
# -----------------------------------

def get_comments(issue_key):
    if not (EMAIL and API_TOKEN and DOMAIN):
        print("Missing environment variables! Check your .env file.")
        sys.exit(1)

    url = f"{JIRA_URL}/rest/api/3/issue/{issue_key}/comment"

    headers = {"Accept": "application/json"}

    response = requests.get(
        url,
        headers=headers,
        auth=HTTPBasicAuth(EMAIL, API_TOKEN)
    )

    if response.status_code != 200:
        print(f"Failed to fetch comments: {response.status_code}")
        print(response.text)
        return

    data = response.json()

    if "comments" not in data or len(data["comments"]) == 0:
        print("No comments found.")
        return

    print(f"\n=== Comments on Issue {issue_key} ===\n")

    for comment in data["comments"]:
        comment_id = comment["id"]

        # Extract ADF comment text
        body_text = ""
        for block in comment["body"].get("content", []):
            for inner in block.get("content", []):
                if inner.get("type") == "text":
                    body_text += inner.get("text", "")

        print(f"Comment ID: {comment_id}")
        print(f"Comment Text: {body_text}")
        print("-" * 40)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python get_comments.py ISSUE_KEY")
        sys.exit(1)

    issue_key = sys.argv[1]
    get_comments(issue_key)

