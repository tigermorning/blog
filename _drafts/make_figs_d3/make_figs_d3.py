import sys
sys.argv = [sys.argv[0], sys.argv[1]] + sys.argv[2:3]
from make_gifs import *

ONLY = sys.argv[2] if len(sys.argv) > 2 else "all"

def head(cv, title, sub):
    cv.text(40, 18, title, 30, INK, True)
    cv.text(40, 60, sub, 16, MUTE)
    cv.line(40, 94, 960, 94, LINE, 2)

def fade(c, a):
    return mix(BG, c, a)

def ramp(i, start, dur=6):
    return smooth((i - start) / dur)

def nbox(cv, x0, y0, x1, y1, lines, fill=WHITE, outline=LINE, tc=INK, sz=19, a=1.0, w=3, bold=True):
    if a <= 0:
        return
    cv.rr(x0, y0, x1, y1, 12, fill=fade(fill, a), outline=fade(outline, a), w=w)
    n = len(lines); cx = (x0 + x1) / 2; cy = (y0 + y1) / 2
    for k, t in enumerate(lines):
        cv.fit(cx, cy + (k - (n - 1) / 2) * (sz + 8), t, sz, (x1 - x0) - 18, fade(tc, a), bold, "mm")

def pill(cv, cx, cy, t, fill, tc, sz=16, a=1.0):
    if a <= 0:
        return
    w = cv.d.textlength(t, font=font(sz, True)) / S + 28
    cv.rr(cx - w / 2, cy - 15, cx + w / 2, cy + 15, 15, fill=fade(fill, a))
    cv.text(cx, cy, t, sz, fade(tc, a), True, "mm")

# ============================================================ fig2 헬스체크
def fig_health():
    fr = []
    N = 134
    xs = [40, 270, 500, 730]
    lanes = [
        dict(y=112, title="수동 헬스체크 · 무료 Nginx", start=6,
             items=[(["green이 멈춤"], LGRAY, LINE, INK),
                    (["사용자의 요청이", "green으로 감"], WHITE, BLUE, INK),
                    (["요청이 실패함"], LRED, RED, RED),
                    (["그제야 Nginx가", "green을 뺌"], LAMB, AMBER, WARN)],
             badge="처음 알아챈 쪽 = 사용자의 요청", bcol=(LRED, RED), foot=None),
        dict(y=282, title="능동 헬스체크 · HAProxy, 클라우드 로드밸런서, 유료 NGINX Plus", start=66,
             items=[(["green이 멈춤"], LGRAY, LINE, INK),
                    (["로드밸런서가 몇 초마다", "/health를 먼저 물음"], WHITE, BLUE, INK),
                    (["정한 횟수만큼", "답이 없음"], LRED, RED, RED),
                    (["사용자 요청이 닿기 전에", "green을 뺌"], LAMB, AMBER, WARN)],
             badge="처음 알아챈 쪽 = 로드밸런서", bcol=(LBLUE, GOOD),
             foot="확인 주기 사이에 간 요청은 실패할 수 있음"),
    ]
    for i in range(N):
        cv = Cv()
        head(cv, "헬스체크: 고장 난 서버를 누가 먼저 알아채나", "green 서버가 갑자기 멈췄을 때, 두 방식의 차례")
        for L in lanes:
            cv.text(40, L["y"], L["title"], 19, INK, True, "lm")
            for k, (lines, fill, outline, tc) in enumerate(L["items"]):
                a = ramp(i, L["start"] + k * 14)
                x0 = xs[k]
                nbox(cv, x0, L["y"] + 22, x0 + 200, L["y"] + 92, lines, fill, outline, tc, 17, a)
                if k > 0:
                    cv.arrow(xs[k - 1] + 204, L["y"] + 57, x0 - 4, L["y"] + 57, fade(MUTE, a), 3, 10)
            ab = ramp(i, L["start"] + 2 * 14 + 8)
            pill(cv, xs[2] + 100, L["y"] + 116, L["badge"], L["bcol"][0], L["bcol"][1], 15, ab)
            if L["foot"]:
                cv.text(40, L["y"] + 150, L["foot"], 14, fade(MUTE, ramp(i, L["start"] + 56)), False, "lm")
        if i < 6:
            caption(cv, "서버 하나가 갑자기 멈췄다고 해 봅시다")
        elif i < 64:
            caption(cv, "수동: 요청이 실패해야 알아챕니다 — 먼저 겪는 쪽은 사용자", RED)
        elif i < 118:
            caption(cv, "능동: 로드밸런서가 미리 물어서 알아챕니다", GOOD)
        else:
            caption(cv, "차이는 하나: 고장을 누가 먼저 알아채느냐", INK)
        fr.append(cv.done())
    return fr

