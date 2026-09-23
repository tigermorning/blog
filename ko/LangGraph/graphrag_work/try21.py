from dotenv import load_dotenv; import os
load_dotenv(os.path.expanduser('~/Documents/openai_key.env'))
from langchain_openai import ChatOpenAI
from langchain_core.documents import Document
from langchain_experimental.graph_transformers import LLMGraphTransformer

REL_TRIPLES = [("Person", "DIRECTED", "Film"), ("Person", "ACTED_IN", "Film"),
               ("Film", "HAS_GENRE", "Genre"), ("Film", "WON_AWARD", "Award")]

tf = LLMGraphTransformer(
    llm=ChatOpenAI(model="gpt-4.1-mini", temperature=0, timeout=120, max_retries=3),
    allowed_nodes=["Film", "Person", "Genre", "Award"],
    allowed_relationships=REL_TRIPLES,          # 삼중항으로 — 방향이 고정된다
    relationship_properties=["category", "character"],
    strict_mode=True,
    additional_instructions="개체 이름은 원문 표기 그대로. Award 노드는 시상식 이름만, 부문은 category 속성에.",
)

title = "기생충 (영화)"
body = open("input/cinephile_kb_80/docs/기생충_(영화).md", encoding="utf-8").read()[:2400]
doc = Document(page_content=f"[문서 제목] {title}\n[문서 유형] Film\n\n{body}")
for r in tf.convert_to_graph_documents([doc])[0].relationships:
    print(f"({r.source.id}) --[{r.type}]--> ({r.target.id})", r.properties or "")