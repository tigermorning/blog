"""GraphRAG 실습 2 — 추출 → 정규화·보강 → 점검 → 커뮤니티 → LangGraph 에이전트 → 골든셋 채점.

키: C:/Users/user/Documents/openai_key.env 의 OPENAI_API_KEY (저장소 밖)
캐시: graphrag_work/output/ (추출·보고서·채점 결과. 다시 돌리면 LLM 을 부르지 않는다)
실행: PYTHONIOENCODING=utf-8 python graphrag_02_pipeline.py
"""
import os, re, glob, json, time, random
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from typing import TypedDict, List, Dict, Any, Literal

import networkx as nx
import pandas as pd
from dotenv import load_dotenv
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.retrievers import BM25Retriever
from langchain_openai import ChatOpenAI
from langchain_experimental.graph_transformers import LLMGraphTransformer
from networkx.algorithms import community as nxc
from langgraph.graph import StateGraph, START, END

load_dotenv(os.path.join(os.path.expanduser("~"), "Documents", "openai_key.env"))
assert os.getenv("OPENAI_API_KEY"), "키 없음"

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graphrag_work")
DOC_DIR = os.path.join(BASE, "input", "cinephile_kb_80", "docs")
GOLD_PATH = os.path.join(BASE, "input", "cinephile_goldenset.json")
OUT_DIR = os.path.join(BASE, "output")
os.makedirs(OUT_DIR, exist_ok=True)

CHAT_MODEL, JUDGE_MODEL = "gpt-4.1-mini", "gpt-4.1"
SEED, MAX_WORKERS = 42, 8
random.seed(SEED)

USAGE = Counter()  # 모델별 토큰 사용량 (비용 확인용)

def chat_model(model=None, **kw):
    return ChatOpenAI(model=model or CHAT_MODEL, temperature=0, timeout=120, max_retries=3, **kw)

def track(msg, model):
    u = getattr(msg, "usage_metadata", None) or {}
    USAGE[(model, "in")] += u.get("input_tokens", 0)
    USAGE[(model, "out")] += u.get("output_tokens", 0)
    return msg

def section(t):
    print("\n" + "=" * 70 + f"\n{t}\n" + "=" * 70)

# ── 코퍼스 · 골든셋 ─────────────────────────────────────────────────────
DOCS = {}
for path in sorted(glob.glob(os.path.join(DOC_DIR, "*.md"))):
    DOCS[os.path.splitext(os.path.basename(path))[0].replace("_", " ")] = open(path, encoding="utf-8").read()
MANIFEST = json.load(open(os.path.join(os.path.dirname(DOC_DIR), "manifest.json"), encoding="utf-8"))
NTYPE = {d["title"]: d["type"] for d in MANIFEST["docs"]}

def categories_of(text):
    m = re.search(r"^분류:\s*(.+)$", text, flags=re.M)
    return [c.strip() for c in m.group(1).split(",")] if m else []
CATS = {t: categories_of(x) for t, x in DOCS.items()}
QUESTIONS = json.load(open(GOLD_PATH, encoding="utf-8"))["items"]

# ═════ 섹션 6: 추출 ═════════════════════════════════════════════════════
section("6. 코퍼스 전체 추출")
NODE_TYPES = ["Film", "Person", "Genre", "Theme", "Award", "Organization", "Location"]
REL_TRIPLES = [
    ("Person", "DIRECTED", "Film"), ("Person", "ACTED_IN", "Film"),
    ("Film", "HAS_GENRE", "Genre"), ("Film", "HAS_THEME", "Theme"),
    ("Film", "SET_IN", "Location"), ("Film", "WON_AWARD", "Award"),
    ("Person", "WON_AWARD", "Award"), ("Film", "PRODUCED_OR_DISTRIBUTED_BY", "Organization"),
]
EDGE_PROPS = ["year", "category", "work", "character"]
NODE_PROPS = ["release_year", "birth_year", "country"]
REL_NAMES = [r for _, r, _ in REL_TRIPLES]
EXPECT_TAIL = {r: t for _, r, t in REL_TRIPLES}
EXPECT_HEAD = {}
for h, r, _ in REL_TRIPLES:
    EXPECT_HEAD.setdefault(r, set()).add(h)

EXTRA = """이 문서는 한국 영화 위키백과 글이다. 다음을 지켜라.

1. 개체 이름은 원문 표기 그대로 쓴다. 《》 같은 기호와 조사는 뗀다. ('《기생충》은' -> '기생충')
2. '영화', '감독', '배우', '작품', '수상' 같은 일반명사는 개체로 만들지 마라.
3. 문서에 적혀 있지 않은 것은 만들지 마라. 감독이 안 적혀 있으면 DIRECTED 를 만들지 않는다.
4. Award 노드는 시상식/영화제 이름만 쓴다. (대종상, 청룡영화상, 칸 영화제)
   부문 이름을 Award 노드로 만들지 마라. 부문은 category 속성에 넣는다.
   '송강호가 기생충으로 대종상 남우주연상을 받았다'
     -> 송강호 -WON_AWARD-> 대종상 { category: "남우주연상", work: "기생충" }
5. TV 드라마와 예능은 이 스키마에 없다. 영화만 Film 으로 뽑는다.
6. ACTED_IN 에는 character(배역 이름)를 채운다.
7. 장르(Genre)는 '스릴러', '코미디' 처럼 짧게. 소재(Theme)는 '가난', '복수' 처럼 짧게.
8. SET_IN 의 도착 노드는 작품의 배경이 되는 장소다. ('조선', '서울특별시', '광주')
   연도는 Location 으로 만들지 마라.
9. 글 맨 앞의 [문서 제목] 이 이 문서가 다루는 대상이다.
   배역 목록처럼 작품 이름이 본문에 없는 부분에서는, 그 배역들이 [문서 제목] 의 작품에 속한다.
   본문에 근거가 없는 다른 작품을 임의로 끌어오지 마라."""

ex_splitter = RecursiveCharacterTextSplitter(chunk_size=2400, chunk_overlap=200)
TASKS = []
for title in DOCS:
    ntype = NTYPE.get(title, "기타")
    for i, piece in enumerate(ex_splitter.split_text(DOCS[title][:6000])):
        TASKS.append(Document(page_content=f"[문서 제목] {title}\n[문서 유형] {ntype}\n\n{piece}",
                              metadata={"doc": title, "chunk": i, "ntype": ntype}))
print(f"청크 {len(TASKS)}개")

CACHE_PATH = os.path.join(OUT_DIR, "graph_triples_llm.json")
if os.getenv("SMOKE"):  # 청크 2개로 스키마·지침이 먹는지만 확인하고 끝낸다
    TASKS = [t for t in TASKS if t.metadata["doc"] == "기생충 (영화)"][:2]
    CACHE_PATH = os.path.join(OUT_DIR, "smoke_triples.json")