# ============================================================ fig3 대기시간
def fig_timeout():
    fr = []
    N = 124
    TX0, TX1 = 350, 940
    rows = [128, 242, 356]
    for i in range(N):
        cv = Cv()
        head(cv, "연결 대기 시간: 짧을수록 좋을까?", "멈춘 green에 연결을 시도한 요청이 기다리는 시간 (proxy_connect_timeout)")
        # row A
        y = rows[0]
        cv.text(40, y + 14, "기본값: 60초", 23, INK, True, "lm")
        cv.text(40, y + 44, "응답 없는 서버를 포기하기까지", 14, MUTE, False, "lm")
        cv.rr(TX0, y, TX1, y + 38, 8, fill=LGRAY, outline=LINE, w=2)
        pa = max(0, min(1, (i - 8) / 56))
        if pa > 0:
            cv.rr(TX0, y, TX0 + (TX1 - TX0) * pa, y + 38, 8, fill=AMBER)
        if 8 <= i < 64:
            cv.text(TX0, y + 56, "요청이 멈춰 있음 — 사용자 화면이 멈춘 채 기다림", 15, RED, True, "lm")
        elif i >= 64:
            cv.text(TX0, y + 56, "이제야 실패로 보고 → 다른 서버로 넘김", 15, MUTE, True, "lm")
        # row B
        y = rows[1]
        a = ramp(i, 66)
        if a > 0:
            cv.text(40, y + 14, "1초로 줄이면", 23, fade(INK, a), True, "lm")
            cv.text(40, y + 44, "60초의 1/60", 14, fade(MUTE, a), False, "lm")
            cv.rr(TX0, y, TX1, y + 38, 8, fill=fade(LGRAY, a), outline=fade(LINE, a), w=2)
            pb = max(0, min(1, (i - 68) / 3))
            cv.rr(TX0, y, TX0 + (TX1 - TX0) / 60 * pb + 2, y + 38, 4, fill=fade(BLUE, a))
            if i >= 72:
                cv.text(TX0 + 24, y + 19, "1초 만에 → 바로 blue로", 17, fade(GOOD, ramp(i, 72)), True, "lm")
        # row C
        y = rows[2]
        a = ramp(i, 88)
        if a > 0:
            cv.text(40, y + 14, "너무 짧게 잡으면", 23, fade(INK, a), True, "lm")
            cv.text(40, y + 44, "예시: 숫자는 설명용", 14, fade(MUTE, a), False, "lm")
            cv.rr(TX0, y, TX1, y + 38, 8, fill=fade(LGRAY, a), outline=fade(LINE, a), w=2)
            mx = TX0 + 40
            cv.line(mx, y - 8, mx, y + 46, fade(RED, a), 4)
            cv.text(mx + 8, y - 16, "여기서 포기", 13, fade(RED, a), True, "lm")
            pc = max(0, min(1, (i - 92) / 22))
            if pc > 0:
                cv.rr(TX0, y + 8, TX0 + 120 * pc, y + 30, 6, fill=BLUE)
            cv.text(TX0 + 130, y + 19, "정상 서버의 느린 응답", 14, fade(MUTE, a), False, "lm")
            if (i - 92) / 22 * 120 > 40:
                xmark(cv, mx, y + 19, 11, RED, 5)
                cv.text(TX0, y + 56, "정상인데 조금 느렸을 뿐인데 실패로 판정", 15, RED, True, "lm")
        if i < 8:
            caption(cv, "멈춘 서버에 연결을 시도한 요청은 얼마나 기다릴까?")
        elif i < 66:
            caption(cv, "기본값 60초: 기다리는 동안 그 요청이 멈춰 있습니다", RED)
        elif i < 88:
            caption(cv, "1초로 줄이면 바로 다른 서버로 넘어갑니다", GOOD)
        else:
            caption(cv, "하지만 너무 짧으면 정상 서버도 실패로 봅니다 → 넉넉하게", WARN)
        fr.append(cv.done())
    return fr

