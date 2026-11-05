import sys, os
from PIL import Image, ImageDraw, ImageFont

W, H, S = 1000, 560, 2
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
os.makedirs(os.path.join(OUT, "preview"), exist_ok=True)
FD = r"C:\Windows\Fonts"

BG = (253, 250, 244); INK = (58, 54, 66); MUTE = (130, 126, 140)
TEAL = (150, 114, 210); AMBER = (250, 190, 80); BLUE = (91, 156, 240)
GREEN = (88, 196, 140); RED = (236, 104, 104); WHITE = (255, 255, 255)
LINE = (222, 216, 230); LTEAL = (237, 228, 250); LAMB = (255, 243, 205)
LRED = (253, 228, 228); LGRAY = (244, 241, 248); DARK = (53, 57, 84)
GOOD = (36, 130, 90); WARN = (190, 110, 20); LBLUE = (219, 234, 254)
LGREEN = (213, 245, 228); BLUE_T = (40, 100, 190); GREEN_T = (30, 130, 90)

_fc = {}
def font(sz, bold=False, mono=False):
    key = (sz, bold, mono)
    if key not in _fc:
        name = "consola.ttf" if mono else ("malgunbd.ttf" if bold else "malgun.ttf")
        _fc[key] = ImageFont.truetype(os.path.join(FD, name), int(sz * S))
    return _fc[key]

def mix(a, b, t):
    t = max(0, min(1, t))
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def smooth(t):
    t = max(0, min(1, t))
    return t * t * (3 - 2 * t)

