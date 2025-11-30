#!/usr/bin/env python3
import os
import subprocess
import re
import json
import platform
from requests.auth import HTTPBasicAuth
import requests
from dotenv import load_dotenv
import socket

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

def get_system_info():
    """Get basic system info for the node."""
    hostname = socket.gethostname()
    os_info = f"{platform.system()} {platform.release()} ({platform.version()})"
    return hostname, os_info

def get_interfaces_status():
    """Get interface names, status, and IP addresses using 'ip addr'."""
    try:
        output = subprocess.check_output(["ip", "-br", "addr"], universal_newlines=True)
    except Exception as e:
        print(f"❌ Failed to run 'ip -br addr': {e}")
        return []

    interfaces = []
    for line in output.splitlines():
        parts = line.split()
        if len(parts) >= 2:
            iface_name = parts[0]
            status = parts[1]
            ips = " ".join(parts[2:]) if len(parts) > 2 else "No IP"
            interfaces.append({"name": iface_name, "status": status, "ips": ips})
    return interfaces

def format_comment_code(hostname, os_info, interfaces):
    """Format the Jira comment as a code block."""
    lines = [
        f"Node: {hostname}",
        f"OS: {os_info}",
        "Network Interfaces:"
    ]
    for iface in interfaces:
        lines.append(f"{iface['name']}: {iface['status']} | {iface['ips']}")
    return "\n".join(lines)

def post_comment(issue_key, comment_text):
    """Post the comment to Jira as a code block."""
    url = f"https://{DOMAIN}/rest/api/3/issue/{issue_key}/comment"
    headers = {"Accept": "application/json", "Content-Type": "application/json"}

    payload = {
        "body": {
            "type": "doc",
            "version": 1,
            "content": [
                {
                    "type": "codeBlock",
                    "attrs": {"language": "bash"},
                    "content": [
                        {"type": "text", "text": comment_text}
                    ]
                }
            ]
        }
    }

    response = requests.post(
        url, headers=headers, data=json.dumps(payload), auth=HTTPBasicAuth(EMAIL, API_TOKEN)
    )

    if response.status_code == 201:
        print("✅ Comment added successfully in code style!")
    else:
        print(f"❌ Failed to add comment: {response.status_code}")
        print(response.text)

# --------------------------
# Interactive
# --------------------------
print("=== 🔵 Jira Network Interfaces Commenter (Code Block) ===\n")
issue_key = input("Enter Jira ISSUE KEY (example: SRE-1): ").strip()

hostname, os_info = get_system_info()
interfaces = get_interfaces_status()

if not interfaces:
    print("❌ No interfaces found. Exiting.")
    exit()

# Preview
print(f"\nNode: {hostname}")
print(f"OS: {os_info}\n")
print("Network Interfaces:")
for iface in interfaces:
    print(f"🔹 {iface['name']}: {iface['status']} | {iface['ips']}")

confirm = input("\nDo you want to comment this on Jira in code style? (y/n): ").strip().lower()
if confirm == "y":
    comment_text = format_comment_code(hostname, os_info, interfaces)
    post_comment(issue_key, comment_text)
else:
    print("❌ Aborted by user.")

