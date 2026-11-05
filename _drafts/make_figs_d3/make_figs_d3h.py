import sys, math, os
from make_figs_d3_p import head, nbox, pill, fade, ramp
from make_gifs_p import *

DBG = os.environ.get("DBGDIR")
PURP = mix(TEAL, INK, 0.35)


def lerp(a, b, t):
    return a + (b - a) * t


def pth(pts, p):
    wts = [math.hypot(pts[k + 1][0] - pts[k][0], pts[k + 1][1] - pts[k][1]) for k in range(len(pts) - 1)]
    return along(pts, wts, p)


def hdot(cv, x, y, c, x0, x1):
    if x0 < x < x1:
        return
    dot(cv, x, y, c)


def pill_row(cv, labels, cur, cols, y=124, sz=15, x=40):
    for k, t in enumerate(labels):
        w = cv.d.textlength(t, font=font(sz, True)) / S + 28
        on = k == cur
        fill, tc = cols if on else (LGRAY, MUTE)
        cv.rr(x, y - 15, x + w, y + 15, 15, fill=fill, outline=tc if on else None, w=2)
        cv.text(x + w / 2, y, t, sz, tc, True, "mm")
        x += w + 10


def dbg(name, frames, idxs):
    if not DBG:
        return
    os.makedirs(DBG, exist_ok=True)
    for ix in idxs:
        if ix < len(frames):
            frames[ix].save(os.path.join(DBG, "%s_%03d.png" % (name, ix)))


