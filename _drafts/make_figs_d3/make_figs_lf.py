"""노션 보고서(Langfuse 2일차, 노드 11)용 움직이는 그림 6장. make_gifs.py 의 팔레트·글꼴·그리기 함수를 그대로 쓴다.
사용: python make_figs_lf.py <출력 폴더> [1~6|all]
숫자는 모두 2026-11-03 도장판 실험 결과(_drafts/langfuse-day2-experiments-v2.json, notion-langfuse-day2-report.md)에서 옮겼다.
"""
import sys

OUT_DIR = sys.argv[1]
ONLY = sys.argv[2] if len(sys.argv) > 2 else "all"
sys.argv = [sys.argv[0], OUT_DIR]
from make_gifs import *  # noqa: F401,F403  W, H, Cv, 색, header, caption, chip, save …

PINK = (252, 234, 232)


def box(cv, x0, y0, x1, y1, title, sub="", state="idle", tsize=20):
    """state: idle(회색 테두리) / on(청록) / bad(빨강) / dim(흐림) / good(청록 채움)"""
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


# ---- 그림 1. 오늘의 순서: 기준을 못 넘으면 되돌아간다 ----
def scene1():
    frames = []
    nodes = [("실패 읽기", "트레이스 46개"), ("유형·기준 문장", "①~⑥"), ("데이터셋", "21 + 12문항"),
             ("평가자", "코드 5 · 심사 3"), ("실험", "두 번씩")]
    xs = [70 + i * 176 for i in range(5)]
    y0, y1 = 150, 230
    ent = [(x + 70, (y0 + y1) / 2) for x in xs]
    DEC = (820, 330)
    PROMPT = (560, 330)
    SHIP = (820, 430)
    N = 150
    for i in range(N):
        cv = Cv()
        header(cv, 1, "오늘의 순서", "먼저 시험지와 채점 기준을 만들고, 고친 뒤 점수가 기준을 넘을 때만 서비스에 내보낸다")
        # 점 경로: 0~50 앞줄, 50~60 판정, (1바퀴) 60~85 되돌아가 지시문 v2 → 실험 → 판정 실패, 85~110 v3 → 실험, 110~130 판정 통과 → 배포
        lap = 0 if i < 85 else 1
        if i < 50:
            p = i / 50
            k = min(4, int(p * 5))
        else:
            k = 4
        for j, (t, s) in enumerate(nodes):
            st = "on" if (i < 50 and j <= k) or i >= 50 else "idle"
            box(cv, xs[j], y0, xs[j] + 140, y1, t, s, st, 19)
            if j < 4:
                cv.arrow(xs[j] + 142, (y0 + y1) / 2, xs[j + 1] - 4, (y0 + y1) / 2, MUTE, 3, 10)
        # 판정 마름모 대신 둥근 상자
        dec_state = "idle"
        if 50 <= i < 70:
            dec_state = "bad"
        elif 100 <= i < 125:
            dec_state = "bad" if False else "good"
        elif i >= 125:
            dec_state = "good"
        box(cv, DEC[0] - 90, DEC[1] - 34, DEC[0] + 90, DEC[1] + 34, "기준을 넘었나?", "실험 전에 정해 둠", dec_state, 18)
        cv.arrow(ent[4][0], y1 + 2, DEC[0], DEC[1] - 38, MUTE, 3, 10)
        # 지시문 상자
        pv = "v2" if i < 85 else "v3"
        pstate = "amber" if 62 <= i < 100 else "idle"
        box(cv, PROMPT[0] - 110, PROMPT[1] - 34, PROMPT[0] + 110, PROMPT[1] + 34, f"지시문 {pv}", "staging 라벨", pstate, 19)
        cv.arrow(DEC[0] - 92, DEC[1], PROMPT[0] + 114, PROMPT[1], RED if 55 <= i < 85 else LINE, 3, 10)
        cv.text(700, DEC[1] + 20, "못 넘음", 15, RED if 55 <= i < 85 else MUTE, True, "mm")
        cv.arrow(PROMPT[0], PROMPT[1] - 36, ent[4][0] - 20, y1 + 4, AMBER if 62 <= i < 100 else LINE, 3, 10)
        # 배포
        sstate = "good" if i >= 118 else "idle"
        box(cv, SHIP[0] - 110, SHIP[1] - 30, SHIP[0] + 110, SHIP[1] + 30, "production 으로", "라벨 이동 · 평가 관문", sstate, 18)
        cv.arrow(DEC[0], DEC[1] + 36, SHIP[0], SHIP[1] - 34, GOOD if i >= 112 else LINE, 3, 10)
        cv.text(DEC[0] + 50, 392, "넘음", 15, GOOD if i >= 112 else MUTE, True, "mm")
        # 움직이는 점
        if i < 50:
            pos = along(ent, [1, 1, 1, 1], i / 50)
        elif i < 60:
            pos = along([ent[4], (DEC[0], DEC[1] - 34)], [1], (i - 50) / 10)
        elif i < 75:
            pos = along([(DEC[0] - 90, DEC[1]), (PROMPT[0] + 110, PROMPT[1])], [1], (i - 60) / 15)
        elif i < 85:
            pos = along([(PROMPT[0], PROMPT[1] - 34), (ent[4][0] - 20, y1)], [1], (i - 75) / 10)
        elif i < 100:
            pos = along([ent[4], (DEC[0], DEC[1] - 34)], [1], (i - 85) / 15)
        elif i < 118:
            pos = along([(DEC[0], DEC[1] + 34), (SHIP[0], SHIP[1] - 30)], [1], (i - 100) / 18)
        else:
            pos = (SHIP[0], SHIP[1] - 30)
        cv.circ(pos[0], pos[1], 11, fill=AMBER, outline=WHITE, w=3)
        # 왼쪽 아래 기록
        cv.text(60, 290, "실제로 돈 바퀴", 17, INK, True)
        cv.text(60, 320, "1바퀴: v2 → +2.5 (기준 +3) 못 넘음", 15, RED if i >= 55 else MUTE)
        cv.text(60, 346, "2바퀴: v3 + 코드 → +3 넘음", 15, GOOD if i >= 105 else MUTE)
        cv.text(60, 372, "그 뒤 두 번 더(빈 맞장구,", 14, MUTE)
        cv.text(60, 394, "관계 고민 회귀를 찾아서)", 14, MUTE)
        msg = ("앞에서부터: 실패를 읽고, 시험지와 채점자를 만든다" if i < 50 else
               "기준은 결과를 보기 전에 정한다 — 못 넘으면 지시문으로 돌아간다" if i < 100 else
               "넘으면 production 라벨을 옮긴다(코드 재배포 없음)")
        caption(cv, msg)
        frames.append(cv.done())
    return frames


