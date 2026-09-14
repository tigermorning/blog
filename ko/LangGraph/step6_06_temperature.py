import json, statistics
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
client = OpenAI()

titles = [tuple(x) for x in json.loads(
    Path(__file__).with_name("step6_titles.json").read_text(encoding="utf-8"))]

RUBRIC = ("당신은 국내 개발팀을 위한 AI 뉴스레터 편집자입니다."
          "아래 기사 제목이 '이번 주 우리가 일하는 방식이 바뀔 만한가'라는 "
          "기준에서 얼마나 중요한지 1~10점으로 매기세요. 숫자만 답하세요.")

REPEATS = 3

def score(job):
    i, temp = job
    r = client.chat.completions.create(
        model="gpt-4.1-mini", temperature=temp, max_tokens=5,
        messages=[{"role": "system", "content": RUBRIC},
                  {"role": "user", "content": titles[i][1]}])
    return i, temp, int(r.choices[0].message.content.strip())

def run_all(temp):
    jobs = [(i, temp) for _ in range(REPEATS) for i in range(len(titles))]
    with ThreadPoolExecutor(max_workers=8) as ex:
        out = list(ex.map(score, jobs))
    runs = [{} for _ in range(REPEATS)]
    seen = {}
    for i, _, s in out:
        k = seen.get(i, 0)
        runs[k][i] = s
        seen[i] = k + 1
    return runs

def report(temp, runs):
    print(f"\n{'='*66}\ntemperature = {temp}  ({REPEATS}회 반복)\n{'='*66}")
    print(f"{'idx':<5}{'1회':<5}{'2회':<5}{'3회':<5}{'표준편차':<10}제목")
    unstable = 0
    for i in range(len(titles)):
        vals = [runs[k][i] for k in range(REPEATS)]
        sd = statistics.pstdev(vals)
        if sd > 0:
            unstable += 1
        flag = " *" if sd > 0 else "  "
        print(f"{i:<5}{vals[0]:<5}{vals[1]:<5}{vals[2]:<5}{sd:<10.2f}{flag}{titles[i][1][:34]}")
    print(f"\n점수가 흔들린 기사: {unstable}/{len(titles)}건  (* 표시)")

    tops = []
    for k in range(REPEATS):
        order = sorted(range(len(titles)), key=lambda i: -runs[k][i])[:5]
        tops.append(order)
        print(f"  {k+1}회차 상위 5건 idx: {order}")
    common = set(tops[0]) & set(tops[1]) & set(tops[2])
    union = set(tops[0]) | set(tops[1]) | set(tops[2])
    print(f"  3회 모두 상위 5건에 든 기사: {len(common)}건 {sorted(common)}")
    print(f"  한 번이라도 상위 5건에 든 기사: {len(union)}건 {sorted(union)}")

for temp in (0, 0.7):
    report(temp, run_all(temp))
