import os, re, glob, json
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.retrievers import BM25Retriever

DOC_DIR = "input/cinephile_kb_80/docs"
DOCS = {os.path.basename(p)[:-3].replace("_", " "): open(p, encoding="utf-8").read()
        for p in sorted(glob.glob(DOC_DIR + "/*.md"))}
QUESTIONS = json.load(open("input/cinephile_goldenset.json", encoding="utf-8"))["items"]

chunks = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120).split_documents(
    [Document(page_content=t, metadata={"title": k}) for k, t in DOCS.items()])

def ko_tokens(text):                      # 한글·영문·숫자 덩어리만
    return re.findall(r"[0-9A-Za-z가-힣]+", text)

PROBE = {"추천-04": "송강호", "추천-06": "살인의 추억",
         "추천-09": "부산행", "추천-12": "버닝 (2018년 영화)"}
for K in (6, 20, 50):
    bm25 = BM25Retriever.from_documents(chunks, preprocess_func=ko_tokens, k=K)
    for qid, leaf in PROBE.items():
        q = next(x for x in QUESTIONS if x["id"] == qid)["user_input"]
        titles = [h.metadata["title"] for h in bm25.invoke(q)]
        rank = titles.index(leaf) + 1 if leaf in titles else "없음"
        print(f"k={K:2d} [{qid}] {leaf} → {rank}")