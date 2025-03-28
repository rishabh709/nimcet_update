import requests
import hashlib
import json
from bs4 import BeautifulSoup

# Website to track
# URL = "https://nimcet.admissions.nic.in/"
URL = "https://rishabh709.github.io/Portfolio/"
WEBHOOK_URL = "https://discord.com/api/webhooks/1355033640370704424/H3mqwauwtr9jvSwD-liFJFR0Q4qe9Drb3MttPvMRgtHkLuGac9DWiYGFNltQ_RLDNuuI"  # Replace with your Discord webhook URL

# Store the previous hash in a text file
HASH_FILE = "hash.txt"

def get_website_content(url):
    """Fetch website content as text."""
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.get_text()

def send_discord_notification():
    """Send notification to Discord when content changes."""
    message = {
        "username": "Website Tracker Bot",
        "embeds": [{
            "title": "🚨 Website Content Changed!",
            "description": f"The content of [this website]({URL}) has changed. Check it out!",
            "color": 16711680  # Red color
        }]
    }
    
    response = requests.post(WEBHOOK_URL, data=json.dumps(message), headers={"Content-Type": "application/json"})
    if response.status_code == 204:
        print("✅ Notification sent to Discord!")
    else:
        print(f"❌ Failed to send notification. Response: {response.text}")

def check_for_updates():
    """Check if website content has changed."""
    content = get_website_content(URL)
    current_hash = hashlib.md5(content.encode()).hexdigest()

    try:
        with open(HASH_FILE, "r") as file:
            previous_hash = file.read().strip()
    except FileNotFoundError:
        previous_hash = ""

    if previous_hash and previous_hash != current_hash:
        print("🚨 Change detected! Sending Discord notification...")
        send_discord_notification()

    with open(HASH_FILE, "w") as file:
        file.write(current_hash)

# Run the check
check_for_updates()
