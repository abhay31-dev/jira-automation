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

BASE_URL = f"https://{DOMAIN}/rest/api/3/issue"


def download_attachments(issue_key, download_dir="attachments"):
    url = f"{BASE_URL}/{issue_key}"

    headers = {"Accept": "application/json"}

    response = requests.get(
        url, headers=headers, auth=HTTPBasicAuth(EMAIL, API_TOKEN)
    )

    if response.status_code != 200:
        print(f"❌ Failed to fetch issue: {response.status_code}")
        print(response.text)
        return

    issue_data = response.json()
    attachments = issue_data["fields"].get("attachment", [])

    if not attachments:
        print("🔍 No attachments found for this issue.")
        return

    os.makedirs(download_dir, exist_ok=True)

    for att in attachments:
        filename = att["filename"]
        content_url = att["content"]

        print(f"⬇ Downloading {filename}...")
        att_response = requests.get(
            content_url, auth=HTTPBasicAuth(EMAIL, API_TOKEN), stream=True
        )

        if att_response.status_code == 200:
            with open(os.path.join(download_dir, filename), "wb") as f:
                for chunk in att_response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"✅ {filename} saved to {download_dir}")
        else:
            print(f"❌ Failed to download {filename}")


def upload_attachment(issue_key, file_path):
    url = f"{BASE_URL}/{issue_key}/attachments"

    if not os.path.isfile(file_path):
        print(f"❌ File not found: {file_path}")
        return

    headers = {"X-Atlassian-Token": "no-check"}
    files = {"file": open(file_path, "rb")}

    response = requests.post(
        url,
        headers=headers,
        files=files,
        auth=HTTPBasicAuth(EMAIL, API_TOKEN),
    )

    files["file"].close()

    if response.status_code == 200:
        print(f"✅ Attachment uploaded successfully: {file_path}")
    else:
        print(f"❌ Failed to upload attachment: {response.status_code}")
        print(response.text)


# ------------------------------
# Interactive Prompt
# ------------------------------
print("=== 🔵 Jira Attachment Tool ===\n")
issue_key = input("Enter ISSUE KEY (example: SRE-1): ").strip()

print("\nChoose an option:")
print("1️⃣ Download all attachments")
print("2️⃣ Upload a new attachment")
choice = input("Enter 1 or 2: ").strip()

if choice == "1":
    download_attachments(issue_key)
elif choice == "2":
    file_path = input("Enter the full path of the file to upload: ").strip()
    upload_attachment(issue_key, file_path)
else:
    print("❌ Invalid choice. Exiting.")

