import json, re, feedparser, requests, trafilatura
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
client = OpenAI()
UA = {"User-Agent": "Mozilla/5.0 (newsletter-agent-course)"}

class Draft(BaseModel):
    headline: str = Field(description="20자 내외의 한국어 헤드라인")
    summary:  str = Field(description="세 문장 요약. ~합니다체, 과장 없이 건조하게")
    why:      str = Field(description="국내 개발팀에게 왜 중요한지 한 문장")

SYS = ("당신은 국내 개발팀을 위한 AI 뉴스레터 기자입니다.\n"
       "아래 기사 본문을 읽고 헤드라인·요약·왜 중요한지를 쓰세요.\n"
       "'주목된다·기대를 모은다' 같은 기자체 표현은 쓰지 마세요.")
RETRY = "\n반드시 한국어로 다시 쓰세요."        # 재요청 때만 덧붙이는 한 줄

def has_korean(text):
    return re.search(r"[가-힣]", text) is not None

def korean_fields(d):                          # 한글이 한 글자도 없는 칸을 돌려준다
    return [k for k in ("headline", "summary", "why") if not has_korean(getattr(d, k))]

def draft(body, sys):
    return client.chat.completions.parse(
        model="gpt-4.1-mini", temperature=0,
        messages=[{"role": "system", "content": sys},
                  {"role": "user", "content": body[:6000]}],
        response_format=Draft).choices[0].message.parsed

def draft_korean(body, max_retry=1):           # 검사 → 실패하면 한 줄 덧붙여 다시
    d = draft(body, SYS)
    first_bad = korean_fields(d)
    retries = 0
    while korean_fields(d) and retries < max_retry:
        retries += 1
        d = draft(body, SYS + RETRY)
    return d, first_bad, retries

# TechCrunch AI 피드에서 본문이 600자 이상인 기사 10건 — 다음 실습에서도 같은 본문을 쓰려고 저장
cache = Path(__file__).with_name("step8_bodies.json")
if cache.exists():
    articles = json.loads(cache.read_text(encoding="utf-8"))
else:
    feed = feedparser.parse(requests.get(
        "https://techcrunch.com/category/artificial-intelligence/feed/",
        headers=UA, timeout=20).content)
    articles = []
    for e in feed.entries:
        downloaded = trafilatura.fetch_url(e.link)
        body = trafilatura.extract(downloaded) if downloaded else None
        if body and len(body) >= 600:
            articles.append({"title": e.title, "url": e.link, "body": body})
        if len(articles) == 10:
            break
    cache.write_text(json.dumps(articles, ensure_ascii=False, indent=1), encoding="utf-8")

rows = []
for a in articles:
    d, first_bad, retries = draft_korean(a["body"])
    final_bad = korean_fields(d)
    rows.append({"title": a["title"], "len": len(a["body"]), "first_bad": first_bad,
                 "retries": retries, "final_bad": final_bad, "headline": d.headline})
    mark = "통과" if not first_bad else ("재시도 후 통과" if not final_bad else "재시도 후에도 실패")
    print(f"{len(a['body']):>6}자  {mark:<10} 첫 시도 영어 칸 {first_bad or '-'}")
    print(f"        {a['title'][:58]}")
    print(f"        → {d.headline}")

n = len(rows)
retried = sum(r["retries"] > 0 for r in rows)
fixed = sum(r["retries"] > 0 and not r["final_bad"] for r in rows)
print(f"\n{n}건 중 첫 시도에 한글 없는 칸이 있던 기사 {retried}건 · 재요청 1번으로 고쳐진 기사 {fixed}건")
Path(__file__).with_name("step8_korean_retry.json").write_text(
    json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
