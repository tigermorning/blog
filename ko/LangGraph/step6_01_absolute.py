import os, json, feedparser, requests
from pathlib import Path
from collections import Counter
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
client = OpenAI()
UA = {"User-Agent": "Mozilla/5.0 (newsletter-agent-course)"}

FEEDS = [("TechCrunch", "https://techcrunch.com/category/artificial-intelligence/feed/"),
         ("AI타임스",    "https://www.aitimes.com/rss/allArticle.xml"),
         ("The Verge",  "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml")]

titles = []
for name, url in FEEDS:
    for e in feedparser.parse(requests.get(url, headers=UA, timeout=20).content).entries[:4]:
        titles.append((name, e.title))

RUBRIC = ("당신은 국내 개발팀을 위한 AI 뉴스레터 편집자입니다."
          "아래 기사 제목이 '이번 주 우리가 일하는 방식이 바뀔 만한가'라는 "
          "기준에서 얼마나 중요한지 1~10점으로 매기세요. 숫자만 답하세요.")

scores = []
for src, t in titles:                      # 기사마다 한 번씩, 서로 모르는 채로
    r = client.chat.completions.create(
        model="gpt-4.1-mini", temperature=0, max_tokens=5,
        messages=[{"role": "system", "content": RUBRIC},
                  {"role": "user", "content": t}])
    scores.append((r.choices[0].message.content.strip(), src, t))

for s, src, t in sorted(scores, key=lambda x: -int(x[0])):
    print(f"{s:<6}{src:<12}{t[:44]}")

dist = Counter(s for s, _, _ in scores)
print("\n점수 분포:", " · ".join(f"{k}점 {v}건" for k, v in sorted(dist.items(), key=lambda kv: -int(kv[0]))))
print(f"서로 다른 점수 값: {len(dist)}개 / 후보 {len(scores)}건")

# 다음 실습에서 '똑같은 12건'을 쓰기 위해 저장
Path(__file__).with_name("step6_titles.json").write_text(
    json.dumps(titles, ensure_ascii=False), encoding="utf-8")
