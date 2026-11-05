"""노션 보고서(크레딧·결제·방어)용 움직이는 그림 7장 + 요약 영상. make_gifs.py 의 팔레트·그리기 함수를 그대로 쓴다.
사용: python make_figs_pay.py <출력 폴더> [1~7|video|all]
  1~7 : 해당 그림 GIF 만 / video : mp4 만 / all : GIF 7장 + mp4
숫자는 모두 작업 명세(이미 검증된 값)에서 그대로 옮겼다.
"""
import sys
import os
import subprocess

OUT_DIR = sys.argv[1]
ONLY = sys.argv[2] if len(sys.argv) > 2 else "all"
sys.argv = [sys.argv[0], OUT_DIR]
from make_gifs import *  # noqa: F401,F403  W, H, Cv, 색, header, caption, chip, save …
from PIL import Image


def prog(i, a, d):
    return smooth((i - a) / d)


def box(cv, x0, y0, x1, y1, title, sub="", state="idle", tsize=20):
    fill, edge, tc = WHITE, LINE, INK
    if state == "on":
        fill, edge = LBLUE, BLUE
    elif state == "bad":
        fill, edge, tc = LRED, RED, (150, 40, 36)
    elif state == "dim":
        fill, edge, tc = LGRAY, LINE, MUTE
    elif state == "good":
        fill, edge = LBLUE, GOOD
    elif state == "amber":
        fill, edge = LAMB, AMBER
    cv.rr(x0, y0, x1, y1, 14, fill=fill, outline=edge, w=3 if state in ("on", "bad", "good", "amber") else 2)
    cy = (y0 + y1) / 2 - (10 if sub else 0)
    cv.fit((x0 + x1) / 2, cy, title, tsize, (x1 - x0) - 16, tc, True, "mm")
    if sub:
        cv.fit((x0 + x1) / 2, cy + 26, sub, 15, (x1 - x0) - 14, MUTE if state != "bad" else (150, 40, 36), False, "mm")


def check(cv, x, y, r=12, color=GOOD):
    cv.circ(x, y, r + 4, fill=WHITE, outline=color, w=3)
    cv.line(x - r * 0.5, y, x - r * 0.1, y + r * 0.45, color, 4)
    cv.line(x - r * 0.1, y + r * 0.45, x + r * 0.6, y - r * 0.4, color, 4)


def tw(i, kf):
    """키프레임 [(프레임, 값)…] 사이를 부드럽게 보간"""
    if i <= kf[0][0]:
        return kf[0][1]
    for a, b in zip(kf, kf[1:]):
        if i <= b[0]:
            return a[1] + (b[1] - a[1]) * smooth((i - a[0]) / (b[0] - a[0]))
    return kf[-1][1]


def last_state(i, tl):
    s = None
    for f, st in tl:
        if i >= f:
            s = st
    return s


