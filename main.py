from flask import Flask, render_template, request, redirect
from extractors.berlin import extract_berlin_jobs
from extractors.web3 import extract_web3_jobs

app = Flask(__name__)

db = {} # 검색 결과 캐시용

@app.route("/")
def home():
    return render_template("home.html")

# /search?keyword=python 대신 /search/python 구조로 변경
@app.route("/search/<keyword>") 
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