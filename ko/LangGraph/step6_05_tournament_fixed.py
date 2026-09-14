import json
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

def ask(first, second):
    user = (f"A. [{titles[first][0]}] {titles[first][1]}\n"
            f"B. [{titles[second][0]}] {titles[second][1]}")
    r = client.chat.completions.create(
        model="gpt-4.1-mini", temperature=0, max_tokens=3,
        messages=[{"role": "system", "content": SYS},
                  {"role": "user", "content": user}])
    return first if r.choices[0].message.content.strip().upper().startswith("A") else second

pairs = list(combinations(range(len(titles)), 2))

def both_orders(pair):
    a, b = pair
    return pair, ask(a, b), ask(b, a)

with ThreadPoolExecutor(max_workers=8) as ex:
    results = list(ex.map(both_orders, pairs))

# 두 순서에서 똑같이 이긴 경우에만 1승. 뒤집힌 쌍은 무승부(양쪽 0.5승) 처리.
wins = Counter({i: 0.0 for i in range(len(titles))})
draws = Counter()
for (a, b), w1, w2 in results:
    if w1 == w2:
        wins[w1] += 1
    else:
        wins[a] += 0.5
        wins[b] += 0.5
        draws[a] += 1
        draws[b] += 1

print("위치 편향 제거 순위 (양쪽 순서에서 모두 이겨야 1승, 뒤집히면 무승부)\n")
for rank, (i, w) in enumerate(sorted(wins.items(), key=lambda kv: -kv[1]), 1):
    mark = "  ← 상위 5" if rank <= 5 else ""
    print(f"  {rank:>2}위  {w:>4}승 (무승부 {draws[i]:>2})  idx{i:<3} [{titles[i][0]}] {titles[i][1][:38]}{mark}")

print("\n동점 확인:", " · ".join(f"{w}승 {c}건" for w, c in sorted(Counter(wins.values()).items(), key=lambda kv: -kv[0])))
