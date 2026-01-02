from flask import Flask, render_template, request, redirect
from extractors.berlin import extract_berlin_jobs
from extractors.web3 import extract_web3_jobs

app = Flask(__name__)

app.config['FREEZER_DESTINATION_IGNORE'] = ['.git*', 'CNAME']
app.config['FREEZER_REMOVE_EXTRA_FILES'] = True

# 핵심 설정: 모든 URL을 디렉토리 구조로 강제 변환
app.config['FREEZER_RELATIVE_URLS'] = True

db = {} # 검색 결과 캐시용

@app.route("/")
def home():
    return render_template("home.html")

# /search?keyword=python 대신 /search/python 구조로 변경
@app.route("/search/<keyword>/")  # 끝에 / 를 붙여줍니다.
def search(keyword):
    if not keyword:
        return redirect("/")
    
    if keyword in db:
        jobs = db[keyword]
    else:
        # 통합 스크래핑 엔진 가동
        jobs = extract_berlin_jobs(keyword) + extract_web3_jobs(keyword)
        db[keyword] = jobs
    
    return render_template("search.html", keyword=keyword, jobs=jobs)

if __name__ == "__main__":
    app.run(debug=True, port=5000)