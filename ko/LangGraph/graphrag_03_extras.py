"""GraphRAG 실습 3 — 블로그 21·23편에 쓸 추가 측정.

1) 위키백과 《기생충》 앞 5,000자를 스키마 없이 / 스키마를 주고 추출해 개수 비교 (LLM 2회)
2) 규칙 엣지 할당량 면제를 켜고 끌 때 문항별 컨텍스트 재현율 차이 (LLM 0회)
graphrag_02_pipeline.py 를 섹션 10까지만 실행해 정의를 빌린다 (캐시가 있어야 한다).
실행: PYTHONIOENCODING=utf-8 python graphrag_03_extras.py
"""
import os, time
from collections import Counter

os.environ["STOP_AT_11"] = "1"
g = {"__name__": "pipeline", "__file__": os.path.join(os.path.dirname(os.path.abspath(__file__)), "graphrag_02_pipeline.py")}
try:
    exec(compile(open(g["__file__"], encoding="utf-8").read(), g["__file__"], "exec"), g)
except SystemExit:
    pass

print("\n" + "=" * 70 + "\nA. 스키마 없이 vs 스키마를 주고 — 《기생충》 위키 앞 5,000자\n" + "=" * 70)
import requests
from bs4 import BeautifulSoup
from langchain_core.documents import Document
from langchain_experimental.graph_transformers import LLMGraphTransformer

resp = requests.get("https://ko.wikipedia.org/wiki/기생충_(영화)",
                    headers={"User-Agent": "Mozilla/5.0 (compatible; tigermorning-blog-practice/1.0)"}, timeout=20)
resp.raise_for_status()
soup = BeautifulSoup(resp.text, "html.parser")
raw = "\n".join(p.get_text().strip() for p in soup.find("div", {"id": "mw-content-text"}).find_all("p") if p.get_text().strip())
print(f"본문 {len(raw):,}자 수집 → 앞 5,000자 사용")
docs = [Document(page_content=raw[:5000])]
llm = g["chat_model"]()

for name, kw in (("제약 없음", {}),
                 ("스키마 제어", {"allowed_nodes": ["영화", "사람", "영화제", "회사", "장르"],
                                "allowed_relationships": ["연출", "출연", "수상", "제작"]})):
    t0 = time.time()
    gd = LLMGraphTransformer(llm=llm, additional_instructions="한국어로 추출해줘", **kw).convert_to_graph_documents(docs)[0]
    rels = [(r.source.id, r.type, r.target.id) for r in gd.relationships]
    print(f"\n[{name}] 노드 {len(gd.nodes)} · 관계 {len(rels)} · {time.time()-t0:.0f}초")
    print("  관계 종류:", Counter(r for _, r, _ in rels).most_common(12))
    for h, r, t in rels[:25]:
        print(f"   ({h}) --[{r}]--> ({t})")

print("\n" + "=" * 70 + "\nB. 규칙 엣지 할당량 면제 on/off — 문항별 컨텍스트 재현율 (10, 200)\n" + "=" * 70)
QUESTIONS, collect_triples, entities_in = g["QUESTIONS"], g["collect_triples"], g["entities_in"]
norm = g["norm"]

def key(x):
    return (norm(x[0]), str(x[1]), norm(x[2]))

tot = {True: 0, False: 0}; need = 0
for q in QUESTIONS:
    if not q["reference_contexts"]:
        continue
    row = {}
    for exempt in (True, False):
        got = set()
        for t in collect_triples(entities_in(q["user_input"]), radius=2, exempt=exempt):
            k = key(t); got |= {k, (k[2], k[1], k[0])}
        row[exempt] = [tuple(c) for c in q["reference_contexts"] if key(c) not in got]
        tot[exempt] += len(q["reference_contexts"]) - len(row[exempt])
    need += len(q["reference_contexts"])
    if row[True] != row[False]:
        print(f"[{q['id']}] 면제 ON 놓침 {row[True]} | 면제 OFF 놓침 {row[False]}")
print(f"면제 ON {tot[True]}/{need} · 면제 OFF {tot[False]}/{need}")
