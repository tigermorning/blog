import re, sys
sp = sys.argv[1]

def rd(n):
    return open(sp + "\\" + n, encoding="utf-8").read()

def wr(n, s):
    open(sp + "\\" + n, "w", encoding="utf-8").write(s)

def sub1(s, a, b, n=1):
    assert s.count(a) == n, ("count", s.count(a), a[:70])
    return s.replace(a, b)

# ---------------------------------------------------------------- make_gifs_p
g = rd("make_gifs.py")
a = g.index("BG = (250, 249, 246)")
b = g.index("_fc = {}")
pal = '''BG = (253, 250, 244); INK = (58, 54, 66); MUTE = (130, 126, 140)
TEAL = (150, 114, 210); AMBER = (250, 190, 80); BLUE = (91, 156, 240)
GREEN = (88, 196, 140); RED = (236, 104, 104); WHITE = (255, 255, 255)
LINE = (222, 216, 230); LTEAL = (237, 228, 250); LAMB = (255, 243, 205)
LRED = (253, 228, 228); LGRAY = (244, 241, 248); DARK = (53, 57, 84)
GOOD = (36, 130, 90); WARN = (190, 110, 20); LBLUE = (219, 234, 254)
LGREEN = (213, 245, 228); BLUE_T = (40, 100, 190); GREEN_T = (30, 130, 90)

'''
g = g[:a] + pal + g[b:]
g = sub1(g, "    durs = [100] * len(frames)\n    durs[0] = 700\n    durs[-1] = 2200",
         "    durs = [130] * len(frames)\n    durs[0] = 900\n    durs[-1] = 3000")
g += '''

# ---- 파스텔 구성 요소 (덮어쓰기)
USER_A, USER_F = (240, 190, 80), (255, 243, 205)
DB_A, DB_F = (236, 132, 158), (253, 228, 232)

def user(cv, x, y, label="사용자"):
    cv.circ(x, y, 30, fill=USER_F, outline=USER_A, w=3)
    cv.circ(x, y - 9, 9, fill=USER_A)
    cv.rr(x - 15, y + 4, x + 15, y + 21, 8, fill=USER_A)
    cv.text(x, y + 40, label, 16, INK, True, "ma")

def server_box(cv, x0, y0, x1, y1, name, status, color, state="active"):
    cx = (x0 + x1) / 2
    if state == "dead":
        cv.rr(x0, y0, x1, y1, 14, fill=LRED, outline=RED, w=4)
        xmark(cv, cx, y0 + 79, 13, RED, 5)
        cv.text(cx, y0 + 22, name, 20, RED, True, "mm")
        cv.text(cx, y0 + 46, status, 15, RED, False, "mm")
        return
    if state == "active":
        fill, outline, tc, sc = mix(WHITE, color, 0.28), color, INK, mix(color, INK, 0.5)
    elif state == "dim":
        fill, outline, tc, sc = LGRAY, LINE, MUTE, MUTE
    else:
        fill, outline, tc, sc = LRED, RED, RED, RED
    cv.rr(x0, y0, x1, y1, 14, fill=fill, outline=outline, w=4)
    cv.text(cx, y0 + 22, name, 20, tc, True, "mm")
    cv.text(cx, y0 + 46, status, 15, sc, state == "active", "mm")

def cylinder(cv, cx, y0, y1, w=84, color=DB_A, label="DB"):
    x0, x1 = cx - w / 2, cx + w / 2
    cv.rr(x0, y0 + 10, x1, y1 - 10, 4, fill=DB_F, outline=None)
    cv.line(x0, y0 + 10, x0, y1 - 10, color, 4)
    cv.line(x1, y0 + 10, x1, y1 - 10, color, 4)
    cv.d.ellipse([x0 * S, (y1 - 22) * S, x1 * S, y1 * S], fill=DB_F, outline=color, width=4 * S // 1)
    cv.rr(x0 + 2, y0 + 12, x1 - 2, y1 - 12, 2, fill=DB_F)
    cv.d.ellipse([x0 * S, y0 * S, x1 * S, (y0 + 22) * S], fill=WHITE, outline=color, width=4 * S // 1)
    cv.text(cx, (y0 + y1) / 2 + 2, label, 18, (190, 90, 120), True, "mm")

def card(cv, cx, cy, color=AMBER, alpha=1.0, w=96):
    cv.rr(cx - w / 2, cy - 13, cx + w / 2, cy + 13, 8, fill=mix(BG, (255, 238, 190), alpha),
          outline=mix(BG, color, alpha), w=2)
    cv.text(cx, cy, "8시 물 마시기", 13, mix(BG, (130, 80, 0), alpha), True, "mm")
'''
wr("make_gifs_p.py", g)

# ---------------------------------------------------------------- make_figs_d3_p
f = rd("make_figs_d3.py").replace("from make_gifs import *", "from make_gifs_p import *")
f = sub1(f, 'cv.text(BX0, 112, "blue (지금 버전)", 15, GOOD, True, "lm")', 'cv.text(BX0, 112, "blue (지금 버전)", 15, BLUE_T, True, "lm")')
f = sub1(f, 'cv.text(BX1, 112, "green (새 버전)", 15, WARN, True, "rm")', 'cv.text(BX1, 112, "green (새 버전)", 15, GREEN_T, True, "rm")')
f = sub1(f, 'cv.rr(BX1 - wg - 0, y, BX1, y + 54, 10 if wg > 20 else 3, fill=AMBER)', 'cv.rr(BX1 - wg - 0, y, BX1, y + 54, 10 if wg > 20 else 3, fill=GREEN)')
f = sub1(f, 'int(g * 100), 20, WARN, True, "lm")', 'int(g * 100), 20, GREEN_T, True, "lm")')
lines = f.split("\n")
for i, ln in enumerate(lines):
    if '["새 리비전"]' in ln or ln.strip().startswith("cv.arrow(440, 380"):
        lines[i] = ln.replace("AMBER", "GREEN")
f = "\n".join(lines)
wr("make_figs_d3_p.py", f)

# ---------------------------------------------------------------- make_figs_d3b_p
h = rd("make_figs_d3b.py").replace("from make_figs_d3 import", "from make_figs_d3_p import").replace("from make_gifs import *", "from make_gifs_p import *")
h = sub1(h, 'LBLUE if l == "blue" else LAMB,\n                     GOOD if l == "blue" else WARN, 14)',
         'LBLUE if l == "blue" else LGREEN,\n                     BLUE_T if l == "blue" else GREEN_T, 14)')
h = sub1(h, 'GOOD if nxt(ct) == "blue" else WARN, True, "mm")', 'BLUE_T if nxt(ct) == "blue" else GREEN_T, True, "mm")')
wr("make_figs_d3b_p.py", h)

# ---------------------------------------------------------------- make_figs_d3c_p
c = rd("make_figs_d3c.py").replace("from make_figs_d3 import", "from make_figs_d3_p import").replace("from make_gifs import *", "from make_gifs_p import *")
c = sub1(c, 'ROWCOL = {"blue": BLUE, "green": AMBER, "spare": MUTE}', 'ROWCOL = {"blue": BLUE, "green": GREEN, "spare": MUTE}')
wr("make_figs_d3c_p.py", c)
print("built")