# ---- 그림 1. 메시지 한 건의 원가 ----
def scene1():
    frames = []
    # (제목, 둘째 줄, 셋째 줄, 종류)  종류: code = 서버 코드만 / llm = 모델 호출
    steps = [("① check-safety", "서버 코드가 낱말만 훑어봄 · 0원", "모델 호출 아님 (0번)", "code"),
             ("② choose-mode", "입력 987 · 출력 15 토큰", "모델 호출 1번: gpt-4o-mini에게 묻는다", "llm"),
             ("③ generate-reply", "입력 2,216 · 출력 74 토큰", "모델 호출 2번: gpt-4o-mini에게 묻는다", "llm")]
    starts = [16, 42, 68]
    N = 140
    BX0, BX1 = 330, 650
    BUS = 304
    for i in range(N):
        cv = Cv()
        header(cv, 1, "메시지 한 건의 원가", "도장 도우미에 한 줄을 보내면 모델이 몇 번, 얼마나 불리나")
        cv.rr(40, 163, 250, 275, 18, fill=LBLUE, outline=BLUE, w=3)
        cv.text(54, 177, "사용자", 15, MUTE, True, "la")
        cv.fit(145, 214, "물 마시기 칸을 만들었는데", 16, 190, INK, True, "mm")
        cv.fit(145, 244, "자꾸 까먹어요.", 16, 190, INK, True, "mm")
        ycs = [108 + k * 84 + 35 for k in range(3)]
        col = BLUE if i >= 10 else LINE
        cv.line(252, 223, BUS, 223, col, 3)
        cv.line(BUS, ycs[0], BUS, ycs[2], col, 3)
        for k, (t, sub, chip, kind) in enumerate(steps):
            y0 = 108 + k * 84
            on = i >= starts[k]
            cv.arrow(BUS, ycs[k], BX0 - 2, ycs[k], BLUE if on else LINE, 3, 9)
            if not on:
                fill, edge, tc = WHITE, LINE, MUTE
            elif kind == "code":
                fill, edge, tc = LGRAY, MUTE, INK
            else:
                fill, edge, tc = LBLUE, GOOD, INK
            cv.rr(BX0, y0, BX1, y0 + 70, 14, fill=fill, outline=edge, w=3 if on else 2)
            cv.fit((BX0 + BX1) / 2, y0 + 16, t, 19, 300, tc, True, "mm")
            cv.fit((BX0 + BX1) / 2, y0 + 38, sub, 14, 300, MUTE, False, "mm")
            cv.fit((BX0 + BX1) / 2, y0 + 56, chip, 14, 304, (GOOD if kind == "llm" else MUTE) if on else MUTE, True, "mm")
            if k < 2:
                cv.arrow(490, y0 + 71, 490, y0 + 83, MUTE, 3, 8)
        cv.text(145, 296, "사용자의 말은", 14, MUTE, False, "mm")
        cv.text(145, 314, "세 단계 모두에 들어간다", 14, MUTE, False, "mm")
        p = prog(i, 88, 10)
        if p > 0.05:
            for k in (1, 2):
                cv.arrow(652, ycs[k], 678, 232, MUTE, 2, 8)
            cv.rr(682, 108, 960, 346, 16, fill=WHITE, outline=BLUE, w=3)
            cv.text(821, 134, "합계 (모델 호출 2번)", 16, MUTE, True, "mm")
            cv.fit(821, 202, "입력 3,203", 30, 250, INK, True, "mm")
            cv.fit(821, 252, "+ 출력 89 토큰", 26, 250, INK, True, "mm")
            cv.fit(821, 306, "② + ③ 의 합", 15, 250, MUTE, False, "mm")
        if i >= 104:
            cv.rr(40, 366, 500, 450, 14, fill=WHITE, outline=LINE, w=2)
            cv.text(56, 382, "단가", 14, MUTE, True, "lm")
            cv.fit(270, 410, "gpt-4o-mini: 입력 $0.15 / 출력 $0.60", 19, 430, INK, True, "mm")
            cv.fit(270, 435, "(백만 토큰당)", 15, 430, MUTE, False, "mm")
        if i >= 118:
            cv.rr(520, 366, 960, 450, 14, fill=LAMB, outline=AMBER, w=3)
            cv.fit(740, 402, "한 건 약 $0.000534 (약 0.75원)", 26, 410, INK, True, "mm")
            cv.fit(740, 432, "(1달러=1,400원으로 가정)", 15, 410, MUTE, False, "mm")
        caption(cv, "«모델 호출»(서버가 gpt-4o-mini에게 묻는 일)은 ②③ 두 번이고, 요금도 이 두 번에만 붙는다")
        frames.append(cv.done())
    return frames


# ---- 그림 2. 사용자 유형별 한 달 원가 ----
def scene2():
    frames = []
    rows = [("보통 사용자", 1, "하루 20개 → $0.32 (약 450원)", BLUE),
            ("많이 쓰는 사용자", 15, "하루 300개 → $4.80 (약 6,700원)", AMBER),
            ("자동화 악용 계정", 150, "하루 3,000개 → $48.05 (약 67,000원)", RED)]
    X0, MAXW = 310, 480
    N = 120
    for i in range(N):
        cv = Cv()
        header(cv, 2, "사용자 유형별 한 달 원가", "한 건 원가 × 하루 메시지 × 30일")
        for j, (name, v, label, col) in enumerate(rows):
            y = 160 + j * 100
            cv.text(40, y + 28, name, 21, INK, True, "lm")
            cv.line(X0, y - 6, X0, y + 66, LINE, 2)
            p = prog(i, 8 + j * 26, 30)
            w = max(12, MAXW * v / 150) * p
            if p > 0.01:
                cv.rr(X0, y, X0 + max(w, 6), y + 56, 8, fill=col)
            if p > 0.97:
                if j < 2:
                    cv.fit(X0 + w + 14, y + 28, label, 20, 470, INK, True, "lm")
                else:
                    cv.fit(X0 + 14, y + 28, label, 20, w - 24, WHITE, True, "lm")
        if i >= 90:
            cv.rr(760, 102, 960, 140, 19, fill=LAMB, outline=AMBER, w=3)
            cv.text(860, 121, "1 : 15 : 150", 24, (150, 90, 0), True, "mm")
        caption(cv, "원가는 사용자 수가 아니라 사용량에 비례한다")
        frames.append(cv.done())
    return frames