# ============================================================ 1) 두 조건
def fig_two():
    NA, NB, NC, NS = 34, 38, 34, 12
    labels = ["① server 한 벌", "② 두 벌 + 메모리", "③ 두 벌 + DB"]
    cols = (LTEAL, PURP)

    def common(cv, sc, ul, ulc):
        head(cv, "무중단 배포의 두 조건", "배포하는 순간 사용자에게 일어날 수 있는 두 가지")
        pill_row(cv, labels, sc, cols)
        user(cv, 80, 255)
        cv.rr(24, 330, 136, 396, 10, fill=WHITE, outline=LINE, w=2)
        cv.text(80, 346, "내 약속 목록", 13, MUTE, False, "mm")
        cv.text(80, 374, ul, 20, ulc, True, "mm")
        nbox(cv, 330, 210, 450, 300, ["Nginx"], LTEAL, TEAL, INK, 20)
        cv.arrow(116, 255, 326, 255, LINE, 3, 10)

    def scene_a(j):
        cv = Cv()
        common(cv, 0, "1개", MUTE)
        cv.arrow(454, 255, 596, 255, LINE, 3, 10)
        if j < 8:
            server_box(cv, 600, 205, 800, 305, "server", "v1 · 받는 중", BLUE, "active")
        elif j < 26:
            server_box(cv, 600, 205, 800, 305, "server", "교체 중 (비어 있음)", BLUE, "dim")
            pill(cv, 700, 182, "새 버전으로 교체 중", LAMB, WARN, 15)
        else:
            server_box(cv, 600, 205, 800, 305, "server", "v2 · 받는 중", GREEN, "active")
        fails = 0
        pts = [(116, 255), (326, 255), (600, 255)]
        for k in range(12):
            s0 = 6 * k
            p = (j - s0) / 26
            dec = s0 + 11
            failed = 8 <= dec < 26
            if failed and j >= s0 + 13:
                fails += 1
            if failed:
                if 0 <= p <= 0.434:
                    x, y = pth(pts, p)
                    hdot(cv, x, y, BLUE, 328, 452)
                elif 0.434 < p <= 0.62:
                    xmark(cv, 318, 255, 9, RED, 4)
            elif 0 <= p <= 1:
                x, y = pth(pts, p)
                hdot(cv, x, y, BLUE if dec < 8 else GREEN, 328, 452)
        cv.text(960, 124, "실패 %d건" % fails, 20, RED if fails else MUTE, True, "ra")
        if j < 8:
            caption(cv, "server가 한 벌이면 모든 요청이 그 server 하나로 갑니다", INK)
        else:
            caption(cv, "조건 ① 깨짐: 교체하는 동안 요청이 실패합니다", RED)
        return cv.done()

    def two_srv(j, sc, db):
        flip = 14 if not db else 12
        if db:
            ulv, ulc = "1개", GOOD
        else:
            ulv, ulc = ("1개", GOOD) if j < flip + 12 else ("없음", RED)
        cv = Cv()
        common(cv, sc, ulv, ulc)
        on_g = j >= flip
        for nm, cy, col in (("blue", 207, BLUE), ("green", 357, GREEN)):
            act = (nm == "green") == on_g
            if act:
                cv.arrow(454, 262 if nm == "blue" else 270, 596, cy, col, 5, 14)
            else:
                cv.dash(454, 262 if nm == "blue" else 270, 596, cy, LINE, 2)
        server_box(cv, 600, 150, 780, 265, "blue", "v1 · 대기" if on_g else "v1 · 받는 중", BLUE, "dim" if on_g else "active")
        server_box(cv, 600, 300, 780, 415, "green", "v2 · 받는 중" if on_g else "v2 · 대기", GREEN, "active" if on_g else "dim")
        if not db:
            cv.text(690, 218, "메모리", 12, MUTE, False, "mm")
            card(cv, 690, 244, AMBER, 1.0, 104)
            cv.text(690, 368, "메모리", 12, MUTE, False, "mm")
            cv.text(690, 393, "(비어 있음)", 14, RED if on_g else MUTE, True, "mm")
        else:
            cv.text(690, 232, "(약속을 안 가짐)", 13, MUTE, False, "mm")
            cv.text(690, 382, "(약속을 안 가짐)", 13, MUTE, False, "mm")
            cylinder(cv, 895, 170, 320, 90, DB_A, "DB")
            card(cv, 895, 352, AMBER, 1.0, 110)
            cv.text(895, 378, "DB 안의 약속", 13, MUTE, False, "mm")
            cv.dash(780, 207, 850, 235, MUTE if not on_g else LINE, 3 if not on_g else 2)
            cv.dash(780, 357, 850, 290, MUTE if on_g else LINE, 3 if on_g else 2)
        for k in range(12):
            s0 = 6 * k
            p = (j - s0) / 26
            dec = s0 + 11
            tg = "green" if dec >= flip else "blue"
            cy = 357 if tg == "green" else 207
            if 0 <= p <= 1:
                x, y = pth([(116, 255), (326, 255), (600, cy)], p)
                hdot(cv, x, y, GREEN if tg == "green" else BLUE, 328, 452)
        cv.text(960, 124, "실패 0건", 20, GOOD, True, "ra")
        return cv

    def scene_b(j):
        cv = two_srv(j, 1, False)
        if j < 14:
            caption(cv, "server는 두 벌이고 요청은 전부 성공합니다 — 약속은 blue 메모리에 있습니다", INK)
        else:
            caption(cv, "조건 ② 깨짐: 요청은 하나도 실패하지 않았는데 하던 일이 사라졌습니다 — 사용자에게는 끊긴 것과 같습니다", RED)
        return cv.done()

    def scene_c(j):
        cv = two_srv(j, 2, True)
        if j < 12:
            caption(cv, "이번에는 약속을 server가 아니라 DB에 둡니다", INK)
        else:
            caption(cv, "방향이 바뀌어도 약속은 DB에 그대로 — 요청도 성공, 하던 일도 이어집니다", GOOD)
        return cv.done()

    def scene_s(j):
        cv = Cv()
        head(cv, "무중단 배포의 두 조건", "배포하는 순간 사용자에게 일어날 수 있는 두 가지")
        pill_row(cv, labels, 2, cols)
        a = smooth(j / 5)
        boxes = [(60, "조건 ①", "요청이 끊기지 않음", ["server를 두 벌 두고", "한쪽을 바꾸는 동안 다른 쪽이 받음"], BLUE, LBLUE),
                 (530, "조건 ②", "하던 일이 이어짐", ["약속을 server 메모리가 아니라", "DB에 두어 server가 바뀌어도 남음"], GREEN, LGREEN)]
        for x0, tag, title, subs, oc, fc in boxes:
            cv.rr(x0, 150, x0 + 410, 410, 18, fill=fade(fc, a), outline=fade(oc, a), w=4)
            cv.text(x0 + 205, 192, tag, 24, fade(INK, a), True, "mm")
            cv.fit(x0 + 205, 262, title, 34, 380, fade(INK, a), True, "mm")
            for q, t in enumerate(subs):
                cv.fit(x0 + 205, 330 + q * 28, t, 16, 380, fade(INK, a), False, "mm")
        cv.text(500, 280, "+", 44, fade(MUTE, a), True, "mm")
        caption(cv, "두 조건을 모두 지켜야 무중단입니다: ① 요청이 끊기지 않음 ② 하던 일이 이어짐", GOOD)
        return cv.done()

    fr = []
    for sc, n, fn in ((0, NA, scene_a), (1, NB, scene_b), (2, NC, scene_c), (3, NS, scene_s)):
        for j in range(n):
            fr.append(fn(j))
    dbg("two", fr, [5, 16, 30, 40, 56, 66, 80, 90, 100, 117])
    return fr


