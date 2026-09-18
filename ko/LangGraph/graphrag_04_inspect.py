"""21편 점검 절용 — 병합 그래프의 관계 분포, 속성 허브, 연결 요소 크기 (LLM 0회, 캐시 필요)."""
import os
from collections import Counter
os.environ["STOP_AT_11"] = "1"
g = {"__name__": "pipeline", "__file__": os.path.join(os.path.dirname(os.path.abspath(__file__)), "graphrag_02_pipeline.py")}
try:
    exec(compile(open(g["__file__"], encoding="utf-8").read(), g["__file__"], "exec"), g)
except SystemExit:
    pass
G = g["G"]; import networkx as nx
print("\n### 병합 그래프 관계:", Counter(d["relation"] for *_, d in G.edges(data=True)).most_common())
print("### LLM만 관계:", Counter(d["relation"] for *_, d in g["G_llm"].edges(data=True)).most_common())
print("### 규칙만 관계:", Counter(d["relation"] for *_, d in g["G_rule"].edges(data=True)).most_common())
attr = [(n, G.degree(n), G.nodes[n].get("type")) for n in G if G.nodes[n].get("type") in ("Genre", "Theme", "Location")]
print("### 속성 허브 상위:", sorted(attr, key=lambda x: -x[1])[:6])
comps = sorted(nx.weakly_connected_components(G), key=len, reverse=True)
print("### 연결 요소 크기:", [len(c) for c in comps])
for c in comps[1:4]:
    print("   작은 덩어리 예:", sorted(c)[:6])
print("### 봉준호→기생충:", G.get_edge_data("봉준호", "기생충"), "| 한진원→기생충:", G.get_edge_data("한진원", "기생충"))