transformer = LLMGraphTransformer(
    llm=chat_model(), allowed_nodes=NODE_TYPES, allowed_relationships=REL_TRIPLES,
    node_properties=NODE_PROPS, relationship_properties=EDGE_PROPS, strict_mode=True,
    additional_instructions=EXTRA.replace("{", "{{").replace("}", "}}"))

EXTRACT_TOKENS = Counter()

def extract_one(task):
    from langchain_community.callbacks import get_openai_callback
    try:
        with get_openai_callback() as cb:  # 스레드마다 따로 센다 (콜백은 스레드를 넘지 않는다)
            gdocs = transformer.convert_to_graph_documents([task])
        EXTRACT_TOKENS["in"] += cb.prompt_tokens
        EXTRACT_TOKENS["out"] += cb.completion_tokens
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}", "doc": task.metadata["doc"], "triples": []}
    out = []
    for gd in gdocs:
        for r in gd.relationships:
            out.append({"h": str(r.source.id), "h_type": r.source.type, "r": r.type,
                        "t": str(r.target.id), "t_type": r.target.type,
                        "props": {k: v for k, v in (r.properties or {}).items() if v},
                        "source": task.metadata["doc"], "origin": "llm"})
    return {"error": None, "doc": task.metadata["doc"], "triples": out}

if os.path.exists(CACHE_PATH):
    RAW_TRIPLES = json.load(open(CACHE_PATH, encoding="utf-8"))
    print(f"캐시 로드 — 삼중항 {len(RAW_TRIPLES)}개")
