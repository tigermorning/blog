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
    """first를 A 자리에, second를 B 자리에 놓고 물어본 뒤 '이긴 기사 인덱스'를 돌려준다."""
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
    return pair, ask(a, b), ask(b, a)      # 정순 / 역순, 같은 쌍

with ThreadPoolExecutor(max_workers=8) as ex:
    results = list(ex.map(both_orders, pairs))

agree = [p for p, w1, w2 in results if w1 == w2]
flip  = [(p, w1, w2) for p, w1, w2 in results if w1 != w2]

first_slot = Counter()                      # 뒤집었을 때도 'A 자리'를 골랐는지
for (a, b), w1, w2 in results:
    first_slot["A자리" if w1 == a else "B자리"] += 1
    first_slot["A자리" if w2 == b else "B자리"] += 1

print(f"호출 횟수: {len(pairs) * 2}번 (쌍마다 정순 + 역순)\n")
print(f"판정 일치: {len(agree)}/{len(pairs)}쌍  ({len(agree)/len(pairs):.0%})")
print(f"순서만 바꿨는데 뒤집힘: {len(flip)}쌍  ({len(flip)/len(pairs):.0%})")
print(f"전체 132번 중 'A 자리' 선택 {first_slot['A자리']}번 / 'B 자리' 선택 {first_slot['B자리']}번")

if flip:
    print("\n뒤집힌 쌍 — 모델이 자기 판정을 스스로 뒤집은 것들")
    for (a, b), w1, w2 in flip:
        print(f"  idx{a} vs idx{b}")
        print(f"      정순 승자: [{titles[w1][0]}] {titles[w1][1][:40]}")
        print(f"      역순 승자: [{titles[w2][0]}] {titles[w2][1][:40]}")

# 동점이던 5/6위 경계, 맞대결 결과
h2h = [(w1, w2) for p, w1, w2 in results if set(p) == {3, 6}][0]
print(f"\n5위/6위 동점(6승 2건) 맞대결 idx3 vs idx6 -> 정순 승자 idx{h2h[0]}, 역순 승자 idx{h2h[1]}")
