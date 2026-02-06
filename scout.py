import os
import requests
from playwright.sync_api import sync_playwright

# This looks for the secret we set in GitHub
WEBHOOK_URL = os.environ.get('MAKE_URL') 

# ... (the rest of your run_scout function stays the same)

def run_scout():
    with sync_playwright() as p:
        print("🌐 Opening Browser...")
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto('https://news.ycombinator.com/')
        
        # Scrape the top 5 headlines
        headlines = page.query_selector_all('.titleline > a')
        text_data = [h.inner_text() for h in headlines[:5]]
        combined_text = "\n".join(text_data)
        
        print(f"🔎 Found: {text_data[0]}...")

        # THE CLOUD PUSH
        payload = {"summary": combined_text, "source": "Hacker News"}
        
        print("📤 Sending to Make.com...")
        response = requests.post(WEBHOOK_URL, json=payload)
        
        if response.status_code == 200:
            print("✅ Success! Check your Make.com screen.")
        else:
            print(f"❌ Failed. Error code: {response.status_code}")
            
        browser.close()

if __name__ == "__main__":

    run_scout()