else:
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        results = list(ex.map(extract_one, TASKS))
    RAW_TRIPLES = [t for r in results for t in r["triples"]]
    errors = [r for r in results if r["error"]]
    print(f"추출 {time.time()-t0:.0f}초 — 삼중항 {len(RAW_TRIPLES)}개, 실패 청크 {len(errors)}개")
    print(f"토큰: 입력 {EXTRACT_TOKENS["in"]:,} · 출력 {EXTRACT_TOKENS["out"]:,}")
    if errors:
        print("  실패 예:", errors[0]["error"][:150])
    json.dump(RAW_TRIPLES, open(CACHE_PATH, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({"secs": round(time.time()-t0), "in": EXTRACT_TOKENS["in"], "out": EXTRACT_TOKENS["out"],
               "triples": len(RAW_TRIPLES), "errors": len(errors)},
              open(os.path.join(OUT_DIR, "extract_stats.json"), "w"), indent=1)
print("관계별:", Counter(t["r"] for t in RAW_TRIPLES).most_common())
print("── 《기생충》 문서에서 나온 삼중항 ──")
for t in [x for x in RAW_TRIPLES if x["source"].startswith("기생충")][:14]:
    print(f"  ({t['h']}) --[{t['r']}]--> ({t['t']}) {t['props'] or ''}")
if os.getenv("SMOKE"):
    raise SystemExit

# ═════ 섹션 7: 정규화 · 보강 ════════════════════════════════════════════
section("7. 정규화 · 위키 분류 보강")
PAREN = re.compile(r"\s*\([^)]*\)\s*$")
BRACKET = re.compile(r"[《》〈〉<>\"']")
JOSA = re.compile(r"^([《〈\"'].+[》〉\"'])[은는이가을를의]$")
CAT_JOSA = re.compile(r"[은는이가을를의]$")
YEAR = re.compile(r"^\d{3,4}\s*년?$")
GENERIC = {"영화", "감독", "배우", "작품", "수상", "출연", "장르", "사람", "영화제",
           "한국", "대한민국", "한국 영화", "영화감독", "주연", "조연", "제작사", "배급사"}

def clean_name(s):
    s = JOSA.sub(r"\1", str(s).strip())
    s = BRACKET.sub("", s).strip()
    return re.sub(r"\s+", " ", s)

def norm(s):
    return re.sub(r"[\s·・\-_]", "", PAREN.sub("", clean_name(s))).lower()

FAMILY = {"Film": "entity", "Person": "entity", "Organization": "entity", "Award": "entity",
          "Genre": "attr", "Theme": "attr", "Location": "attr"}

def is_junk(name, ntype):
    s = clean_name(name)
    if len(s) < 2 or s in GENERIC or FAMILY.get(ntype) is None:
        return True
    if YEAR.match(s) and FAMILY[ntype] == "attr":
        return True
    return False

for s in ["《기생충》은", "기생충 (영화)", "괴물 (2006년 영화)", "황금 종려상", "황금종려상", "2019년"]:
    print(f"  {s:18s} → clean={clean_name(s):16s} norm={norm(s)}")

def normalize_triples(raw):
    type_votes, surface_votes = defaultdict(Counter), defaultdict(Counter)
    for t in raw:
        for name, ntype in ((t["h"], t["h_type"]), (t["t"], t["t_type"])):
            if is_junk(name, ntype):
                continue
            key = (FAMILY[ntype], norm(name))
            type_votes[key][ntype] += 1
            surface_votes[key][clean_name(name)] += 1
    canon, canon_type, taken = {}, {}, {}
    for key in sorted(surface_votes, key=lambda k: -sum(surface_votes[k].values())):
        sc = surface_votes[key]
        ntype = type_votes[key].most_common(1)[0][0]
        for cand in sorted(sc, key=lambda x: (-sc[x], len(x))):
            if cand not in taken:
                best = cand; break
        else:
            best = f"{max(sc, key=sc.get)} ({ntype})"
        taken[best] = key; canon[key] = best; canon_type[best] = ntype
    out, report = [], Counter()
    for t in raw:
        if is_junk(t["h"], t["h_type"]) or is_junk(t["t"], t["t_type"]):
            report["개체 아님(일반명사·연도)"] += 1; continue
        if t["r"] not in EXPECT_TAIL:
            report["스키마에 없는 관계"] += 1; continue
        h = canon[(FAMILY[t["h_type"]], norm(t["h"]))]
        tt = canon[(FAMILY[t["t_type"]], norm(t["t"]))]
        if norm(h) == norm(tt) and canon_type[h] == canon_type[tt]:
            report["자기 자신을 가리킴"] += 1; continue
        if canon_type[tt] != EXPECT_TAIL[t["r"]]:
            report[f"도착 타입 불일치({t['r']})"] += 1; continue
        if canon_type[h] not in EXPECT_HEAD[t["r"]]:
            report[f"출발 타입 불일치({t['r']})"] += 1; continue
        out.append({"h": h, "r": t["r"], "t": tt, "h_type": canon_type[h], "t_type": canon_type[tt],
                    "props": t.get("props", {}), "source": t["source"], "origin": t.get("origin", "llm")})
        report["통과"] += 1
    return out, report, canon, surface_votes

def dejosa(s):
    return CAT_JOSA.sub("", clean_name(s)).strip()

CAT_RULES = [
    (re.compile(r"^(.+?)\s*감독 영화$"), "Film", lambda t, m: (dejosa(m.group(1)), "Person", "DIRECTED", t, "Film")),
    (re.compile(r"^대한민국의 (.+?) 영화$"), "Film", lambda t, m: (t, "Film", "HAS_GENRE", dejosa(m.group(1)), "Genre")),
    (re.compile(r"^(.+?) 배경으로 한 영화$"), "Film", lambda t, m: (t, "Film", "SET_IN", dejosa(m.group(1)), "Location")),
    (re.compile(r"^(.+?) 소재로 한 영화$"), "Film", lambda t, m: (t, "Film", "HAS_THEME", dejosa(m.group(1)), "Theme")),
    (re.compile(r"^(.+?) 영화$"), "Film", lambda t, m: (t, "Film", "PRODUCED_OR_DISTRIBUTED_BY", dejosa(m.group(1)), "Organization")),
]
AWARD_NAMES = sorted(
    {t for t, k in NTYPE.items() if k == "Award"} |
    {"대종상", "청룡영화상", "백상예술대상", "부일영화상", "춘사영화상", "황금촬영상",
     "대한민국 영화대상", "디렉터스 컷 시상식", "맥스무비 최고의 영화상", "올해의 영화상",
     "한국영화평론가협회상", "칸 영화제", "베를린 국제 영화제", "베네치아 국제 영화제",
     "아카데미상", "골든 글로브상", "청룡영화제", "들꽃영화상"}, key=len, reverse=True)

def award_in(text):
    return next((a for a in AWARD_NAMES if a in text), None)

ORG_HINT = re.compile(r"(엔터테인먼트|필름|픽처스|미디어|스튜디오|CJ|NEW|쇼박스|롯데|워너|폭스|유니버설|소니|NEON|HBO|CGV|ENM|E&M)")

def build_rule_triples():
    tri = []
    for title, cs in CATS.items():
        kind = NTYPE.get(title)
        for c in cs:
            if kind == "Person" and c.endswith(("수상자", "수훈자")):
                aw = award_in(c)
                if aw:
                    cat = c.replace(aw, "").replace("수상자", "").replace("영화부문", "").strip()
                    tri.append({"h": title, "h_type": "Person", "r": "WON_AWARD", "t": aw, "t_type": "Award",
                                "props": {"category": cat} if cat else {}, "source": title, "origin": "rule"})
                continue
            if kind == "Film" and c.endswith("수상작"):
                aw = award_in(c) or dejosa(c[:-len("수상작")])
                if aw and not is_junk(aw, "Award"):
                    tri.append({"h": title, "h_type": "Film", "r": "WON_AWARD", "t": aw, "t_type": "Award",
                                "props": {}, "source": title, "origin": "rule"})
                continue
            for pat, want_kind, fn in CAT_RULES:
                if kind != want_kind:
                    continue
                m = pat.match(c)
                if not m:
                    continue
                h, ht, r, t, tt = fn(title, m)
                if r == "PRODUCED_OR_DISTRIBUTED_BY" and not ORG_HINT.search(t):
                    break
                if not h or not t or is_junk(h, ht) or is_junk(t, tt):
                    break
                tri.append({"h": h, "h_type": ht, "r": r, "t": t, "t_type": tt,
                            "props": {}, "source": title, "origin": "rule"})
                break
    return tri

RAW_RULE = build_rule_triples()

def build_graph(triple_sets):
    G = nx.DiGraph()
    for triples, origin, base_conf in triple_sets:
        for t in triples:
            h, r, tail = t["h"], t["r"], t["t"]
            G.add_node(h, type=t["h_type"]); G.add_node(tail, type=t["t_type"])
            if G.has_edge(h, tail) and G[h][tail]["relation"] == r:
                e = G[h][tail]
                e["count"] += 1
                e["confidence"] = min(1.0, e["confidence"] + 0.05)
                e["sources"] = sorted(set(e["sources"]) | {t["source"]})
                if origin == "rule":
                    e["origin"], e["confidence"] = "rule+llm", 1.0
            elif G.has_edge(h, tail):
                continue
            else:
                G.add_edge(h, tail, relation=r, origin=origin, confidence=base_conf,
                           count=1, sources=[t["source"]], props=t.get("props", {}))
    return G

_, REPORT_LLM_ONLY, _, _ = normalize_triples(RAW_TRIPLES)
print("── 정규화 리포트 (LLM 추출분) ──")
for k, v in REPORT_LLM_ONLY.most_common():
    print(f"  {k:28s} {v:5d}")

TRI_ALL, REPORT_ALL, CANON, SURFACES = normalize_triples(RAW_TRIPLES + RAW_RULE)
TRI_LLM = [t for t in TRI_ALL if t["origin"] == "llm"]
TRI_RULE = [t for t in TRI_ALL if t["origin"] == "rule"]
print(f"\n합쳐서 정규화 → 삼중항 {len(TRI_ALL)}개 (LLM {len(TRI_LLM)} · 규칙 {len(TRI_RULE)})")
print("규칙 관계별:", Counter(t["r"] for t in TRI_RULE).most_common())
print("규칙 예시:")
for t in TRI_RULE[:8]:
    print(f"  ({t['h']}) --[{t['r']}]--> ({t['t']}) {t['props'] or ''}")

nodes_before = len({x for t in RAW_TRIPLES for x in (t["h"], t["t"])})
print(f"\n고유 노드(LLM 원본) {nodes_before}")
print("── 합쳐진 표기 ──")
merged = sorted([(k, sc) for k, sc in SURFACES.items() if len(sc) > 1], key=lambda kv: -sum(kv[1].values()))
for key, sc in merged[:12]:
    print(f"  '{CANON[key]}' ← {list(sc)}")
print(f"  (여러 표기가 합쳐진 노드 {len(merged)}개)")

G_llm = build_graph([(TRI_LLM, "llm", 0.7)])
G_rule = build_graph([(TRI_RULE, "rule", 1.0)])
G = build_graph([(TRI_LLM, "llm", 0.7), (TRI_RULE, "rule", 1.0)])
G.remove_nodes_from([n for n, d in G.degree if d == 0])
for name, g in (("LLM", G_llm), ("규칙", G_rule), ("병합", G)):
    print(f"{name} 그래프 — 노드 {g.number_of_nodes()} · 엣지 {g.number_of_edges()}")
print("엣지 출처:", Counter(d["origin"] for _, _, d in G.edges(data=True)).most_common())

def has_triple(graph, h, r, t):
    hk, tk = norm(h), norm(t)
    for u, v, d in graph.edges(data=True):
        if d["relation"] == r and ((norm(u) == hk and norm(v) == tk) or (norm(u) == tk and norm(v) == hk)):
            return True
    return False

def coverage(graph):
    hit, need, miss = 0, 0, []
    for q in QUESTIONS:
        for c in q["reference_contexts"]:
            need += 1
            if has_triple(graph, c[0], c[1], c[2]):
                hit += 1
            else:
                miss.append((q["id"], tuple(c)))
    return hit, need, miss

print("\n── 기준 삼중항 커버리지 ──")
for name, g in (("LLM 추출만", G_llm), ("위키 분류 규칙만", G_rule), ("병합", G)):
    hit, need, _ = coverage(g)
    print(f"  {name:10s} {hit}/{need} ({hit/need*100:.0f}%)")
rows = []
for name, g in (("LLM", G_llm), ("규칙", G_rule), ("병합", G)):
    row = {"방식": name}
    for rel in REL_NAMES:
        want = [c for q in QUESTIONS for c in q["reference_contexts"] if c[1] == rel]
        if want:
            row[rel] = f"{sum(has_triple(g, *c) for c in want)}/{len(want)}"
    rows.append(row)
print(pd.DataFrame(rows).fillna("-").to_string(index=False))
_, _, MISS = coverage(G)
print("병합이 놓친 것:", MISS)

# ═════ 섹션 8: 점검 ═════════════════════════════════════════════════════
section("8. 그래프 점검")
print("타입:", Counter(d.get("type") for _, d in G.nodes(data=True)).most_common())
print("── 허브 상위 12 ──")
for n, deg in sorted(G.degree, key=lambda x: -x[1])[:12]:
    rels = Counter(d["relation"] for _, _, d in list(G.out_edges(n, data=True)) + list(G.in_edges(n, data=True)))
    print(f"  {deg:4d} [{G.nodes[n].get('type','?'):12s}] {str(n)[:20]:22s} {dict(rels.most_common(3))}")
comps = sorted(nx.weakly_connected_components(G), key=len, reverse=True)
deg1 = [n for n, d in G.degree if d == 1]
print(f"연결 요소 {len(comps)}개 · 최대 {len(comps[0])}노드 ({len(comps[0])/G.number_of_nodes()*100:.0f}%)")
print(f"차수 1 노드 {len(deg1)}개 ({len(deg1)/G.number_of_nodes()*100:.0f}%)")

# ═════ 섹션 9: 커뮤니티 ═════════════════════════════════════════════════
section("9. 커뮤니티")
ATTR_TYPES = {"Genre", "Theme", "Location"}

def community_graph(attr_w):
    CG = nx.Graph()
    for u, v, d in G.edges(data=True):
        tu, tv = G.nodes[u].get("type"), G.nodes[v].get("type")
        w = d["confidence"] * (attr_w if (tu in ATTR_TYPES or tv in ATTR_TYPES) else 1.0)
        CG.add_edge(u, v, weight=CG[u][v]["weight"] + w if CG.has_edge(u, v) else w)
    return CG

CG = community_graph(0.3)
levels = list(nxc.louvain_partitions(CG, weight="weight", seed=SEED))
for i, part in enumerate(levels):
    print(f"  레벨 {i}: 커뮤니티 {len(part)}개 · 모듈러리티 {nxc.modularity(CG, part, weight='weight'):.3f}")
PART = sorted([c for c in levels[-1] if len(c) >= 4], key=len, reverse=True)
print(f"요약 대상 {len(PART)}개 · 크기 {[len(c) for c in PART]}")
for aw in (1.0,):
    cg = community_graph(aw)
    lv = list(nxc.louvain_partitions(cg, weight="weight", seed=SEED))
    pp = sorted([c for c in lv[-1] if len(c) >= 4], key=len, reverse=True)
    print(f"  (비교) ATTR_W={aw}: 커뮤니티 {len(pp)}개 · 크기 {[len(c) for c in pp[:8]]}")

def profile_community(com):
    sub = G.subgraph(com)
    by_type = defaultdict(list)
    for n in com:
        by_type[G.nodes[n].get("type", "?")].append(n)
    top = lambda t, k=6: [str(x) for x in sorted(by_type.get(t, []), key=lambda n: -G.degree(n))[:k]]
    return {"size": len(com), "n_edges": sub.number_of_edges(),
            "n_people": len(by_type.get("Person", [])), "n_films": len(by_type.get("Film", [])),
            "people": top("Person"), "films": top("Film"), "genres": top("Genre", 5),
            "themes": top("Theme", 5), "awards": top("Award", 4), "orgs": top("Organization", 3),
            "locations": top("Location", 3), "period": ""}

PROFILES = [profile_community(c) for c in PART]
for i, p in enumerate(PROFILES, 1):
    print(f"  C{i} {p['size']}노드 · 인물 {p['people'][:4]} · 작품 {p['films'][:4]} · 조직 {p['orgs']}")

REPORT_SYSTEM = """당신은 한국 영화 지식 그래프의 커뮤니티(밀접하게 연결된 인물·작품 집단)를 요약한다.
주어진 집계 정보만 근거로 삼고, 없는 사실은 절대 지어내지 마라.

출력은 JSON 객체 하나:
{{"title": "이 집단을 부르는 짧은 이름(15자 내외)",
  "summary": "이 집단이 어떤 집단인지 2~3문장. 시대·장르·수상 경향·핵심 인물을 담아라.",
  "findings": ["이 집단에 대해 말할 수 있는 구체적 사실 3개"]}}"""
REPORT_PROMPT = ChatPromptTemplate.from_messages([("system", REPORT_SYSTEM), ("human", "{facts}")])
report_llm = chat_model().bind(response_format={"type": "json_object"})

def facts_of(p):
    f = [f"규모: 노드 {p['size']}개 (인물 {p['n_people']}명, 작품 {p['n_films']}편), 관계 {p['n_edges']}개"]
    for label, key in (("핵심 인물", "people"), ("대표 작품", "films"), ("주요 장르", "genres"),
                       ("주요 소재", "themes"), ("주요 배경", "locations"), ("수상 이력", "awards"),
                       ("제작/배급", "orgs")):
        if p[key]:
            f.append(f"{label}: {', '.join(p[key])}")
    return "\n".join(f)

def make_report(ip):
    i, p = ip
    facts = facts_of(p)
    try:
        r = json.loads(track(report_llm.invoke(REPORT_PROMPT.format_messages(facts=facts)), CHAT_MODEL).content)
    except Exception as e:
        r = {"title": (p["people"] or p["films"] or ["미상"])[0], "summary": facts, "findings": [], "error": str(e)[:80]}
    r.update({"id": f"C{i}", "profile": p, "facts": facts})
    return r

REPORT_CACHE = os.path.join(OUT_DIR, "community_reports.json")
if os.path.exists(REPORT_CACHE):
    REPORTS = json.load(open(REPORT_CACHE, encoding="utf-8"))
else:
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        REPORTS = list(ex.map(make_report, enumerate(PROFILES, 1)))
    json.dump(REPORTS, open(REPORT_CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r in REPORTS:
    print(f"  ■ [{r['id']}] {r['title']} — {r['summary'][:110]}")

# ═════ 섹션 10: LangGraph 에이전트 ══════════════════════════════════════
section("10. LangGraph 에이전트")

class RAGState(TypedDict):
    question: str
    route: str
    seeds: List[str]
    radius: int
    triples: List[Any]
    candidates: List[Any]
    reports: List[Dict]
    context: str
    answer: str
    sources: List[str]
    trace: List[str]

def related(node, relation=None):
    out = []
    if node not in G:
        return out
    for _, v, d in G.out_edges(node, data=True):
        if relation is None or d["relation"] == relation:
            out.append((node, d["relation"], v, d))
    for u, _, d in G.in_edges(node, data=True):
        if relation is None or d["relation"] == relation:
            out.append((u, d["relation"], node, d))
    return out

def node_kind(n):
    return G.nodes[n].get("type", "?") if n in G else "?"

def entities_in(question, top=3):
    q = norm(question)
    found = [n for n in G.nodes if len(norm(n)) >= 2 and str(n) not in GENERIC and norm(n) in q]
    found.sort(key=lambda n: (FAMILY.get(node_kind(n)) != "entity", -len(str(n)), -G.degree(n)))
    return found[:top]

GLOBAL_HINTS = ["전체", "전반", "자료에", "코퍼스", "집단", "그룹", "경향", "흐름",
                "어떤 것들이 있", "반복적으로", "대체로"]
PATH_HINTS = ["추천", "비슷한", "다른 작품", "다른 영화", "함께", "같은", "출연한 배우의",
              "감독이 만든", "왜 비슷"]

def route_rule(question):
    if any(h in question for h in GLOBAL_HINTS):
        return "global"
    if any(h in question for h in PATH_HINTS):
        return "path"
    return None

ROUTER_PROMPT = ChatPromptTemplate.from_template(
    "질문을 다음 세 가지 중 하나로만 분류하라. 다른 말은 하지 마라.\n"
    "- local : 질문에 등장하는 특정 개체의 직접 속성을 묻는다 (감독은? 배급사는? 어떤 영화를 연출했나?)\n"
    "- path  : 개체에서 출발해 다른 개체로 건너가야 한다 (추천, 비슷한 작품, 같이 작업한 사람, 조건 필터)\n"
    "- global: 특정 개체가 아니라 자료 전체의 구성·경향을 묻는다\n\n"
    "질문: {q}\n분류:")
router_llm = chat_model()
ROUTE_FALLBACKS = Counter()

def route_llm(question):
    try:
        out = track(router_llm.invoke(ROUTER_PROMPT.format_messages(q=question)), CHAT_MODEL).content.strip().lower()
    except Exception as e:
        ROUTE_FALLBACKS[f"호출 실패({type(e).__name__})"] += 1
        return None
    hit = next((k for k in ("global", "path", "local") if k in out), None)
    if hit is None:
        ROUTE_FALLBACKS["응답 해석 실패"] += 1
    return hit

def route(question):
    r = route_rule(question)
    if r:
        return r
    ROUTE_FALLBACKS["규칙 판단 불가 → LLM"] += 1
    r = route_llm(question)
    if r is None:
        ROUTE_FALLBACKS["LLM 도 실패 → 기본값 local"] += 1
    return r or "local"

KIND2ROUTE = {"단순": "local", "추천": "path", "전역": "global"}
hit_rule = hit_llm = hit_two = 0
ROUTE_FALLBACKS.clear()
for q in QUESTIONS:
    want = KIND2ROUTE[q["kind"]]
    gr, gl, gt = route_rule(q["user_input"]), route_llm(q["user_input"]), route(q["user_input"])
    hit_rule += ((gr or "local") == want); hit_llm += ((gl or "local") == want); hit_two += (gt == want)
    if len({gr or "local", gl or "local", gt}) > 1 or gt != want:
        print(f"  X [{q['id']}] 기대 {want} | 규칙 {gr} | LLM {gl} | 2단 {gt} | {q['user_input'][:30]}")
print(f"라우터 정확도 — 규칙 {hit_rule}/15 · LLM {hit_llm}/15 · 2단 {hit_two}/15")
n_llm_calls = ROUTE_FALLBACKS["규칙 판단 불가 → LLM"]
print(f"2단 라우터의 LLM 호출 {n_llm_calls}회 / 15 · 폴백 {dict(ROUTE_FALLBACKS)}")

RELATION_HINTS = {
    "DIRECTED": ["감독", "연출", "만든"],
    "ACTED_IN": ["출연", "배우", "나온", "역을", "캐스팅", "함께 만든"],
    "WON_AWARD": ["수상", "상을 받", "받은 작품", "영화제", "시상식", "상을"],
    "HAS_GENRE": ["장르", "스릴러", "코미디", "미스터리", "액션", "공포", "멜로", "드라마"],
    "HAS_THEME": ["소재", "주제", "다룬"],
    "SET_IN": ["배경", "무대"],
    "PRODUCED_OR_DISTRIBUTED_BY": ["배급", "제작사", "제작한", "만든 회사"],
}

def required_relations(question):
    return {r for r, ws in RELATION_HINTS.items() if any(w in question for w in ws)}

def relation_degree(nodes, relation):
    return sum(len(related(n, relation)) for n in nodes)

for name in ("기생충", "송강호", "극한직업", "대종상"):
    n = next((x for x in G if norm(x) == norm(name)), None)
    if n:
        print(f"  {n}: 전체 차수 {G.degree(n)} · " +
              " ".join(f"{r}={relation_degree([n], r)}" for r in REL_NAMES if relation_degree([n], r)))
dj = next((x for x in G if norm(x) == "대종상"), None)
if dj:
    wa = related(dj, "WON_AWARD")
    print(f"  대종상 WON_AWARD {len(wa)}개 중 confidence 1.0: {sum(1 for *_, d in wa if d['confidence'] >= 1.0)}개")
n_rule_edges = sum(1 for *_, d in G.edges(data=True) if d["origin"] in ("rule", "rule+llm"))
print(f"  규칙 계열 엣지 {n_rule_edges}/{G.number_of_edges()} ({n_rule_edges/G.number_of_edges()*100:.0f}%)")
gold_edges = [c for q in QUESTIONS for c in q["reference_contexts"]]
def edge_origin(c):
    for u, v in ((c[0], c[2]), (c[2], c[0])):
        uu = next((x for x in G if norm(x) == norm(u)), None); vv = next((x for x in G if norm(x) == norm(v)), None)
        if uu and vv and G.has_edge(uu, vv) and G[uu][vv]["relation"] == c[1]:
            return G[uu][vv]["origin"]
    return None
go = Counter(edge_origin(c) for c in gold_edges)
print(f"  골든셋 기준 삼중항의 엣지 출처: {dict(go)}")

PER_RELATION, MAX_TRIPLES, RADIUS = 10, 200, 2
RULE_ORIGINS = ("rule", "rule+llm")

def collect_triples(seeds, radius=1, per_relation=PER_RELATION, max_triples=MAX_TRIPLES, exempt=True):
    seen, out, visited = set(), [], set()
    frontier = [s for s in seeds if s in G]
    for _ in range(radius):
        nxt = []
        for node in frontier:
            if node in visited:
                continue
            visited.add(node)
            by_rel = defaultdict(list)
            for u, r, v, d in related(node):
                by_rel[r].append((u, r, v, d))
            for r, ts in by_rel.items():
                if exempt:
                    rule = [t for t in ts if t[3]["origin"] in RULE_ORIGINS]
                    rest = [t for t in ts if t[3]["origin"] not in RULE_ORIGINS]
                else:
                    rule, rest = [], ts
                llm = sorted(rest, key=lambda x: -x[3]["confidence"])[:per_relation]
                for u, rr, v, d in rule + llm:
                    key = (u, rr, v)
                    if key not in seen:
                        seen.add(key); out.append((u, rr, v, d))
                        if len(out) >= max_triples:
                            return out
                    nxt.append(v if u == node else u)
        frontier = nxt
    return out

def recommend(seeds, top=8, max_hops=3,
              relations=("DIRECTED", "ACTED_IN", "HAS_GENRE", "HAS_THEME", "SET_IN", "WON_AWARD")):
    seed_keys = {norm(s) for s in seeds}
    scores, why = defaultdict(float), defaultdict(list)
    frontier = [(s, 1.0, []) for s in seeds if s in G]
    visited = set(seed_keys)
    for hop in range(max_hops):
        nxt = []
        for node, score, path in frontier:
            for u, r, v, d in related(node):
                if r not in relations:
                    continue
                other = v if norm(v) != norm(node) else u
                if norm(other) in seed_keys:
                    continue
                penalty = 1.0 / (1 + G.degree(other) ** 0.5)
                sc = score * d["confidence"] * penalty
                reason = path + [f"{r}:{other}"]
                if node_kind(other) == "Film":
                    scores[other] += sc
                    if len(why[other]) < 3:
                        why[other].append(" → ".join(reason))
                elif hop + 1 < max_hops and norm(other) not in visited:
                    visited.add(norm(other))
                    nxt.append((other, sc, reason))
        frontier = nxt
    ranked = sorted(scores.items(), key=lambda kv: -kv[1])[:top]
    return [(film, round(sc, 4), why[film]) for film, sc in ranked]

seeds = entities_in("영화 《기생충》에 출연한 배우의 다른 작품을 추천해줘.")
tri = collect_triples(seeds, radius=RADIUS)
print(f"\n씨앗 {seeds} · 삼중항 {len(tri)} · {Counter(r for _, r, _, _ in tri).most_common()}")
for film, sc, w in recommend(seeds)[:6]:
    print(f"  {str(film)[:22]:24s} {sc:.3f} ← {w[0]}")

NO_EVIDENCE = "근거가 부족합니다. 이 자료만으로는 확인할 수 없습니다."
MAX_RADIUS = 3

def relation_gap(state):
    if str(state.get("route", "")).startswith("global"):
        return set()
    want = required_relations(state["question"])
    if not want:
        return set()
    return want - {r for _, r, _, _ in state["triples"]}

def n_route(state):
    r = route(state["question"])
    return {"route": r, "radius": 1 if r == "local" else 2, "trace": state.get("trace", []) + [f"route={r}"]}

def n_find_seeds(state):
    seeds = entities_in(state["question"])
    want = sorted(required_relations(state["question"]))
    deg = {r: relation_degree(seeds, r) for r in want}
    tr = state["trace"] + [f"seeds={seeds} · 요구관계 차수={deg or '—'}"]
    if not seeds:
        tr.append("개체 없음 → global 로 폴백")
        return {"seeds": [], "route": "global", "trace": tr}
    return {"seeds": seeds, "trace": tr}

def after_seeds(state) -> Literal["global", "expand"]:
    return "expand" if state["seeds"] else "global"

def n_expand(state):
    tri = collect_triples(state["seeds"], radius=state["radius"])
    cands = recommend(state["seeds"]) if state["route"] == "path" else []
    gap = relation_gap({**state, "triples": tri})
    return {"triples": tri, "candidates": cands,
            "trace": state["trace"] + [f"expand(r={state['radius']})→삼중항 {len(tri)}"
                                       + (f" · 아직 없는 관계 {sorted(gap)}" if gap else "")]}

def n_deepen(state):
    return {"radius": state["radius"] + 1, "trace": state["trace"] + [f"deepen→r={state['radius']+1}"]}

def need_more(state) -> Literal["deepen", "build"]:
    if not state["seeds"] or state["radius"] >= MAX_RADIUS:
        return "build"
    return "deepen" if relation_gap(state) else "build"

def n_global_map(state):
    qk = set(re.findall(r"[0-9A-Za-z가-힣]{2,}", state["question"]))
    def score(r):
        text = r["title"] + " " + r["summary"] + " " + r["facts"]
        return sum(1 for w in qk if w in text) + r["profile"]["size"] / 100
    picked = sorted(REPORTS, key=score, reverse=True)[:5]
    return {"reports": picked, "trace": state["trace"] + [f"global_map→보고서 {len(picked)}개"]}

def n_global_reduce(state):
    lines = []
    for r in state["reports"]:
        p = r["profile"]
        lines.append(f"[{r['id']}] {r['title']} (노드 {p['size']}개)\n  요약: {r['summary']}\n"
                     f"  핵심 인물: {', '.join(p['people'])}\n  대표 작품: {', '.join(p['films'])}\n"
                     f"  장르/수상: {', '.join(p['genres'])} / {', '.join(p['awards'])}")
    return {"context": "\n\n".join(lines), "sources": [r["id"] for r in state["reports"]],
            "trace": state["trace"] + ["global_reduce"]}

def n_build_context(state):
    if state["route"] == "global":
        return {}
    parts, srcs = [], set()
    if state["triples"]:
        parts.append("[관계 사실]")
        for u, r, v, d in state["triples"]:
            prop = f" {d['props']}" if d.get("props") else ""
            parts.append(f"({u}, {r}, {v}){prop} <출처:{','.join(d['sources'][:2])}, {d['origin']}>")
            srcs.update(d["sources"][:2])
    if state["candidates"]:
        parts.append("\n[관계로 계산한 추천 후보 — 점수와 이유]")
        for film, sc, why in state["candidates"]:
            parts.append(f"{film} (점수 {sc}) ← 경로: {' | '.join(why)}")
    ctx = "\n".join(parts)
    return {"context": ctx, "sources": sorted(srcs), "trace": state["trace"] + [f"context {len(ctx)}자"]}

ANSWER_PROMPT = ChatPromptTemplate.from_template(
    "너는 한국 영화 위키 에이전트다. 아래 '근거'만 사용해 한국어로 답하라.\n"
    "규칙:\n"
    "1. 근거로 확정할 수 없으면 반드시 '근거가 부족합니다' 라고만 답하라. 추측하지 마라.\n"
    "2. 근거에 없는 고유명사(작품·인물·시상식)를 답에 쓰지 마라. 근거에 있는 것만 쓴다.\n"
    "3. 추천 질문이면 근거가 실제로 뒷받침하는 작품만 고르고, 각각 왜 추천하는지 근거의 관계를 들어\n"
    "   한 줄로 설명하라. **개수를 채우려고 근거가 약한 작품을 끼워 넣지 마라.** 2편뿐이면 2편만 답한다.\n"
    "4. 답 끝에 사용한 근거 삼중항을 괄호로 표시하라.\n"
    "5. 간결하게. 목록은 5줄 이내.\n\n"
    "근거:\n{evidence}\n\n질문: {question}\n답변:")
answer_llm = chat_model()

def n_synthesize(state):
    gap = relation_gap(state)
    if not state["context"].strip() or gap:
        why = "근거없음" if not state["context"].strip() else f"{'·'.join(sorted(gap))} 관계 없음"
        return {"answer": NO_EVIDENCE, "trace": state["trace"] + [f"synthesize({why}·LLM미호출)"]}
    out = track(answer_llm.invoke(ANSWER_PROMPT.format_messages(
        evidence=state["context"][:12000], question=state["question"])), CHAT_MODEL).content
    return {"answer": out, "trace": state["trace"] + ["synthesize"]}

builder = StateGraph(RAGState)
for name, fn in (("route", n_route), ("find_seeds", n_find_seeds), ("expand", n_expand), ("deepen", n_deepen),
                 ("global_map", n_global_map), ("global_reduce", n_global_reduce),
                 ("build_context", n_build_context), ("synthesize", n_synthesize)):
    builder.add_node(name, fn)
builder.add_edge(START, "route")
builder.add_conditional_edges("route", lambda s: "global" if s["route"] == "global" else "seeds",
                              {"global": "global_map", "seeds": "find_seeds"})
builder.add_conditional_edges("find_seeds", after_seeds, {"global": "global_map", "expand": "expand"})
builder.add_conditional_edges("expand", need_more, {"deepen": "deepen", "build": "build_context"})
builder.add_edge("deepen", "expand")
builder.add_edge("global_map", "global_reduce")
builder.add_edge("global_reduce", "build_context")
builder.add_edge("build_context", "synthesize")
builder.add_edge("synthesize", END)
app = builder.compile()
try:
    print(app.get_graph().draw_ascii())
except Exception as e:
    print("(ascii 그리기 실패:", type(e).__name__, ")")

def ask(question, verbose=True):
    init = {"question": question, "route": "", "seeds": [], "radius": 1, "triples": [], "candidates": [],
            "reports": [], "context": "", "answer": "", "sources": [], "trace": []}
    final = app.invoke(init)
    if verbose:
        print(f"Q: {question}\n  경로: {' → '.join(final['trace'])}\n  답변: {final['answer']}\n  출처: {final['sources'][:6]}\n")
    return final

# ═════ 섹션 11: 직접 질의 ═══════════════════════════════════════════════
if os.getenv("STOP_AT_11"):  # graphrag_03_extras.py 가 여기까지의 정의만 빌려 쓴다
    raise SystemExit
section("11. 직접 질의")
DEMO = ["영화 《기생충》의 감독은 누구인가?",
        "영화 《괴물》의 감독이 만든 다른 영화를 추천해줘.",
        "영화 《기생충》과 비슷한 영화를 추천하고 왜 비슷한지도 알려줘.",
        "이 자료에 담긴 한국 영화계에는 어떤 집단들이 있고 각각 어떤 특징을 가지는가?",
        "송강호 감독의 영화를 알려줘.",
        "2035년에 개봉할 봉준호 감독의 신작 제목은?",
        "영화 《살인의 추억》의 줄거리를 요약해 줘."]
RESULTS = {q: ask(q) for q in DEMO}
r = RESULTS[DEMO[2]]
print("── 《기생충》 비슷한 영화: LLM 에게 넘어간 근거 앞부분 ──\n" + r["context"][:1500])

# ═════ 섹션 12: 평가 ═══════════════════════════════════════════════════
section("12. 평가")
def triple_key(x):
    parts = list(x)[:3]
    return (norm(parts[0]), str(parts[1]).strip(), norm(parts[2]))

def sym(k):
    return {k, (k[2], k[1], k[0])}

def context_recall(per_relation=PER_RELATION, radius=RADIUS, max_triples=MAX_TRIPLES, exempt=True):
    hit = need = 0
    for q in QUESTIONS:
        if not q["reference_contexts"]:
            continue
        got = set()
        for t in collect_triples(entities_in(q["user_input"]), radius=radius, per_relation=per_relation,
                                 max_triples=max_triples, exempt=exempt):
            got |= sym(triple_key(t))
        for c in q["reference_contexts"]:
            need += 1
            hit += bool(sym(triple_key(c)) & got)
    return hit, need

print("── 컨텍스트 재현율 격자 (행=per_relation, 열=max_triples) ──")
for exempt in (True, False):
    print(f"  [규칙 엣지 할당량 면제={exempt}]")
    for pr in (5, 10, 20):
        cells = []
        for mt in (60, 150, 300):
            h, n = context_recall(per_relation=pr, max_triples=mt, exempt=exempt)
            cells.append(f"{h}/{n}({h/n*100:.0f}%)")
        print(f"    per_relation={pr:2d}  " + "  ".join(f"mt={mt}:{c}" for mt, c in zip((60, 150, 300), cells)))
h, n = context_recall()
print(f"현재 설정 (10, 200, 면제) → {h}/{n} ({h/n*100:.0f}%)")

raw_docs = [Document(page_content=t, metadata={"title": ti}) for ti, t in DOCS.items()]
chunks = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120).split_documents(raw_docs)
def ko_tokens(text):
    return re.findall(r"[0-9A-Za-z가-힣]+", text)
basic_retriever = BM25Retriever.from_documents(chunks, preprocess_func=ko_tokens, k=6)

BASIC_PROMPT = ChatPromptTemplate.from_template(
    "너는 한국 영화 위키 에이전트다. 아래 '근거'만 사용해 한국어로 답하라.\n"
    "규칙:\n"
    "1. 근거로 확정할 수 없으면 반드시 '근거가 부족합니다' 라고만 답하라. 추측하지 마라.\n"
    "2. 근거에 없는 고유명사(작품·인물·시상식)를 답에 쓰지 마라. 근거에 있는 것만 쓴다.\n"
    "3. 추천 질문이면 근거가 실제로 뒷받침하는 작품만 고르고, 각각 왜 추천하는지 한 줄로 설명하라.\n"
    "   **개수를 채우려고 근거가 약한 작품을 끼워 넣지 마라.** 2편뿐이면 2편만 답한다.\n"
    "4. 간결하게. 목록은 5줄 이내.\n\n"
    "근거:\n{evidence}\n\n질문: {question}\n답변:")

def ask_basic(question, k=6):
    hits = basic_retriever.invoke(question)[:k]
    ev = "\n\n".join(f"[{h.metadata['title']}] {re.sub(r'\s+', ' ', h.page_content)[:700]}" for h in hits)
    out = track(answer_llm.invoke(BASIC_PROMPT.format_messages(evidence=ev, question=question)), CHAT_MODEL).content
    return {"answer": out, "sources": [h.metadata["title"] for h in hits]}

judge_llm = chat_model(JUDGE_MODEL).bind(response_format={"type": "json_object"})
JUDGE_PROMPT = ChatPromptTemplate.from_template(
    "너는 한국 영화 QA 시스템의 채점자다. 아래 정보를 보고 '답변'을 채점하라.\n\n"
    "[질문] {question}\n[기대 정답] {reference}\n[원문 근거] {evidence}\n[채점할 답변] {answer}\n\n"
    "채점 기준:\n"
    "- 1.0(정답): 기대 정답의 핵심을 맞혔다. 목록형 정답이면 핵심 항목을 하나 이상 정확히 포함하고 "
    "틀린 항목을 섞지 않았다. 표현이 달라도 의미가 같으면 정답이다.\n"
    "- 0.5(부분정답): 방향은 맞지만 핵심이 빠졌거나, 맞는 항목과 틀린 항목이 섞였다.\n"
    "- 0.0(오답): 틀렸거나, 답할 수 있는 질문인데 '근거가 부족합니다'라고 했다.\n"
    "네 사전 지식이 아니라 위의 기대 정답과 원문 근거만을 기준으로 삼아라.\n\n"
    "JSON 하나로만 답하라: {{\"score\": 1.0, \"reason\": \"한 문장\"}}")
JUDGE_FAILS = []

def judge(question, reference, evidence, answer):
    try:
        raw = track(judge_llm.invoke(JUDGE_PROMPT.format_messages(
            question=question, reference=reference, evidence=evidence[:900], answer=str(answer)[:1500])), JUDGE_MODEL).content
        r = json.loads(raw)
        return float(r.get("score", 0)), str(r.get("reason", ""))[:200]
    except Exception as e:
        JUDGE_FAILS.append(f"{type(e).__name__}: {str(e)[:60]}")
        return None, "(심판 실패)"

EVAL_CACHE = os.path.join(OUT_DIR, "eval_results.json")
if os.path.exists(EVAL_CACHE):
    EVAL = json.load(open(EVAL_CACHE, encoding="utf-8"))
else:
    EVAL = []
    for q in QUESTIONS:
        g = ask(q["user_input"], verbose=False)
        b = ask_basic(q["user_input"])
        gs, gw = judge(q["user_input"], q["reference"], q["evidence"], g["answer"])
        bs, bw = judge(q["user_input"], q["reference"], q["evidence"], b["answer"])
        EVAL.append({"id": q["id"], "kind": q["kind"], "question": q["user_input"], "reference": q["reference"],
                     "graph_answer": g["answer"], "graph_score": gs, "graph_why": gw, "graph_route": g["route"],
                     "graph_trace": g["trace"], "graph_context": g["context"],
                     "basic_answer": b["answer"], "basic_score": bs, "basic_why": bw, "basic_sources": b["sources"]})
        print(f"  [{q['id']}] GraphRAG {gs} · basic {bs}")
    json.dump(EVAL, open(EVAL_CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

ev = pd.DataFrame(EVAL)
print(ev.groupby("kind")[["basic_score", "graph_score"]].agg(["mean", "count"]).round(2).to_string())
print(f"전체 basic {ev['basic_score'].mean():.2f} (만점 {int((ev['basic_score']==1).sum())}) · "
      f"graph {ev['graph_score'].mean():.2f} (만점 {int((ev['graph_score']==1).sum())}) · 심판 실패 {len(JUDGE_FAILS)}")
for r in EVAL:
    print(f"\n[{r['id']}] {r['question']}\n  기대: {r['reference'][:90]}\n"
          f"  graph({r['graph_score']}): {r['graph_answer'][:160]!r}\n    심판: {r['graph_why']}\n"
          f"  basic({r['basic_score']}): {r['basic_answer'][:160]!r}\n    심판: {r['basic_why']}")

# 심판 흔들림 — 같은 답변을 3번
demo = QUESTIONS[3]
g_ans = next(r for r in EVAL if r["id"] == demo["id"])["graph_answer"]
rep = [judge(demo["user_input"], demo["reference"], demo["evidence"], g_ans)[0] for _ in range(3)]
print(f"\n같은 답변 3회 채점 [{demo['id']}]: {rep}")

print("\n── 실패 원인 분류 ──")
causes = Counter()
for q, r in zip(QUESTIONS, EVAL):
    if r["graph_score"] is None or r["graph_score"] >= 1.0:
        continue
    need = q["reference_contexts"]
    in_graph = all(has_triple(G, *c) for c in need) if need else True
    got = set()
    for t in collect_triples(entities_in(q["user_input"]), radius=RADIUS):
        got |= sym(triple_key(t))
    in_ctx = all(sym(triple_key(c)) & got for c in need) if need else bool(r["graph_context"])
    ok_route = r["graph_route"] == KIND2ROUTE[q["kind"]]
    cause = ("라우팅 오류" if not ok_route else "① 색인" if not in_graph else "② 검색" if not in_ctx else "③ 생성")
    causes[cause] += 1
    print(f"  [{q['id']}] {r['graph_score']} · {cause}")
print("원인별:", causes.most_common())

section("토큰 사용량 (추출 제외)")
print(dict(USAGE))