class Cv:
    def __init__(s):
        s.im = Image.new("RGB", (W * S, H * S), BG)
        s.d = ImageDraw.Draw(s.im)
    def rr(s, x0, y0, x1, y1, r=12, fill=None, outline=None, w=2):
        s.d.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=r * S,
                              fill=fill, outline=outline, width=int(w * S))
    def text(s, x, y, t, sz=20, color=INK, bold=False, anchor="la", mono=False):
        s.d.text((x * S, y * S), t, font=font(sz, bold, mono), fill=color, anchor=anchor)
    def fit(s, x, y, t, sz, maxw, color=INK, bold=True, anchor="mm"):
        while sz > 10 and s.d.textlength(t, font=font(sz, bold)) / S > maxw:
            sz -= 1
        s.text(x, y, t, sz, color, bold, anchor)
    def circ(s, cx, cy, r, fill=None, outline=None, w=2):
        s.d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S],
                    fill=fill, outline=outline, width=int(w * S))
    def line(s, x0, y0, x1, y1, color, w=3):
        s.d.line([x0 * S, y0 * S, x1 * S, y1 * S], fill=color, width=int(w * S))
    def arrow(s, x0, y0, x1, y1, color, w=4, head=12):
        import math
        s.line(x0, y0, x1, y1, color, w)
        a = math.atan2(y1 - y0, x1 - x0)
        p1 = (x1 - head * math.cos(a - 0.45), y1 - head * math.sin(a - 0.45))
        p2 = (x1 - head * math.cos(a + 0.45), y1 - head * math.sin(a + 0.45))
        s.d.polygon([x1 * S, y1 * S, p1[0] * S, p1[1] * S, p2[0] * S, p2[1] * S], fill=color)
    def dash(s, x0, y0, x1, y1, color, w=2, on=8, off=6):
        import math
        L = math.hypot(x1 - x0, y1 - y0)
        n = int(L // (on + off)) + 1
        for k in range(n):
            a = k * (on + off) / L
            b = min(1, (k * (on + off) + on) / L)
            s.line(x0 + (x1 - x0) * a, y0 + (y1 - y0) * a, x0 + (x1 - x0) * b, y0 + (y1 - y0) * b, color, w)
    def done(s):
        return s.im.resize((W, H), Image.LANCZOS)

def along(pts, wts, p):
    p = max(0, min(1, p)); tot = sum(wts); acc = 0
    for k in range(len(pts) - 1):
        w = wts[k] / tot
        if p <= acc + w or k == len(pts) - 2:
            q = (p - acc) / w if w else 1
            q = max(0, min(1, q))
            return (pts[k][0] + (pts[k + 1][0] - pts[k][0]) * q,
                    pts[k][1] + (pts[k + 1][1] - pts[k][1]) * q)
        acc += w

def xmark(cv, x, y, r=9, color=RED, w=4):
    cv.line(x - r, y - r, x + r, y + r, color, w)
    cv.line(x - r, y + r, x + r, y - r, color, w)

def dot(cv, x, y, color):
    cv.circ(x, y, 8, fill=color, outline=WHITE, w=2)

def header(cv, num, title, sub):
    cv.circ(52, 48, 24, fill=TEAL)
    cv.text(52, 48, str(num), 26, WHITE, True, "mm")
    cv.text(92, 22, title, 30, INK, True)
    cv.text(92, 60, sub, 16, MUTE)
    cv.line(40, 92, 960, 92, LINE, 2)

def chip(cv, x, y, t, fill=LAMB, color=(150, 90, 0)):
    w = cv.d.textlength(t, font=font(17, True)) / S + 28
    cv.rr(x, y, x + w, y + 32, 16, fill=fill)
    cv.text(x + 14, y + 16, t, 17, color, True, "lm")

def caption(cv, t, color=INK):
    cv.rr(40, 466, 960, 534, 14, fill=WHITE, outline=LINE, w=2)
    cv.fit(500, 500, t, 24, 880, color, True, "mm")

def user(cv, x, y, label="사용자"):
    cv.circ(x, y, 30, fill=LTEAL, outline=TEAL, w=3)
    cv.circ(x, y - 9, 9, fill=TEAL)
    cv.rr(x - 15, y + 4, x + 15, y + 21, 8, fill=TEAL)
    cv.text(x, y + 40, label, 16, INK, True, "ma")

def server_box(cv, x0, y0, x1, y1, name, status, color, state="active"):
    cx = (x0 + x1) / 2
    if state == "dead":
        cv.rr(x0, y0, x1, y1, 14, fill=LRED, outline=RED, w=4)
        xmark(cv, cx, y0 + 79, 13, RED, 5)
        cv.text(cx, y0 + 22, name, 20, RED, True, "mm")
        cv.text(cx, y0 + 46, status, 15, RED, False, "mm")
        return
    outline = {"active": color, "dim": LINE, "warn": RED}[state]
    fill = {"active": WHITE, "dim": LGRAY, "warn": LRED}[state]
    tcolor = INK if state == "active" else (MUTE if state == "dim" else RED)
    cv.rr(x0, y0, x1, y1, 14, fill=fill, outline=outline, w=4)
    cv.text(cx, y0 + 22, name, 20, tcolor, True, "mm")
    cv.text(cx, y0 + 46, status, 15, tcolor if state != "active" else mix(color, INK, 0.4), state == "active", "mm")

def nginx_box(cv, x0, y0, x1, y1, sub="로드밸런서"):
    cv.rr(x0, y0, x1, y1, 14, fill=LTEAL, outline=TEAL, w=4)
    cv.text((x0 + x1) / 2, y0 + 24, "Nginx", 22, TEAL, True, "mm")
    if sub:
        cv.text((x0 + x1) / 2, y0 + 50, sub, 15, INK, False, "mm")

def counter(cv, succ, fail, show_fail=True):
    cv.text(960, 108, "성공 %d" % succ, 20, GOOD, True, "ra")
    if show_fail:
        cv.text(870, 108, "실패 %d" % fail, 20, RED if fail else MUTE, True, "ra")

# ------------------------------------------------------------------ scene 1
def scene1():
    frames = []
    NA, NB = 46, 60
    for i in range(NA + NB):
        cv = Cv()
        header(cv, 1, "버틴다", "하나가 고장 나도 서비스가 안 멈추게 — 이중화")
        if i < NA:
            chip(cv, 40, 104, "A. 서버가 1대일 때")
            user(cv, 110, 270)
            dead = i >= 26
            cv.arrow(150, 270, 596, 270, LINE, 3)
            server_box(cv, 600, 205, 820, 335, "서버 1대", "단일 장애점", BLUE,
                       "dead" if dead else "active")
            succ = fail = 0
            for k in range(0, 12):
                s0 = 5 * k
                arr = s0 + 18
                p = (i - s0) / 18
                failed = arr > 26
                if arr <= i:
                    if failed: fail += 1
                    else: succ += 1
                if failed:
                    if 0 <= p <= 0.85:
                        dot(cv, 150 + 450 * p, 270, BLUE if i < 26 else RED)
                    elif 0.85 < p <= 1.15:
                        xmark(cv, 150 + 450 * 0.85, 270)
                else:
                    if 0 <= p <= 1:
                        dot(cv, 150 + 450 * p, 270, BLUE)
            counter(cv, succ, fail)
            if i < 26:
                caption(cv, "서버가 한 대면 모든 요청이 그 서버 하나로 갑니다")
            else:
                caption(cv, "그 한 대가 고장 나면 → 전부 실패 (단일 장애점)", RED)
        else:
            j = i - NA
            chip(cv, 40, 104, "B. 서버 2대 + 앞에 로드밸런서")
            user(cv, 90, 270)
            cv.arrow(130, 270, 286, 270, LINE, 3)
            nginx_box(cv, 290, 225, 410, 315, "로드밸런서")
            dead2 = j >= 20
            cy1, cy2 = 180, 370
            cv.dash(410, 255, 616, cy1, LINE, 2)
            cv.dash(410, 285, 616, cy2, LINE, 2)
            server_box(cv, 620, 130, 840, 230, "서버 1", "정상", BLUE, "active")
            server_box(cv, 620, 320, 840, 420, "서버 2", "고장" if dead2 else "정상", GREEN,
                       "dead" if dead2 else "active")
            succ = fail = 0
            for k in range(0, 14):
                s0 = 5 * k
                dec = s0 + 8
                arr = s0 + 24
                to2 = (k % 2 == 1) and dec < 32
                cy = cy2 if to2 else cy1
                failed = to2 and arr > 20
                if arr <= j:
                    if failed: fail += 1
                    else: succ += 1
                pts = [(130, 270), (290, 270), (620, cy)]
                p = (j - s0) / 24
                if failed:
                    if 0 <= p <= 0.9:
                        x, y = along(pts, [8, 16], p)
                        dot(cv, x, y, BLUE if j < 20 else RED)
                    elif 0.9 < p <= 1.2:
                        x, y = along(pts, [8, 16], 0.9)
                        xmark(cv, x, y)
                elif 0 <= p <= 1:
                    x, y = along(pts, [8, 16], p)
                    dot(cv, x, y, BLUE if not to2 else GREEN)
            counter(cv, succ, fail)
            if j < 20:
                caption(cv, "서버를 두 벌 두면 요청을 나눠 받습니다 (이중화)")
            elif j < 32:
                caption(cv, "서버 2가 고장 → 알아채기 전 잠깐은 실패가 납니다", RED)
            else:
                caption(cv, "알아챈 뒤에는 서버 1이 계속 처리 → 서비스는 멈추지 않음", GREEN)
        frames.append(cv.done())
    return frames

# ------------------------------------------------------------------ scene 2
def scene2():
    frames = []
    N = 128
    FLIP1, FLIP2 = 68, 108
    def route(f):
        return "green" if FLIP1 <= f < FLIP2 else "blue"
    for i in range(N):
        cv = Cv()
        header(cv, 2, "바꾼다", "끄지 않고 새 버전으로 — 블루그린 배포")
        chip(cv, 40, 104, "서버 두 벌을 두고, 방향만 바꿉니다")
        user(cv, 90, 275)
        cv.arrow(130, 275, 286, 275, LINE, 3)
        nginx_box(cv, 290, 230, 410, 320, "Nginx")
        cur = route(i)
        cyb, cyg = 185, 355
        # arrows from nginx to servers
        for nm, cy in (("blue", cyb), ("green", cyg)):
            if cur == nm:
                cv.arrow(410, 275, 614, cy, TEAL, 5, 14)
            else:
                cv.dash(410, 275, 614, cy, LINE, 2)
        # blue box
        if i < FLIP1:
            blue_state, blue_status = "active", "v1 · 운영 중"
        elif i < FLIP2:
            blue_state, blue_status = "dim", "v1 · 대기 (롤백용으로 남김)"
        else:
            blue_state, blue_status = "active", "v1 · 운영 중"
        server_box(cv, 620, 130, 840, 240, "blue", blue_status, BLUE, blue_state)
        # green box
        if i < 24:
            gs, gt = "dim", "(아직 없음)"
        elif i < 50:
            gs, gt = "dim", "v2 올리는 중…"
        elif i < FLIP1:
            gs, gt = "dim", "v2 준비 완료"
        elif i < 98:
            gs, gt = "active", "v2 · 운영 중"
        elif i < FLIP2:
            gs, gt = "warn", "v2 문제 발견!"
        else:
            gs, gt = "dim", "v2 · 문제 있음 → 대기"
        server_box(cv, 620, 300, 840, 410, "green", gt, GREEN, gs)
        if 24 <= i < 50:
            pr = smooth((i - 24) / 24)
            cv.rr(640, 388, 820, 400, 6, fill=LGRAY, outline=LINE, w=1)
            cv.rr(640, 388, 640 + 180 * pr, 400, 6, fill=GREEN)
        if 50 <= i < 66:
            cv.rr(850, 330, 960, 372, 10, fill=LTEAL, outline=GREEN, w=2)
            cv.text(905, 351, "헬스체크 ✓", 16, GREEN, True, "mm")
        # config chip
        if FLIP1 - 8 <= i < FLIP1 + 10:
            cv.rr(290, 160, 450, 198, 8, fill=DARK)
            cv.text(370, 179, "server green:8080;", 14, AMBER, False, "mm", True)
            cv.text(370, 208, "→ reload", 14, AMBER, True, "mm")
        if FLIP2 - 8 <= i < FLIP2 + 10:
            cv.rr(290, 160, 450, 198, 8, fill=DARK)
            cv.text(370, 179, "server blue:8080;", 14, AMBER, False, "mm", True)
            cv.text(370, 208, "→ reload", 14, AMBER, True, "mm")
        # dots
        for k in range(0, 24):
            s0 = 6 * k
            dec = s0 + 8
            tgt = route(dec)
            cy = cyb if tgt == "blue" else cyg
            pts = [(130, 275), (290, 275), (620, cy)]
            p = (i - s0) / 24
            if 0 <= p <= 1:
                x, y = along(pts, [8, 16], p)
                dot(cv, x, y, BLUE if tgt == "blue" else GREEN)
        if i >= FLIP1 - 6:
            cv.text(960, 108, "끊긴 요청 0건", 20, GREEN, True, "ra")
        if i < 24:
            caption(cv, "지금은 blue(v1)가 요청을 받는 중입니다")
        elif i < 50:
            caption(cv, "옆의 green에 새 버전(v2)을 다 올립니다 — 사용자는 모릅니다")
        elif i < 62:
            caption(cv, "전환하기 전에 green이 정상인지 먼저 확인합니다 (헬스체크)")
        elif i < 76:
            caption(cv, "설정 한 줄 바꾸고 reload → 방향만 blue에서 green으로", TEAL)
        elif i < 98:
            caption(cv, "이제 v2(green)가 받습니다 · 끊긴 요청은 0건", GREEN)
        elif i < FLIP2 + 2:
            caption(cv, "만약 green에 문제가 있다면?", RED)
        else:
            caption(cv, "한 줄만 되돌리면 끝 — blue를 안 껐으니 몇 초 만에 롤백", TEAL)
        frames.append(cv.done())
    return frames

# ------------------------------------------------------------------ scene 3
def scene3():
    frames = []
    N = 112
    ADD = 40
    for i in range(N):
        cv = Cv()
        header(cv, 3, "돌린다", "요청 방향을 정하는 장치 — Nginx")
        two = i >= ADD + 8
        user(cv, 80, 270)
        cv.text(80, 322, "주소는 하나", 14, MUTE, False, "ma")
        cv.text(80, 342, "localhost:8080", 13, MUTE, False, "ma", True)
        cv.arrow(120, 270, 226, 270, LINE, 3)
        # nginx big box
        cv.rr(230, 130, 450, 400, 14, fill=LTEAL, outline=TEAL, w=4)
        cv.text(340, 152, "Nginx", 22, TEAL, True, "mm")
        role = "로드밸런서" if two else "리버스 프록시"
        rc = TEAL if two else AMBER
        cv.rr(262, 172, 418, 204, 16, fill=rc)
        cv.text(340, 188, role, 17, WHITE, True, "mm")
        cv.rr(244, 216, 436, 388, 10, fill=DARK)
        cv.text(256, 228, "upstream active_app {", 13, (200, 215, 225), False, "la", True)
        cv.text(256, 252, "  server blue:8080;", 13, (200, 215, 225), False, "la", True)
        if i >= ADD:
            t = smooth((i - ADD) / 8)
            col = mix((60, 75, 90), AMBER, t) if i < ADD + 30 else (200, 215, 225)
            cv.text(256, 276, "  server green:8080;", 13, col, False, "la", True)
        cv.text(256, 300, "}", 13, (200, 215, 225), False, "la", True)
        cv.text(256, 328, "location / {", 13, (200, 215, 225), False, "la", True)
        cv.text(256, 352, "  proxy_pass http://active_app;", 12, (200, 215, 225), False, "la", True)
        cv.text(256, 372, "}", 13, (200, 215, 225), False, "la", True)
        # boundary of hidden servers
        cv.dash(632, 128, 872, 128, MUTE, 2)
        cv.dash(632, 405, 872, 405, MUTE, 2)
        cv.dash(632, 128, 632, 405, MUTE, 2)
        cv.dash(872, 128, 872, 405, MUTE, 2)
        cv.text(752, 414, "바깥에 포트를 안 열어 둠 · Nginx만 접근", 14, MUTE, False, "ma")
        cyb, cyg = 190, 335
        server_box(cv, 650, 148, 850, 232, "blue", "v1", BLUE, "active")
        server_box(cv, 650, 290, 850, 374, "green", "v2" if two else "(목록에 없음)", GREEN,
                   "active" if two else "dim")
        cv.dash(450, 255, 646, cyb, LINE, 2)
        if two:
            cv.dash(450, 285, 646, cyg, LINE, 2)
        # dots
        for k in range(0, 24):
            s0 = 6 * k
            dec = s0 + 8
            to_green = (dec >= ADD + 8) and (k % 2 == 1)
            cy = cyg if to_green else cyb
            pts = [(120, 270), (230, 270), (650, cy)]
            p = (i - s0) / 24
            if 0 <= p <= 1:
                x, y = along(pts, [6, 18], p)
                dot(cv, x, y, GREEN if to_green else BLUE)
        if i < ADD:
            caption(cv, "서버가 한 줄이면 → 리버스 프록시: 요청을 대신 받아 뒤로 넘겨 줌")
        elif i < ADD + 8:
            caption(cv, "목록에 서버를 한 줄 더하면 …", AMBER)
        else:
            caption(cv, "→ 로드밸런서: 여러 서버에 나눠 보냄 (같은 Nginx, 설정만 다름)", TEAL)
        frames.append(cv.done())
    return frames

# ------------------------------------------------------------------ scene 4
def card(cv, cx, cy, color=AMBER, alpha=1.0, w=96):
    cv.rr(cx - w / 2, cy - 13, cx + w / 2, cy + 13, 8,
          fill=mix(BG, LAMB, alpha), outline=mix(BG, color, alpha), w=2)
    cv.text(cx, cy, "8시 물 마시기", 13, mix(BG, (150, 90, 0), alpha), True, "mm")

def cylinder(cv, cx, y0, y1, w=84, color=TEAL, label="DB"):
    x0, x1 = cx - w / 2, cx + w / 2
    cv.rr(x0, y0 + 10, x1, y1 - 10, 4, fill=LTEAL, outline=None)
    cv.line(x0, y0 + 10, x0, y1 - 10, color, 4)
    cv.line(x1, y0 + 10, x1, y1 - 10, color, 4)
    cv.d.ellipse([x0 * S, (y1 - 22) * S, x1 * S, y1 * S], fill=LTEAL, outline=color, width=4 * S // 1)
    cv.rr(x0 + 2, y0 + 12, x1 - 2, y1 - 12, 2, fill=LTEAL)
    cv.d.ellipse([x0 * S, y0 * S, x1 * S, (y0 + 22) * S], fill=WHITE, outline=color, width=4 * S // 1)
    cv.text(cx, (y0 + y1) / 2 + 2, label, 18, color, True, "mm")

def panel(cv, ox, db, i):
    bx0, bx1 = ox + 215, ox + 345
    by0, by1 = 150, 255
    gy0, gy1 = 300, 405
    ncx = ox + 120
    route_green = 40 <= i
    # panel frame + title
    cv.rr(ox + 14, 102, ox + 486, 450, 16, fill=None, outline=LINE, w=2)
    t = "상태를 DB에 둘 때" if db else "상태를 컨테이너 메모리에 둘 때"
    cv.text(ox + 250, 118, t, 19, TEAL if db else RED, True, "mm")
    user(cv, ox + 50, 290)
    cv.arrow(ox + 84, 290, ox + 84 + 4, 290, LINE, 1)
    cv.arrow(ox + 82, 290, ox + 90, 290, LINE, 3)
    cv.rr(ox + 94, 258, ox + 150, 322, 10, fill=LTEAL, outline=TEAL, w=3)
    cv.text(ox + 122, 290, "Nginx", 14, TEAL, True, "mm")
    # arrows to servers
    cur = "green" if route_green else "blue"
    for nm, cy in (("blue", (by0 + by1) / 2), ("green", (gy0 + gy1) / 2)):
        if cur == nm:
            cv.arrow(ox + 150, 290, bx0 - 2, cy, TEAL, 5, 12)
        else:
            cv.dash(ox + 150, 290, bx0 - 2, cy, LINE, 2)
    restart = 70 <= i < 100
    bstate = "dim" if route_green and not restart else "active"
    server_box(cv, bx0, by0, bx1, by1, "blue", "↻ 재시작!" if restart else "v1", BLUE,
               "warn" if restart else bstate)
    server_box(cv, bx0, gy0, bx1, gy1, "green", "v2", GREEN, "active" if route_green else "dim")
    # memory slots
    mxo0, mxo1 = bx0 + 10, bx1 - 10
    cv.rr(mxo0, by0 + 56, mxo1, by1 - 10, 6, fill=LGRAY, outline=LINE, w=1)
    cv.rr(mxo0, gy0 + 56, mxo1, gy1 - 10, 6, fill=LGRAY, outline=LINE, w=1)
    if not db:
        cv.text(ox + 435, 290, "DB 없음", 16, MUTE, True, "mm")
        cv.dash(ox + 395, 245, ox + 475, 245, LINE, 2)
        cv.dash(ox + 395, 335, ox + 475, 335, LINE, 2)
        cv.dash(ox + 395, 245, ox + 395, 335, LINE, 2)
        cv.dash(ox + 475, 245, ox + 475, 335, LINE, 2)
        cv.text(bx0 + 65, by0 + 62 - 0, "메모리", 11, MUTE, False, "ma")
        cv.text(bx0 + 65, gy0 + 62, "메모리", 11, MUTE, False, "ma")
    else:
        cylinder(cv, ox + 435, 235, 345)
        # connectors blue/green -> DB
        bcy, gcy = (by0 + by1) / 2, (gy0 + gy1) / 2
        cv.line(bx1, bcy, ox + 393, 270, LINE, 2)
        cv.line(bx1, gcy, ox + 393, 310, LINE, 2)
        cv.text(bx0 + 65, by0 + 62, "(상태 없음)", 11, MUTE, False, "ma")
        cv.text(bx0 + 65, gy0 + 62, "(상태 없음)", 11, MUTE, False, "ma")
    bmy = by1 - 24
    gmy = gy1 - 24
    # card flight 14..24 from user to storage
    if i < 14:
        pass
    elif i < 24:
        p = smooth((i - 14) / 10)
        if db:
            sx, sy = ox + 435, 290
        else:
            sx, sy = (bx0 + bx1) / 2, bmy
        sx0, sy0 = ox + 150, 290
        # fly via blue
        mx, my = (bx0 + bx1) / 2, (by0 + by1) / 2
        if p < 0.5:
            q = p / 0.5
            x, y = sx0 + (mx - sx0) * q, sy0 + (my - sy0) * q
        else:
            q = (p - 0.5) / 0.5
            x, y = mx + (sx - mx) * q, my + (sy - my) * q
        card(cv, x, y)
    else:
        if db:
            card(cv, ox + 435, 290, TEAL, 1.0, 76)
        else:
            if i < 78:
                card(cv, (bx0 + bx1) / 2, bmy, AMBER, 1.0, 100)
            elif i < 90:
                a = 1 - (i - 78) / 12
                card(cv, (bx0 + bx1) / 2, bmy, RED, a, 100)
                xmark(cv, (bx0 + bx1) / 2, bmy, 12, RED, 4)
    # green view
    if route_green and 44 <= i:
        if db:
            a = smooth((i - 44) / 8)
            card(cv, (bx0 + bx1) / 2, gmy, TEAL, a, 100)
            cv.text((bx0 + bx1) / 2, gy1 + 14, "약속이 보임", 15, GREEN, True, "mm")
        else:
            cv.text((bx0 + bx1) / 2, gmy, "(비어 있음)", 13, MUTE, True, "mm")
            cv.text((bx0 + bx1) / 2, gy1 + 14, "약속이 안 보임", 15, RED, True, "mm")
    # blue after restart in db panel reads from DB again
    if db and i >= 92:
        a = smooth((i - 92) / 8)
        card(cv, (bx0 + bx1) / 2, bmy, TEAL, a, 100)
    if not db and i >= 90:
        cv.text((bx0 + bx1) / 2, bmy, "(비어 있음)", 13, MUTE, True, "mm")
    if not db and 46 <= i < 70:
        cv.text((bx0 + bx1) / 2, by1 + 14, "blue 안에는 그대로", 13, MUTE, False, "mm")
    return

def scene4():
    frames = []
    N = 132
    for i in range(N):
        cv = Cv()
        header(cv, 4, "이어간다", "기억을 서버가 아니라 DB가 갖는다 — 무상태")
        panel(cv, 0, False, i)
        panel(cv, 500, True, i)
        # user dots (short) toward nginx for both panels
        for ox in (0, 500):
            for k in range(0, 22):
                s0 = 6 * k
                p = (i - s0) / 14
                if 0 <= p <= 1:
                    cur_green = (s0 + 8) >= 40
                    tx, ty = ox + 215, (330 + 0) if cur_green else 202
                    pts = [(ox + 84, 290), (ox + 150, 290), (tx - 4, 352 if cur_green else 202)]
                    x, y = along(pts, [3, 3, 4], p)
                    dot(cv, x, y, GREEN if cur_green else BLUE)
        if i < 14:
            caption(cv, "blue가 요청을 받는 중 — 사용자가 약속을 하나 만듭니다")
        elif i < 30:
            caption(cv, "약속이 저장됩니다 — 왼쪽은 blue 메모리, 오른쪽은 DB")
        elif i < 44:
            caption(cv, "이제 방향을 green으로 바꿉니다", TEAL)
        elif i < 70:
            caption(cv, "전환 후 — 왼쪽은 약속이 안 보임 / 오른쪽은 그대로 보임", RED)
        elif i < 100:
            caption(cv, "blue를 재시작 — 왼쪽은 진짜 사라짐 / 오른쪽은 DB에 남아 있음", RED)
        else:
            caption(cv, "기억을 서버가 아니라 DB가 가지면, 서버는 언제 바뀌어도 됩니다", GREEN)
        frames.append(cv.done())
    return frames

# ------------------------------------------------------------------ save
def save(name, frames):
    stride = max(1, len(frames) // 14)
    sample = Image.new("RGB", (W, H * len(frames[::stride])))
    for k, f in enumerate(frames[::stride]):
        sample.paste(f, (0, k * H))
    pal = sample.quantize(colors=255, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    q = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in frames]
    durs = [130] * len(frames)
    durs[0] = 900
    durs[-1] = 3000
    path = os.path.join(OUT, name)
    q[0].save(path, save_all=True, append_images=q[1:], duration=durs, loop=0, disposal=1, optimize=False)
    pv = os.path.join(OUT, "preview")
    for idx in (len(frames) // 5, len(frames) // 2, len(frames) - 1):
        frames[idx].save(os.path.join(pv, "%s_%03d.png" % (name[:-4], idx)))
    print(name, len(frames), "frames", os.path.getsize(path) // 1024, "KB")

if __name__ == "__main__":
    only = sys.argv[2] if len(sys.argv) > 2 else "all"
    jobs = {"1": ("01_버틴다.gif", scene1), "2": ("02_바꾼다.gif", scene2),
            "3": ("03_돌린다.gif", scene3), "4": ("04_이어간다.gif", scene4)}
    for k, (nm, fn) in jobs.items():
        if only in ("all", k):
            save(nm, fn())


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
