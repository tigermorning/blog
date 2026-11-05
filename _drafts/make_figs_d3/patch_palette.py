import re, sys
sp = sys.argv[1]

def sub_once(s, old, new):
    assert s.count(old) == 1, ("not unique/found", old[:50], s.count(old))
    return s.replace(old, new)

p = sp + r"\make_gifs.py"
s = open(p, encoding="utf-8").read()
old_const = s[s.index("BG = (246, 250, 250)"):s.index("_fc = {}")]
new_const = '''BG = (250, 249, 246); INK = (48, 44, 40); MUTE = (138, 129, 119)
TEAL = (98, 92, 84); AMBER = (232, 163, 61); BLUE = (31, 158, 143)
GREEN = (232, 163, 61); RED = (217, 83, 79); WHITE = (255, 255, 255)
LINE = (214, 208, 198); LTEAL = (244, 241, 236); LAMB = (251, 239, 213)
LRED = (252, 234, 232); LGRAY = (244, 241, 236); DARK = (44, 40, 36)
GOOD = (24, 120, 108); WARN = (168, 105, 8); LBLUE = (223, 243, 240)

'''
s = s.replace(old_const, new_const)
s = sub_once(s, 'cv.text(cx, y0 + 46, status, 15, tcolor if state != "active" else color, state == "active", "mm")',
             'cv.text(cx, y0 + 46, status, 15, tcolor if state != "active" else mix(color, INK, 0.4), state == "active", "mm")')
s = sub_once(s, 'cv.text(960, 108, "성공 %d" % succ, 20, GREEN, True, "ra")',
             'cv.text(960, 108, "성공 %d" % succ, 20, GOOD, True, "ra")')
open(p, "w", encoding="utf-8").write(s)

p = sp + r"\make_all.py"
s = open(p, encoding="utf-8").read()
s = sub_once(s, "colr = TEAL", 'colr = BLUE if nm == "blue" else GREEN')
s = sub_once(s, 'cv.text(960, 108, "끊긴 요청 0건", 20, GREEN, True, "ra")', 'cv.text(960, 108, "끊긴 요청 0건", 20, GOOD, True, "ra")')
s = sub_once(s, 'cv.text(872, 369, "헬스체크: 정상", 17, GREEN, True, "mm")', 'cv.text(872, 369, "헬스체크: 정상", 17, GOOD, True, "mm")')
s = sub_once(s, 'cv.text(670, GY1 + 14, "약속이 보임", 15, GREEN, True, "mm")', 'cv.text(670, GY1 + 14, "약속이 보임", 15, GOOD, True, "mm")')
s = sub_once(s, "fill, col = GREEN, WHITE", "fill, col = GOOD, WHITE")
a = s.index("def caption_for"); b = s.index("def draw_cfg")
seg = s[a:b].replace(", GREEN),", ", GOOD),").replace(", AMBER),", ", WARN),")
s = s[:a] + seg + s[b:]
open(p, "w", encoding="utf-8").write(s)
print("patched")