# ============================================================ 2) 배포 방식
def fig_methods():
    names = ["① 블루그린", "② 롤링", "③ 카나리"]
    cols = (LTEAL, PURP)

    def base(cv, cur):
        head(cv, "새 버전으로 바꾸는 세 가지 방식", "모두 load balancer가 요청 보내는 곳을 바꾸는 방법")
        pill_row(cv, names, cur, cols)
        user(cv, 70, 270)
        nbox(cv, 190, 225, 324, 315, ["load balancer"], LTEAL, TEAL, INK, 17)
        cv.arrow(104, 270, 186, 270, LINE, 3, 10)

    # ---- 블루그린
    F = 34

    def scene_a(j):
        cv = Cv()
        base(cv, 0)
        cur = "green" if j >= F else "blue"
        for nm, cy, col in (("blue", 190, BLUE), ("green", 370, GREEN)):
            if cur == nm:
                cv.arrow(328, 270, 556, cy, col, 5, 14)
            else:
                cv.dash(328, 270, 556, cy, LINE, 2)
        server_box(cv, 560, 140, 800, 240, "blue 묶음", "옛 v1 · 롤백용 대기" if j >= F else "옛 v1 · 운영 중",
                   BLUE, "dim" if j >= F else "active")
        if j >= F:
            cv.text(680, 224, "(꺼지지 않음)", 13, MUTE, False, "mm")
        if j < 18:
            gs, gt = "dim", "새 v2 · 준비 중"
        elif j < F:
            gs, gt = "dim", "새 v2 · 준비 완료"
        else:
            gs, gt = "active", "새 v2 · 운영 중"
        server_box(cv, 560, 320, 800, 420, "green 묶음", gt, GREEN, gs)
        if 2 <= j < 18:
            pr = smooth((j - 2) / 16)
            cv.rr(590, 398, 770, 410, 6, fill=LGRAY, outline=LINE, w=1)
            cv.rr(590, 398, 590 + 180 * pr, 410, 6, fill=GREEN)
        if 18 <= j < F + 6:
            pill(cv, 895, 370, "헬스체크 통과", LGREEN, GOOD, 15)
        if F - 3 <= j < F + 10:
            pill(cv, 258, 196, "방향 바꿈!", LAMB, WARN, 15)
        for k in range(10):
            s0 = 6 * k
            p = (j - s0) / 26
            tg = "green" if s0 + 12 >= F else "blue"
            cy = 370 if tg == "green" else 190
            if 0 <= p <= 1:
                x, y = pth([(104, 270), (324, 270), (556, cy)], p)
                hdot(cv, x, y, GREEN if tg == "green" else BLUE, 188, 326)
        if j < 18:
            caption(cv, "green에 새 버전(v2)을 올리는 동안에도 요청은 blue(v1)로 갑니다", INK)
        else:
            caption(cv, "새 쪽을 다 준비한 뒤 방향을 한 번에 바꿉니다. blue는 롤백을 위해 남겨 둡니다", INK if j < F else GOOD)
        return cv.done()

    # ---- 롤링
    def srv(s, j):
        d = j - (6 + 20 * s)
        if d < 0:
            return "v1"
        if d < 9:
            return "drain"
        if d < 15:
            return "swap"
        if d < 20:
            return "health"
        return "v2"

    ys = [128, 223, 318]

    def scene_b(j):
        cv = Cv()
        base(cv, 1)
        st = [srv(s, j) for s in range(3)]
        for s in range(3):
            y0 = ys[s]
            cy = y0 + 40
            col = BLUE if st[s] == "v1" else GREEN
            nm = "server %d" % (s + 1)
            if st[s] in ("v1", "v2"):
                cv.arrow(328, 270, 516, cy, col, 4, 12)
            else:
                cv.dash(328, 270, 516, cy, LINE, 2)
            if st[s] == "v1":
                server_box(cv, 520, y0, 720, y0 + 80, nm, "옛 v1 · 받는 중", BLUE, "active")
            elif st[s] == "drain":
                server_box(cv, 520, y0, 720, y0 + 80, nm, "빠짐 (새 요청 끊음)", BLUE, "dim")
                dot(cv, 696, y0 + 64, AMBER)
                cv.text(734, cy - 10, "drain: 하던 요청은", 14, WARN, True, "lm")
                cv.text(734, cy + 12, "끝까지 마침", 14, WARN, True, "lm")
            elif st[s] == "swap":
                server_box(cv, 520, y0, 720, y0 + 80, nm, "v2로 교체 중", GREEN, "dim")
                cv.text(734, cy, "새 버전(v2)으로 교체", 14, MUTE, True, "lm")
            elif st[s] == "health":
                server_box(cv, 520, y0, 720, y0 + 80, nm, "v2 · 헬스체크 통과", GREEN, "active")
                cv.text(734, cy, "다시 투입", 14, GOOD, True, "lm")
            else:
                server_box(cv, 520, y0, 720, y0 + 80, nm, "새 v2 · 받는 중", GREEN, "active")
        for k in range(14):
            s0 = 6 * k
            p = (j - s0) / 26
            dec = s0 + 12
            pool = [s for s in range(3) if srv(s, dec) in ("v1", "v2")]
            tgt = pool[k % len(pool)]
            ver = srv(tgt, dec)
            if 0 <= p <= 1:
                x, y = pth([(104, 270), (324, 270), (516, ys[tgt] + 40)], p)
                hdot(cv, x, y, BLUE if ver == "v1" else GREEN, 188, 326)
        vers = set(x for x in st if x in ("v1", "v2"))
        if len(vers) == 2:
            pill(cv, 840, 124, "v1과 v2가 함께 요청 받는 중", LAMB, WARN, 15)
        caption(cv, "한 대씩 빼서 바꾸고 다시 넣습니다. 그동안 옛 버전과 새 버전이 함께 일합니다", INK if len(vers) < 2 else WARN)
        return cv.done()

    # ---- 카나리
    RATIOS = [0.01, 0.10, 0.50, 1.0]
    LAB = ["1%", "10%", "50%", "100%"]
    SETS = [{3}, {2}, {1, 3}, {0, 1, 2, 3}]

    def stage_of(f):
        return max(0, min(3, (f - 6) // 16))

    def scene_c(j):
        cv = Cv()
        base(cv, 2)
        st = stage_of(j)
        ph = (j - 6) - 16 * st
        if j < 6:
            r = 0.0
        else:
            prev = RATIOS[st - 1] if st > 0 else 0.0
            r = lerp(prev, RATIOS[st], smooth(ph / 5)) if j < 70 else 1.0
        done = j >= 62
        v1dim = done
        for nm, cy, col in (("v1", 170, BLUE), ("v2", 290, GREEN)):
            frac = (1 - r) if nm == "v1" else r
            if frac > 0.005:
                cv.arrow(328, 270 if nm == "v2" else 262, 516, cy, col, 2 + int(4 * frac), 12)
            else:
                cv.dash(328, 270, 516, cy, LINE, 2)
        server_box(cv, 520, 125, 740, 215, "옛 v1", "여러 대 · 대기" if v1dim else "여러 대 · 운영 중", BLUE, "dim" if v1dim else "active")
        server_box(cv, 520, 245, 740, 335, "새 v2", "한 대", GREEN, "active")
        # 지표 표시
        if j >= 6 and j < 70:
            good = ph >= 10
            if good:
                pill(cv, 870, 290, "지표 괜찮음", LGREEN, GOOD, 15)
            else:
                pill(cv, 870, 290, "지표 확인 중", LAMB, WARN, 15)
        # 비율 막대
        BX0, BX1 = 140, 860
        cv.text(BX0, 346, "옛 v1  %d%%" % round((1 - r) * 100), 14, BLUE_T, True, "lm")
        cv.text(BX1, 346, "새 v2  %d%%" % round(r * 100), 14, GREEN_T, True, "rm")
        cv.rr(BX0, 358, BX1, 378, 8, fill=LGRAY, outline=LINE, w=2)
        if r < 0.995:
            cv.rr(BX0, 358, BX0 + (BX1 - BX0) * (1 - r), 378, 8, fill=BLUE)
        if r > 0.005:
            wg = max(6, (BX1 - BX0) * r)
            cv.rr(BX1 - wg, 358, BX1, 378, 6, fill=GREEN)
        # 단계 막대
        for k in range(4):
            x0 = 140 + k * 180
            cur = (j >= 6 and st == k and j < 62) or (k == 3 and j >= 62)
            passed = j >= 6 and (st > k or (st == k and ph >= 10)) and not (k == 3 and False)
            if k == 3 and j >= 62:
                fill, oc, tc = LGREEN, GOOD, GOOD
            elif passed:
                fill, oc, tc = LGREEN, GREEN, GOOD
            elif j >= 6 and st == k:
                fill, oc, tc = LAMB, AMBER, WARN
            else:
                fill, oc, tc = LGRAY, LINE, MUTE
            cv.rr(x0, 398, x0 + 160, 442, 12, fill=fill, outline=oc, w=3)
            cv.text(x0 + 80, 420, LAB[k], 20, tc, True, "mm")
            if k < 3:
                cv.arrow(x0 + 163, 420, x0 + 177, 420, MUTE, 2, 8)
        for k in range(24):
            s0 = 4 * k
            p = (j - s0) / 24
            dec = s0 + 11
            if dec < 6:
                tv2 = False
            else:
                sd = stage_of(dec)
                idx = (dec - (6 + 16 * sd)) // 4
                tv2 = idx in SETS[sd] if dec < 70 else True
            cy = 290 if tv2 else 170
            if 0 <= p <= 1:
                x, y = pth([(104, 270), (324, 270), (516, cy)], p)
                hdot(cv, x, y, GREEN if tv2 else BLUE, 188, 326)
        if j < 6:
            caption(cv, "새 버전에 일부 요청만 먼저 보내 보고, 괜찮으면 비율을 올립니다", INK)
        elif j < 62:
            caption(cv, "새 버전에 일부 요청만 먼저 보내 보고, 괜찮으면 비율을 올립니다", WARN if ph < 10 else GOOD)
        else:
            caption(cv, "끝까지 지표가 괜찮으면 모든 요청이 새 버전으로 갑니다", GOOD)
        return cv.done()

    fr = []
    for n, fn in ((56, scene_a), (80, scene_b), (78, scene_c)):
        for j in range(n):
            fr.append(fn(j))
    dbg("methods", fr, [10, 28, 45, 55, 66, 76, 90, 110, 128, 140, 160, 175, 190, 205, 213])
    return fr


# ============================================================ 3) Nginx 길
CODE = ["server {", "  listen 80;", "  location / {", "    proxy_pass http://active_app;", "  }", "}",
        "upstream active_app {", "  zone active_app 64k;", "  server blue:8080 weight=3;", "  server green:8080;", "}"]
AREA_IX = {"listen": 0, "proxy": 1, "list": 2, "rule": 3, "zone": 4, "send": 5}


def fig_path():
    STEP, RESET, REQ, TAIL = 11, 6, 11, 8
    T_STEPS = 6 * STEP
    T_RESET = T_STEPS + RESET
    T_REQ = T_RESET + 4 * REQ
    TOTAL = T_REQ + TAIL
    CAPS = ["① 요청이 80번 포트로 들어옵니다 (listen 80)",
            "② proxy_pass: 요청을 대신 받아 active_app 목록으로 넘깁니다",
            "③ upstream active_app 목록에는 blue와 green이 있습니다",
            "④ 규칙(weight 3 : 1)에 따라 이번에는 blue를 고릅니다",
            "⑤ zone: 공유 메모리의 \"다음 차례\" 카운터가 한 칸 올라갑니다",
            "⑥ 고른 blue에 전달하고, 응답이 사용자에게 되돌아옵니다"]
    ROWY = {"blue": 251, "green": 279}
    SY = {"blue": 180, "green": 390}
    HEXTRA = (88, 80, 124)

    def lines_for(area, tg):
        if area == "listen":
            return {1}
        if area == "proxy":
            return {3}
        if area == "list":
            return {6, 8, 9}
        if area == "rule":
            return {8 if tg == "blue" else 9}
        if area == "zone":
            return {7}
        if area == "send":
            return {3}
        return set()

    def draw(i):
        cv = Cv()
        head(cv, "요청 하나가 Nginx 설정을 지나는 길", "아래는 오늘 실습의 설정 한 벌: 요청은 위에서 아래로 이 순서로 지난다")
        area, tg, cnt, tally, dpos, dcol, cap, capc = None, "blue", 0, [], None, AMBER, "", INK
        resp = False
        if i < T_STEPS:
            s = i // STEP
            p = smooth((i % STEP) / (STEP - 1))
            area = ["listen", "proxy", "list", "rule", "zone", "send"][s]
            cap = CAPS[s]
            cnt = 1 if (s >= 5 or (s == 4 and p > 0.5)) else 0
            if s == 5 and p > 0.92:
                tally = ["blue"]
            if s == 0:
                dpos = (lerp(522, 624, p), lerp(230, 186, p))
            elif s == 1:
                dpos = (lerp(624, 731, p), 186)
            elif s == 2:
                dpos = (lerp(731, 675, p), lerp(200, 236, p))
            elif s == 3:
                dpos = (lerp(640, 592, p), lerp(228, 251, p))
                dcol = BLUE if p > 0.6 else AMBER
            elif s == 4:
                dpos = (lerp(600, 675, p), lerp(251, 372, p))
                dcol = BLUE
            else:
                pts = [(675, 372), (800, 251), (850, 190), (800, 251), (560, 230), (524, 230)]
                dpos = pth(pts, p)
                dcol = BLUE if p < 0.5 else GOOD
                resp = p >= 0.5
        elif i < T_RESET:
            cap = "이번에는 요청 4건을 연달아 봅니다 (카운터 0에서 시작)"
            cnt = 0
        elif i < T_REQ:
            r = (i - T_RESET) // REQ
            p = smooth(((i - T_RESET) % REQ) / (REQ - 1))
            tg = ["blue", "blue", "blue", "green"][r]
            area = "listen" if p < .2 else "proxy" if p < .4 else "list" if p < .52 else "rule" if p < .64 else "zone" if p < .8 else "send"
            cnt = (r + 1) % 4 if p > 0.7 else r
            tally = [["blue", "blue", "blue", "green"][q] for q in range(r)]
            if p > 0.88:
                tally.append(tg)
            ry = ROWY[tg]
            pts = [(522, 230), (560, 230), (675, ry), (790, ry), (850, SY[tg] + 10)]
            dpos = pth(pts, p)
            dcol = AMBER if p < 0.5 else (BLUE if tg == "blue" else GREEN)
            cap = "요청 %d: %s로 갑니다 · 카운터 %d → %d" % (r + 1, tg, r, (r + 1) % 4)
            capc = BLUE_T if tg == "blue" else GREEN_T
        else:
            tally = ["blue", "blue", "blue", "green"]
            cap = "같은 요청이 매번 이 순서로 지나고, 3 : 1 로 나뉩니다"
            capc = GOOD
            cnt = 0

        # ---- 코드 패널
        cv.rr(30, 104, 430, 452, 14, fill=DARK, outline=None)
        cv.text(418, 116, "nginx.conf", 12, (150, 160, 190), False, "ra")
        hl = lines_for(area, tg)
        for q, t in enumerate(CODE):
            cy = 136 + q * 28.5
            if q in hl:
                cv.rr(36, cy - 13, 424, cy + 13, 6, fill=HEXTRA)
            cv.text(48, cy, t, 14, AMBER if q in hl else (200, 215, 225), q in hl, "lm", True)
        # ---- 번호표
        act_ix = AREA_IX.get(area, -1)
        for k in range(6):
            cx = 480 + k * 44
            on = k == act_ix
            cv.circ(cx, 118, 14, fill=TEAL if on else LGRAY, outline=TEAL if on else LINE, w=2)
            cv.text(cx, 118, str(k + 1), 15, WHITE if on else MUTE, True, "mm")
        # ---- 사용자와 받은 곳
        user(cv, 490, 230)
        cv.text(490, 312, "받은 server", 13, MUTE, False, "mm")
        for k, c in enumerate(tally):
            cv.circ(464 + k * 24, 336, 9, fill=BLUE if c == "blue" else GREEN, outline=WHITE, w=2)
        # ---- Nginx 박스
        cv.rr(560, 136, 790, 452, 14, fill=LTEAL, outline=TEAL, w=4)
        cv.text(675, 152, "Nginx", 20, TEAL, True, "mm")
        for nm, x0, x1, key in (("listen 80", 572, 676, "listen"), ("proxy_pass", 684, 778, "proxy")):
            on = area == key
            cv.rr(x0, 170, x1, 200, 8, fill=LAMB if on else WHITE, outline=AMBER if on else LINE, w=2)
            cv.text((x0 + x1) / 2, 185, nm, 13, WARN if on else INK, True, "mm")
        on_list = area in ("list", "rule")
        cv.rr(572, 214, 778, 302, 8, fill=LAMB if area == "list" else WHITE, outline=AMBER if on_list else LINE, w=2)
        cv.text(675, 228, "upstream active_app", 13, INK, True, "mm")
        for nm, key, wt, y0 in (("blue", "blue", "weight 3", 240), ("green", "green", "weight 1", 268)):
            sel = area in ("rule", "zone", "send") and tg == key
            cv.rr(580, y0, 770, y0 + 24, 6, fill=(LBLUE if key == "blue" else LGREEN) if sel else LGRAY,
                  outline=(BLUE if key == "blue" else GREEN) if sel else LINE, w=2)
            cv.text(675, y0 + 12, "%s   %s" % (nm, wt), 13, INK, sel, "mm")
        onz = area == "zone"
        cv.rr(572, 316, 778, 444, 8, fill=LAMB if onz else WHITE, outline=AMBER if onz else LINE, w=2)
        cv.text(675, 332, "zone: 공유 메모리", 13, INK, True, "mm")
        cv.text(675, 354, "다음 차례 카운터", 13, MUTE, False, "mm")
        cv.text(675, 394, str(cnt), 34, WARN if onz else INK, True, "mm")
        cv.text(675, 428, "0·1·2 는 blue, 3 은 green", 13, MUTE, False, "mm")
        # ---- server
        for nm, y0, col in (("blue", 150, BLUE), ("green", 360, GREEN)):
            act = area == "send" and tg == nm
            server_box(cv, 840, y0, 970, y0 + 80, nm, "v1" if nm == "blue" else "v2", col, "active")
            cv.arrow(792, ROWY[nm], 836, y0 + 40, col, 4, 10) if act else cv.dash(792, ROWY[nm], 836, y0 + 40, LINE, 2)
        if dpos:
            dot(cv, dpos[0], dpos[1], dcol)
        if resp:
            cv.text(490, 188, "응답", 14, GOOD, True, "mm")
        caption(cv, cap, capc)
        return cv.done()

    fr = [draw(i) for i in range(TOTAL)]
    dbg("path", fr, [3, 15, 27, 38, 49, 60, 70, 76, 93, 104, 112, 123])
    return fr


# ============================================================ 4) 배포와 요청
def fig_cicd():
    N = 112
    FL = 64
    LIT = [6, 18, 30, 42, FL]
    CH = ["push", "테스트", "이미지 만들기", "새 버전(green) 올리기", "방향 바꾸기"]

    def draw(j):
        cv = Cv()
        head(cv, "배포할 때와 요청이 올 때는 서로 다른 시간", "CI/CD는 배포할 때 한 번, Nginx의 길 정하기는 요청이 올 때마다 계속")
        hl1 = j < 44
        hl2 = 44 <= j < FL or j >= FL
        cv.rr(24, 102, 976, 256, 16, fill=WHITE, outline=TEAL if hl1 else LINE, w=3 if hl1 else 2)
        cv.rr(24, 262, 976, 456, 16, fill=WHITE, outline=TEAL if (44 <= j) else LINE, w=3 if j >= 44 else 2)
        cv.text(44, 120, "배포할 때 (코드를 push할 때마다 한 번)", 19, INK, True, "lm")
        for k, t in enumerate(CH):
            x0 = 40 + k * 184
            a = ramp(j, LIT[k], 4)
            last = k == 4
            fill = mix(LGRAY, LAMB if last else LBLUE, a)
            oc = mix(LINE, AMBER if last else BLUE, a)
            tc = mix(MUTE, INK, a)
            w = 4
            if last and FL <= j < FL + 14:
                oc, w = AMBER, 6
            cv.rr(x0, 140, x0 + 160, 192, 12, fill=fill, outline=oc, w=w)
            cv.fit(x0 + 80, 166, t, 16, 144, tc, True, "mm")
            if k > 0:
                cv.arrow(x0 - 22, 166, x0 - 3, 166, mix(LINE, MUTE, a), 3, 8)
        na = ramp(j, FL + 2, 5)
        if na > 0:
            cv.fit(956, 214, "오늘 실습: 사람이 upstream 줄을 고치고 reload", 15, 440, fade(WARN, na), True, "ra")
            cv.fit(956, 238, "Cloud Run: 플랫폼이 대신 함", 15, 440, fade(GOOD, na), True, "ra")
        # ---- 아래 레인
        cv.text(44, 280, "요청이 올 때 (사용자가 쓰는 동안 계속)", 19, INK, True, "lm")
        cv.text(956, 280, "실패 0건", 20, GOOD, True, "rm")
        user(cv, 80, 372)
        nbox(cv, 270, 336, 390, 406, ["Nginx"], LTEAL, TEAL, INK, 20)
        cv.arrow(114, 372, 266, 372, LINE, 3, 10)
        on_g = j >= FL
        for nm, cy, col in (("blue", 329, BLUE), ("green", 411, GREEN)):
            act = (nm == "green") == on_g
            if act:
                cv.arrow(394, 371, 596, cy, col, 5, 14)
            else:
                cv.dash(394, 371, 596, cy, LINE, 2)
        server_box(cv, 600, 296, 780, 362, "blue", "v1 · 대기" if on_g else "v1 · 받는 중", BLUE, "dim" if on_g else "active")
        server_box(cv, 600, 378, 780, 444, "green", "v2 · 받는 중" if on_g else "v2 · 대기", GREEN, "active" if on_g else "dim")
        if FL <= j < FL + 14:
            pill(cv, 330, 316, "방향 바꿈!", LAMB, WARN, 15)
        for k in range(20):
            s0 = 6 * k
            p = (j - s0) / 26
            dec = s0 + 11
            tg = "green" if dec >= FL else "blue"
            cy = 411 if tg == "green" else 329
            if 0 <= p <= 1:
                x, y = pth([(114, 372), (268, 372), (596, cy)], p)
                hdot(cv, x, y, GREEN if tg == "green" else BLUE, 268, 392)
        if j < 44:
            caption(cv, "배포는 push할 때 한 번 일어납니다", INK)
        elif j < FL:
            caption(cv, "요청은 배포와 상관없이 계속 옵니다", INK)
        else:
            caption(cv, "배포의 마지막 단계가 요청의 길을 바꿉니다 — 요청은 끊기지 않습니다", GOOD)
        return cv.done()

    fr = [draw(j) for j in range(N)]
    dbg("cicd", fr, [8, 30, 50, 66, 80, 111])
    return fr


if __name__ == "__main__":
    only = sys.argv[2] if len(sys.argv) > 2 else "all"
    if only in ("all", "two"):
        save("fig-1-두조건.gif", fig_two())
    if only in ("all", "methods"):
        save("fig-2-배포방식.gif", fig_methods())
    if only in ("all", "path"):
        save("fig-3-Nginx길.gif", fig_path())
    if only in ("all", "cicd"):
        save("fig-4-배포와요청.gif", fig_cicd())
