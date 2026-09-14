import operator, re
from pathlib import Path
from typing import Annotated, TypedDict
from datetime import datetime, timedelta, timezone
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

import feedparser, requests, trafilatura
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
client = OpenAI()

# ── 11편 뼈대: State ──────────────────────────────────────────────
class Brief(TypedDict):
    hours:     int                              # 수집 시간 창(시간)
    collected: list                             # ① 수집한 기사
    picked:    list                             # ② 선별해 남긴 다섯 건
    drafted:   Annotated[list, operator.add]    # ③ 취재한 초안 — 워커들이 나눠 채운다
    log:       Annotated[list, operator.add]    # 무슨 일이 있었는지

# ── 12편 ① 수집 ──────────────────────────────────────────────────
UA = {"User-Agent": "Mozilla/5.0 (newsletter-agent)"}
SOURCES = [
    ("OpenAI",     "https://openai.com/blog/rss.xml"),
    ("DeepMind",   "https://deepmind.google/blog/rss.xml"),
    ("TechCrunch", "https://techcrunch.com/category/artificial-intelligence/feed/"),
    ("The Verge",  "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"),
    ("AI타임스",    "https://www.aitimes.com/rss/allArticle.xml"),
]
KST_NO_ZONE = {"AI타임스"}          # 시간대 표시 없이 한국 시각을 적는 소스

def strip_tags(s):
    return re.sub(r"<[^>]+>", "", s or "").strip()

def published_at(entry, name):
    t = entry.get("published_parsed")
    if not t:
        return None
    at = datetime(*t[:6], tzinfo=timezone.utc)
    return at - timedelta(hours=9) if name in KST_NO_ZONE else at

def url_key(link):                              # utm_ 꼬리표만 떼고 나머지 주소는 그대로
    p = urlsplit(link)
    query = [(k, v) for k, v in parse_qsl(p.query) if not k.startswith("utm_")]
    return urlunsplit((p.scheme, p.netloc, p.path.rstrip("/"), urlencode(query), ""))

def collect(s: dict) -> dict:                   # ① 자료 수집
    cutoff = datetime.now(timezone.utc) - timedelta(hours=s["hours"])
    items, dead, seen = [], [], set()
    for name, url in SOURCES:
        try:
            r = requests.get(url, headers=UA, timeout=20)
            r.raise_for_status()                # 403·404도 실패로 친다
            feed = feedparser.parse(r.content)
        except Exception:
            dead.append(name)                   # 한 곳이 죽어도 나머지는 계속
            continue
        for e in feed.entries:
            at = published_at(e, name)
            if not at or at < cutoff:           # 시간 창 밖이거나 날짜가 없으면 버린다
                continue
            key = url_key(e.link)
            if key in seen:                     # 같은 주소는 한 번만
                continue
            seen.add(key)
            items.append({"title": e.title, "url": e.link, "source": name, "at": at,
                          "summary": strip_tags(e.get("summary", ""))[:300]})
    return {"collected": items,
            "log": [f"① 수집   {s['hours']}시간 창 · {len(items)}건"
                    + (f" · 응답 없음 {dead}" if dead else "")]}

# ── 13편 ② 선별 ──────────────────────────────────────────────────
class Pick(BaseModel):
    index: int = Field(description="후보 목록에서의 번호")
    reason: str = Field(description="왜 골랐는지 한 문장")
    event: str = Field(description="이 기사가 다루는 사건을 짧은 라벨로. 같은 사건이면 같은 라벨")

class Shortlist(BaseModel):
    picks: list[Pick]

BATCH, TARGET = 40, 5          # 예선 묶음 크기, 최종 발행 건수

CRITERIA = ("독자는 AI를 실제 제품에 붙이는 국내 개발팀입니다.\n"
            "- 이번 주 일하는 방식이 바뀔 만한가\n"
            "- 지금 쓰는 도구·API의 가격·한도·정책이 실제로 변했나\n"
            "버릴 것: 발표 예정·로드맵만 있는 것, MOU·투자유치·수상 같은 홍보성 소식")

