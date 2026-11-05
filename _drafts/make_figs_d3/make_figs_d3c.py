import sys
from make_figs_d3 import head, nbox, pill, fade, ramp
from make_gifs import *

# ================================================================ proxy
def fig_proxy():
    fr = []
    N = 134
    UX = 80
    SV = (800, 250, 940, 350)

    def px(i):
        # 프록시 상자 왼쪽 x 위치: A 가운데 -> B 사용자 쪽 -> C server 쪽
        if i < 48: return 430
        if i < 62: return 430 + (250 - 430) * smooth((i - 48) / 14)
        if i < 86: return 250
        if i < 100: return 250 + (630 - 250) * smooth((i - 86) / 14)
        return 630

    for i in range(N):
        cv = Cv()
        head(cv, "proxy: 대신 받아 넘기는 중간 창구", "요청과 응답이 모두 proxy를 거친다 · 서는 자리에 따라 이름이 달라진다")
        xp = px(i)
        in_b = 48 <= i < 100
        in_c = i >= 86
        # 구역
        if i >= 48:
            a = ramp(i, 48, 8)
            cv.rr(30, 140, 380, 440, 16, fill=fade(LGRAY, a), outline=fade(LINE, a), w=2)
            cv.text(205, 158, "사용자 쪽", 16, fade(MUTE, a), True, "mm")
            cv.rr(590, 140, 970, 440, 16, fill=fade(LAMB, a), outline=fade(LINE, a), w=2)
            cv.text(780, 158, "server 쪽", 16, fade(WARN, a), True, "mm")
        user(cv, UX, 300)
        server_box(cv, SV[0], SV[1], SV[2], SV[3], "server", "", BLUE, "active")
        # 길
        cv.line(UX + 40, 297, xp, 297, LINE, 3)
        cv.line(xp + 120, 297, SV[0], 297, LINE, 3)
        cv.text((UX + 40 + xp) / 2, 270, "요청 →", 14, MUTE, True, "mm") if xp - UX > 150 else None
        cv.text((xp + 120 + SV[0]) / 2, 270, "요청 →", 14, MUTE, True, "mm") if SV[0] - xp - 120 > 100 else None
        cv.text((UX + 40 + xp) / 2, 326, "← 응답", 14, MUTE, True, "mm") if xp - UX > 150 else None
        cv.text((xp + 120 + SV[0]) / 2, 326, "← 응답", 14, MUTE, True, "mm") if SV[0] - xp - 120 > 100 else None
        # reverse 장면: 울타리와 직접 접근 불가 표시
        if i >= 100:
            a = ramp(i, 100, 8)
            cv.dash(792, 238, 948, 238, fade(RED, a), 3)
            cv.dash(792, 362, 948, 362, fade(RED, a), 3)
            cv.dash(792, 238, 792, 362, fade(RED, a), 3)
            cv.dash(948, 238, 948, 362, fade(RED, a), 3)
            pill(cv, 870, 388, "바깥에 직접 드러나지 않음", LRED, RED, 14, a)
        # 점: 요청(청록) / 응답(앰버)
        for s in range(0, N, 24):
            p = (i - s) / 24
            if 0 <= p <= 1:
                x = UX + 40 + (SV[0] - UX - 40) * p
                dot(cv, x, 297 - 0, BLUE)
            q = (i - (s + 24)) / 24
            if 0 <= q <= 1:
                x = SV[0] - (SV[0] - UX - 40) * q
                dot(cv, x, 297, AMBER)
        # proxy 상자 (점을 가려서 '안으로 들어갔다 나오는' 모습)
        cv.rr(xp, 240, xp + 120, 354, 14, fill=LTEAL, outline=TEAL, w=4)
        cv.text(xp + 60, 275, "proxy", 22, TEAL, True, "mm")
        cv.text(xp + 60, 308, "대신 받아", 14, INK, False, "mm")
        cv.text(xp + 60, 328, "대신 넘김", 14, INK, False, "mm")
        if i < 48:
            caption(cv, "proxy는 요청과 응답을 대신 받아 넘겨 주는 중간 창구입니다")
        elif i < 86:
            caption(cv, "사용자 쪽에 서면 forward proxy: 나가는 요청을 대신 보냅니다", INK)
        else:
            caption(cv, "server 쪽에 서면 reverse proxy: 들어오는 요청을 대신 받습니다 (Nginx의 역할)", GOOD)
        fr.append(cv.done())
    return fr

