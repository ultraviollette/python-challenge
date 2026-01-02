from playwright.sync_api import sync_playwright
import time


def extract_web3_jobs(keyword):
    url = f"https://web3.career/{keyword}-jobs"
    print(f"🌐 Scraping Web3Career: {keyword}")
    
    with sync_playwright() as p:
        # 1. 봇 감지를 피하기 위해 실제 브라우저와 거의 흡사한 환경 구축
        browser = p.chromium.launch(headless=True) 
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080}
        )
        page = context.new_page()
        
        # 2. 타임아웃을 늘리고 로딩 대기 전략 수정
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        
        # 3. 데이터가 그려질 시간을 넉넉히 줌 (Web3는 이게 중요!)
        time.sleep(5)

        jobs_data = page.evaluate("""
            () => {
                const results = [];
                // Web3Career는 데이터가 들어있는 행의 구조가 독특합니다.
                // 클래스가 없는 tr 중에서도 데이터가 있는 것들을 타겟팅합니다.
                const rows = document.querySelectorAll('tr'); 
                
                rows.forEach(row => {
                    // h2 태그가 들어있는 행이 실제 공고 행입니다.
                    const titleEl = row.querySelector('h2');
                    const companyEl = row.querySelector('h3');
                    const linkEl = row.querySelector('a');
                    
                    if (titleEl && companyEl) {
                        results.push({
                            title: titleEl.innerText.trim(),
                            company: companyEl.innerText.trim(),
                            description: "Web3/Crypto Job",
                            link: linkEl.href
                        });
                    }
                });
                return results;
            }
        """)
        browser.close()
        return jobs_data