# ============================================================ fig4 가중치
def fig_weight():
    fr = []
    N = 78
    BX0, BX1 = 330, 800
    rows = [("3 : 1", 0.25, "실습 예시"), ("9 : 1", 0.10, "카나리: 일부에게만"),
            ("99 : 1", 0.01, "카나리: 아주 일부"), ("44 : 55", 55 / 99, "거의 반반")]
    for i in range(N):
        cv = Cv()
        head(cv, "가중치: 새 버전에 요청을 몇 %나 보낼까", "green = 새 버전이라고 가정 · 비율은 설정 파일의 숫자라서 운영자가 정함")
        cv.text(BX0, 112, "blue (지금 버전)", 15, GOOD, True, "lm")
        cv.text(BX1, 112, "green (새 버전)", 15, WARN, True, "rm")
        for k, (lab, g, sub) in enumerate(rows):
            y = 138 + k * 80
            st = 8 + k * 12
            p = smooth((i - st) / 12)
            cv.text(40, y + 22, "blue : green", 14, MUTE, False, "lm")
            cv.text(40, y + 44, lab, 26, INK, True, "lm")
            cv.rr(BX0, y, BX1, y + 54, 10, fill=LGRAY, outline=LINE, w=2)
            wtot = BX1 - BX0
            wb = wtot * (1 - g) * p
            wg = wtot * g * p
            if wb > 2:
                cv.rr(BX0, y, BX0 + wb, y + 54, 10, fill=BLUE)
            if wg > 1:
                cv.rr(BX1 - wg - 0, y, BX1, y + 54, 10 if wg > 20 else 3, fill=AMBER)
            if p > 0.9:
                cv.text(820, y + 20, "green %.4g%%" % round(g * 100, 1) if g * 100 != int(g * 100) else "green %d%%" % int(g * 100), 20, WARN, True, "lm")
                cv.text(820, y + 44, sub, 13, MUTE, False, "lm")
        if i < 8:
            caption(cv, "같은 Nginx, 가중치 숫자만 바꾸면 보내는 비율이 달라집니다")
        elif i < 58:
            caption(cv, "앰버 부분만큼의 사용자가 새 버전을 겪습니다", WARN)
        else:
            caption(cv, "1%로 시작하면 새 버전이 망가져도 100명 중 1명만 겪습니다", GOOD)
        fr.append(cv.done())
    return fr

# ============================================================ fig5 reload vs 재시작
def fig_reload():
    fr = []
    N = 92
    for i in range(N):
        cv = Cv()
        head(cv, "reload와 재시작은 무엇이 다른가", "같은 '다시 적용'처럼 보이지만 바뀌는 범위가 다르다")
        # left panel
        cv.rr(30, 106, 490, 450, 16, fill=WHITE, outline=LINE, w=2)
        cv.text(260, 130, "nginx -s reload", 22, INK, True, "mm", True)
        cv.text(260, 158, "Nginx의 설정만 바꿔 끼움", 15, MUTE, False, "mm")
        cv.rr(60, 184, 460, 330, 12, fill=LGRAY, outline=TEAL, w=3)
        cv.text(260, 202, "Nginx", 17, TEAL, True, "mm")
        oa = 1.0 if i < 44 else max(0.25, 1 - (i - 44) / 10)
        nbox(cv, 80, 222, 230, 316, ["이전 작업 프로세스", "(이전 설정)"], WHITE, MUTE, INK, 14, oa, 3)
        na = ramp(i, 16, 8)
        nbox(cv, 290, 222, 440, 316, ["새 작업 프로세스", "(새 설정)"], WHITE, BLUE, INK, 14, na, 3)
        if i < 40:
            dot(cv, 112, 302, AMBER)
            cv.text(126, 302, "요청 A", 12, MUTE, True, "lm")
        if 26 <= i:
            for k, off in enumerate((30, 62, 94, 126)):
                if i >= 26 + k * 6:
                    dot(cv, 290 + off - 6 + 0, 296, BLUE)
        if 12 <= i < 28:
            pill(cv, 395, 203, "reload!", LAMB, WARN, 14, ramp(i, 12, 3))
        lt = ("요청 A를 처리 중" if i < 14 else "새 설정을 읽은 새 프로세스가 뜸" if i < 26
              else "이전은 요청 A를 마무리 · 새 것은 새 요청부터" if i < 50 else "끊긴 요청 없음")
        cv.fit(260, 366, lt, 17, 400, GOOD if i >= 50 else INK, True, "mm")
        if i >= 30:
            cv.text(155, 340, "", 12)
        # right panel
        cv.rr(510, 106, 970, 450, 16, fill=WHITE, outline=LINE, w=2)
        cv.text(740, 130, "docker restart blue", 22, INK, True, "mm", True)
        cv.text(740, 158, "컨테이너 전체를 껐다 켬", 15, MUTE, False, "mm")
        restart = 14 <= i < 28
        if restart:
            cv.rr(560, 190, 920, 340, 14, fill=LRED, outline=RED, w=4)
            cv.text(740, 214, "blue  ·  재시작!", 19, RED, True, "mm")
        else:
            cv.rr(560, 190, 920, 340, 14, fill=WHITE, outline=BLUE, w=4)
            cv.text(740, 214, "blue", 19, INK, True, "mm")
        cv.rr(580, 244, 900, 322, 8, fill=LGRAY, outline=LINE, w=1)
        cv.text(590, 254, "메모리", 12, MUTE, False, "la")
        if i < 14:
            card(cv, 740, 292, AMBER, 1.0, 130)
        elif i < 24:
            a = 1 - (i - 14) / 10
            card(cv, 740, 292, RED, a, 130)
            xmark(cv, 740, 292, 12, RED, 4)
        else:
            cv.text(740, 292, "(비어 있음)", 15, MUTE, True, "mm")
        rt = ("메모리에 약속이 들어 있음" if i < 14 else "껐다 켜는 중" if i < 28 else "메모리가 비워짐 → 약속이 사라짐")
        cv.fit(740, 366, rt, 17, 400, RED if i >= 28 else INK, True, "mm")
        if i < 14:
            caption(cv, "지금: 왼쪽 Nginx는 요청을 처리 중 · 오른쪽 blue는 메모리에 약속이 있음")
        elif i < 28:
            caption(cv, "왼쪽은 reload, 오른쪽은 docker restart를 실행합니다", WARN)
        elif i < 58:
            caption(cv, "reload는 하던 요청을 마무리 · 재시작은 메모리까지 비워짐", INK)
        else:
            caption(cv, "reload는 설정만 바꿔 끼우는 것 · 재시작은 다 껐다 켜는 것", GOOD)
        fr.append(cv.done())
    return fr

