import os
import requests
from playwright.sync_api import sync_playwright

def run_scout():
    # Target: Companies hiring for 'Director of Sales' in Tech
    # This signals they have money and need to grow.
    search_url = "https://www.google.com/search?q=site:greenhouse.io+OR+site:lever.co+%22Director+of+Sales%22+SaaS"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(search_url)

        # Grab the top 5 results (Company names usually in the title)
        results = page.locator("h3").all_text_contents()[:5]
        
        # Clean the data
        found_leads = ", ".join(results)

        payload = {
            "source": "Hiring Signal",
            "content": found_leads
        }

        # Send to Make.com
        webhook_url = os.environ.get('MAKE_URL')
        if webhook_url:
            requests.post(webhook_url, json=payload)
        
        browser.close()

if __name__ == "__main__":
    run_scout()