# ---- 그림 3. 잔액 칸 하나 vs 원장 ----
def scene3():
    frames = []
    N = 170
    RED_T = (150, 40, 36)
    for i in range(N):
        cv = Cv()
        header(cv, 3, "크레딧이 1개 남았는데 메시지 2개가 동시에 오면?", "같은 상황을 두 방법으로 처리한다: 왼쪽은 확인과 저장을 따로, 오른쪽은 한 동작으로")
        # ---------- 왼쪽: 문제 ----------
        cv.rr(40, 104, 490, 432, 16, fill=WHITE, outline=LINE, w=2)
        cv.text(265, 126, "방법 1 (문제): 읽고 → 계산하고 → 저장, 따로", 18, INK, True, "mm")
        for nm, cx, st in (("메시지 A", 150, 10), ("메시지 B", 380, 14)):
            if prog(i, st, 10) > 0.05:
                cv.rr(cx - 80, 146, cx + 80, 184, 12, fill=WHITE, outline=AMBER, w=3)
                cv.text(cx, 165, nm, 18, INK, True, "mm")
        if i >= 26:
            cv.fit(150, 202, "«1개 남았네, 쓰자»", 15, 160, WARN, True, "mm")
            cv.fit(380, 202, "«1개 남았네, 쓰자»", 15, 160, WARN, True, "mm")
        if i >= 34:
            cv.arrow(150, 214, 215, 258, BLUE, 3, 9)
            cv.arrow(380, 214, 315, 258, BLUE, 3, 9)
        done = i >= 62
        cv.rr(180, 262, 350, 316, 12, fill=LRED if done else LBLUE, outline=RED if done else BLUE, w=3)
        cv.fit(265, 278, "남은 크레딧", 14, 150, MUTE, True, "mm")
        cv.fit(265, 300, "0개" if done else "1개", 24, 150, INK, True, "mm")
        if i >= 50:
            cv.fit(265, 336, "둘 다 «1 - 1 = 0»을 저장했다", 17, 410, RED_T, True, "mm")
        if i >= 78:
            cv.rr(70, 354, 460, 420, 12, fill=LRED, outline=RED, w=3)
            cv.fit(265, 372, "답은 2개 나갔는데 크레딧은 1개만 줄었다", 17, 360, RED_T, True, "mm")
            cv.fit(265, 396, "1개는 공짜가 되고, 왜 0인지 기록도 없다", 16, 360, RED_T, False, "mm")
        # ---------- 오른쪽: 해결 ----------
        cv.rr(510, 104, 960, 432, 16, fill=WHITE, outline=LINE, w=2)
        cv.text(735, 126, "방법 2 (해결): 확인과 -1 줄 쓰기를 한 동작으로", 18, INK, True, "mm")
        if i >= 20:
            cv.rr(530, 146, 940, 192, 10, fill=LBLUE, outline=GOOD, w=2)
            cv.text(548, 169, "+1", 24, GOOD, True, "lm")
            cv.fit(600, 169, "원장에 +1 줄이 있다 → 합계 1개", 17, 320, INK, True, "lm")
        if i >= 56:
            cv.rr(530, 200, 940, 262, 10, fill=LBLUE, outline=GOOD, w=3)
            cv.text(548, 221, "A", 22, GOOD, True, "lm")
            cv.fit(580, 218, "합계 1개 확인 → -1 줄 쓰기 (한 동작)", 16, 350, INK, True, "lm")
            cv.fit(580, 244, "통과: 이제 합계가 0개가 된다", 15, 350, GOOD, True, "lm")
        if i >= 82:
            cv.rr(530, 270, 940, 332, 10, fill=LRED, outline=RED, w=3)
            cv.text(548, 291, "B", 22, RED_T, True, "lm")
            cv.fit(580, 288, "A가 끝난 뒤에 확인 → 합계 0개, 크레딧 부족", 16, 350, INK, True, "lm")
            cv.fit(580, 314, "거절한다 (402), 줄을 쌓지 않는다", 15, 350, RED_T, True, "lm")
        if i >= 108:
            cv.rr(530, 346, 940, 392, 12, fill=LBLUE, outline=GOOD, w=3)
            cv.fit(735, 369, "답 1개 · 크레딧 1개 사용 · -1 줄이 남는다", 17, 380, GOOD, True, "mm")
        if i >= 124:
            cv.fit(735, 412, "원장을 쓰더라도 확인과 줄 쓰기를 따로 하면 왼쪽과 같은 문제가 생긴다", 14, 410, MUTE, True, "mm")
        caption(cv, "초과 사용은 «합계 확인과 -1 줄 쓰기를 한 동작으로» 묶어야 막힌다. 원장은 그 줄을 남긴다")
        frames.append(cv.done())
    return frames


# ---- 그림 4. 결제 한 번의 여정 ----
def _state_chip(cv, x, y, label, val, fill, color):
    t = f"{label} {val}"
    w = cv.d.textlength(t, font=font(18, True)) / S + 30
    cv.rr(x, y, x + w, y + 34, 17, fill=fill, outline=color, w=2)
    cv.text(x + 15, y + 17, t, 18, color, True, "lm")


