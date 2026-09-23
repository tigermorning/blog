import networkx as nx

G = nx.DiGraph()
G.add_edge("봉준호", "기생충", relation="DIRECTED")
G.add_edge("송강호", "기생충", relation="ACTED_IN")
G.add_edge("송강호", "택시운전사", relation="ACTED_IN")

print("나가는 선 (송강호):", list(G.out_edges("송강호")))
print("들어오는 선 (기생충):", list(G.in_edges("기생충")))
print("successors(봉준호):", list(G.successors("봉준호")))
print("successors(기생충):", list(G.successors("기생충")))

U = G.to_undirected()          # 방향을 지운 사본
print("무방향 이웃(기생충):", list(U.neighbors("기생충")))
print("봉준호→택시운전사 경로(방향 지킴):", nx.has_path(G, "봉준호", "택시운전사"))
print("봉준호→택시운전사 경로(방향 무시):", nx.shortest_path(U, "봉준호", "택시운전사"))
