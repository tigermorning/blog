import json, re
from pathlib import Path
from itertools import combinations
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
client = OpenAI()

titles = [tuple(x) for x in json.loads(
    Path(__file__).with_name("step6_titles.json").read_text(encoding="utf-8"))]

SYS = ("당신은 국내 개발팀을 위한 AI 뉴스레터 편집자입니다.\n"
       "두 기사 중 '이번 주 우리가 일하는 방식이 바뀔 만한' 쪽은 어느 것입니까?\n"
       "A 또는 B 한 글자만 답하세요. 설명 금지.")

pairs = list(combinations(range(len(titles)), 2))

def judge(pair):
    a, b = pair
    user = f"A. [{titles[a][0]}] {titles[a][1]}\nB. [{titles[b][0]}] {titles[b][1]}"
    r = client.chat.completions.create(
        model="gpt-4.1-mini", temperature=0, max_tokens=3,
        messages=[{"role": "system", "content": SYS},
                  {"role": "user", "content": user}])
    ans = r.choices[0].message.content.strip().upper()
    side = "A" if ans.startswith("A") else "B"
    return pair, side

with ThreadPoolExecutor(max_workers=8) as ex:      # 66번을 순서대로 돌리면 느려서 병렬만 붙임
    results = list(ex.map(judge, pairs))

wins = Counter()
side_count = Counter()
for (a, b), side in results:
    wins[a if side == "A" else b] += 1
    side_count[side] += 1

print(f"호출 횟수: {len(pairs)}번\n")
print("승수 순위 (토너먼트 ②)")
for rank, (i, w) in enumerate(sorted(wins.items(), key=lambda kv: -kv[1]), 1):
    mark = "  ← 상위 5" if rank <= 5 else ""
    print(f"  {rank:>2}위  {w:>2}승 / 11  idx{i:<3} [{titles[i][0]}] {titles[i][1][:40]}{mark}")

print("\n동점 확인:", " · ".join(f"{w}승 {c}건" for w, c in sorted(Counter(wins.values()).items(), key=lambda kv: -kv[0])))
print(f"위치 편향 확인: A 선택 {side_count['A']}번 / B 선택 {side_count['B']}번 (총 {len(pairs)})")

Path(__file__).with_name("step6_tournament.json").write_text(
    json.dumps({str(k): v for k, v in wins.items()}, ensure_ascii=False), encoding="utf-8")