def scene4():
    frames = []
    lanes = [("사용자 화면", 150), ("도장 서버", 370), ("토스페이먼츠", 600), ("데이터베이스", 830)]
    steps = [(0, 1, "① 상품 고름 credits_100"),
             (1, 3, "② 서버가 주문 저장 (주문번호 A1 · 1,000원 · 대기)"),
             (0, 2, "③ 결제창에서 카드 인증"),
             (0, 1, "④ successUrl로 이동 (paymentKey, orderId, amount=1000)"),
             None,
             (1, 2, "⑥ 시크릿 키로 승인 요청"),
             (2, 1, "⑦ 승인 성공"),
             (1, 3, "⑧ 주문 완료 + 원장 +100(order:A1)")]
    a = [8 + 16 * k for k in range(8)]
    N = 165
    for i in range(N):
        cv = Cv()
        header(cv, 4, "결제 한 번의 여정", "사용자가 크레딧 100개(1,000원)를 사는 한 번의 흐름")
        # 상태 칩
        o_done = i >= a[7] + 12
        c_done = i >= a[7] + 12
        if i < a[1] + 10:
            _state_chip(cv, 40, 102, "주문 상태:", "(없음)", LGRAY, MUTE)
        elif not o_done:
            _state_chip(cv, 40, 102, "주문 상태:", "대기", LAMB, WARN)
        else:
            _state_chip(cv, 40, 102, "주문 상태:", "대기 → 완료", LBLUE, GOOD)
        if not c_done:
            _state_chip(cv, 330, 102, "크레딧 잔액:", "0", LAMB, WARN)
        else:
            _state_chip(cv, 330, 102, "크레딧 잔액:", "0 → 100", LBLUE, GOOD)
        for nm, x in lanes:
            cv.rr(x - 80, 144, x + 80, 176, 10, fill=LTEAL, outline=TEAL, w=2)
            cv.fit(x, 160, nm, 18, 150, INK, True, "mm")
            cv.dash(x, 180, x, 454, LINE, 2)
        # 승인 전/후 경계
        if i >= a[3] + 10:
            cv.dash(40, 322, 960, 322, AMBER, 2)
            cv.rr(560, 302, 958, 320, 6, fill=BG)
            cv.text(956, 311, "↑ ⑤번 전까지 크레딧은 그대로 0", 15, WARN, True, "rm")
        for k, st in enumerate(steps):
            y = 204 + 34 * k
            if st is None:
                p = prog(i, a[k], 8)
                if p > 0.05:
                    cv.rr(235, y - 14, 505, y + 14, 10, fill=LAMB, outline=AMBER, w=3)
                    cv.fit(370, y, "⑤ 서버가 저장한 금액·상태와 비교", 15, 258, INK, True, "mm")
                continue
            f, t, label = st
            x0, x1 = lanes[f][1], lanes[t][1]
            p = prog(i, a[k], 10)
            if p < 0.03:
                continue
            col = GOOD if k >= 6 else BLUE
            cv.arrow(x0, y + 6, x0 + (x1 - x0) * p, y + 6, col, 3, 10)
            if p > 0.3:
                lx = (x0 + x1) / 2
                wl = cv.d.textlength(label, font=font(15, True)) / S
                wl = min(wl, 440)
                cv.rr(lx - wl / 2 - 4, y - 21, lx + wl / 2 + 4, y - 1, 5, fill=BG)
                cv.fit(lx, y - 11, label, 15, 440, INK, True, "mm")
        caption(cv, "크레딧은 승인이 성공한 뒤에만 들어간다")
        frames.append(cv.done())
    return frames


# ---- 그림 5. 주소의 금액을 고치면? ----
def scene5():
    frames = []
    N = 135
    f = font(24, False, True)
    prefix = "…?orderId=A1&amount="
    for i in range(N):
        cv = Cv()
        header(cv, 5, "주소의 금액을 고치면?", "브라우저 주소창의 amount는 사용자가 바꿀 수 있다")
        cv.rr(40, 108, 960, 164, 14, fill=WHITE, outline=BLUE if i < 24 else AMBER, w=3)
        cv.text(58, 136, "주소창", 15, MUTE, True, "lm")
        ux = 150
        cv.text(ux, 136, prefix, 24, INK, False, "lm", True)
        vx = ux + cv.d.textlength(prefix, font=f) / S
        if i < 14:
            val, vcol, hl = "1000", INK, False
        elif i < 22:
            val, vcol, hl = "1000", INK, True
        elif i < 26:
            val, vcol, hl = "100", INK, True
        else:
            val, vcol, hl = "100", (150, 40, 36), False
        vw = cv.d.textlength(val, font=f) / S
        if hl:
            cv.rr(vx - 4, 118, vx + vw + 4, 154, 6, fill=LAMB)
        cv.text(vx, 136, val, 24, vcol, True, "lm", True)
        if 14 <= i < 34:
            cv.text(vx + vw + 10, 136, "← 사용자가 고침" if i >= 22 else "← 이 값을 지움", 16, WARN, True, "lm")
        if i >= 34:
            cv.arrow(300, 168, 300, 196, MUTE, 3, 9)
        if i >= 40:
            left_state = "bad" if i >= 64 else "idle"
            box(cv, 40, 200, 300, 282, "주소로 받은 금액", "amount = 100", left_state, 20)
            box(cv, 380, 200, 690, 282, "저장해 둔 주문", "1,000원 / 대기", "bad" if i >= 64 else "idle", 20)
        if i >= 64:
            cv.text(340, 232, "≠", 40, RED, True, "mm")
            cv.text(340, 262, "불일치", 15, RED, True, "mm")
        if i >= 76:
            cv.rr(40, 308, 690, 442, 16, fill=LRED, outline=RED, w=3)
            items = ["승인 API를 부르지 않음", "주문은 대기 그대로", "원장 변화 없음"]
            for k, t in enumerate(items):
                if i >= 78 + k * 10:
                    xmark(cv, 74, 342 + k * 40, 9, RED, 4)
                    cv.fit(100, 342 + k * 40, t, 22, 560, (150, 40, 36), True, "lm")
        if i >= 100:
            cv.rr(720, 200, 960, 442, 16, fill=LAMB, outline=AMBER, w=3)
            cv.text(840, 226, "함께 기억할 것", 15, WARN, True, "mm")
            cv.fit(840, 290, "시크릿 키는", 22, 220, INK, True, "mm")
            cv.fit(840, 322, "서버에만", 22, 220, INK, True, "mm")
            cv.fit(840, 366, "(화면·저장소에", 16, 220, MUTE, False, "mm")
            cv.fit(840, 390, "두지 않음)", 16, 220, MUTE, False, "mm")
        caption(cv, "서버는 받은 금액을 믿지 않고 저장해 둔 금액과 비교한다")
        frames.append(cv.done())
    return frames