# ============================================================ fig6 파이프라인
def fig_pipeline():
    fr = []
    N = 112
    steps = [["① test", "(ci.yml)"], ["② 코드", "내려받기"], ["③ Google Cloud", "인증"],
             ["④ 커밋 번호를", "화면에 새기기"], ["⑤ Cloud Run", "배포"]]
    sx = [40 + k * 184 for k in range(5)]
    for i in range(N):
        cv = Cv()
        head(cv, "배포 파이프라인의 마지막 칸", "내 deploy.yml의 순서 — main에 push하면 위에서 아래로 자동 실행")
        for k, lines in enumerate(steps):
            on = i >= 8 + k * 11
            a = ramp(i, 8 + k * 11, 5)
            last = (k == 4)
            fill = mix(LGRAY, LAMB if last else LBLUE, a)
            outline = mix(LINE, AMBER if last else BLUE, a)
            nbox(cv, sx[k], 130, sx[k] + 172, 206, lines, fill, outline, INK, 16, 1.0, 3)
            if k > 0:
                cv.arrow(sx[k - 1] + 174, 168, sx[k] - 3, 168, MUTE, 3, 9)
        cv.text(40, 232, "CI/CD 1~2일차: 이 줄을 자동으로 돌게 만듦", 15, MUTE, False, "lm")
        pl = ramp(i, 62, 8)
        if pl > 0:
            cv.text(sx[4] + 86, 232, "오늘 노드는 ⑤ 안쪽", 15, fade(WARN, pl), True, "mm")
            cv.arrow(sx[4] + 86, 244, sx[4] + 86, 284, fade(AMBER, pl), 4, 12)
            cv.rr(40, 292, 960, 452, 14, fill=fade(WHITE, pl), outline=fade(AMBER, pl), w=3)
            if pl > 0.5:
                cv.text(60, 304, "⑤ Cloud Run 배포 안에서 일어나는 '교체'", 17, INK, True, "la")
                user(cv, 110, 376)
                cv.arrow(150, 376, 296, 376, LINE, 3)
                nbox(cv, 300, 340, 440, 412, ["서비스", "주소 하나"], LGRAY, TEAL, INK, 17, 1.0, 3)
                nbox(cv, 580, 322, 760, 372, ["이전 리비전"], WHITE, BLUE, INK, 17, 1.0, 3)
                nbox(cv, 580, 394, 760, 444, ["새 리비전"], WHITE, AMBER, INK, 17, 1.0, 3)
                flip = i >= 84
                if not flip:
                    cv.arrow(440, 372, 576, 347, BLUE, 5, 14)
                    cv.dash(440, 380, 576, 419, LINE, 2)
                else:
                    cv.dash(440, 372, 576, 347, LINE, 2)
                    cv.arrow(440, 380, 576, 419, AMBER, 5, 14)
                cv.text(780, 346, "Cloud Run이 대신 함", 15, MUTE, True, "lm")
                cv.text(780, 372, "→ 지금껏 안 보였음", 14, MUTE, False, "lm")
                cv.text(780, 420, "오늘은 내 컴퓨터에서", 14, WARN, True, "lm")
                cv.text(780, 442, "직접 손으로 해 봄", 14, WARN, True, "lm")
        if i < 62:
            caption(cv, "main에 push하면 다섯 칸이 차례로 자동 실행됩니다")
        elif i < 84:
            caption(cv, "마지막 칸 '배포' 안에서 이전 버전이 새 버전으로 교체됩니다", WARN)
        else:
            caption(cv, "이 교체가 사용자에게 안 끊기게 하는 원리가 오늘의 주제", GOOD)
        fr.append(cv.done())
    return fr

