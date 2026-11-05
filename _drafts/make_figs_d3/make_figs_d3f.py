import sys, math
from make_figs_d3_p import head, nbox, pill, fade, ramp
from make_gifs_p import *

# ============================================================ 응답 없는 server 앞에서 기다리는 시간
# 왼쪽: Nginx 안에서 일어나는 일 / 오른쪽: 사용자 화면. 같은 시계(경과 시간) 하나로 움직인다.
AX0, AX1 = 40, 600  # 하단 막대(green을 기다린 시간) 가로 범위. 눈금은 두 경우 모두 0~60초.
LIMIT_SCALE = 60.0


def spinner(cv, cx, cy, i):
    for k in range(8):
        ang = 2 * math.pi * k / 8
        lead = (i // 2 - k) % 8
        a = max(0.18, 1 - lead / 7.0)
        cv.circ(cx + 24 * math.cos(ang), cy + 24 * math.sin(ang), 5, fill=fade(RED, a))


def browser(cv, state, i, shown):
    x0, y0, x1, y1 = 640, 116, 960, 330
    cv.rr(x0, y0, x1, y1, 12, fill=WHITE, outline=LINE, w=3)
    cv.rr(x0, y0, x1, y0 + 34, 12, fill=LGRAY, outline=LINE, w=3)
    for k in range(3):
        cv.circ(x0 + 18 + k * 16, y0 + 17, 4, fill=LINE)
    cv.rr(x0 + 72, y0 + 7, x1 - 14, y0 + 27, 10, fill=WHITE)
    cv.text(x0 + 84, y0 + 17, "도장판", 12, MUTE, False, "lm")
    cx, cy = (x0 + x1) / 2, (y0 + 34 + y1) / 2
    if state == "wait":
        spinner(cv, cx, cy - 12, i)
        cv.text(cx, cy + 36, "응답 없음 · 화면이 멈춰 있음", 14, RED, True, "mm")
    else:
        cv.text(x0 + 24, y0 + 60, "오늘의 도장", 18, INK, True, "lm")
        for k in range(3):
            yy = y0 + 92 + k * 34
            cv.rr(x0 + 24, yy, x1 - 24, yy + 24, 8, fill=LGREEN, outline=GREEN, w=2)
        cv.text(x1 - 34, y0 + 60, "표시됨", 14, GOOD, True, "rm")
    # 이 화면의 상태 막대
    return


def clock_text(cv, t, state, setting):
    x, y = 800, 350
    if state == "wait":
        cv.text(x, y, "사용자 화면이 멈춘 시간", 15, MUTE, False, "mm")
        cv.text(x, y + 40, "%d초" % int(t), 40, RED, True, "mm")
    else:
        lab = "60초" if setting == "default" else "약 1초"
        col = RED if setting == "default" else GOOD
        cv.text(x, y, "사용자가 기다린 시간", 15, MUTE, False, "mm")
        cv.text(x, y + 40, lab, 40, col, True, "mm")


def frame(i, setting, t, phase, caption_txt, cap_col):
    """setting: default | one. phase: try (green 대기) | switch (blue로 넘김) | done (화면 뜸)."""
    cv = Cv()
    head(cv, "응답 없는 server 앞에서 사용자가 기다리는 시간",
         "green이 꺼져 있고 요청이 green 차례일 때 · 왼쪽은 Nginx 안, 오른쪽은 사용자 화면 (blue의 응답 시간은 예시)")
    lim = 60.0 if setting == "default" else 1.0
    pill(cv, 180, 126, "기본값 60초" if setting == "default" else "1초로 줄이면",
         LAMB if setting == "default" else LGREEN, WARN if setting == "default" else GOOD, 15)
    cv.text(262, 126, "proxy_connect_timeout %s" % ("60s" if setting == "default" else "1s"), 12, MUTE, False, "lm", True)

    # ---- 왼쪽 그림
    user(cv, 90, 250)
    nbox(cv, 200, 215, 310, 285, ["Nginx"], WHITE, TEAL, INK, 19)
    cv.arrow(124, 250, 196, 250, MUTE, 3, 10)
    server_box(cv, 440, 150, 580, 250, "green", "꺼져 있음", GREEN, "dead")
    blue_on = phase in ("switch", "done")
    server_box(cv, 440, 290, 580, 390, "blue", "정상", BLUE, "active" if blue_on else "dim")
    if phase == "try":
        cv.arrow(314, 238, 434, 204, AMBER, 4, 12)
        # 응답을 기다리며 오가는 점
        p = (i % 14) / 14.0
        cv.circ(314 + 120 * p, 238 - 34 * p, 7, fill=AMBER, outline=WHITE, w=2)
        cv.text(372, 188, "연결 시도", 13, WARN, True, "mm")
    else:
        cv.dash(314, 238, 434, 204, LINE, 2)
        cv.arrow(314, 262, 434, 322, BLUE, 4, 12)
        cv.text(386, 312, "blue로", 13, BLUE_T, True, "mm")

    # ---- 오른쪽: 사용자 화면
    browser(cv, "wait" if phase == "try" else "ok", i, True)
    clock_text(cv, t, "wait" if phase == "try" else "ok", setting)

    # ---- 아래: green을 기다린 시간 막대 (두 경우 모두 0~60초 눈금)
    by = 420
    cv.text(AX0, by - 16, "Nginx가 green을 기다린 시간", 14, INK, True, "lm")
    cv.rr(AX0, by, AX1, by + 22, 8, fill=LGRAY, outline=LINE, w=2)
    waited = min(t, lim)
    w = (AX1 - AX0) * waited / LIMIT_SCALE
    if w > 1:
        cv.rr(AX0, by, AX0 + max(w, 6), by + 22, 8 if w > 16 else 3, fill=AMBER if setting == "default" else GREEN)
    cv.text(AX1 + 14, by + 11, "%s초 / 한도 %d초" % (("%d" % int(waited)) if setting == "default" else ("%.1f" % waited), int(lim)),
            14, INK, True, "lm")
    for s in (0, 20, 40, 60):
        xx = AX0 + (AX1 - AX0) * s / LIMIT_SCALE
        cv.line(xx, by + 24, xx, by + 30, MUTE, 2)
        cv.text(xx, by + 40, "%d초" % s, 11, MUTE, False, "mm")

    caption(cv, caption_txt, cap_col)
    return cv.done()


def fig_wait():
    fr = []
    # --- 기본값 60초: 60초를 1초에 한 프레임씩
    for j in range(0, 8):
        fr.append(frame(j, "default", 0, "try", "요청이 green 차례가 됐는데, green은 꺼져 있습니다", INK))
    for j in range(0, 61):
        fr.append(frame(j + 8, "default", j, "try",
                        "Nginx는 green이 응답하길 기다립니다 — 사용자 화면은 그동안 멈춰 있습니다", RED))
    for j in range(0, 6):
        fr.append(frame(j, "default", 60, "switch", "60초가 지나서야 포기하고 blue로 보냅니다", WARN))
    for j in range(0, 14):
        fr.append(frame(j, "default", 60, "done", "blue가 응답해 화면이 뜹니다 — 사용자는 60초를 기다렸습니다", RED))
    # --- 1초로 줄이면
    for j in range(0, 6):
        fr.append(frame(j, "one", 0, "try", "같은 상황에서 한도를 1초로 줄이면 …", INK))
    for j in range(0, 4):
        fr.append(frame(j, "one", min(1.0, j / 3.0), "try", "1초만 기다립니다", WARN))
    for j in range(0, 5):
        fr.append(frame(j, "one", 1.0, "switch", "1초가 지나자마자 blue로 보냅니다", WARN))
    for j in range(0, 26):
        fr.append(frame(j, "one", 1.0, "done", "화면이 거의 바로 뜹니다 — 사용자가 기다린 시간은 약 1초입니다", GOOD))
    return fr


if __name__ == "__main__":
    save("figT-시간표.gif", fig_wait())
