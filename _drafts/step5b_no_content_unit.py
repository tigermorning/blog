import io, os, zipfile, urllib.request
from pathlib import Path

DATA_URL = ("https://raw.githubusercontent.com/88chacha/deepresearch-agent-data/"
            "main/data/deepresearch_d48_data.zip")

if not Path("corpus.json").exists():
    with urllib.request.urlopen(DATA_URL, timeout=60) as r:
        zipfile.ZipFile(io.BytesIO(r.read())).extractall(".")

import json, operator, re, time
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv(Path.home() / "Documents" / "openai_key.env")
assert os.getenv("OPENAI_API_KEY", "").startswith("sk-"), "키를 못 찾았다"

CORPUS = json.loads(Path("corpus.json").read_text(encoding="utf-8"))
DOCS, LINKS = CORPUS["docs"], CORPUS["links"]

class Research(TypedDict):
    question: str
    plan:     dict
    sections: Annotated[list, operator.add]
    visited:  Annotated[list, operator.add]
    report:   str
    metrics:  dict
    log:      Annotated[list, operator.add]
    task:     dict
    prior:    dict

# ---- 5강: ① 기획 노드 (강의 코드 그대로 옮김) ----
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, timeout=60, max_retries=0)

설정 = {
    "절수": 4, "절예산": 3, "최대바퀴": 2,
    "역할": True, "배정": True, "구역": True, "재위임": True,
}

ROSTER = {
    "큰그림 담당": "주제의 윤곽을 잡고 핵심 사건과 인물을 간추린다",
    "시간순 담당": "사건을 일어난 순서대로 늘어놓고 언제였는지를 못 박는다",
    "인물 담당":   "한 사람이 무엇에 관여했고 어떤 일을 겪었는지 좇는다",
    "원인 담당":   "무엇이 무엇으로 이어졌는지 자료에 적힌 대로 따라간다",
    "비교 담당":   "둘 이상을 같은 잣대로 견주어 어디가 다른지 정리한다",
}

COST = {"calls": 0, "sub_chars": 0, "coord_chars": 0}

일시적오류 = ("RateLimit", "APIConnection", "Timeout", "InternalServer")

def ask(system: str, user: str, coord: bool = False, cap: int = 60000) -> str:
    body = user[:cap]
    COST["calls"] += 1
    COST["coord_chars" if coord else "sub_chars"] += len(body)
    msgs = [{"role": "system", "content": system}, {"role": "user", "content": body}]
    for 시도 in range(3):
        try:
            return llm.invoke(msgs).content
        except Exception as e:
            잠깐뿐 = any(k in type(e).__name__ for k in 일시적오류)
            if 시도 == 2 or not 잠깐뿐:
                raise
            time.sleep(2 ** 시도)

def jload(raw: str, default):
    try:
        m = re.search(r"\[.*\]" if isinstance(default, list) else r"\{.*\}", raw, re.S)
        return json.loads(m.group(0))
    except Exception:
        return default

CARD = 250

def cards() -> str:
    """34건 전체를 제목 + 앞 250자로 요약한 '카드 목록'. 전체의 1.9% 다."""
    return "\n".join(f"- {t}: {re.sub(chr(10), ' ', v[:CARD])}" for t, v in DOCS.items())

