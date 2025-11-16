#!/usr/bin/env python3
import os
import sys
import json
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def get_env(name):
    value = os.getenv(name)
    if not value:
        print(f"Missing required environment variable: {name}")
        sys.exit(1)
    return value

def add_comment(issue_key, comment_text):
    email = get_env("JIRA_EMAIL")
    token = get_env("JIRA_API_TOKEN")
    domain = get_env("JIRA_DOMAIN")

    url = f"https://{domain}/rest/api/3/issue/{issue_key}/comment"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # ADF-compliant body format
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
                            "text": comment_text
                        }
                    ]
                }
            ]
        }
    })

    auth = HTTPBasicAuth(email, token)

    response = requests.post(url, headers=headers, data=payload, auth=auth)

    if response.status_code == 201:
        comment_id = response.json().get("id")
        print(f"✅ Comment added successfully! Comment ID: {comment_id}")
    else:
        print("❌ Failed to add comment:")
        print("Status:", response.status_code)
        print("Response:", response.text)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python add_comment.py ISSUE_KEY \"Comment text\"")
        sys.exit(1)

    issue_key = sys.argv[1]
    comment_text = sys.argv[2]

    add_comment(issue_key, comment_text)

