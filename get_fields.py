import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

load_dotenv()

# Load values
JIRA_DOMAIN = os.getenv("JIRA_DOMAIN")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

# Build base URL
if JIRA_DOMAIN:
    JIRA_URL = f"https://{JIRA_DOMAIN}"
else:
    print("❌ ERROR: JIRA_DOMAIN missing in .env file")
    exit()

def get_admin_custom_fields():
    """Fetches only manually created fields from Jira admin."""
    url = f"{JIRA_URL}/rest/api/3/field"

    response = requests.get(url, auth=HTTPBasicAuth(JIRA_EMAIL, JIRA_API_TOKEN))

    if response.status_code != 200:
        print("\n❌ Failed to fetch custom fields")
        print(response.text)
        return

    fields = response.json()

    print("\n=== 🎨 MANUALLY CREATED CUSTOM FIELDS ===\n")

    admin_fields = []

    for field in fields:
        # Only keep manually-created fields
        if field.get("custom") is True and field.get("scope", {}).get("type") == "PROJECT":
            field_name = field.get("name")
            field_id = field.get("id")
            admin_fields.append((field_name, field_id))

    if not admin_fields:
        print("No manually created fields found.")
        return

    for name, field_id in admin_fields:
        print(f"{name} → {field_id}")

if __name__ == "__main__":
    print("=== 🔵 Jira Admin Custom Field Viewer ===\n")

    project_key = input("Enter your Jira PROJECT KEY (Example: SRE): ").strip()

    print("\nFetching manually created fields…\n")

    get_admin_custom_fields()