def plan(s: dict) -> dict:
    titles = cards()
    roster = "\n".join(f"- {k}: {v}" for k, v in ROSTER.items())
    raw = ask(
        "너는 리서치 팀의 코디네이터다. 아래 질문에 답하는 보고서의 목차를 짜고, 각 절을 조사관 "
        f"한 명에게 맡긴다. 절은 최대 {설정['절수']}개.\n"
        "절마다 그 절을 쓰는 데 가장 먼저 읽어야 할 문서를 문서 목록에서 하나 배정하라. "
        "절끼리 다른 문서를 주어라.\n"
        f"절의 성격에 맞는 조사관을 명단에서 골라 붙여라.\n[조사관 명단]\n{roster}\n"
        'JSON으로만: {"제목":"보고서 제목","목차":[{"절":"절 제목","지시":"이 절에서 '
        '밝혀야 할 것 한두 문장","역할":"명단에 있는 이름 그대로","시작문서":"목록에 있는 제목"}]}',
        f"[질문] {s['question']}\n[읽을 수 있는 문서 카드]\n{titles}", coord=True)
    obj = jload(raw, {})
    toc = []
    taken = set()
    for item in obj.get("목차", [])[:설정["절수"]]:
        role, seed = item.get("역할", ""), str(item.get("시작문서") or "")
        if not 설정["배정"] or seed not in DOCS or seed in taken:
            seed = "" if not 설정["배정"] else next((t for t in DOCS if t not in taken), "")
        if seed:
            taken.add(seed)
        toc.append({"절": item.get("절", "무제"),
                    "지시": item.get("지시", s["question"]),
                    "역할": role if (설정["역할"] and role in ROSTER) else "큰그림 담당",
                    "시작문서": seed, "예산": 설정["절예산"]})
    if not toc:
        toc = [{"절": "개요", "지시": s["question"], "역할": "큰그림 담당",
                "시작문서": "", "예산": 설정["절예산"]}]
    p = {"제목": obj.get("제목", s["question"]), "목차": toc,
         "배치": list(range(len(toc))), "바퀴": 1}
    seeds = " · ".join(f"{t['역할']}→«{t['시작문서'] or '자율'}»" for t in toc)
    return {"plan": p,
            "log": [f"① 기획   목차 {len(toc)}절 · {seeds}"]}

# ---- 나머지는 2강 그대로 빈 노드 ----
def dispatch(s: dict) -> dict:
    return {"log": [f"② 배치   서브에이전트 {len(s['plan']['배치'])}명 파견 (빈 노드)"]}

def researcher(s: dict) -> dict:
    return {"sections": [{"번호": 0, "절": s["task"]["절"], "역할": s["task"]["역할"],
                          "본문": "", "읽은문서": [], "메모": [], "인용": [],
                          "허위인용": [], "충분": True, "부족": ""}],
            "visited": [],
            "log": [f"   ③ 조사관   «{s['task']['절']}» 0건 읽고 0자 (빈 노드)"]}

def 절모음(s: dict) -> dict:
    return {sec["절"]: sec for sec in s["sections"]}

def review(s: dict) -> dict:
    return {"plan": {**s["plan"], "배치": []},
            "log": [f"④ 점검   {len(절모음(s))}절 중 빈 칸 0개 (빈 노드)"]}

def synthesize(s: dict) -> dict:
    return {"report": "", "log": [f"⑤ 종합   {len(절모음(s))}절 → 보고서 0자 (빈 노드)"]}

def evaluate(s: dict) -> dict:
    return {"metrics": {}, "log": ["⑥ 평가   지표 0개 (빈 노드)"]}

def fanout(s: dict):
    idxs = s["plan"].get("배치", [])
    if not idxs:
        return "review"
    return [Send("researcher", {"question": s["question"],
                                "task": s["plan"]["목차"][i], "prior": {}})
            for i in idxs]

def route(s: dict) -> str:
    return "more" if s["plan"].get("배치") else "done"

NODES = ("plan", "dispatch", "researcher", "review", "synthesize", "evaluate")

def build():
    g = StateGraph(Research)
    for name in NODES:
        g.add_node(name, globals()[name])
    g.add_edge(START, "plan")
    g.add_edge("plan", "dispatch")
    g.add_conditional_edges("dispatch", lambda s: globals()["fanout"](s),
                            ["researcher", "review"])
    g.add_edge("researcher", "review")
    g.add_conditional_edges("review", lambda s: globals()["route"](s),
                            {"more": "dispatch", "done": "synthesize"})
    g.add_edge("synthesize", "evaluate")
    g.add_edge("evaluate", END)
    return g

QUESTION = "1894년에 일어난 주요 사건들은 무엇이고 각각의 원인은 무엇인가?"
INIT = {"question": QUESTION, "plan": {}, "sections": [], "visited": [],
        "report": "", "metrics": {}, "log": [], "task": {}, "prior": {}}

def run():
    return build().compile().invoke(INIT)

if __name__ == "__main__":
    print(f"코퍼스 {len(DOCS)}건 · {sum(len(v) for v in DOCS.values()):,}자\n")
    result = run()
    for line in result["log"]:
        print(line)
    print(f"\nCOST: {COST}")
    print("\n목차 상세:")
    for t in result["plan"]["목차"]:
        print(f"  절={t['절']!r} 역할={t['역할']!r} 시작문서={t['시작문서']!r}")