# ---- 그림 6. 같은 승인 요청이 두 번 오면? ----
def scene6():
    frames = []
    cols = [("① 주문 상태 확인", 245), ("② 원장 참조 유일", 485), ("③ Idempotency-Key", 725)]
    CW = 230
    rows = [
        ("새로고침으로|같은 요청이 또 옴",
         [("막는다", "이미 완료면 승인을 안 부름", "key"), ("①이 꺼지면 막는다", "두 번째 +100 거절", "back"), ("①이 꺼지면 받쳐 줌", "토스가 첫 응답을 돌려줌", "back")]),
        ("응답이 끊겨|서버가 다시 보냄",
         [("관여 안 함", "주문이 아직 «대기»", "none"), ("관여 안 함", "원장이 아직 비어 있음", "none"), ("막는다", "첫 승인 응답을 돌려줘 끝냄", "key")]),
        ("두 요청이|동시에 도착",
         [("못 막는다", "둘 다 «대기»를 읽음", "miss"), ("막는다", "두 번째 +100 거절", "key"), ("관여 안 함", "토스는 둘 다 성공 응답", "none")]),
    ]
    starts = [14, 54, 94]
    N = 170
    for i in range(N):
        cv = Cv()
        header(cv, 6, "세 장치는 서로 다른 상황을 막는다", "같은 승인 요청이 두 번 올 때, 상황마다 결정적인 장치가 다르다")
        for c, (nm, x0) in enumerate(cols):
            cv.rr(x0, 102, x0 + CW, 134, 10, fill=LGRAY, outline=LINE, w=2)
            cv.fit(x0 + CW / 2, 118, nm, 17, CW - 14, INK, True, "mm")
        for r, (lab, cells) in enumerate(rows):
            y0 = 142 + r * 90
            p = prog(i, starts[r], 10)
            if p < 0.05:
                continue
            ox = (1 - p) * 40
            cv.rr(40, y0, 232, y0 + 82, 12, fill=WHITE, outline=LINE, w=2)
            l1, l2 = lab.split("|")
            cv.fit(136, y0 + 28, l1, 16, 172, INK, True, "mm")
            cv.fit(136, y0 + 54, l2, 16, 172, INK, True, "mm")
            for c, (t1, t2, kind) in enumerate(cells):
                x0 = cols[c][1] + ox
                fill, edge, tc = {"key": (LBLUE, GOOD, GOOD), "back": (LAMB, AMBER, WARN),
                                  "none": (LGRAY, LINE, MUTE), "miss": (LRED, RED, (150, 40, 36))}[kind]
                cv.rr(x0, y0, x0 + CW, y0 + 82, 12, fill=fill, outline=edge, w=3 if kind in ("key", "miss") else 2)
                cv.fit(x0 + CW / 2, y0 + 28, t1, 19, CW - 16, tc, True, "mm")
                cv.fit(x0 + CW / 2, y0 + 56, t2, 14, CW - 16, MUTE if kind == "none" else INK, False, "mm")
        if i >= 124:
            cv.rr(40, 414, 960, 460, 12, fill=WHITE, outline=RED, w=2)
            cv.fit(500, 428, "②를 끄면: 동시 도착에서 크레딧 200개(중복 지급) · ③을 끄면: 끊김에서 돈만 빠지고 크레딧 0", 15, 900, (150, 40, 36), True, "mm")
            cv.fit(500, 448, "①을 끄면: 새로고침은 ②③이 이어서 막는다", 15, 900, GOOD, True, "mm")
        caption(cv, "한 장치가 모든 상황을 막지 않는다 — 상황마다 막는 장치가 다르다")
        frames.append(cv.done())
    return frames