def ask_picks(items, n):
    listing = "\n".join(f"{i}. [{it['source']}] {it['title']}" for i, it in enumerate(items))
    sys = (f"{CRITERIA}\n\n아래 목록에서 중요한 순서대로 {n}건을 고르세요.\n"
           "같은 사건을 다룬 기사에는 같은 event 라벨을 붙이세요.")
    out = client.chat.completions.parse(
        model="gpt-4.1-mini", temperature=0,
        messages=[{"role": "system", "content": sys},
                  {"role": "user", "content": listing}],
        response_format=Shortlist).choices[0].message.parsed
    return [p for p in out.picks if 0 <= p.index < len(items)]      # 없는 번호는 버린다

def select(s: dict) -> dict:                   # ② 중요도 선별
    items = s["collected"]
    survivors = []
    for i in range(0, len(items), BATCH):       # 예선 — 묶음마다 여덟 건
        chunk = items[i:i + BATCH]
        survivors += [chunk[p.index] for p in ask_picks(chunk, 8)]
    finals = ask_picks(survivors, TARGET)       # 본선 — 한 화면에 놓고 다섯 건
    return {"picked": [survivors[p.index] for p in finals],
            "log": [f"② 선별   {len(items)} → 예선 {len(survivors)} → {len(finals)}건"]}

# ── 8강 ③ 취재 (14편의 고친 버전) ────────────────────────────────
class Draft(BaseModel):
    headline: str = Field(description="20자 내외의 한국어 헤드라인")
    summary:  str = Field(description="세 문장 요약. ~합니다체, 과장 없이 건조하게")
    why:      str = Field(description="국내 개발팀에게 왜 중요한지 한 문장")

SYS = ("당신은 국내 개발팀을 위한 AI 뉴스레터 기자입니다.\n"
       "아래 기사 본문을 읽고 헤드라인·요약·왜 중요한지를 쓰세요.\n"
       "'주목된다·기대를 모은다' 같은 기자체 표현은 쓰지 마세요.")

class ReportIn(TypedDict):                     # 워커가 받는 것은 기사 하나뿐
    item: dict

def extract_body(url):
    d = trafilatura.fetch_url(url)
    return trafilatura.extract(d) if d else None

def draft(body):
    return client.chat.completions.parse(
        model="gpt-4.1-mini", temperature=0,
        messages=[{"role": "system", "content": SYS},
                  {"role": "user", "content": body[:6000]}],
        response_format=Draft).choices[0].message.parsed

def fan_report(s: dict):                      # 기사 수만큼 워커를 펼친다
    return [Send("report", {"item": it}) for it in s["picked"]] or "verify"   # ← 0건이면 verify로

def report(s: ReportIn) -> dict:               # ③ 취재 — 기사 한 건을 맡는다
    it = s["item"]
    body = extract_body(it["url"])
    if not body or len(body) < 600:            # ← 본문 기준선
        return {"drafted": [],
                "log": [f"③ 취재   제외 {it['source']} · 본문 {len(body or '')}자"]}
    d = draft(body)
    return {"drafted": [{**it, "body": body[:6000], **d.model_dump()}],
            "log": [f"③ 취재   {it['source']} · 본문 {len(body)}자"]}     # ← 성공해도 한 줄

# ── ④ ⑤ 아직 빈 노드 (9·10강에서 채운다) ─────────────────────────
def verify(s: dict) -> dict:
    return {"log": [f"④ 검수   {len(s['drafted'])}건 (빈 노드)"]}

def publish(s: dict) -> dict:
    return {"log": [f"⑤ 발행   {len(s['drafted'])}건 (빈 노드)"]}

def build():                                   # 엣지 한 줄이 팬아웃으로 바뀐다
    g = StateGraph(Brief)
    for name in ("collect", "select", "report", "verify", "publish"):
        g.add_node(name, globals()[name])
    g.add_edge(START, "collect")
    g.add_edge("collect", "select")
    g.add_conditional_edges("select", fan_report, ["report", "verify"])   # ← 고정 엣지 대신
    g.add_edge("report", "verify")
    g.add_edge("verify", "publish")
    g.add_edge("publish", END)
    return g

INIT = {"hours": 24, "collected": [], "picked": [], "drafted": [], "log": []}

def run():
    return build().compile().invoke(INIT)

out = run()
for line in out["log"]:
    print(line)

print()
for d in out["drafted"]:
    lang = "한" if re.search(r"[가-힣]", d["summary"]) else "영"
    print(f"[{lang}] {d['source']:<11}{d['headline']}")
