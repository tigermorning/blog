"""20편용 — BM25 검색 품질 지표 (Hit Rate@K, Precision@K, Recall@K, MRR, nDCG@K). 키 불필요.

정답 문서가 사람이 정해 둔 4문항(PROBE)만 쓴다. 문항마다 정답 문서는 1건이다.
"""
import os, re, glob, json, math
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.retrievers import BM25Retriever

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "graphrag_work", "input")
DOCS = {os.path.basename(p)[:-3].replace("_", " "): open(p, encoding="utf-8").read()
        for p in sorted(glob.glob(BASE + "/cinephile_kb_80/docs/*.md"))}
Q = {q["id"]: q for q in json.load(open(BASE + "/cinephile_goldenset.json", encoding="utf-8"))["items"]}
chunks = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120).split_documents(
    [Document(page_content=t, metadata={"title": k}) for k, t in DOCS.items()])
tok = lambda s: re.findall(r"[0-9A-Za-z가-힣]+", s)
PROBE = {"추천-04": "송강호", "추천-06": "살인의 추억", "추천-09": "부산행", "추천-12": "버닝 (2018년 영화)"}

bm25 = BM25Retriever.from_documents(chunks, preprocess_func=tok, k=100)
ranks = {}
for qid, leaf in PROBE.items():
    hits = bm25.invoke(Q[qid]["user_input"])
    # 청크 순위 → 문서 순위 (같은 문서의 두 번째 청크부터는 건너뛴다)
    docs = []
    for h in hits:
        if h.metadata["title"] not in docs:
            docs.append(h.metadata["title"])
    chunk_titles = [h.metadata["title"] for h in hits]
    ranks[qid] = (chunk_titles.index(leaf) + 1 if leaf in chunk_titles else None,
                  docs.index(leaf) + 1 if leaf in docs else None)
    print(qid, leaf, "청크 순위", ranks[qid][0], "· 문서 순위", ranks[qid][1])

for K in (6, 10, 20, 50):
    hit = [1 if r and r <= K else 0 for r, _ in ranks.values()]
    prec = [h / K for h in hit]
    mrr = [1 / r if r and r <= K else 0 for r, _ in ranks.values()]
    ndcg = [1 / math.log2(r + 1) if r and r <= K else 0 for r, _ in ranks.values()]
    n = len(hit)
    print(f"K={K:2d}  HitRate {sum(hit)/n:.2f}  Recall {sum(hit)/n:.2f}  Precision {sum(prec)/n:.3f}  "
          f"MRR {sum(mrr)/n:.3f}  nDCG {sum(ndcg)/n:.3f}")