# ============================================================ fig7 SPOF
def fig_spof():
    fr = []
    NA, NB = 58, 70
    for i in range(NA + NB):
        cv = Cv()
        head(cv, "단일 장애점(SPOF): 앞문이 하나뿐이면?", "분산해 주는 Nginx도 고장 날 수 있다")
        if i < NA:
            j = i
            chip(cv, 40, 104, "A. Nginx가 한 대일 때")
            user(cv, 90, 300)
            dead = j >= 24
            cv.arrow(130, 300, 286, 300, LINE, 3)
            server_box(cv, 290, 250, 410, 355, "Nginx", "고장" if dead else "정상", TEAL, "dead" if dead else "active")
            server_box(cv, 620, 150, 840, 255, "blue", "정상", BLUE, "active")
            server_box(cv, 620, 345, 840, 450, "green", "정상", GREEN, "active")
            for nm, cy in (("blue", 202), ("green", 397)):
                if dead:
                    cv.dash(410, 302, 614, cy, LINE, 2)
                else:
                    cv.arrow(410, 302, 614, cy, BLUE if nm == "blue" else GREEN, 4, 12)
            for k in range(0, 12):
                s0 = 8 * k
                p = (j - s0) / 32
                tgt_blue = k % 2 == 0
                cy = 202 if tgt_blue else 397
                col = BLUE if tgt_blue else GREEN
                dec = s0 + 16
                if dec < 24:
                    pts = [(130, 300), (290, 300), (614, cy)]
                    if 0 <= p <= 1:
                        x, y = along(pts, [1, 1.6], p)
                        dot(cv, x, y, col)
                else:
                    if 0 <= p <= 0.6:
                        x = 130 + 150 * min(1, p / 0.5)
                        dot(cv, x, 300, RED if dead else col)
                        if x >= 270 and dead:
                            xmark(cv, 276, 300, 9, RED, 4)
            if j < 24:
                caption(cv, "앞에 서 있는 건 Nginx 한 대 — 모든 요청이 여기를 지나갑니다")
            elif j < 46:
                caption(cv, "Nginx가 멈추면 → 뒤의 서버가 멀쩡해도 요청이 못 들어갑니다", RED)
            else:
                caption(cv, "분산해 주는 장치가 새로운 단일 장애점(SPOF)이 됩니다", WARN)
        else:
            j = i - NA
            chip(cv, 40, 104, "B. Nginx를 두 대로 (액티브-스탠바이) + 가상 IP")
            user(cv, 90, 300)
            dead = j >= 22
            takeover = 36
            vip_main = j < 28
            if j < 28:
                vy = 222
            elif j < takeover:
                vy = 222 + (372 - 222) * smooth((j - 28) / (takeover - 28))
            else:
                vy = 372
            server_box(cv, 320, 168, 440, 276, "Nginx 주", "고장" if dead else "일하는 중", TEAL, "dead" if dead else "active")
            server_box(cv, 320, 318, 440, 426, "Nginx 예비", "대기" if j < takeover else "일하는 중",
                       TEAL, "dim" if j < takeover else "active")
            pill(cv, 214, vy, "가상 IP", LAMB, WARN, 15)
            hold_y = 222 if j < 32 else 372
            cv.arrow(130, 300, 190, vy, MUTE, 3, 10)
            cv.arrow(244, vy, 316, 222 if vy < 297 else 372, MUTE, 3, 10)
            server_box(cv, 650, 168, 860, 262, "blue", "정상", BLUE, "active")
            server_box(cv, 650, 340, 860, 434, "green", "정상", GREEN, "active")
            act_y = 222 if j < 22 else 372
            for nm, cy in (("blue", 215), ("green", 387)):
                if j >= takeover or j < 22:
                    ay = 222 if j < 22 else 372
                    cv.arrow(444, ay, 646, cy, BLUE if nm == "blue" else GREEN, 3, 10)
            for k in range(0, 14):
                s0 = 8 * k
                p = (j - s0) / 28
                if 22 <= s0 + 8 < takeover + 4:
                    continue
                to_blue = k % 2 == 0
                cy = 215 if to_blue else 387
                col = BLUE if to_blue else GREEN
                hy = 222 if s0 + 8 < 22 else 372
                pts = [(130, 300), (200, hy), (316, hy), (646, cy)]
                if 0 <= p <= 1:
                    x, y = along(pts, [1, 1, 2.2], p)
                    dot(cv, x, y, col)
            cv.text(40, 442, "예비는 평소 쉬는 대기라 속도를 높이진 않음 — 목적은 안 멈추는 것", 14, MUTE, False, "lm")
            if j < 22:
                caption(cv, "Nginx를 두 대로: 평소엔 주가 일하고 예비는 대기합니다")
            elif j < takeover + 4:
                caption(cv, "주가 멈추면 → 예비가 가상 IP를 넘겨받습니다", WARN)
            else:
                caption(cv, "사용자는 같은 주소로 접속하니 바뀐 줄 모릅니다", GOOD)
        fr.append(cv.done())
    return fr