# ================================================================ upstream
def fig_upstream():
    fr = []
    N = 150
    CODE_A = ["upstream active_app {", "  server blue:8080;", "  server green:8080;", "}"]
    CODE_B = ["upstream active_app {", "  server blue:8080 weight=3;", "  server green:8080;",
              "  server spare:8080 backup;", "}"]
    NX = (470, 255, 580, 345)
    CARD = (690, 124, 960, 436)
    ROWS = {"blue": (170, 246), "green": (256, 332), "spare": (342, 418)}
    RC = {k: (v[0] + v[1]) / 2 for k, v in ROWS.items()}
    ROWCOL = {"blue": BLUE, "green": AMBER, "spare": MUTE}

    def dest_list():
        d = []
        # A: round robin
        for k in range(4):
            d.append((8 + k * 11, "blue" if k % 2 == 0 else "green"))
        # B: weight 3:1 (blue, blue, blue, green) 반복
        seq = ["blue", "blue", "blue", "green", "blue", "blue"]
        for k, nm in enumerate(seq):
            d.append((56 + k * 7, nm))
        # C
        d.append((104, "blue"))        # 이 요청이 실패
        for k in range(5):
            d.append((114 + k * 6, "green"))
        d.append((146 - 4, "blue"))    # 10초 뒤 다시 보내 봄
        return d
    reqs = dest_list()
    for i in range(N):
        cv = Cv()
        head(cv, "upstream: 넘겨받을 server의 목록", "proxy_pass가 가리키는 이름의 server 목록을 Nginx가 이 블록에서 읽는다")
        phase = 0 if i < 52 else (1 if i < 100 else 2)
        code = CODE_A if phase == 0 else CODE_B
        cv.rr(40, 108, 450, 452, 14, fill=DARK)
        for k, t in enumerate(code):
            cv.text(56, 140 + k * 30, t, 15, (225, 220, 210), False, "lm", True)
        if phase >= 1:
            a = ramp(i, 52, 6)
            cv.rr(52, 168 - 14 + 0, 440, 168 + 14 + 0, 6, fill=fade(DARK, 0)) if False else None
        cv.text(56, 140 + len(code) * 30 + 26, "# proxy_pass http://active_app;", 13, (140, 132, 120), False, "lm", True)
        # Nginx
        nginx_box(cv, NX[0], NX[1], NX[2], NX[3], "")
        cv.text(525, 315, "proxy_pass", 13, INK, False, "mm", True)
        # 목록 카드
        cv.rr(CARD[0], CARD[1], CARD[2], CARD[3], 14, fill=WHITE, outline=BLUE, w=3)
        cv.text(825, 146, "active_app 목록", 17, INK, True, "mm")
        blue_down = 104 <= i < 140
        names = ["blue", "green"] + (["spare"] if phase >= 1 else [])
        for nm in names:
            y0, y1 = ROWS[nm]
            col = ROWCOL[nm]
            if nm == "blue" and blue_down:
                cv.rr(700, y0, 950, y1, 10, fill=LRED, outline=RED, w=3)
                cv.text(716, y0 + 18, "blue:8080", 16, RED, True, "lm")
                xmark(cv, 925, y0 + 18, 8, RED, 4)
                cv.text(716, y0 + 44, "10초 동안 제외", 14, RED, True, "lm")
                cv.text(716, y0 + 62, "max_fails=1 fail_timeout=10s", 11, RED, False, "lm", True)
            else:
                cv.rr(700, y0, 950, y1, 10, fill=LGRAY if nm == "spare" else WHITE, outline=col, w=3)
                cv.text(716, y0 + 18, nm + ":8080", 16, INK, True, "lm")
                if nm == "blue" and phase >= 1:
                    pill(cv, 830, y0 + 54, "weight=3: 몫 3배", LBLUE, GOOD, 13)
                if nm == "spare":
                    pill(cv, 830, y0 + 54, "backup: 나머지가 다 빠지면", LGRAY, MUTE, 13)
        if blue_down:
            pr = (i - 104) / 36
            cv.rr(716, ROWS["blue"][1] - 8, 716 + 220 * pr, ROWS["blue"][1] - 3, 3, fill=RED) if False else None
        # 요청 점
        for (s, nm) in reqs:
            p = (i - s) / 18
            if 0 <= p <= 1:
                y1 = RC[nm]
                x, y = along([(NX[2], 300), (690, y1), (700, y1)], [1.0, 0.08], p) if False else (NX[2] + (698 - NX[2]) * p, 300 + (y1 - 300) * p)
                failed = (s == 104)
                dot(cv, x, y, RED if (failed and p > 0.6) else ROWCOL[nm] if nm != "spare" else MUTE)
                if failed and p > 0.85:
                    xmark(cv, 712, y1, 9, RED, 4)
        if i < 52:
            caption(cv, "upstream은 넘겨받을 server의 목록입니다. 요청마다 규칙으로 한 줄을 고릅니다")
        elif i < 100:
            caption(cv, "server 줄 뒤의 옵션으로 몫(weight)과 역할(backup)을 정합니다", INK)
        elif i < 124:
            caption(cv, "요청이 실패한 server는 일정 시간 목록에서 빠집니다", RED)
        elif i < 140:
            caption(cv, "빠진 동안은 목록의 다른 server가 요청을 받습니다", INK)
        else:
            caption(cv, "10초가 지나면 요청 하나를 다시 보내 봅니다", GOOD)
        fr.append(cv.done())
    return fr

if __name__ == "__main__":
    only = sys.argv[2] if len(sys.argv) > 2 else "all"
    if only in ("all", "p"):
        save("figP-proxy.gif", fig_proxy())
    if only in ("all", "u"):
        save("figU-upstream.gif", fig_upstream())
