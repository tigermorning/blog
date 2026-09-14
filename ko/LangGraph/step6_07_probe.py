import json
from pathlib import Path
from collections import Counter
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(Path(__file__).resolve().parent.parent / ".env")
client = OpenAI()
titles = [tuple(x) for x in json.loads(
    Path(__file__).with_name("step6_titles.json").read_text(encoding="utf-8"))]

RUBRIC = ("당신은 국내 개발팀을 위한 AI 뉴스레터 편집자입니다."
          "아래 기사 제목이 '이번 주 우리가 일하는 방식이 바뀔 만한가'라는 "
          "기준에서 얼마나 중요한지 1~10점으로 매기세요. 숫자만 답하세요.")

# 1) 한 기사만 붙잡고 temperature 별로 10번씩, 순차 호출
for idx in (7, 0):
    print(f"\nidx{idx}  {titles[idx][1][:50]}")
    for temp in (0, 0.7, 1.5):
        vals = []
        for _ in range(10):
            r = client.chat.completions.create(
                model="gpt-4.1-mini", temperature=temp, max_tokens=5,
                messages=[{"role": "system", "content": RUBRIC},
                          {"role": "user", "content": titles[idx][1]}])
            vals.append(r.choices[0].message.content.strip())
        print(f"  temp={temp:<4} {vals}  분포 {dict(Counter(vals))}")

# 2) 모델이 실제로 어떤 확률분포를 갖고 있는지 직접 확인
print("\n\n토큰 확률 (temperature=1, 상위 5개 후보)")
for idx in (7, 0, 3):
    r = client.chat.completions.create(
        model="gpt-4.1-mini", temperature=1, max_tokens=1,
        logprobs=True, top_logprobs=5,
        messages=[{"role": "system", "content": RUBRIC},
                  {"role": "user", "content": titles[idx][1]}])
    tl = r.choices[0].logprobs.content[0].top_logprobs
    dist = " · ".join(f"{t.token!r} {pow(2.718281828, t.logprob):.3%}" for t in tl)
    print(f"  idx{idx}: {dist}")