# ---- 그림 7. 도장 서버 공격 시험 결과 ----
def scene7():
    frames = []
    rows = [("A  같은 주소에서 동시 10건 (대화)", 10, 0, ""),
            ("B  같은 주소에서 동시 30건 (대화)", 20, 10, "주소당 한도 20에서 멈춤"),
            ("C  주소 표시(X-Forwarded-For)를 요청마다 바꿔 130건 (대화)", 120, 10,
             "주소당 한도는 피했지만|전체 한도 120에서 멈춤"),
            ("D  같은 주소에서 10건 (도장 그림)", 5, 5, ""),
            ("E  주소 표시를 바꿔 50건 (도장 그림)", 30, 20, "전체 한도 30에서 멈춤")]
    X0, SC = 40, 4.0
    N = 130
    for i in range(N):
        cv = Cv()
        header(cv, 7, "도장 서버 공격 시험 결과", "내 컴퓨터에서 연 서버(가짜 LLM)에만 시험, 요청 수 vs 통과·막힘")
        cv.rr(700, 104, 718, 122, 4, fill=BLUE)
        cv.text(724, 113, "통과", 15, INK, True, "lm")
        cv.rr(790, 104, 808, 122, 4, fill=RED)
        cv.text(814, 113, "막힘", 15, INK, True, "lm")
        for j, (lab, ok, bad, note) in enumerate(rows):
            y = 132 + j * 62
            cv.fit(X0, y + 10, lab, 17, 560, INK, True, "lm")
            p = prog(i, 6 + j * 20, 20)
            tot = ok + bad
            w = tot * SC * p
            wo = min(w, ok * SC)
            if p > 0.02:
                cv.rr(X0, y + 26, X0 + max(wo, 4), y + 52, 5, fill=BLUE)
                if w > ok * SC:
                    cv.rr(X0 + ok * SC, y + 26, X0 + w, y + 52, 5, fill=RED)
            if p > 0.97:
                cv.fit(X0 + tot * SC + 12, y + 39, f"통과 {ok} · 막힘 {bad}", 17, 190, INK, True, "lm")
                if note:
                    ls = note.split("|")
                    for q, t in enumerate(ls):
                        yy = y + 39 + (q - (len(ls) - 1) / 2) * 22
                        cv.fit(742, yy, t, 15, 218, WARN, True, "lm")
        caption(cv, "주소당 한도는 주소 표시를 바꾸면 피해 간다 — 마지막 방어선은 전체 한도")
        frames.append(cv.done())
    return frames


# ---- 그림 8. 무료 한도가 손익을 바꾼다 ----
def scene8():
    frames = []
    zones = [("하루 무료 메시지", "10개", 213006, 44393, "-168,613원", RED, LRED, (150, 40, 36)),
             ("하루 무료 메시지", "3개", 63902, 44393, "-19,509원", AMBER, LAMB, WARN),
             ("하루 무료 메시지", "1개", 21301, 44393, "+23,092원", GOOD, LBLUE, GOOD)]
    X0, MAXW = 215, 380
    N = 135
    for i in range(N):
        cv = Cv()
        header(cv, 8, "무료 한도가 손익을 가장 크게 바꾼다",
               "사용자 1,000명 · 5%만 결제 · 한 건 0.75원 가정(내가 세운 단순 모델)")
        cv.rr(40, 104, 58, 122, 4, fill=RED)
        cv.fit(66, 113, "무료 사용자 950명 한 달 원가", 15, 300, INK, True, "lm")
        cv.rr(400, 104, 418, 122, 4, fill=BLUE)
        cv.fit(426, 113, "유료 50명 수입 - 수수료 - 그들의 원가", 15, 530, INK, True, "lm")
        for j, (l1, l2, red, teal, res, rc, rf, rt) in enumerate(zones):
            t0 = 6 + j * 34
            p = prog(i, t0, 26)
            if p < 0.02:
                continue
            y0 = 130 + j * 92
            cv.rr(40, y0, 960, y0 + 84, 14, fill=WHITE, outline=LINE, w=2)
            cv.fit(56, y0 + 28, l1, 18, 150, INK, True, "lm")
            cv.fit(56, y0 + 56, l2, 26, 150, rc if rc != AMBER else WARN, True, "lm")
            cv.line(X0, y0 + 10, X0, y0 + 74, LINE, 2)
            wr = max(6, MAXW * red / 213006) * p
            wt = max(6, MAXW * teal / 213006) * p
            cv.rr(X0, y0 + 12, X0 + wr, y0 + 38, 6, fill=RED)
            cv.rr(X0, y0 + 46, X0 + wt, y0 + 72, 6, fill=BLUE)
            if p > 0.97:
                cv.fit(X0 + wr + 10, y0 + 25, f"{red:,}원", 19, 740 - (X0 + wr + 10), INK, True, "lm")
                cv.fit(X0 + wt + 10, y0 + 59, f"{teal:,}원", 19, 740 - (X0 + wt + 10), INK, True, "lm")
            if i >= t0 + 26:
                cv.rr(752, y0 + 10, 948, y0 + 74, 14, fill=rf, outline=rc, w=3)
                cv.fit(850, y0 + 26, "한 달 손익", 15, 180, MUTE, True, "mm")
                cv.fit(850, y0 + 54, res, 30, 180, rt, True, "mm")
        if i >= 110:
            cv.fit(500, 424, "유료 50명은 1,000원(100크레딧)을 한 번 사서 다 씀 · 수수료 3.74%", 15, 920, MUTE, True, "mm")
            cv.fit(500, 446, "무료 사용자는 한도를 매일 다 씀(최악) · 고정비 제외", 15, 920, MUTE, True, "mm")
        caption(cv, "한도를 줄일수록 흑자 쪽으로 간다 — 단, 한도를 줄이면 전환율이 내려갈 수 있다(재 봐야 안다)")
        frames.append(cv.done())
    return frames


