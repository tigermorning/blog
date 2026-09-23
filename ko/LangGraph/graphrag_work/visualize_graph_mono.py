# -*- coding: utf-8 -*-
"""pyvis(vis-network.js) 인터랙티브 버전. 어두운 배경 + 힘 기반 레이아웃은
그대로 두되, 색은 (사람/영화/... 타입이 아니라) 커뮤니티별로 칠해서
"관련 없는 덩어리"가 한눈에 갈라져 보이게 한다. 노드를 클릭하면 그
2단계 이웃만 밝게 남고 나머지는 흐려지고(select_menu), 위쪽 필터 메뉴에서
property=community, value=원하는 커뮤니티 id를 골라 그 커뮤니티만 남길
수도 있다(filter_menu)."""
import colorsys
import json
import networkx as nx
from pyvis.network import Network

TRIPLES_PATH = "output/graph_triples_llm.json"
COMMUNITIES_PATH = "output/community_reports.json"
OUT_PATH = "output/graph_visualization_mono.html"

MEMBER_KEYS = ["people", "films", "genres", "themes", "awards", "orgs", "locations"]

with open(TRIPLES_PATH, encoding="utf-8") as f:
    triples = json.load(f)
with open(COMMUNITIES_PATH, encoding="utf-8") as f:
    communities = json.load(f)

G = nx.Graph()
for t in triples:
    G.add_node(t["h"], type=t["h_type"])
    G.add_node(t["t"], type=t["t_type"])
    G.add_edge(t["h"], t["t"], rel=t["r"])

# community_reports.json의 people/films/... 목록은 "대표로 뽑은 몇 명"만
# 들어 있어서(전체 1,449개 중 394개만 걸림) 그래프 전체를 커버 못 한다.
# 그래서 커뮤니티 소속은 그래프 구조로 직접 다시 계산하고(루뱅 알고리즘,
# 100% 커버), 각 계산된 무리에 이름표를 붙일 때만 리포트의 대표 인물
# 목록과 겹치는 정도를 봐서 리포트 제목을 재사용한다.
member_sets = []
report_titles = []
for c in communities:
    members = set()
    for key in MEMBER_KEYS:
        members.update(c["profile"].get(key, []))
    member_sets.append(members)
    report_titles.append(c["title"])

detected = list(nx.community.louvain_communities(G, seed=42))

name_to_community = {}
community_titles = {}
for idx, comm in enumerate(detected):
    cid = f"G{idx}"
    best_i, best_overlap = None, 0
    for i, members in enumerate(member_sets):
        overlap = len(comm & members)
        if overlap > best_overlap:
            best_i, best_overlap = i, overlap
    if best_i is not None and best_overlap / len(comm) >= 0.15:
        community_titles[cid] = f"{report_titles[best_i]} (컴퓨터가 다시 나눈 {len(comm)}개 무리)"
    else:
        community_titles[cid] = f"이름 없는 무리 {idx} ({len(comm)}개)"
    for name in comm:
        name_to_community[name] = cid

# 커뮤니티마다 색상을 하나씩 — 어두운 배경 위에서 잘 보이게 채도·명도 고정.
ids = list(community_titles.keys())
palette = {}
for i, cid in enumerate(ids):
    hue = i / max(len(ids), 1)
    r, g, b = colorsys.hls_to_rgb(hue, 0.62, 0.55)
    palette[cid] = "#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255))
NO_COMMUNITY_COLOR = "#555555"

net = Network(
    height="850px", width="100%",
    bgcolor="#111111", font_color="#eaeaea",
    notebook=False, cdn_resources="in_line",
    select_menu=True, filter_menu=True,
)

for n, data in G.nodes(data=True):
    node_type = data.get("type", "")
    deg = G.degree(n)
    cid = name_to_community.get(n)
    ctitle = community_titles.get(cid, "미분류")
    color = palette.get(cid, NO_COMMUNITY_COLOR)
    net.add_node(
        n,
        label=n,
        title=f"{n} ({node_type}) · 연결 {deg}개<br>커뮤니티 {cid or '-'}: {ctitle}",
        color=color,
        community=cid or "미분류",
        size=8 + deg * 0.9,
        font={"color": "#eaeaea", "size": 12},
    )

for u, v, data in G.edges(data=True):
    net.add_edge(u, v, title=data.get("rel", ""), color="#3a3a3a", width=0.6)

net.set_options("""
{
  "physics": {
    "forceAtlas2Based": {
      "gravitationalConstant": -60,
      "centralGravity": 0.01,
      "springLength": 90,
      "springConstant": 0.06
    },
    "solver": "forceAtlas2Based",
    "stabilization": { "iterations": 200 }
  },
  "interaction": {
    "hover": true,
    "zoomView": true,
    "dragView": true,
    "tooltipDelay": 100
  }
}
""")

html = net.generate_html(notebook=False)

# 일부 임베드형 뷰어(예: 데스크톱 앱의 내장 미리보기)는 console.info 등을
# 아예 안 만들어 둬서, vis-network.js 내부의 폴백 레이아웃 코드가
# console.info를 호출하는 순간 TypeError로 죽어 물리 시뮬레이션이
# 0%에서 멈춘다. head 맨 앞에 빠진 console 메서드를 채워 넣는다.
console_shim = (
    "<script>(function(){var m=['log','info','warn','error','debug'];"
    "window.console=window.console||{};"
    "m.forEach(function(k){if(typeof console[k]!=='function'){console[k]=function(){};}});"
    "})();</script>"
)
html = html.replace("<head>", "<head>\n" + console_shim, 1)

with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write(html)

matched = sum(1 for n in G.nodes if n in name_to_community)
print("saved:", OUT_PATH)
print("nodes:", G.number_of_nodes(), "matched to a community:", matched, "communities:", len(ids))
