import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()
EMAIL = os.getenv("JIRA_EMAIL")
API_TOKEN = os.getenv("JIRA_API_TOKEN")
DOMAIN = os.getenv("JIRA_DOMAIN")

if not all([EMAIL, API_TOKEN, DOMAIN]):
    print("❌ ERROR: Missing environment variables. Check .env file.")
    exit()

BASE_URL = f"https://{DOMAIN}/rest/api/3/search/jql"


def search_issues_by_summary(project_key, subject_text):
    jql_query = f'project = "{project_key}" AND summary ~ "{subject_text}"'

    payload = {
    "jql": jql_query,
    "fields": ["summary", "issuetype"]  # or ["*all"] for everything
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.post(
        BASE_URL,
        json=payload,
        headers=headers,
        auth=HTTPBasicAuth(EMAIL, API_TOKEN)
    )

    if response.status_code not in [200, 201]:
        print(f"\n❌ Error: {response.status_code}")
        print(response.text)
        return

    data = response.json()
    issues = data.get("issues", [])

    if not issues:
        print("\n🔍 No issues found.")
        return

    print(f"\n=== ✅ Results Found: {len(issues)} ===\n")
    for issue in issues:
        key = issue.get("key") or issue.get("id", "UNKNOWN_KEY")
        fields = issue.get("fields", {})
        summary = fields.get("summary", "No Summary")
        print(f"🔹 {key}: {summary}")


# ------------------------------
# Interactive Prompt
# ------------------------------

print("=== 🔵 Jira Issue Search (By Subject) ===\n")

project = input("Enter PROJECT KEY (example: SRE): ").strip()
subject = input("Enter text to search in SUMMARY: ").strip()

search_issues_by_summary(project, subject)