def scene0():
    frames = []
    items = [("① 원가", "메시지 한 건은 얼마인가"), ("② 가격·무료 한도", "얼마를 받고 얼마까지 공짜로 줄까"),
             ("③ 크레딧 원장", "남은 크레딧을 서버가 기록으로 관리"), ("④ 결제 승인", "서버가 확인한 뒤에만 크레딧 지급"),
             ("⑤ 중복·위조 방어", "같은 요청이 두 번 와도 한 번만 반영"), ("⑥ 테스트로 남기기", "방어가 계속 지켜지는지 자동으로 확인")]
    starts = [10, 28, 46, 64, 82, 100]
    N = 140
    for i in range(N):
        cv = Cv()
        header(cv, 0, "오늘의 흐름", "크레딧과 결제를 붙이는 여섯 단계")
        for k, (t, sub) in enumerate(items):
            col, row = k % 3, k // 3
            x0 = 40 + col * 310
            y0 = 130 + row * 150
            if i < starts[k]:
                continue
            p = prog(i, starts[k], 10)
            st = "amber" if k >= 2 else "on"
            box(cv, x0, y0 + (1 - p) * 20, x0 + 290, y0 + 120 + (1 - p) * 20, t, sub, st, 21)
            if col < 2 and k + 1 < len(items) and i >= starts[k + 1] - 2:
                cv.arrow(x0 + 292, y0 + 60, x0 + 308, y0 + 60, MUTE, 3, 8)
        if i >= 100:
            cv.text(500, 436, "①②는 «숫자를 정하는 단계», ③~⑥은 «서버가 안전하게 구현하는 단계»", 17, MUTE, True, "mm")
        caption(cv, "앞 단계에서 정한 값(원가·가격·한도)이 뒤 단계의 설계 재료가 된다")
        frames.append(cv.done())
    return frames


