from playwright.sync_api import sync_playwright
import time

def extract_berlin_jobs(keyword):
    url = f"https://berlinstartupjobs.com/skill-areas/{keyword}/"
    print(f"🌐 Scraping Berlin: {url}")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        time.sleep(3)

        jobs_data = page.evaluate("""
            () => {
                const results = [];
                const items = document.querySelectorAll('li.bjs-jlid');
                items.forEach(item => {
                    const titleEl = item.querySelector('h4 a');
                    const companyEl = item.querySelector('a.bjs-jlid__b');
                    const descEl = item.querySelector('.bjs-jlid__description');
                    
                    if (titleEl) {
                        results.push({
                            title: titleEl.innerText.trim(),
                            company: companyEl ? companyEl.innerText.trim() : "Unknown",
                            description: descEl ? descEl.innerText.trim() : "No description",
                            link: titleEl.href
                        });
                    }
                });
                return results;
            }
        """)
        browser.close()
        return jobs_data