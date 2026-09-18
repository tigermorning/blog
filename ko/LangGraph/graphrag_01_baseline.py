"""GraphRAG 실습 1 — 키 없이 도는 부분: 코퍼스 통계, BM25 기준선, 추출 비용 추정.

데이터: https://github.com/88chacha/cinephile-agent-data (위키백과 문서 80건 + 골든셋 15문항, CC BY-SA)
graphrag_work/input/ 에 풀어 둔다 (저장소에는 올리지 않는다).
실행: PYTHONIOENCODING=utf-8 python graphrag_01_baseline.py
"""
import os, re, glob, json
from collections import Counter

import pandas as pd
import tiktoken
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.retrievers import BM25Retriever

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graphrag_work")
DATA_DIR = os.path.join(BASE, "input")
DOC_DIR = os.path.join(DATA_DIR, "cinephile_kb_80", "docs")
GOLD_PATH = os.path.join(DATA_DIR, "cinephile_goldenset.json")

# ── 코퍼스 ──
DOCS = {}
for path in sorted(glob.glob(os.path.join(DOC_DIR, "*.md"))):
    title = os.path.splitext(os.path.basename(path))[0].replace("_", " ")
    DOCS[title] = open(path, encoding="utf-8").read()
MANIFEST = json.load(open(os.path.join(os.path.dirname(DOC_DIR), "manifest.json"), encoding="utf-8"))
NTYPE = {d["title"]: d["type"] for d in MANIFEST["docs"]}
print(f"문서 {len(DOCS)}개 · 유형 {Counter(NTYPE.values()).most_common()}")

def categories_of(text):
    m = re.search(r"^분류:\s*(.+)$", text, flags=re.M)
    return [c.strip() for c in m.group(1).split(",")] if m else []

CATS = {t: categories_of(x) for t, x in DOCS.items()}
df = pd.DataFrame({"title": list(DOCS), "type": [NTYPE.get(t, "?") for t in DOCS],
                   "chars": [len(x) for x in DOCS.values()], "n_cats": [len(CATS[t]) for t in DOCS]})
print(df["chars"].describe().round(0).to_string())
print("분류 없는 문서:", int((df["n_cats"] == 0).sum()))
print(df.nlargest(5, "chars")[["title", "type", "chars"]].to_string(index=False))
print("\n── 박찬욱 문서 앞부분 ──\n" + DOCS["박찬욱"][:300])

# ── 골든셋 ──
GOLD = json.load(open(GOLD_PATH, encoding="utf-8"))
QUESTIONS = GOLD["items"]
print(f"\n골든셋 {len(QUESTIONS)}문항 · {Counter(q['kind'] for q in QUESTIONS).most_common()}")
need = Counter(c[1] for q in QUESTIONS for c in q["reference_contexts"])
print("요구 관계:", need.most_common(), "· 기준 삼중항", sum(need.values()))
for q in QUESTIONS:
    print(f"  [{q['id']}] {q['user_input']}")

# ── BM25 기준선 ──
raw_docs = [Document(page_content=text, metadata={"title": title}) for title, text in DOCS.items()]
chunks = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120).split_documents(raw_docs)
print(f"\n문서 {len(raw_docs)} → 청크 {len(chunks)}")

def ko_tokens(text):
    return re.findall(r"[0-9A-Za-z가-힣]+", text)

bm25 = BM25Retriever.from_documents(chunks, preprocess_func=ko_tokens, k=6)
print("Q: 영화 《기생충》의 감독은 누구인가?")
for h in bm25.invoke("영화 《기생충》의 감독은 누구인가?")[:4]:
    print(f"  · [{h.metadata['title']}] {h.page_content.replace(chr(10), ' ')[:50]}")

def nz(s):
    return re.sub(r"[\s·・\-]", "", re.sub(r"\s*\([^)]*\)\s*$", "", str(s))).lower()

def answer_in_context(question, expected, retriever, k=6):
    hits = retriever.invoke(question)[:k]
    ctx = " ".join(h.page_content for h in hits).replace(" ", "")
    return expected.replace(" ", "") in ctx

def facts_supported(question, refs, retriever, k=6):
    txt = [nz(h.page_content) for h in retriever.invoke(question)[:k]]
    return [any(nz(c[0]) in x and nz(c[2]) in x for x in txt) for c in refs]

def measure(retriever, k):
    rows, facts = [], []
    for q in QUESTIONS:
        rows.append({"kind": q["kind"], "ok": answer_in_context(q["user_input"], q["reference"], retriever, k)})
        for c, ok in zip(q["reference_contexts"], facts_supported(q["user_input"], q["reference_contexts"], retriever, k)):
            facts.append({"id": q["id"], "kind": q["kind"], "t": tuple(c), "ok": ok})
    return pd.DataFrame(rows), pd.DataFrame(facts)

res, facts = measure(bm25, 6)
print("\n① 정답 문자열 포함 (k=6)\n", res.groupby("kind")["ok"].agg(["sum", "count"]).to_string())
print("② 사실 단위 확보 (k=6)\n", facts.groupby("kind")["ok"].agg(["sum", "count"]).to_string())
print(f"   전체 {int(facts['ok'].sum())}/{len(facts)}")
print("   놓친 사실:")
for _, r in facts[~facts["ok"]].iterrows():
    print(f"     [{r['id']}] {r['t']}")

for K in (20, 50):
    rt = BM25Retriever.from_documents(chunks, preprocess_func=ko_tokens, k=K)
    _, f = measure(rt, K)
    print(f"② 사실 단위 확보 (k={K}): " + " · ".join(
        f"{k} {int(g['ok'].sum())}/{len(g)}" for k, g in f.groupby("kind")) + f" · 전체 {int(f['ok'].sum())}/{len(f)}")

PROBE = {"추천-04": "송강호", "추천-06": "살인의 추억", "추천-09": "부산행", "추천-12": "버닝 (2018년 영화)"}
for K in (6, 20, 50):
    rt = BM25Retriever.from_documents(chunks, preprocess_func=ko_tokens, k=K)
    out = []
    for qid, leaf in PROBE.items():
        titles = [h.metadata["title"] for h in rt.invoke(next(x for x in QUESTIONS if x["id"] == qid)["user_input"])]
        rank = next((i + 1 for i, t in enumerate(titles) if t == leaf), None)
        out.append(f"{qid}:{leaf}→{rank or '없음'}")
    print(f"top-{K}: " + " | ".join(out))

# ── 추출 비용 추정 (6-3) ──
ENC = tiktoken.get_encoding("o200k_base")
sp = RecursiveCharacterTextSplitter(chunk_size=2400, chunk_overlap=200)
TASKS = [f"[문서 제목] {t}\n[문서 유형] {NTYPE.get(t, '기타')}\n\n{p}"
         for t in DOCS for p in sp.split_text(DOCS[t][:6000])]
in_tok = sum(len(ENC.encode(x)) for x in TASKS)
print(f"\n추출 청크 {len(TASKS)}개 · 본문 토큰 {in_tok:,} · 총 입력 추정 {in_tok + len(TASKS) * 850:,}")