def scene9():
    frames = []
    N = 150
    L, M, R = (40, 330), (350, 650), (670, 960)
    yy = [128, 198, 268, 338]
    left = [("POST /api/chat", "메시지를 받는다", "on"), ("속도 한도 (limited)", "지금도 있다", "on"),
            ("크레딧 확인·차감", "새로 만들 곳 · 서버에서만", "amber"), ("도우미가 답을 만든다", "① 검사 → ② 모드 고르기 → ③ 답 쓰기", "on")]
    right = [("GET /api/products", "상품 목록(금액·크레딧)", "amber"), ("POST /api/orders", "주문을 «대기»로 저장", "amber"),
             ("결제위젯 (토스페이먼츠)", "사용자가 카드 인증", "dim"), ("POST /api/payments/confirm", "금액 확인 → 승인 → 크레딧 지급", "amber")]
    for i in range(N):
        cv = Cv()
        header(cv, 9, "도장에 붙일 자리", "지금 있는 길(초록)에 크레딧 확인을 끼우고, 결제 길(노랑)을 새로 만든다")
        cv.text(L[0], 112, "메시지 보내기", 17, INK, True, "lm")
        cv.text(R[0], 112, "크레딧 사기", 17, INK, True, "lm")
        cv.text(M[0] + 150, 112, "새로 만들 표", 17, INK, True, "mm")
        for k, (t, sub, st) in enumerate(left):
            if prog(i, 8 + k * 9, 8) > 0.05:
                box(cv, L[0], yy[k], L[1], yy[k] + 56, t, sub, st, 17)
                if k < 3:
                    cv.arrow((L[0] + L[1]) / 2, yy[k] + 57, (L[0] + L[1]) / 2, yy[k] + 69, MUTE, 3, 8)
        for k, (t, sub, st) in enumerate(right):
            if prog(i, 52 + k * 9, 8) > 0.05:
                box(cv, R[0], yy[k], R[1], yy[k] + 56, t, sub, st, 17)
                if k < 3:
                    cv.arrow((R[0] + R[1]) / 2, yy[k] + 57, (R[0] + R[1]) / 2, yy[k] + 69, MUTE, 3, 8)
        if i >= 96:
            box(cv, M[0] + 40, 190, M[1] - 40, 240, "주문 orders", "주문번호 · 금액 · 상태", "amber", 17)
            box(cv, M[0] + 40, 300, M[1] - 40, 350, "원장 credit_ledger", "크레딧이 늘고 준 줄", "amber", 17)
        if i >= 108:
            cv.arrow(R[0] - 2, 226, M[1] - 38, 215, MUTE, 3, 9)
            cv.arrow(L[1] + 2, 296, M[0] + 42, 322, MUTE, 3, 9)
            cv.fit((L[1] + M[0] + 40) / 2 + 10, 352, "-1 줄 쌓기", 14, 110, GOOD, True, "mm")
        if i >= 120:
            cv.arrow(R[0] - 2, 366, M[1] - 38, 338, MUTE, 3, 9)
            cv.fit((R[0] + M[1]) / 2 - 8, 392, "+크레딧 줄 쌓기", 14, 130, GOOD, True, "mm")
        if i >= 20:
            cv.rr(40, 424, 260, 452, 8, fill=LBLUE, outline=GOOD, w=2)
            cv.text(150, 438, "초록: 지금 있는 것", 14, INK, True, "mm")
            cv.rr(274, 424, 494, 452, 8, fill=LAMB, outline=AMBER, w=2)
            cv.text(384, 438, "노랑: 새로 만들 것", 14, INK, True, "mm")
            cv.rr(508, 424, 728, 452, 8, fill=LGRAY, outline=LINE, w=2)
            cv.text(618, 438, "회색: 토스페이먼츠", 14, INK, True, "mm")
        caption(cv, "크레딧은 두 군데에서 바뀐다: 메시지를 보낼 때 줄고, 결제가 승인되면 는다")
        frames.append(cv.done())
    return frames


JOBS = {"0": ("pay0-flow.gif", scene0), "1": ("pay1-cost.gif", scene1), "2": ("pay2-users.gif", scene2),
        "3": ("pay3-ledger.gif", scene3), "4": ("pay4-flow.gif", scene4), "5": ("pay5-tamper.gif", scene5),
        "6": ("pay6-idem.gif", scene6), "7": ("pay7-attack.gif", scene7), "8": ("pay8-profit.gif", scene8),
        "9": ("pay9-map.gif", scene9)}


class VideoWriter:
    """장면 프레임을 한 장씩 ffmpeg 에 흘려 넣는다(메모리 절약). 장면 사이는 5프레임 크로스페이드."""

    def __init__(self, path):
        self.n = 0
        self.prev_last = None
        self.p = subprocess.Popen(
            ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
             "-r", "10", "-i", "-", "-c:v", "libx264", "-crf", "29", "-preset", "medium",
             "-pix_fmt", "yuv420p", "-movflags", "+faststart", path], stdin=subprocess.PIPE)

    def put(self, im, times=1):
        b = im.convert("RGB").tobytes()
        for _ in range(times):
            self.p.stdin.write(b)
            self.n += 1

    def title_card(self):
        cv = Cv()
        cv.rr(0, 0, W, H, 0, fill=DARK)
        cv.fit(500, 240, "크레딧과 결제 — 도장 도우미에 붙이면", 44, 880, WHITE, True, "mm")
        cv.fit(500, 310, "원가 → 원장 → 결제 → 방어 → 도장에 붙이기, %d장면" % len(JOBS), 24, 880, AMBER, True, "mm")
        self.put(cv.done(), 30)
        self.prev_last = None
        self._title = True

    def scene(self, frames):
        first = frames[0]
        if self.prev_last is not None or getattr(self, "_title", False):
            base = self.prev_last if self.prev_last is not None else Image.new("RGB", (W, H), DARK)
            for k in range(1, 6):
                self.put(Image.blend(base.convert("RGB"), first.convert("RGB"), k / 6))
        for f in frames[:-1]:
            self.put(f)
        self.put(frames[-1], 20)
        self.prev_last = frames[-1]

    def close(self):
        self.p.stdin.close()
        self.p.wait()


want_gif = ONLY != "video"
want_video = ONLY in ("video", "all")
if want_video:
    vw = VideoWriter(os.path.join(OUT_DIR, "pay-video.mp4"))
    vw.title_card()
for k, (nm, fn) in JOBS.items():
    if ONLY in ("all", "video", k):
        fr = fn()
        if want_gif:
            save(nm, fr)
        if want_video:
            vw.scene(fr)
if want_video:
    vw.close()
    print("pay-video.mp4", vw.n, "frames", round(vw.n / 10, 1), "s",
          os.path.getsize(os.path.join(OUT_DIR, "pay-video.mp4")) // 1024, "KB")