# ============================================================ fig8 Cloud Run 대응
def fig_cloudrun():
    fr = []
    N = 84
    rows = [
        ("Nginx", "서비스: 안정적인 주소 하나"),
        ("blue · green 컨테이너", "리비전: 이미지 + 설정 한 벌 (만든 뒤 수정 불가)"),
        ("설정 한 줄 바꾸고 reload", "트래픽을 어느 리비전으로 보낼지 바꾸기"),
        ("이전 줄로 되돌리기 (롤백)", "이전 리비전으로 롤백"),
        ("컨테이너 메모리의 대화", "인스턴스 메모리 · 인스턴스가 0개로 줄면 사라짐"),
    ]
    for i in range(N):
        cv = Cv()
        head(cv, "Cloud Run이 대신 해 주는 것", "오늘 내 컴퓨터에서 직접 만든 것과 나란히 놓기")
        cv.text(250, 112, "내 컴퓨터 (오늘 실습)", 19, INK, True, "mm")
        cv.text(700, 112, "Cloud Run", 19, GOOD, True, "mm")
        for k, (l, r) in enumerate(rows):
            y = 134 + k * 64
            a = ramp(i, 6 + k * 11)
            nbox(cv, 40, y, 440, y + 52, [l], LGRAY, LINE, INK, 18, a, 3)
            nbox(cv, 500, y, 960, y + 52, [r], LBLUE, BLUE, INK, 17, a, 3)
            cv.arrow(446, y + 26, 494, y + 26, fade(MUTE, a), 3, 10)
        if i >= 66:
            cv.text(500, 456, "※ 문서 요약 기준 · Cloud Run 내부 규칙은 확인 못 함", 14, fade(MUTE, ramp(i, 66)), False, "lm")
        if i < 6:
            caption(cv, "오늘 직접 한 것이 Cloud Run 안에서는 무엇에 해당할까")
        elif i < 62:
            caption(cv, "내가 손으로 한 일을 Cloud Run이 서비스 안에서 대신 합니다", INK)
        else:
            caption(cv, "그래서 지금까지 배포가 '그냥 됐던' 것입니다", GOOD)
        fr.append(cv.done())
    return fr

if __name__ == "__main__":
    jobs = [("2", "fig2-헬스체크.gif", fig_health), ("3", "fig3-대기시간.gif", fig_timeout),
            ("4", "fig4-가중치.gif", fig_weight), ("5", "fig5-reload와재시작.gif", fig_reload),
            ("6", "fig6-파이프라인.gif", fig_pipeline), ("7", "fig7-SPOF.gif", fig_spof),
            ("8", "fig8-CloudRun대응.gif", fig_cloudrun)]
    for k, nm, fn in jobs:
        if ONLY in ("all", k):
            save(nm, fn())
