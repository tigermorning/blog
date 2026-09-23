import io, zipfile, urllib.request
from pathlib import Path

DATA_URL = ("https://raw.githubusercontent.com/88chacha/deepresearch-agent-data/"
            "main/data/deepresearch_d48_data.zip")

if not Path("corpus.json").exists():
    with urllib.request.urlopen(DATA_URL, timeout=60) as r:
        zipfile.ZipFile(io.BytesIO(r.read())).extractall(".")

import json, operator
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

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

def plan(s: dict) -> dict:
    빈절 = {"절": "(빈 절)", "지시": s["question"], "역할": "큰그림 담당",
            "시작문서": "", "예산": 0}
    return {"plan": {"제목": s["question"], "목차": [빈절], "배치": [0], "바퀴": 1},
            "log": ["① 기획   목차 1절 (빈 노드)"]}

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

print(f"코퍼스 {len(DOCS)}건 · {sum(len(v) for v in DOCS.values()):,}자\n")
for line in run()["log"]:
    print(line)
