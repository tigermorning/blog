import sys, math, os
from make_figs_d3_p import head, nbox, pill, fade, ramp
from make_gifs_p import *
from make_figs_d3h import lerp, pth, hdot

DBG = os.environ.get("DBGDIR")
DUR = 200
CODE_BG = (40, 43, 64)
TERM_BG = (28, 30, 46)
CODE_TX = (226, 226, 240)
CODE_KW = (190, 170, 245)
CODE_DIM = (140, 140, 165)
HL_BG = (104, 88, 44)
HL_TX = (255, 224, 140)


def save_slow(name, frames, dur=DUR):
    stride = max(1, len(frames) // 14)
    sample = Image.new("RGB", (W, H * len(frames[::stride])))
    for k, f in enumerate(frames[::stride]):
        sample.paste(f, (0, k * H))
    pal = sample.quantize(colors=255, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
    q = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in frames]
    durs = [dur] * len(frames)
    durs[0] = 1200
    durs[-1] = 3500
    path = os.path.join(OUT, name)
    q[0].save(path, save_all=True, append_images=q[1:], duration=durs, loop=0, disposal=1, optimize=False)
    print(path, len(frames), "frames", os.path.getsize(path) // 1024, "KB", dur, "ms")


def dbg(name, frames, idxs):
    if not DBG:
        return
    os.makedirs(DBG, exist_ok=True)
    for ix in idxs:
        if ix < len(frames):
            frames[ix].save(os.path.join(DBG, "%s_%03d.png" % (name, ix)))


# ============================================================ 1) 같은 결함
def fig_fault():
    N, T0, TD, TT, SW, RB = 96, 14, 70, 84, 22, 72
    cxs = [190, 500, 810]
    names = ["롤링", "블루그린", "카나리"]
    TX0, TX1 = 90, 940

    def tx(f):
        return TX0 + (TX1 - TX0) * min(f, TT) / TT

    def v2_roll(i, f):
        return (i == 0 and f >= 18) or (i == 1 and f >= 44)

    def rollc(i, cx):
        return cx - 144 + i * 74 + 33

    def target(m, k, fd):
        cx = cxs[m]
        if m == 0:
            i = k % 4
            return rollc(i, cx), v2_roll(i, fd)
        if m == 1:
            g = SW <= fd < RB
            return (cx + 66, True) if g else (cx - 66, False)
        bad = fd >= T0 and k % 10 == 5
        return (cx + 98, True) if bad else (cx - 52, False)

    def val(m, f):
        if m == 0:
            return 25 * ramp(f, 18, 5) + 25 * ramp(f, 44, 5)
        if m == 1:
            return 100 * ramp(f, SW, 6)
        return 10 * ramp(f, T0 + 2, 10)

    def draw(f):
        cv = Cv()
        head(cv, "같은 결함, 방식마다 영향이 다르다", "새 버전에 결함이 있고 세 방식 모두 같은 시각에 발견한다 (숫자는 설명용 예시)")
        final = f >= TT
        for m, cx in enumerate(cxs):
            cv.rr(cx - 150, 102, cx + 150, 404, 14, fill=WHITE, outline=LINE, w=2)
            cv.text(cx, 120, names[m], 20, INK, True, "mm")
            nbox(cv, cx - 45, 166, cx + 45, 198, ["Nginx"], LTEAL, TEAL, INK, 16, w=2)
            # server boxes
            if m == 0:
                for i in range(4):
                    x0 = cx - 144 + i * 74
                    bad = v2_roll(i, f)
                    swapping = (i == 0 and 14 <= f < 18) or (i == 1 and 40 <= f < 44)
                    if swapping:
                        cv.rr(x0, 244, x0 + 66, 296, 10, fill=LAMB, outline=AMBER, w=3)
                        cv.text(x0 + 33, 270, "교체", 15, WARN, True, "mm")
                    elif bad:
                        cv.rr(x0, 244, x0 + 66, 296, 10, fill=LRED, outline=RED, w=3)
                        cv.text(x0 + 33, 270, "v2", 20, RED, True, "mm")
                    else:
                        cv.rr(x0, 244, x0 + 66, 296, 10, fill=mix(WHITE, BLUE, 0.28), outline=BLUE, w=3)
                        cv.text(x0 + 33, 270, "v1", 20, INK, True, "mm")
                st = "v1 4대 (정상)" if f < 18 else ("v2 1대 / 4대" if f < 44 else "v2 2대 / 4대")
                stc = INK if f < 18 else RED
            elif m == 1:
                on_g = SW <= f < RB
                bx0, gx0 = cx - 126, cx + 6
                cv.rr(bx0, 244, bx0 + 120, 296, 10, fill=LGRAY if on_g else mix(WHITE, BLUE, 0.28),
                      outline=LINE if on_g else BLUE, w=3)
                cv.text(bx0 + 60, 262, "blue", 17, MUTE if on_g else INK, True, "mm")
                cv.text(bx0 + 60, 282, "v1", 14, MUTE if on_g else BLUE_T, True, "mm")
                if f < T0:
                    cv.rr(gx0, 244, gx0 + 120, 296, 10, fill=BG, outline=LINE, w=2)
                    cv.text(gx0 + 60, 270, "(미배포)", 14, MUTE, False, "mm")
                else:
                    cv.rr(gx0, 244, gx0 + 120, 296, 10, fill=mix(WHITE, GREEN, 0.28) if on_g else LGRAY,
                          outline=RED if on_g else LINE, w=4 if on_g else 2)
                    cv.text(gx0 + 60, 262, "green", 17, INK if on_g else MUTE, True, "mm")
                    cv.text(gx0 + 60, 282, "v2 (결함)", 14, RED if on_g else MUTE, True, "mm")
                if f < T0:
                    st, stc = "blue가 받는 중", INK
                elif f < SW:
                    st, stc = "green(v2) 준비만 함", WARN
                elif f < RB:
                    st, stc = "모두 green(v2)으로 전환", RED
                else:
                    st, stc = "blue로 되돌림, 오류 멈춤", GOOD
            else:
                cv.rr(cx - 142, 244, cx + 38, 296, 10, fill=mix(WHITE, BLUE, 0.28), outline=BLUE, w=3)
                cv.text(cx - 52, 262, "v1", 18, INK, True, "mm")
                cv.text(cx - 52, 282, "90%", 14, BLUE_T, True, "mm")
                if f < T0:
                    cv.rr(cx + 54, 244, cx + 142, 296, 10, fill=BG, outline=LINE, w=2)
                    cv.text(cx + 98, 270, "(미배포)", 14, MUTE, False, "mm")
                else:
                    cv.rr(cx + 54, 244, cx + 142, 296, 10, fill=LRED, outline=RED, w=3)
                    cv.text(cx + 98, 262, "v2", 18, RED, True, "mm")
                    cv.text(cx + 98, 282, "10%", 14, RED, True, "mm")
                st, stc = ("v1이 전부 받음", INK) if f < T0 else ("v2는 10%만 받음", RED)
            cv.fit(cx, 311, st, 15, 280, stc, True, "mm")
            # 오류 비율 막대
            cv.text(cx, 331, "오류를 본 요청 비율", 14, MUTE, False, "mm")
            bx0, bx1 = cx - 120, cx + 120
            cv.rr(bx0, 341, bx1, 361, 10, fill=LGRAY, outline=LINE, w=2)
            v = val(m, f)
            if v > 0.5:
                cv.rr(bx0, 341, bx0 + (bx1 - bx0) * v / 100, 361, 10, fill=RED)
            if final:
                t = ["약 50%", "100%", "약 10%"][m]
                tw = cv.d.textlength(t, font=font(30, True)) / S + 30
                cv.rr(cx - tw / 2, 365, cx + tw / 2, 398, 12, fill=LRED, outline=RED, w=2)
                cv.text(cx, 382, t, 30, RED, True, "mm")
            else:
                cv.text(cx, 384, "%d%%" % round(v), 24, RED if v > 0.5 else MUTE, True, "mm")
        # 점 흐름
        for m, cx in enumerate(cxs):
            for k in range(-4, 27):
                s0 = 4 * k + m
                p = (f - s0) / 17.0
                if p < 0 or p > 1:
                    continue
                if p < 0.35:
                    cv.circ(cx, 138 + 24 * p / 0.35, 8, fill=BLUE, outline=WHITE, w=2)
                elif p >= 0.55:
                    sx, bad = target(m, k, s0 + 0.55 * 17)
                    q = (p - 0.55) / 0.45
                    cv.circ(lerp(cx, sx, q), 200 + 28 * q, 8, fill=RED if bad else BLUE, outline=WHITE, w=2)
        # 공통 시간 막대
        cv.text(40, 437, "시간", 14, MUTE, True, "lm")
        cv.rr(TX0, 432, TX1, 442, 5, fill=LGRAY, outline=LINE, w=1)
        cv.rr(TX0, 432, tx(f), 442, 5, fill=TEAL)
        for fx, lab, col in ((T0, "결함 있는 새 버전 투입 시작", WARN), (TD, "결함 발견", RED)):
            x = tx(fx)
            passed = f >= fx
            cv.line(x, 426, x, 448, col if passed else MUTE, 3)
            cv.text(x, 414, lab, 14, col if passed else MUTE, True, "mm")
        cv.circ(tx(f), 437, 7, fill=WHITE, outline=TEAL, w=3)
        if f < 36:
            caption(cv, "같은 결함 버전이 들어갑니다", INK)
        elif f < TT:
            caption(cv, "결함을 발견할 때까지 각 방식이 보낸 요청", INK)
        else:
            caption(cv, "카나리는 일부만, 블루그린은 전환 직후 전부 겪지만 되돌리기가 빠릅니다. 롤링은 교체한 만큼 겪습니다", GOOD)
        return cv.done()

    fr = [draw(f) for f in range(N)]
    dbg("fault", fr, [6, 20, 30, 50, 68, 76, 90, N - 1])
    return fr


# ============================================================ 2) 블루그린 실습
def fig_lab():
    lens = [30, 26, 30, 28, 38]
    starts = [sum(lens[:i]) for i in range(5)]
    N = sum(lens)
    GRN_FROM = starts[2] + 19
    GRN_TO = starts[4] + 16
    tabs = ["1 전환 전 확인", "2 설정 줄 고치기", "3 검사 후 reload", "4 결과", "5 롤백"]
    caps = ["전환 전에 green이 정상인지 먼저 확인합니다", "upstream 안의 server 한 줄만 바꿉니다",
            "문법 검사에 성공한 뒤에만 reload합니다", "전환하는 동안 실패한 요청이 없었습니다 (내 실습 결과)",
            "blue를 끄지 않았기 때문에 줄만 되돌리면 바로 돌아옵니다"]

    def stepof(f):
        s = 0
        for i in range(5):
            if f >= starts[i]:
                s = i
        return s, f - starts[s]

    def route(f):
        return "g" if GRN_FROM <= f < GRN_TO else "b"

    def rev(t, j, start, cps=8):
        if j < start:
            return None
        return t[: int((j - start + 1) * cps)]

    def mono_w(t, sz):
        return cv_measure.d.textlength(t, font=font(sz, False, True)) / S

    cv_measure = Cv()

    def draw(f):
        cv = Cv()
        s, j = stepof(f)
        head(cv, "블루그린 전환 실습 따라가기", "내 컴퓨터에서 실제로 한 순서와 결과")
        # ---- 탭
        x = 40
        for k, t in enumerate(tabs):
            w = cv.d.textlength(t, font=font(16, True)) / S + 30
            if k == s:
                cv.rr(x, 108, x + w, 140, 16, fill=TEAL, outline=TEAL, w=2)
                tc = WHITE
            elif k < s:
                cv.rr(x, 108, x + w, 140, 16, fill=LTEAL, outline=TEAL, w=2)
                tc = PURP
            else:
                cv.rr(x, 108, x + w, 140, 16, fill=LGRAY, outline=None)
                tc = MUTE
            cv.text(x + w / 2, 124, t, 16, tc, True, "mm")
            x += w + 12
        # ---- 왼쪽 그림
        rt = route(f)
        user(cv, 62, 290)
        cv.arrow(96, 290, 146, 290, LINE, 3, 9)
        nbox(cv, 150, 255, 250, 325, ["Nginx", "bg-nginx"], LTEAL, TEAL, INK, 18)
        for nm, cy, col, key in (("blue", 210, BLUE, "b"), ("green", 370, GREEN, "g")):
            act = rt == key
            if act:
                cv.arrow(254, 290, 314, cy, col, 5, 13)
            else:
                cv.dash(254, 290, 314, cy, LINE, 2)
        bl_on, gr_on = rt == "b", rt == "g"
        server_box(cv, 320, 175, 440, 245, "blue", "v1 · 받는 중" if bl_on else "v1 · 대기", BLUE, "active" if bl_on else "dim")
        server_box(cv, 320, 335, 440, 405, "green", "v2 · 받는 중" if gr_on else "v2 · 대기", GREEN, "active" if gr_on else "dim")
        if s == 0 and j >= 3:
            a = ramp(j, 3, 4)
            cv.arrow(316, 372, 262, 318, mix(BG, GOOD, a), 4, 11)
            if j >= 12:
                pill(cv, 380, 428, "정상 (헬스체크 응답)", LGREEN, GOOD, 14, ramp(j, 12, 3))
            else:
                pill(cv, 380, 428, "/health 확인 중", LAMB, WARN, 14, a)
        if s == 1:
            pill(cv, 160, 430, "요청은 아직 blue로 갑니다", LAMB, WARN, 14)
        if (s == 2 and 13 <= j < 24) or (s == 4 and 10 <= j < 21):
            pill(cv, 200, 238, "reload!", LAMB, WARN, 15)
        # 요청 점
        for k in range(-4, N // 5 + 3):
            s0 = 5 * k
            p = (f - s0) / 18.0
            if p < 0 or p > 1:
                continue
            tg = route(int(s0 + 0.62 * 18))
            cy = 370 if tg == "g" else 210
            x, y = pth([(96, 290), (256, 290), (306, cy)], p)
            hdot(cv, x, y, AMBER if x < 150 else (GREEN if tg == "g" else BLUE), 148, 252)
        # ---- default.conf 패널
        cv.rr(460, 148, 960, 330, 12, fill=CODE_BG)
        cv.text(476, 164, "default.conf", 14, CODE_DIM, True, "lm")
        if s == 0:
            tgt, hl = "blue", False
        elif s == 1:
            tgt, hl = ("blue", False) if j < 6 else ("green", True)
        elif s in (2, 3):
            tgt, hl = "green", False
        else:
            tgt, hl = ("green", False) if j < 4 else ("blue", j < 16)
        lines = [("upstream active_app {", 0), ("    zone active_app 64k;", 0), ("    server %s:8080;" % tgt, 1), ("}", 0),
                 ("# inside server { }", 0), ("location / { proxy_pass http://active_app; }", 0)]
        ly = 196
        for k, (t, kind) in enumerate(lines):
            y = ly + k * 24
            if kind == 1 and hl:
                cv.rr(468, y - 11, 952, y + 11, 4, fill=HL_BG)
                cv.text(480, y, t, 16, HL_TX, True, "lm", True)
                cv.text(944, y, "바뀐 줄", 14, HL_TX, True, "rm")
            elif t:
                cv.text(480, y, t, 16, CODE_TX, False, "lm", True)
        # ---- 터미널 / 결과
        if s <= 2 or (s == 4 and j < 22):
            cv.rr(460, 340, 960, 456, 12, fill=TERM_BG)
            cv.text(476, 356, "터미널", 13, CODE_DIM, True, "lm")
            rows = []
            if s == 0:
                rows = [(rev("$ docker exec bg-nginx wget -qO- http://green:8080/health", j, 3, 9), CODE_TX),
                        ('{"ok":true,"ocr_enabled":true}' if j >= 14 else None, (140, 230, 180))]
            elif s == 1:
                rows = [("# 설정 줄만 고쳤습니다. 아직 reload 전입니다" if j >= 6 else None, CODE_DIM)]
            elif s == 2:
                rows = [(rev("$ nginx -t", j, 2), CODE_TX), ("test is successful" if j >= 8 else None, (140, 230, 180)),
                        (rev("$ nginx -s reload", j, 13), CODE_TX)]
            else:
                rows = [(rev("$ nginx -s reload", j, 10), CODE_TX)]
            for k, (t, c) in enumerate(rows):
                if t:
                    y = 382 + k * 24
                    if t.startswith("#"):
                        cv.text(476, y, t, 14, c, False, "lm")
                    else:
                        cv.text(476, y, t, 14, c, False, "lm", True)
        else:
            cv.rr(460, 340, 960, 456, 12, fill=WHITE, outline=GOOD, w=3)
            cv.text(476, 356, "요청 확인 결과", 14, MUTE, True, "lm")
            if s == 3:
                a1 = ramp(j, 3, 3)
                cv.text(710, 388, "150건 중 실패 0건", 26, fade(GOOD, a1), True, "mm")
                a2 = ramp(j, 9, 3)
                if a2 > 0:
                    cv.rr(500, 407, 500 + 420 * 0.32, 425, 6, fill=fade(BLUE, a2))
                    cv.rr(500 + 420 * 0.32, 407, 920, 425, 6, fill=fade(GREEN, a2))
                    cv.text(710, 441, "blue 32%    green 68%", 20, fade(INK, a2), True, "mm")
            else:
                a1 = ramp(j, 22, 3)
                cv.text(710, 392, "70건 중 실패 0건", 26, fade(GOOD, a1), True, "mm")
                a2 = ramp(j, 28, 3)
                cv.text(710, 428, "blue는 켜져 있어 바로 복귀", 18, fade(BLUE_T, a2), True, "mm")
        caption(cv, caps[s], INK if s < 3 else GOOD)
        return cv.done()

    fr = [draw(f) for f in range(N)]
    dbg("lab", fr, [starts[0] + 20, starts[1] + 12, starts[2] + 10, starts[2] + 24, starts[3] + 14,
                    starts[4] + 8, starts[4] + 20, starts[4] + 34, N - 1])
    return fr


PURP = mix(TEAL, INK, 0.35)

if __name__ == "__main__":
    only = sys.argv[2] if len(sys.argv) > 2 else "all"
    if only in ("all", "fault"):
        save_slow("fig-5-같은결함.gif", fig_fault())
    if only in ("all", "lab"):
        save_slow("fig-6-블루그린실습.gif", fig_lab())
