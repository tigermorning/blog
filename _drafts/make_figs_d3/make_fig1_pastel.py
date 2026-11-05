import sys, os
sys.argv = [sys.argv[0], sys.argv[1]]
import make_gifs as mg
import make_all as ma
from PIL import Image

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
os.makedirs(os.path.join(OUT, "preview"), exist_ok=True)

P = dict(BG=(253, 250, 244), INK=(58, 54, 66), MUTE=(130, 126, 140), TEAL=(150, 114, 210),
         AMBER=(250, 190, 80), BLUE=(91, 156, 240), GREEN=(88, 196, 140), RED=(236, 104, 104),
         LINE=(222, 216, 230), LTEAL=(237, 228, 250), LAMB=(255, 243, 205), LRED=(253, 228, 228),
         LGRAY=(244, 241, 248), DARK=(53, 57, 84), GOOD=(36, 130, 90), WARN=(190, 110, 20),
         LBLUE=(219, 234, 254))
for mod in (mg, ma):
    for k, v in P.items():
        setattr(mod, k, v)

WHITE = (255, 255, 255)
USER_A, USER_F = (240, 190, 80), (255, 243, 205)
DB_A, DB_F = (236, 132, 158), (253, 228, 232)

def user(cv, x, y, label="사용자"):
    cv.circ(x, y, 30, fill=USER_F, outline=USER_A, w=3)
    cv.circ(x, y - 9, 9, fill=USER_A)
    cv.rr(x - 15, y + 4, x + 15, y + 21, 8, fill=USER_A)
    cv.text(x, y + 40, label, 16, P["INK"], True, "ma")

def server_box(cv, x0, y0, x1, y1, name, status, color, state="active"):
    cx = (x0 + x1) / 2
    if state == "dead":
        cv.rr(x0, y0, x1, y1, 14, fill=P["LRED"], outline=P["RED"], w=4)
        ma.xmark(cv, cx, y0 + 79, 13, P["RED"], 5)
        cv.text(cx, y0 + 22, name, 20, P["RED"], True, "mm")
        cv.text(cx, y0 + 46, status, 15, P["RED"], False, "mm")
        return
    if state == "active":
        fill, outline, tc, sc = mg.mix(WHITE, color, 0.28), color, P["INK"], mg.mix(color, P["INK"], 0.5)
    elif state == "dim":
        fill, outline, tc, sc = P["LGRAY"], P["LINE"], P["MUTE"], P["MUTE"]
    else:
        fill, outline, tc, sc = P["LRED"], P["RED"], P["RED"], P["RED"]
    cv.rr(x0, y0, x1, y1, 14, fill=fill, outline=outline, w=4)
    cv.text(cx, y0 + 22, name, 20, tc, True, "mm")
    cv.text(cx, y0 + 46, status, 15, sc, state == "active", "mm")

def cylinder(cv, cx, y0, y1, w=84, color=DB_A, label="DB"):
    S = mg.S
    x0, x1 = cx - w / 2, cx + w / 2
    cv.rr(x0, y0 + 10, x1, y1 - 10, 4, fill=DB_F, outline=None)
    cv.line(x0, y0 + 10, x0, y1 - 10, color, 4)
    cv.line(x1, y0 + 10, x1, y1 - 10, color, 4)
    cv.d.ellipse([x0 * S, (y1 - 22) * S, x1 * S, y1 * S], fill=DB_F, outline=color, width=4 * S // 1)
    cv.rr(x0 + 2, y0 + 12, x1 - 2, y1 - 12, 2, fill=DB_F)
    cv.d.ellipse([x0 * S, y0 * S, x1 * S, (y0 + 22) * S], fill=WHITE, outline=color, width=4 * S // 1)
    cv.text(cx, (y0 + y1) / 2 + 2, label, 18, (190, 90, 120), True, "mm")

def card(cv, cx, cy, color=P["AMBER"], alpha=1.0, w=96):
    cv.rr(cx - w / 2, cy - 13, cx + w / 2, cy + 13, 8, fill=mg.mix(P["BG"], (255, 238, 190), alpha),
          outline=mg.mix(P["BG"], color, alpha), w=2)
    cv.text(cx, cy, "8시 물 마시기", 13, mg.mix(P["BG"], (130, 80, 0), alpha), True, "mm")

def tracker(cv, i):
    names = ["이중화", "블루그린", "Nginx", "무상태"]
    acc = [(250, 170, 150), (110, 170, 245), (170, 135, 225), (100, 205, 150)]
    pas = [(255, 232, 224), (222, 236, 255), (238, 229, 250), (218, 246, 232)]
    cur = ma.stage_of(i)
    x = 40
    for k, n in enumerate(names):
        w = cv.d.textlength(n, font=mg.font(16, True)) / mg.S + 30
        if i >= ma.END - 14:
            fill, outline = acc[k], acc[k]
        elif k == cur:
            fill, outline = acc[k], acc[k]
        elif k < cur:
            fill, outline = pas[k], acc[k]
        else:
            fill, outline = (246, 244, 249), (232, 228, 238)
        cv.rr(x, 102, x + w, 134, 16, fill=fill, outline=outline, w=2)
        cv.text(x + w / 2, 118, n, 16, P["INK"] if (k <= cur or i >= ma.END - 14) else P["MUTE"], True, "mm")
        x += w + 10

for mod in (mg, ma):
    mod.user = user
    mod.server_box = server_box
    mod.cylinder = cylinder
    mod.card = card
ma.tracker = tracker

def save_slow(name, frames, dur=130):
    stride = max(1, len(frames) // 14)
    sample = Image.new("RGB", (mg.W, mg.H * len(frames[::stride])))
    for k, f in enumerate(frames[::stride]):
        sample.paste(f, (0, k * mg.H))
    pal = sample.quantize(colors=255, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    q = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in frames]
    durs = [dur] * len(frames)
    durs[0] = 900
    durs[-1] = 3000
    path = os.path.join(OUT, name)
    q[0].save(path, save_all=True, append_images=q[1:], duration=durs, loop=0, disposal=1, optimize=False)
    for idx in (52, 100, 136, 190, 232, 262, 296, 330):
        if idx < len(frames):
            frames[idx].save(os.path.join(OUT, "preview", "p_%03d.png" % idx))
    total = sum(durs) / 1000
    print(name, len(frames), "frames", os.path.getsize(path) // 1024, "KB", "총", round(total, 1), "초")

if __name__ == "__main__":
    save_slow("fig1-통합흐름.gif", ma.scene_all())
