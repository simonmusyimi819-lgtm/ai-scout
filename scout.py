import os, requests
from playwright.sync_api import sync_playwright

def run_scout():
    # We use a 'User-Agent' to trick Google into thinking we are a normal Chrome browser
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Apply the User-Agent here
        context = browser.new_context(user_agent=user_agent)
        page = context.new_page()
        
        # SEARCH FOR JOBS
        page.goto("https://www.google.com/search?q=site:greenhouse.io+%22Director+of+Sales%22")
        
        # Wait for results to load
        page.wait_for_selector("h3")
        results = page.locator("h3").all_text_contents()[:5]
        
        if not results:
            print("No results found. Google might be blocking us.")
            return

        payload = {"source": "Money Scout", "content": str(results)}
        requests.post(os.environ.get('MAKE_URL'), json=payload)
        browser.close()

if __name__ == "__main__":
    run_scout()
