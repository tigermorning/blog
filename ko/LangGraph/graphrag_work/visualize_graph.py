# -*- coding: utf-8 -*-
"""LLM이 뽑은 삼중항(graph_triples_llm.json)을 Plotly로 인터랙티브 시각화.
matplotlib 정적 이미지 대신, 확대·이동·호버·범례 토글이 되는 HTML을 만든다."""
import json
import sys
import networkx as nx
import plotly.graph_objects as go

sys.stdout.reconfigure(encoding="utf-8")

TRIPLES_PATH = "output/graph_triples_llm.json"
OUT_PATH = "output/graph_visualization.html"

TYPE_COLORS = {
    "Person": "#4C78A8",
    "Film": "#F58518",
    "Award": "#E45756",
    "Location": "#72B7B2",
    "Genre": "#54A24B",
    "Organization": "#B279A2",
    "Theme": "#EECA3B",
}
REL_COLORS = {
    "WON_AWARD": "#E45756",
    "ACTED_IN": "#4C78A8",
    "DIRECTED": "#F58518",
    "PRODUCED_OR_DISTRIBUTED_BY": "#B279A2",
    "SET_IN": "#72B7B2",
    "HAS_GENRE": "#54A24B",
    "HAS_THEME": "#EECA3B",
}

with open(TRIPLES_PATH, encoding="utf-8") as f:
    triples = json.load(f)

G = nx.Graph()
for t in triples:
    G.add_node(t["h"], type=t["h_type"])
    G.add_node(t["t"], type=t["t_type"])
    G.add_edge(t["h"], t["t"], rel=t["r"])

print("노드 수:", G.number_of_nodes(), "/ 엣지 수:", G.number_of_edges())

pos = nx.spring_layout(G, k=0.35, iterations=40, seed=42)

# 관계(엣지)마다 하나의 트레이스 — 범례에서 켜고 끌 수 있다.
edge_traces = []
for rel, color in REL_COLORS.items():
    xs, ys = [], []
    for u, v, data in G.edges(data=True):
        if data.get("rel") != rel:
            continue
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        xs += [x0, x1, None]
        ys += [y0, y1, None]
    edge_traces.append(
        go.Scatter(
            x=xs, y=ys, mode="lines",
            line=dict(width=0.6, color=color),
            opacity=0.35,
            name=rel, legendgroup="edge-" + rel,
            hoverinfo="none",
        )
    )

# 노드는 타입마다 하나의 트레이스 — 크기는 연결 수(degree)로.
node_traces = []
for node_type, color in TYPE_COLORS.items():
    xs, ys, sizes, texts = [], [], [], []
    for n, data in G.nodes(data=True):
        if data.get("type") != node_type:
            continue
        x, y = pos[n]
        deg = G.degree(n)
        xs.append(x)
        ys.append(y)
        sizes.append(6 + deg * 1.5)
        texts.append(f"{n} ({node_type})<br>연결 {deg}개")
    node_traces.append(
        go.Scatter(
            x=xs, y=ys, mode="markers",
            marker=dict(size=sizes, color=color, line=dict(width=0.5, color="white")),
            name=node_type, legendgroup="node-" + node_type,
            text=texts, hoverinfo="text",
        )
    )

fig = go.Figure(data=edge_traces + node_traces)
fig.update_layout(
    title="영화 지식 그래프 — 노드 1,451개 · 엣지 2,383개 (범례 클릭으로 토글)",
    showlegend=True,
    hovermode="closest",
    xaxis=dict(showgrid=False, zeroline=False, visible=False),
    yaxis=dict(showgrid=False, zeroline=False, visible=False),
    plot_bgcolor="white",
    width=1100, height=850,
)

fig.write_html(OUT_PATH, include_plotlyjs=True)
print("저장:", OUT_PATH)
