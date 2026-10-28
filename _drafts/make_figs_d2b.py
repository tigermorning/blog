# Docker 2일차 보고서 추가 모션 그림 (글자 크게): 4-1 SHA·태그·다이제스트 구분, 4-2 화면 v 값이 생기는 과정
import os, html

OUT = os.path.join(os.path.dirname(__file__), "notion-figs-d2")
TEAL, TEAL_BG, TEAL_DK = "#1f9e8f", "#dff3f0", "#085c52"
AMB, AMB_BG, AMB_DK = "#e8a33d", "#fbefd5", "#6b4710"
GRAY, GRAY_BG, INK = "#8a8177", "#f4f1ec", "#3b3630"

CSS = f"""
text {{ font-family: 'Malgun Gothic','Apple SD Gothic Neo','Noto Sans KR',sans-serif; fill:{INK}; }}
.t {{ font-size:24px; }} .s {{ font-size:20px; }} .b {{ font-weight:700; }} .h {{ font-size:28px; font-weight:700; }}
.m {{ font-family:Consolas,'Cascadia Mono',monospace; font-size:23px; }}
.march {{ stroke-dasharray:8 8; animation: march .75s linear infinite; }}
@keyframes march {{ to {{ stroke-dashoffset:-16; }} }}
"""

def esc(t): return html.escape(t, quote=False)

def svg(name, w, h, body, extra=""):
    s = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<defs>
<marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{GRAY}"/></marker>
<marker id="ahT" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{TEAL}"/></marker>
<marker id="ahA" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{AMB}"/></marker>
</defs>
<style>{CSS}{extra}</style>
<rect width="{w}" height="{h}" fill="#fffdf9"/>
{body}
</svg>"""
    open(os.path.join(OUT, name), "w", encoding="utf-8").write(s)

def T(x, y, t, cls="t", anchor="middle"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{cls}">{esc(t)}</text>'

def R(x, y, w, h, fill, stroke, sw=3, dash=False, rx=14):
    d = ' stroke-dasharray="8 6"' if dash else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>'

# ───────── 그림 4-1: 커밋 SHA · 태그 · 다이제스트 구분 ─────────
extra = """
.copy { animation: copy 6s ease-in-out infinite; }
@keyframes copy {
  0%,10% { transform: translate(0,0); opacity:1; }
  42% { transform: translate(425px,-15px); opacity:1; }
  78% { transform: translate(425px,-15px); opacity:1; }
  90%,100% { transform: translate(425px,-15px); opacity:0; }
}
.tagshow { animation: tagshow 6s ease-in-out infinite; }
@keyframes tagshow { 0%,41% { opacity:0; } 46%,88% { opacity:1; } 96%,100% { opacity:0; } }
.dig { animation: dig 6s ease-in-out infinite; }
@keyframes dig { 0%,52% { opacity:0; transform: scale(.85); } 62%,88% { opacity:1; transform: scale(1); } 96%,100% { opacity:0; } }
.dig { transform-box: fill-box; transform-origin: center; }
.pulse { animation: pulse 6s ease-in-out infinite; }
@keyframes pulse { 0%,40% { opacity:1; } 50%,80% { opacity:.55; } 90%,100% { opacity:1; } }
"""
b = T(380, 44, "SHA·태그·다이제스트는 이렇게 다르다", "h")
# 왼쪽: 커밋(코드)
b += R(24, 100, 270, 220, GRAY_BG, GRAY)
b += T(159, 142, "커밋 (코드)", "t b")
b += T(159, 182, "커밋 SHA", "s")
b += T(159, 226, "92d2c86647dd…", "m b")
b += T(159, 270, "코드의 지문", "s")
b += T(159, 298, "git이 자동으로 만든다", "s")
# 오른쪽: 이미지(상자)
b += R(430, 84, 306, 380, TEAL_BG, TEAL, sw=3.5)
b += T(583, 124, "이미지 (상자)", "t b")
b += R(450, 142, 266, 104, "#ffffff", AMB, sw=3, dash=True)
b += T(583, 172, "태그 (이름표)", "s b")
b += R(450, 290, 266, 154, "#ffffff", TEAL, sw=3, dash=True)
b += T(583, 318, "다이제스트 (지문)", "s b")
b += T(583, 426, "내용에서 자동 계산", "s")
# 복사되는 태그 알약 (왼쪽 SHA에서 → 태그 칸으로)
pill = lambda x, y: f'<rect x="{x}" y="{y}" width="236" height="42" rx="21" fill="{AMB_BG}" stroke="{AMB}" stroke-width="3"/><text x="{x+118}" y="{y+29}" text-anchor="middle" class="m b">92d2c86647dd…</text>'
b += f'<g class="copy">{pill(40, 194)}</g>'
# 화살표(복사 방향 표시)
b += f'<line x1="296" y1="210" x2="426" y2="168" stroke="{AMB}" stroke-width="3.5" class="march" marker-end="url(#ahA)"/>'
b += T(361, 176, "복사", "s b")
# 다이제스트 알약 (이미지 안에서 자동 생성)
b += f'<g class="dig"><rect x="465" y="338" width="236" height="46" rx="23" fill="{TEAL_BG}" stroke="{TEAL}" stroke-width="3"/><text x="583" y="369" text-anchor="middle" class="m b">61e4310e0460…</text></g>'
# 아래 요약 두 줄
b += T(380, 512, "태그 = SHA를 복사한 이름표 → 글자가 같다", "t b")
b += T(380, 552, "다이제스트 = 이미지 내용에서 따로 계산 → 글자가 다르다", "t b")
svg("fig4-1-names.svg", 760, 584, b, extra)

# ───────── 그림 4-2: 화면의 v 값이 생기는 과정 ─────────
extra = "".join(f".hl{i} {{ animation: hl 7.5s ease-in-out {i*1.2}s infinite; }}" for i in range(4)) + """
@keyframes hl { 0%,14% { opacity:1; } 18%,86% { opacity:.38; } 100% { opacity:1; } }
.swap1 { animation: swap1 7.5s ease-in-out infinite; }
.swap2 { animation: swap2 7.5s ease-in-out infinite; }
@keyframes swap1 { 0%,30% { opacity:1; } 38%,92% { opacity:0; } 100% { opacity:1; } }
@keyframes swap2 { 0%,30% { opacity:0; } 38%,92% { opacity:1; } 100% { opacity:0; } }
"""
b = T(380, 46, "화면의 v 값은 이렇게 생긴다", "h")
# 1. index.html
b += f'<g class="hl0">{R(60, 78, 640, 108, GRAY_BG, GRAY)}{T(380, 114, "① index.html에 미리 적어 둔 자리 표시", "t b")}{T(380, 160, "var v=\'__COMMIT__\'", "m b")}</g>'
# 2. sed
b += f'<line x1="380" y1="190" x2="380" y2="226" stroke="{AMB}" stroke-width="4" class="march" marker-end="url(#ahA)"/>'
b += f'<g class="hl1">{R(60, 232, 640, 132, AMB_BG, AMB)}{T(380, 270, "② 배포할 때 sed가 글자를 바꾼다", "t b")}{T(380, 308, "__COMMIT__ → 커밋 앞 7자리", "t")}{T(380, 346, "(글자 교체 명령 = sed)", "s")}</g>'
# 3. 이미지 안의 파일 (글자가 바뀌는 연출)
b += f'<line x1="380" y1="368" x2="380" y2="404" stroke="{TEAL}" stroke-width="4" class="march" marker-end="url(#ahT)"/>'
b += f'<g class="hl2">{R(60, 410, 640, 108, TEAL_BG, TEAL)}{T(380, 446, "③ 이미지 안에 들어간 파일", "t b")}<g class="swap1">{T(380, 494, "var v=\'__COMMIT__\'", "m b")}</g><g class="swap2">{T(380, 494, "var v=\'92d2c86\'", "m b")}</g></g>'
# 4. 화면
b += f'<line x1="380" y1="522" x2="380" y2="558" stroke="{TEAL}" stroke-width="4" class="march" marker-end="url(#ahT)"/>'
b += f'<g class="hl3">{R(60, 564, 640, 132, "#ffffff", TEAL, sw=4)}{R(60, 564, 640, 40, TEAL_BG, TEAL, sw=4, rx=14)}{T(380, 592, "④ 앱 화면 (구석)", "t b")}<rect x="256" y="624" width="248" height="56" rx="12" fill="{TEAL_BG}" stroke="{TEAL}" stroke-width="3"/>{T(380, 662, "v 92d2c86", "m b")}</g>'
svg("fig4-2-screen.svg", 760, 720, b, extra)
print("완료")
