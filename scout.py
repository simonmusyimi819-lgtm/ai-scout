import os
import requests
from playwright.sync_api import sync_playwright

def run_scout():
    # Target: Companies hiring for 'Director of Sales' in Tech
    # This signals they have money and need to grow.
    search_url = "https://www.google.com/search?q=site:greenhouse.io+OR+site:lever.co+%22Director+of+Sales%22+SaaS"

    try:
        with sync_playwright() as p:
            print("🌐 Opening Browser...")
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(search_url)

            # Grab the top 5 results (Company names usually in the title)
            results = page.locator("h3").all() if hasattr(page.locator("h3"), 'all') else page.query_selector_all("h3")
            found_leads = ", ".join([r.inner_text() for r in results[:5]])
            
            # Clean the data
            print(f"🔎 Found leads: {found_leads[:50]}...")

            payload = {
                "source": "Hiring Signal",
                "content": found_leads
            }

            # Send to Make.com
            webhook_url = os.environ.get('MAKE_URL')
            if webhook_url:
                response = requests.post(webhook_url, json=payload)
                if response.status_code == 200:
                    print("✅ Success! Payload sent to Make.com")
                else:
                    print(f"❌ Failed. Error code: {response.status_code}")
            else:
                print("⚠️  MAKE_URL environment variable not set")
            
            browser.close()
    except Exception as e:
        print(f"❌ Error during execution: {e}")

if __name__ == "__main__":
    run_scout()