# ---- 그림 2. 트레이스를 앞에서부터 읽기 ----
def scene2():
    frames = []
    steps = [("check-safety", "위기 표현?", "아니요"), ("choose-mode", "모드·카드 고르기", "listen (기대: advise)"),
             ("generate-reply", "답 쓰기", "'5분 해 보세요'"), ("check-numbers", "숫자 검사", "ok = false")]
    xs = [60 + i * 228 for i in range(4)]
    y0, y1 = 220, 330
    N = 100
    for i in range(N):
        cv = Cv()
        header(cv, 2, "트레이스는 앞에서부터 읽는다", "답이 이상하면, 맨 앞 단계부터 하나씩 열어 처음 잘못된 곳을 찾는다")
        cv.rr(60, 112, 940, 168, 14, fill=WHITE, outline=LINE)
        cv.text(80, 140, "사용자", 16, MUTE, True, "lm")
        cv.text(150, 140, "일을 시작하는 게 안 돼요. 방법 좀 알려 주세요.", 20, INK, True, "lm")
        lit = min(4, i // 14)  # 0..4 단계까지 켜짐
        for j, (name, what, res) in enumerate(steps):
            if j < lit:
                st = "bad" if j == 1 else ("dim" if j > 1 and i >= 70 else "on")
            else:
                st = "idle"
            box(cv, xs[j], y0, xs[j] + 200, y1, name, what, st, 19)
            if j < 3:
                cv.arrow(xs[j] + 202, (y0 + y1) / 2, xs[j + 1] - 4, (y0 + y1) / 2, MUTE, 3, 10)
            if j < lit:
                color = RED if j == 1 else (MUTE if j > 1 else GOOD)
                cv.fit(xs[j] + 100, y1 + 26, res, 17, 196, color, True, "mm")
        if i >= 32:
            # 처음 틀린 곳 표시
            p = smooth((i - 32) / 10)
            cv.rr(xs[1] - 8, y0 - 14, xs[1] + 208, y1 + 46, 18, outline=mix(BG, RED, p), w=4)
            cv.text(xs[1] + 100, y0 - 32, "처음 틀린 곳", 18, mix(BG, RED, p), True, "mm")
        if i >= 70:
            p = smooth((i - 70) / 10)
            cv.text(xs[2] + 214, y1 + 70, "뒤 단계의 '5분'은 원인이 아니라 결과", 17, mix(BG, MUTE, p), True, "mm")
            cv.arrow(xs[2] + 100, y1 + 52, xs[1] + 140, y1 + 52, mix(BG, MUTE, p), 3, 10)
        cv.text(60, 430, "고칠 곳: 모드 고르기 지시문(stamp-plan) — '방법을 직접 청하면 advise'", 18,
                mix(BG, INK, smooth((i - 50) / 10)), True)
        msg = ("메시지 하나가 지나는 단계가 차례로 켜진다" if i < 32 else
               "앞 단계가 틀리면 뒤 단계가 맞게 돌아도 답이 틀린다" if i < 70 else
               "그래서 처음 틀린 단계 하나만 고친다")
        caption(cv, msg)
        frames.append(cv.done())
    return frames


# ---- 그림 3. 심사를 믿기까지: 사람 라벨과 맞춰 보기 ----
def scene3():
    frames = []
    # (일치율 %, 놓친 실패, 과한 실패, 단계, 한 일) — langfuse-day2-calibration-v2~v5.json 과 첫 실행 출력에서 다시 계산(2026-11-03)
    stages = [(65, 6, 2, "1 처음", "효과 단정 심사 하나"), (74, 5, 1, "2 말투·뜻 심사 추가", "존댓말↔반말, 뜻 모를 문장"),
              (65, 0, 8, "3 맥락 심사 추가", "내 판정 이유를 기준 글로"), (61, 0, 9, "4 말투 설정 결정", "설정을 바꾼 대화는 통과"),
              (91, 0, 2, "5 경계 4가지 정함", "되묻기·막연한 제안·열린 질문·방법 되묻기")]
    X0, X1 = 260, 900
    STEP = 28
    N = len(stages) * STEP
    for i in range(N):
        cv = Cv()
        header(cv, 3, "LLM 심사를 믿기까지", "내가 직접 판정한 답 23개와 Claude 심사 판정이 얼마나 같은가")
        k = min(len(stages) - 1, i // STEP)
        p = smooth((i - k * STEP) / 16)
        prev = stages[k - 1] if k else (0, 6, 2)
        val = prev[0] + (stages[k][0] - prev[0]) * p
        miss = round(prev[1] + (stages[k][1] - prev[1]) * p)
        over = round(prev[2] + (stages[k][2] - prev[2]) * p)
        # 막대
        cv.text(60, 148, "일치율", 20, INK, True)
        cv.rr(X0, 128, X1, 168, 12, fill=LGRAY)
        w = (X1 - X0) * val / 100
        cv.rr(X0, 128, X0 + max(24, w), 168, 12, fill=BLUE if val >= 90 else AMBER)
        cv.text(X0 + max(24, w) - 10, 148, f"{val:.0f}%", 20, WHITE, True, "rm")
        tx = X0 + (X1 - X0) * 0.9
        cv.dash(tx, 118, tx, 178, RED, 3)
        cv.text(tx, 192, "믿고 쓸 기준 90%", 14, RED, True, "mm")
        # 놓친 실패 / 과한 실패
        for row, (label, sub, cnt, mx, color) in enumerate([("놓친 실패", "나는 실패, 심사는 통과", miss, 6, RED),
                                                            ("과한 실패", "나는 통과, 심사는 실패", over, 9, WARN)]):
            y = 228 + row * 50
            cv.text(60, y - 8, label, 19, INK, True)
            cv.text(60, y + 14, sub, 13, MUTE)
            for m in range(mx):
                x = X0 + m * 46
                if m < cnt:
                    xmark(cv, x + 16, y, 12, color, 4)
                else:
                    check(cv, x + 16, y, 9, LINE)
            cv.text(X0 + 440, y, f"{cnt}개", 24, color if cnt else GOOD, True, "lm")
        # 단계 목록
        for j, (v, mi, ov, t, s) in enumerate(stages):
            y = 332 + j * 26
            on = j <= k
            cv.circ(70, y, 7, fill=(BLUE if on else LINE))
            cv.text(86, y, t, 16, INK if on else MUTE, True, "lm")
            cv.text(270, y, s, 14, INK if on else MUTE, False, "lm")
            if on and (j < k or p > 0.95):
                cv.text(700, y, f"{v}% · 놓침 {mi} · 과함 {ov}", 15, BLUE if v >= 90 else WARN, True, "lm")
        msg = ("맥락 심사를 넣자 놓친 실패는 0, 대신 좋은 답 8개를 실패로 잡았다" if k in (2, 3) else
               "경계를 내 말로 정해 기준 글에 넣자 91% · 놓친 실패 0" if k == 4 else
               "심사가 틀린 게 아니라, 판정 기준 글에 빈 곳이 있었다")
        caption(cv, msg)
        frames.append(cv.done())
    return frames


# ---- 그림 4. 문장 걸러 내기(코드로 옮긴 규칙) ----
def scene4():
    frames = []
    sents = [("퇴근하면 피곤해서 운동이 안 되시는군요.", "pass", "되받기"),
             ("5분만 걸어 보면 도움이 될 거예요.", "block", "근거 없는 숫자"),
             ("언제가 제일 힘드세요?", "block2", "직전이 질문 → 되묻기 금지"),
             ("오늘은 운동복으로 갈아입기까지만 해 볼까요?", "pass", "제안은 통과"),
             ("어떤 운동이 좋을까요?", "block", "두 번째 질문")]
    GX = 520
    N = 150
    per = 26
    for i in range(N):
        cv = Cv()
        header(cv, 4, "지시문으로 안 지켜지던 규칙은 코드가 거른다", "모델이 쓴 문장을 하나씩 검사해서, 규칙에 어긋난 문장은 사용자 화면에 보내지 않는다")
        cv.text(70, 118, "모델이 쓰는 답", 18, MUTE, True)
        cv.text(GX + 60, 118, "사용자 화면", 18, MUTE, True)
        cv.rr(GX - 40, 140, GX - 10, 440, 8, fill=LAMB, outline=AMBER, w=3)
        cv.text(GX - 25, 290, "관\n문", 18, WARN, True, "mm")
        cv.rr(GX + 50, 140, 950, 440, 14, fill=WHITE, outline=LINE)
        cv.text(GX + 60, 450, "직전 도우미 말: \"뭐가 제일 힘들어요?\" (질문)", 14, MUTE)
        shown_y = 160
        for j, (t, kind, why) in enumerate(sents):
            start = j * per
            if i < start:
                continue
            p = smooth((i - start) / 12)
            y = 140 + j * 60  # 문장 상자 34 + 이유 글 줄 + 여백
            if p < 1:
                cv.rr(70, y, 440, y + 34, 10, fill=WHITE, outline=LINE)
                cv.fit(255, y + 17, t, 15, 360, INK, False, "mm")
                cv.arrow(445, y + 17, 445 + (GX - 50 - 445) * p, y + 17, MUTE, 3, 9)
            else:
                cv.rr(70, y, 440, y + 34, 10, fill=LGRAY if kind != "pass" else WHITE, outline=LINE)
                cv.fit(255, y + 17, t, 15, 360, MUTE if kind != "pass" else INK, False, "mm")
                if kind == "pass":
                    check(cv, 462, y + 17, 9)
                    cv.rr(GX + 66, shown_y, 934, shown_y + 40, 10, fill=LBLUE, outline=BLUE, w=2)
                    cv.fit((GX + 66 + 934) / 2, shown_y + 20, t, 15, 340, INK, True, "mm")
                    shown_y += 52
                else:
                    xmark(cv, 462, y + 17, 9, RED, 4)
                cv.fit(255, y + 46, why, 13, 360, GOOD if kind == "pass" else RED, True, "mm")
        msg = ("질문은 하나만 · 직전이 질문이면 되묻지 않기 · 근거 없는 숫자 금지 — 지시문에 있어도 안 지켜졌다" if i < 100 else
               "'~해 볼까요?'는 되묻기가 아니라 제안 — 지웠더니 맞장구 한 줄만 남는 실패가 났었다")
        caption(cv, msg)
        frames.append(cv.done())
    return frames


# ---- 그림 5. 라벨을 옮기면 배포, 거꾸로 옮기면 롤백 ----
def scene5():
    frames = []
    cards = [("v1", "처음 문장"), ("v2", "실패 유형 고침"), ("v3", "남은 표현 막기")]
    xs = [120, 400, 680]
    y0, y1 = 220, 330
    N = 130
    for i in range(N):
        cv = Cv()
        header(cv, 5, "배포는 라벨을 옮기는 일", "서비스는 production 이름표가 붙은 버전을 가져다 쓴다 — 이름표만 옮기면 코드를 고치지 않아도 바뀐다")
        for j, (v, s) in enumerate(cards):
            appear = j == 0 or i >= 15 + (j - 1) * 20
            if not appear:
                continue
            box(cv, xs[j], y0, xs[j] + 200, y1, f"버전 {v[1]}", s, "on" if j == 2 and i >= 70 else "idle", 22)
            if j:
                cv.arrow(xs[j - 1] + 204, (y0 + y1) / 2, xs[j] - 4, (y0 + y1) / 2, LINE, 3, 9)
        # staging 이름표: v1 → v2(15~) → v3(35~)
        st_idx = 0 if i < 15 else (1 if i < 35 else 2)
        cv.rr(xs[st_idx] + 30, y0 - 56, xs[st_idx] + 170, y0 - 22, 16, fill=LAMB)
        cv.text(xs[st_idx] + 100, y0 - 39, "staging(시험)", 16, WARN, True, "mm")
        # production 이름표: v1 에 있다가 70~90 사이 v3 로, 100~115 롤백 시연(점선), 115~ 다시 v3
        if i < 70:
            px = xs[0]
        elif i < 90:
            px = xs[0] + (xs[2] - xs[0]) * smooth((i - 70) / 20)
        else:
            px = xs[2]
        cv.rr(px + 20, y1 + 22, px + 180, y1 + 58, 16, fill=BLUE)
        cv.text(px + 100, y1 + 40, "production(서비스)", 16, WHITE, True, "mm")
        if 50 <= i < 70:
            cv.text(500, 420, "실험 두 번 → 기준을 넘음", 18, GOOD, True, "mm")
        if i >= 100:
            p = smooth((i - 100) / 12)
            cv.dash(xs[2] + 20, y1 + 80, xs[0] + 180, y1 + 80, mix(BG, RED, p), 3)
            cv.arrow(xs[0] + 200, y1 + 80, xs[0] + 182, y1 + 80, mix(BG, RED, p), 3, 10)
            cv.text(500, y1 + 104, "문제가 생기면: 이전 버전에 production 을 다시 붙인다(몇 초)", 16, mix(BG, RED, p), True, "mm")
        msg = ("새 버전은 staging 에 두고 같은 시험지로 잰다" if i < 50 else
               "기준을 넘으면 production 이름표를 새 버전으로 옮긴다 = 배포" if i < 100 else
               "롤백도 이름표를 옮기는 일 — 트레이스에 '버전 3'이 함께 남는다")
        caption(cv, msg)
        frames.append(cv.done())
    return frames


# ---- 그림 6. 전후 비교 ----
def scene6():
    frames = []
    rows = [("심사 셋 모두 통과", 5.5, 10.5, 12), ("지어낸 숫자 없음", 10.5, 12, 12), ("되묻기 없음", 1, 4, 4),
            ("질문 하나", 6, 12, 12), ("모드를 맞게 고름", 18, 20, 21)]
    X0, X1 = 330, 860
    N = 90
    for i in range(N):
        cv = Cv()
        header(cv, 6, "같은 시험지, 고치기 전과 후", "두 번씩 돌린 평균 · 도우미 gpt-4o-mini · 심사 Claude Sonnet")
        cv.rr(600, 104, 626, 124, 6, fill=LINE)
        cv.text(632, 114, "기준선(v1)", 15, MUTE, True, "lm")
        cv.rr(740, 104, 766, 124, 6, fill=BLUE)
        cv.text(772, 114, "지금(v3 + 코드)", 15, INK, True, "lm")
        for j, (name, a, b, tot) in enumerate(rows):
            y = 152 + j * 60
            cv.text(70, y + 14, name, 18, INK, True, "lm")
            cv.text(70, y + 38, f"{tot}개 중", 13, MUTE, False, "lm")
            p = smooth((i - j * 6) / 30)
            wa = (X1 - X0) * a / tot
            wb = (X1 - X0) * (a + (b - a) * p) / tot
            cv.rr(X0, y, X0 + max(10, wa), y + 18, 6, fill=LINE)
            cv.text(X0 + wa + 8, y + 9, f"{a:g}", 14, MUTE, True, "lm")
            cv.rr(X0, y + 24, X0 + max(10, wb), y + 44, 6, fill=BLUE)
            cv.text(X0 + wb + 8, y + 34, f"{a + (b - a) * p:.1f}".rstrip("0").rstrip("."), 15, BLUE, True, "lm")
        caption(cv, "지시문(v3)은 해석의 문제를, 코드는 매번 같아야 하는 규칙을 고쳤다")
        frames.append(cv.done())
    return frames


JOBS = {"1": ("lf1-order.gif", scene1), "2": ("lf2-trace.gif", scene2), "3": ("lf3-judge.gif", scene3),
        "4": ("lf4-gate.gif", scene4), "5": ("lf5-labels.gif", scene5), "6": ("lf6-before-after.gif", scene6)}
for k, (nm, fn) in JOBS.items():
    if ONLY in ("all", k):
        save(nm, fn())
