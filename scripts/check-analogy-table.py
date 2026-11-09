"""비유 절의 줄글(대비표 바로 위 문단)에 표 왼쪽 칸 요소가 나오는지 낱말로 점검한다(후보만 알려 줌 — 같은 뜻의 다른 낱말이면 오탐이니 사람이 읽고 판단).
사용: python scripts/check-analogy-table.py            (ko 전체)
규칙 출처: .claude/skills/tigermorning-blog-post/SKILL.md «줄글과 대비표는 양방향 1:1» (2026-11-09 사용자 지적)
"""
import re,glob,html,json,os
def txt(t): return re.sub(r"\s+"," ",html.unescape(re.sub(r"<[^>]+>"," ",t))).strip()
STOP=set("그리고 하지만 그래서 있어요 해요 이에요 예요 에서 으로 에게 처럼 하는 하고 해서 되는 같은 모든 어떤 하나 우리 그냥 아직 이미 먼저 다시 또는 때문".split())
def words(cell):
    ws=re.findall(r"[가-힣A-Za-z0-9_.]{2,}",cell)
    return [w for w in ws if w not in STOP]
res=[]
for f in sorted(glob.glob("ko/*.html")):
    if "beginner-python" in f: continue
    s=open(f,encoding="utf8").read()
    if "<main>" not in s: continue
    s=s[s.index("<main>"):]
    for m in re.finditer(r"<table[^>]*>\s*<thead>\s*<tr>\s*<th[^>]*>\s*비유 속 요소",s):
        t0=m.start()
        # 비유 상황 줄글: 표 직전 가장 가까운 h2/h3 이후부터 표 앞까지
        pre=s[:t0]; h=[x for x in re.finditer(r"<h[23][^>]*>",pre)]
        start=h[-1].start() if h else 0
        para=txt(pre[start:])
        end=s.index("</table>",t0)
        rows=re.findall(r"<tr[^>]*>(.*?)</tr>",s[t0:end],re.S)[1:]
        miss=[]
        for r in rows:
            cells=re.findall(r"<td[^>]*>(.*?)</td>",r,re.S)
            if len(cells)<2: continue
            left=txt(cells[0]); ws=words(left.split(" — ")[0] if " — " in left else left)
            if not ws: continue
            if not any(w[:3] in para or w in para for w in ws): miss.append(left[:60])
        res.append((f,len(rows),len(miss),miss,len(para)))
bad=[r for r in res if r[2]]
print("tables",len(res),"with-unmatched-rows",len(bad),"rows-total",sum(r[1] for r in res),"unmatched-rows",sum(r[2] for r in res))
for f,n,k,miss,pl in bad[:200]: print(f[3:34],f"{k}/{n}", "|", " ; ".join(miss)[:150])
