# Docker 2일차 Notion 보고서용 모션 SVG 생성기 (점선이 흐르고 칸이 깜박이는 SVG).
# 실행: python make_figs_d2.py  → notion-figs-d2/figN-*.svg
import os, html

OUT = os.path.join(os.path.dirname(__file__), "notion-figs-d2")
os.makedirs(OUT, exist_ok=True)

TEAL, TEAL_BG, TEAL_DK = "#1f9e8f", "#dff3f0", "#085c52"
AMB, AMB_BG, AMB_DK = "#e8a33d", "#fbefd5", "#6b4710"
GRAY, GRAY_BG, INK = "#8a8177", "#f4f1ec", "#3b3630"

CSS = f"""
text {{ font-family: 'Malgun Gothic','Apple SD Gothic Neo','Noto Sans KR',sans-serif; fill:{INK}; }}
.t {{ font-size:15px; }} .s {{ font-size:12.5px; }} .b {{ font-weight:700; }} .h {{ font-size:18px; font-weight:700; }}
.m {{ font-family:Consolas,'Cascadia Mono',monospace; }}
.march {{ stroke-dasharray:6 6; animation: march .9s linear infinite; }}
@keyframes march {{ to {{ stroke-dashoffset:-12; }} }}
.blink {{ animation: blink 2.4s ease-in-out infinite; }}
@keyframes blink {{ 0%,100% {{ opacity:1; }} 50% {{ opacity:.35; }} }}
"""

def svg(name, w, h, body, extra_css=""):
    s = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<defs>
<marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{GRAY}"/></marker>
<marker id="ahT" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{TEAL}"/></marker>
</defs>
<style>{CSS}{extra_css}</style>
<rect width="{w}" height="{h}" fill="#fffdf9"/>
{body}
</svg>"""
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(s)

def esc(t): return html.escape(t, quote=False)

def box(x, y, w, h, fill, stroke, lines, cls="", sw=2, dash=False, mono_last=False, anchor="middle"):
    d = ' stroke-dasharray="5 4"' if dash else ""
    out = f'<g class="{cls}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>'
    n = len(lines)
    lh = 19
    y0 = y + h / 2 - (n - 1) * lh / 2 + 5
    for i, (t, st) in enumerate(lines):
        out += f'<text x="{x + w/2}" y="{y0 + i*lh}" text-anchor="middle" class="{st}">{esc(t)}</text>'
    return out + "</g>"

def arrow(x1, y1, x2, y2, teal=False, march=True):
    c = TEAL if teal else GRAY
    m = "ahT" if teal else "ah"
    cls = "march" if march else ""
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="2.4" class="{cls}" marker-end="url(#{m})"/>'

def text(x, y, t, cls="t", anchor="middle"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}">{esc(t)}</text>'

# ───────────────────────── 그림 1: 라이브러리 >= 와 다시 빌드 ─────────────────────────
b = text(380, 26, "「이 버전 이거나 더 새 버전이면 아무거나(>=, 이상)」로 적으면", "h")
b += text(380, 50, "빌드할 때마다 그 순간의 최신을 받는다", "h")
b += box(30, 66, 700, 44, GRAY_BG, GRAY, [("requirements.txt   fastapi>=0.115   pillow>=10.4   (실제 파일)", "t m")])
cols = [(60, "월요일", "staging에서 빌드·시험"), (290, "화요일", "라이브러리 새 버전 발표"), (520, "수요일", "main 머지 → 다시 빌드")]
for x, d, sub in cols:
    b += text(x + 90, 134, d, "t b") + text(x + 90, 154, sub, "s")
b += box(60, 164, 180, 86, TEAL_BG, TEAL, [("staging 상자", "t b"), ("fastapi 0.162", "s m"), ("(오늘 빌드 로그 값)", "s")], sw=2.5)
b += box(290, 164, 180, 86, GRAY_BG, GRAY, [("새 버전 0.163 발표", "t b"), ("(예시: 노드의 설명)", "s")], dash=True)
b += box(520, 164, 180, 86, AMB_BG, AMB, [("production 상자", "t b"), ("fastapi 0.163", "s m"), ("← 시험 안 한 새 재료", "s")], cls="blink", sw=2.5)
b += arrow(245, 207, 285, 207) + arrow(475, 207, 515, 207)
b += text(380, 280, "시험한 상자(staging) ≠ 내보낸 상자(production)  →  staging에서 한 확인이 production에 대해 아무것도 보장하지 못한다", "s b")
b += text(380, 304, "※ 0.163은 노드가 든 가상의 예시이고 이 프로젝트에서 실제로 일어난 사고가 아닙니다. 0.162는 오늘 빌드 로그의 fastapi-0.162.0.", "s")
svg("fig1-library.svg", 760, 322, b)

# ───────────────────────── 그림 2: 이미지를 만드는 곳 ─────────────────────────
b = text(380, 28, "이전 노드는 GCP가 자동으로, 이번 노드는 GitHub가 직접 이미지(상자)를 만든다", "h")
b += text(24, 62, "이전 노드 (source: .)  GCP가 만든다", "t b", "start")
xs = [18, 186, 346, 572]
w = 135
items_old = [("소스 코드", "통째로 넘김", GRAY_BG, GRAY), ("Cloud Build", "GCP가 상자를 만듦", AMB_BG, AMB),
             ("cloud-run-source-deploy", "자동 저장소 · 태그 없음", AMB_BG, AMB), ("Cloud Run", "서비스", GRAY_BG, GRAY)]
for i, (a, s, f, st) in enumerate(items_old):
    b += box(xs[i], 76, [150, 140, 205, 170][i], 62, f, st, [(a, "t b"), (s, "s")])
b += arrow(170, 107, 183, 107) + arrow(328, 107, 343, 107) + arrow(553, 107, 569, 107)
b += text(24, 200, "이번 노드 (image: …)  GitHub가 만든다", "t b", "start")
items_new = [("GitHub 커밋", "PR·CI를 거친 코드", TEAL_BG, TEAL), ("Actions 러너", "docker build + push", TEAL_BG, TEAL),
             ("friend-agent 저장소", "커밋 SHA 태그", TEAL_BG, TEAL), ("Cloud Run", "image: 로 받음", GRAY_BG, GRAY)]
for i, (a, s, f, st) in enumerate(items_new):
    b += box(xs[i], 214, [150, 140, 205, 170][i], 62, f, st, [(a, "t b"), (s, "s")])
b += arrow(170, 245, 183, 245, teal=True) + arrow(328, 245, 343, 245, teal=True) + arrow(553, 245, 569, 245, teal=True)
b += text(380, 312, "GitHub에서 만들면: 검토·테스트를 거친 커밋으로만 만들어지고, 누가 언제 만들었는지 기록이 남는다", "s b")
svg("fig2-where.svg", 760, 330, b)

# ───────────────────────── 그림 3: 태그 vs 다이제스트 ─────────────────────────
extra = """
.sticker { animation: slide 6s ease-in-out infinite; }
@keyframes slide { 0%,20% { transform: translateX(0); } 45%,70% { transform: translateX(300px); } 95%,100% { transform: translateX(0); } }
"""
b = text(380, 28, "태그는 스티커(옮겨 붙는다), 다이제스트는 지문(상자에서 안 떨어진다)", "h")
b += box(70, 74, 250, 150, TEAL_BG, TEAL, [("상자 A", "t b"), ("지문(다이제스트)", "s"), ("sha256:64c25be3bf9d…", "s m")], sw=2.5)
b += box(370, 74, 250, 150, TEAL_BG, TEAL, [("상자 B", "t b"), ("지문(다이제스트)", "s"), ("sha256:5d64baf7278c…", "s m")], sw=2.5)
b += '<g class="sticker"><rect x="100" y="186" width="190" height="30" rx="15" fill="%s" stroke="%s" stroke-width="2"/><text x="195" y="206" text-anchor="middle" class="s b m">태그: 같은 이름표</text></g>' % (AMB_BG, AMB)
b += text(195, 250, "내용이 같아야 지문이 같다 → 지문은 바뀔 수 없다", "s")
b += text(495, 250, "태그는 다른 상자로 옮겨 붙일 수 있다", "s")
b += text(380, 290, "그래서 사람이 찾을 땐 태그(커밋 SHA), 실제로 무엇이 실행 중인지는 지문(다이제스트)으로 확인한다", "s b")
b += text(380, 312, "※ 오늘 AR의 이미지는 태그가 모두 달랐음(커밋 SHA). 같은 태그가 옮겨 가는 장면은 개념 설명용입니다.", "s")
svg("fig3-tag-digest.svg", 760, 326, b, extra)

# ───────────────────────── 그림 4: 연결표 사슬 ─────────────────────────
extra = "".join(f".hl{i} {{ animation: hl 7.5s ease-in-out {i*1.0}s infinite; }}" for i in range(5)) + """
@keyframes hl { 0%,14% { opacity:1; } 18%,86% { opacity:.4; } 100% { opacity:1; } }
"""
b = text(380, 28, "연결표: 커밋에서 화면까지 한 줄로 잇는다 (production, 오늘 확인한 값)", "h")
nodes = [("커밋 SHA", "92d2c86647dd…", "GitHub 커밋", GRAY_BG, GRAY),
         ("이미지 태그", "92d2c86647dd…", "Artifact Registry", TEAL_BG, TEAL),
         ("다이제스트", "61e4310e0460…", "리비전 상세 · AR", TEAL_BG, TEAL),
         ("리비전", "…-00011-vgr", "Cloud Run", AMB_BG, AMB),
         ("화면", "v 92d2c86", "앱을 열면 보임", AMB_BG, AMB)]
xs = [20, 169, 318, 467, 616]
for i, (n, v, where, f, st) in enumerate(nodes):
    b += box(xs[i], 80, 124, 96, f, st, [(n, "t b"), (v, "s m")], cls=f"hl{i}", sw=2.5)
    b += text(xs[i] + 62, 202, "어디서 보나", "s") + text(xs[i] + 62, 220, where, "s b")
for i in range(4):
    b += arrow(xs[i] + 126, 128, xs[i + 1] - 2, 128, teal=True)
b += text(380, 258, "커밋 SHA(코드의 지문)를 태그 이름으로 쓰고, 다이제스트(이미지 내용의 지문)는 내용에서 계산된다", "s")
b += text(380, 278, "리비전이 그 다이제스트로 이미지를 고정하고, 화면에는 커밋 앞 7자리가 새겨진다", "s")
b += text(380, 304, "다섯 칸이 같은 커밋을 가리키면 「지금 production 코드는 어느 커밋인가」에 화면 몇 개로 답할 수 있다", "s b")
svg("fig4-chain.svg", 760, 324, b, extra)

# ───────────────────────── 그림 5: 다시 빌드 vs 승격 ─────────────────────────
extra = """
.travel { animation: travel 5s ease-in-out infinite; }
@keyframes travel { 0%,15% { transform: translateX(0); } 55%,85% { transform: translateX(380px); } 100% { transform: translateX(0); } }
"""
b = text(380, 28, "「한 번 만들고, 여러 환경(staging, production)에 그대로 보낸다」", "h")
b += text(24, 62, "다시 빌드 (승격 이전 방식)", "t b", "start")
b += box(40, 76, 250, 66, TEAL_BG, TEAL, [("staging 상자", "t b"), ("지문 64c25be3bf9d…", "s m")])
b += box(430, 76, 290, 66, AMB_BG, AMB, [("production 상자 (머지 때 새로 빌드)", "t b"), ("지문 6d29e8d854f1…", "s m")], cls="blink")
b += text(360, 114, "≠", "h")
b += text(24, 196, "승격 (지금: 새로 만들지 않고 그대로 보냄)", "t b", "start")
b += box(40, 212, 250, 66, GRAY_BG, GRAY, [("staging", "t b"), ("", "s")], dash=True)
b += box(430, 212, 290, 66, GRAY_BG, GRAY, [("production", "t b"), ("", "s")], dash=True)
b += '<g class="travel"><rect x="60" y="222" width="210" height="46" rx="9" fill="%s" stroke="%s" stroke-width="2.5"/><text x="165" y="241" text-anchor="middle" class="s b">같은 상자</text><text x="165" y="258" text-anchor="middle" class="s m">64c25be3bf9d…</text></g>' % (TEAL_BG, TEAL)
b += text(380, 312, "오늘 production(리비전 00011-vgr)과 staging(00009-cbp)의 다이제스트가 64자리 모두 같았다 = 61e4310e0460…", "s b")
b += text(380, 334, "※ 위쪽 지문 값은 옛 production 이미지(소스 배포)의 앞 12자리입니다.", "s")
svg("fig5-promote.svg", 760, 348, b, extra)

# ───────────────────────── 그림 6: 리비전 변천과 롤백 ─────────────────────────
extra = "".join(f".rv{i} {{ animation: pop 9s ease-out {i*0.9}s infinite both; }}" for i in range(7)) + """
@keyframes pop { 0% { opacity:0; transform: translateY(8px); } 12%,88% { opacity:1; transform: translateY(0); } 100% { opacity:0; } }
"""
b = text(380, 28, "리비전은 계속 늘어난다: 승격도 롤백도 「새 리비전 만들기」", "h")
b += text(24, 58, "production (오늘 순서)", "t b", "start")
prod = [("00008-bt5", "소스 배포", "6d29e8d854f1", GRAY_BG, GRAY), ("00009-7gr", "손으로 승격", "64c25be3bf9d", TEAL_BG, TEAL),
        ("00010-bv7", "워크플로 승격", "5d64baf7278c", TEAL_BG, TEAL), ("00011-vgr", "워크플로 승격", "61e4310e0460", TEAL_BG, TEAL)]
xs = [20, 205, 390, 575]
for i, (r, how, dg, f, st) in enumerate(prod):
    b += f'<g class="rv{i}">' + box(xs[i], 72, 165, 82, f, st, [(r, "t b m"), (how, "s"), (dg, "s m")], sw=2.5) + "</g>"
    if i < 3: b += f'<g class="rv{i+1}">' + arrow(xs[i] + 167, 113, xs[i + 1] - 2, 113, teal=True) + "</g>"
b += text(24, 206, "staging 롤백 훈련 (과제 1)", "t b", "start")
st = [("00006-ppb", "시작", "5d64baf7278c", GRAY_BG, GRAY), ("00007-jrz", "롤백 (한 커밋 전)", "64c25be3bf9d", AMB_BG, AMB), ("00008-fnl", "복구 (최신)", "5d64baf7278c", TEAL_BG, TEAL)]
xs2 = [20, 205, 390]
for i, (r, how, dg, f, s2) in enumerate(st):
    b += f'<g class="rv{i+4}">' + box(xs2[i], 220, 165, 82, f, s2, [(r, "t b m"), (how, "s"), (dg, "s m")], sw=2.5) + "</g>"
    if i < 2: b += arrow(xs2[i] + 167, 261, xs2[i + 1] - 2, 261, teal=True)
b += box(580, 220, 160, 82, GRAY_BG, GRAY, [("되돌려도 번호는 증가", "s b"), ("00006→00007→00008", "s m"), ("「복귀」가 아니라", "s"), ("새로 만든 것", "s")], dash=True)
b += text(380, 336, "롤백 중 화면은 v fc01d21, 복구 뒤 v 0304f99 (staging, 오늘 확인)", "s b")
svg("fig6-revisions.svg", 760, 352, b, extra)

# ───────────────────────── 그림 7: 정리 정책 ─────────────────────────
extra = """
.g-del { animation: gdel 9s ease-in-out infinite; }
.g-keep { animation: gkeep 9s ease-in-out infinite; }
.g-gone { animation: ggone 9s ease-in-out infinite; }
@keyframes gdel { 0%,10% { stroke-width:2; } 22%,40% { stroke-width:5; } 50%,100% { stroke-width:2; } }
@keyframes gkeep { 0%,45% { opacity:1; } 55%,70% { opacity:.55; } 80%,100% { opacity:1; } }
@keyframes ggone { 0%,70% { opacity:1; } 85%,100% { opacity:.12; } }
"""
b = text(380, 28, "정리 정책: 「7일보다 오래된 건 삭제」 + 「최근 10개는 유지」, 둘에 걸리면 유지", "h")
b += text(380, 54, "예: 이미지 15개 중 6개가 7일보다 오래됨 (노드 퀴즈)", "s")
sx = 28; sw_ = 40; gap = 7
b += text(24, 88, "오래된 쪽 ← → 최근", "s", "start")
for i in range(15):
    x = sx + i * (sw_ + gap)
    old = i < 6          # 7일 넘음(삭제 조건)
    keep = i >= 5        # 최근 10개(유지 조건)
    fill = GRAY_BG if i < 5 else TEAL_BG
    stroke = AMB if old else TEAL
    cls = "g-gone" if i < 5 else ""
    b += f'<g class="{cls}"><rect class="{"g-del" if old else ""}" x="{x}" y="100" width="{sw_}" height="54" rx="7" fill="{fill}" stroke="{stroke}" stroke-width="2"/><text x="{x+sw_/2}" y="132" text-anchor="middle" class="s b">{i+1}</text></g>'
b += box(28, 178, 292, 44, AMB_BG, AMB, [("삭제 조건: 7일 넘음 → 1~6번 (노랑 테두리)", "s b")])
b += box(340, 178, 392, 44, TEAL_BG, TEAL, [("유지 조건: 최근 10개 → 6~15번 (초록)", "s b")], cls="g-keep")
b += text(380, 258, "6번은 두 조건에 모두 걸림 → 유지.  지워지는 것은 1~5번 = 5개", "t b")
b += text(380, 284, "오늘 실제 상태: 두 저장소에 정책 2개를 --dry-run으로 적용 (실제 삭제 없음, 후보 0개로 계산, 결과는 하루 뒤 감사 로그)", "s")
b += text(380, 306, "※ 「최근 10개」는 저장소 전체가 아니라 패키지(이미지 이름)마다 센다 (공식 문서)", "s")
svg("fig7-cleanup.svg", 760, 322, b, extra)

# ───────────────────────── 그림 8: slim vs 전체 크기 ─────────────────────────
extra = """
.bar1 { transform-box: fill-box; transform-origin: left; animation: grow1 6s ease-out infinite; }
.bar2 { transform-box: fill-box; transform-origin: left; animation: grow2 6s ease-out infinite; }
@keyframes grow1 { 0% { transform: scaleX(0); } 20%,90% { transform: scaleX(1); } 100% { transform: scaleX(0); } }
@keyframes grow2 { 0%,10% { transform: scaleX(0); } 45%,90% { transform: scaleX(1); } 100% { transform: scaleX(0); } }
"""
b = text(380, 28, "FROM 한 줄만 바꿨더니 이미지가 약 3.8배", "h")
b += text(24, 70, "slim 기반", "t b", "start")
b += f'<rect class="bar1" x="130" y="52" width="164" height="30" rx="6" fill="{TEAL}"/>'
b += text(306, 73, "431MB", "t b", "start")
b += text(24, 130, "전체판 기반", "t b", "start")
b += f'<rect class="bar2" x="130" y="112" width="620" height="30" rx="6" fill="{AMB}"/>'
b += text(560, 133, "1.63GB", "t b")
b += text(380, 190, "코드·설치 목록은 같고 FROM python:3.13-slim-bookworm → python:3.13-bookworm 한 줄만 다름 (+약 1.2GB)", "s b")
b += text(380, 222, "※ 위는 로컬 크기(압축 풀린 값). AR에는 압축해서 저장: slim 기반 이미지가 약 106MiB(111,483,083바이트)였다.", "s")
b += text(380, 244, "전체판 베이스만 내려받은 양이 약 383MB(압축) → 이미지 하나가 무료 0.5GB의 약 77% 이상일 것으로 추정", "s")
b += text(380, 264, "(push해 보지 않아 실제 압축 크기는 모름)", "s")
svg("fig8-size.svg", 760, 282, b, extra)

print("완료:", sorted(os.listdir(OUT)))
