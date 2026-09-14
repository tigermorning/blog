import json, re
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
client = OpenAI()

class Draft(BaseModel):
    headline: str = Field(description="20자 내외의 한국어 헤드라인")
    summary:  str = Field(description="세 문장 요약. ~합니다체, 과장 없이 건조하게")
    why:      str = Field(description="국내 개발팀에게 왜 중요한지 한 문장")

SYS = ("당신은 국내 개발팀을 위한 AI 뉴스레터 기자입니다.\n"
       "아래 기사 본문을 읽고 헤드라인·요약·왜 중요한지를 쓰세요.\n"
       "'주목된다·기대를 모은다' 같은 기자체 표현은 쓰지 마세요.")
RETRY = "\n반드시 한국어로 다시 쓰세요."

def has_korean(text):
    return re.search(r"[가-힣]", text) is not None

def draft(body, temperature):                  # 영어로 오면 앞 실습처럼 한 번 재요청
    sys, retried = SYS, False
    for _ in range(2):
        d = client.chat.completions.parse(
            model="gpt-4.1-mini", temperature=temperature,
            messages=[{"role": "system", "content": sys},
                      {"role": "user", "content": body[:6000]}],
            response_format=Draft).choices[0].message.parsed
        if has_korean(d.summary):
            break
        sys, retried = SYS + RETRY, True
    return d, retried

NUM = re.compile(r"\d[\d,.]*\d|\d")
def numbers(text):                             # "2026", "500", "1.5" 같은 숫자열
    return {n.replace(",", "").rstrip(".") for n in NUM.findall(text)}

def latin_names(text):                         # 요약에 영문 그대로 남은 고유명사 (OpenAI, Sequoia …)
    return set(re.findall(r"\b[A-Z][A-Za-z0-9]+(?:[ -][A-Z][A-Za-z0-9]+)*", text))

def sentences(text):
    return len([s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s])

# 앞 실습에서 저장한 본문 중 숫자가 가장 많은 기사 한 건
articles = json.loads(Path(__file__).with_name("step8_bodies.json").read_text(encoding="utf-8"))
a = max(articles, key=lambda x: len(NUM.findall(x["body"][:6000])))
body_nums = numbers(a["body"][:6000])
print("기사:", a["title"], f"(본문 {len(a['body'])}자, 앞 6000자 안 숫자열 {len(body_nums)}종)\n")

results = {}
for t in (0, 0.7):
    runs = []
    for k in range(3):
        d, retried = draft(a["body"], t)
        nums = numbers(d.summary)
        runs.append({"headline": d.headline, "summary": d.summary, "retried": retried,
                     "sentences": sentences(d.summary), "numbers": sorted(nums),
                     "not_in_body": sorted(nums - body_nums),
                     "latin": sorted(latin_names(d.summary))})
    results[str(t)] = runs
    print(f"══ temperature {t} ══")
    for k, r in enumerate(runs, 1):
        print(f"[{k}] 문장 {r['sentences']} · 숫자 {r['numbers']} · 원문에 없는 숫자 {r['not_in_body'] or '-'}"
              + (" · 재요청함" if r["retried"] else ""))
        print(f"    헤드라인: {r['headline']}")
        print(f"    요약    : {r['summary']}")
    print(f"→ 서로 다른 헤드라인 {len({r['headline'] for r in runs})}개 · "
          f"서로 다른 요약 {len({r['summary'] for r in runs})}개 / 3번\n")

Path(__file__).with_name("step8_temperature.json").write_text(
    json.dumps({"title": a["title"], "runs": results}, ensure_ascii=False, indent=1), encoding="utf-8")
