import json
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
client = OpenAI()

# 실습 1과 '똑같은 12건'을 다시 사용
titles = [tuple(x) for x in json.loads(
    Path(__file__).with_name("step6_titles.json").read_text(encoding="utf-8"))]

listing = "\n".join(f"{i}. [{s}] {t}" for i, (s, t) in enumerate(titles))
SYS = ("당신은 국내 개발팀을 위한 AI 뉴스레터 편집자입니다.\n"
       "아래 후보를 서로 비교해 '이번 주 우리가 일하는 방식이 바뀔 만한' 순서대로 "
       "상위 5건을 고르세요. 번호만 쉼표로 구분해 답하세요. 설명 금지.")

r = client.chat.completions.create(                # 호출 한 번, 전부 한 화면에
    model="gpt-4.1-mini", temperature=0, max_tokens=40,
    messages=[{"role": "system", "content": SYS},
              {"role": "user", "content": listing}])
picked = [int(x) for x in r.choices[0].message.content.strip().replace(" ", "").split(",")][:5]

print("모델 원본 응답:", r.choices[0].message.content.strip())
print("\n한 화면에 놓고 비교한 결과 — 상위 5건")
for rank, i in enumerate(picked, 1):
    print(f"  {rank}위  [{titles[i][0]}] {titles[i][1][:46]}")
