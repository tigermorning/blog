import sys
from make_figs_d3_p import head, nbox, pill, fade, ramp
from make_gifs_p import *

# ============================================================ 한 요청의 시간표
def fig_timeline():
    fr = []
    N = 168
    X0, X1, T = 170, 900, 64.0
    k = (X1 - X0) / T

    def xs(t):
        return X0 + t * k

    lanes = [("기본값 60초", 60.0, 150), ("1초로 줄이면", 1.0, 296)]
    for i in range(N):
        t = min(T, i * 0.5)
        cv = Cv()
        head(cv, "한 사용자의 요청 시간표", "green이 꺼져 있을 때, 그 요청이 green 차례였다면 (시간 눈금은 예시)")
        cv.dash(xs(2), 124, xs(2), 400, RED, 2)
        cv.text(xs(2) + 8, 107, "2초: 요청 확인 스크립트의 실패 기준", 13, RED, True, "lm")
        for title, lim, y in lanes:
            cv.text(40, y + 20, title, 20, INK, True, "lm")
            cv.text(40, y + 46, "proxy_connect_timeout", 11, MUTE, False, "lm", True)
            cv.rr(X0, y, X1, y + 40, 8, fill=LGRAY, outline=LINE, w=2)
            wait = min(t, lim)
            if wait > 0:
                cv.rr(X0, y, xs(wait), y + 40, 8 if xs(wait) - X0 > 16 else 3, fill=AMBER)
            if t >= lim:
                xmark(cv, xs(lim), y + 20, 11, RED, 5)
                tb = min(t, lim + 0.5)
                if tb > lim:
                    cv.rr(xs(lim) + 8, y + 8, xs(tb) + 8, y + 32, 6, fill=BLUE)
            done = lim + 0.5
            if t < lim:
                cv.text(X0, y + 58, "green에 연결하려고 기다리는 중 %d초 · 사용자 화면이 멈춰 있음" % int(t), 15, RED, True, "lm")
            elif t < done:
                cv.text(X0, y + 58, "한도 도달 → blue로 다시 보냄", 15, WARN, True, "lm")
            else:
                cv.text(X0, y + 58, "blue가 응답 · 사용자가 기다린 시간 약 %d초" % int(lim), 15, GOOD, True, "lm")
            if lim > 2 and t >= 2:
                cv.text(X0, y + 80, "스크립트 기준: 2초를 넘겨 실패로 기록", 14, RED, True, "lm")
            if lim <= 2 and t >= done:
                cv.text(X0, y + 80, "스크립트 기준: 2초 안에 응답 → 성공", 14, GOOD, True, "lm")
        # 시간 눈금
        for s in range(0, 61, 10):
            cv.line(xs(s), 392, xs(s), 400, MUTE, 2)
            cv.text(xs(s), 412, "%d초" % s, 12, MUTE, False, "mm")
        cv.line(X0, 396, X1, 396, LINE, 2)
        # 지금 시각
        cv.line(xs(t), 132, xs(t), 392, TEAL, 3)
        pill(cv, xs(t), 138, "경과 %d초" % int(t), LTEAL, TEAL, 13)
        if t < 2:
            caption(cv, "같은 요청이 green에 연결하려 합니다. 두 줄의 차이는 대기 한도뿐입니다")
        elif t < 60:
            if t < 4:
                caption(cv, "1초 한도는 이미 blue로 넘어가 응답을 받았지만, 60초 한도는 아직 기다립니다", WARN)
            else:
                caption(cv, "위쪽 요청은 계속 멈춘 채 기다립니다 — 사용자 화면이 멈춰 있습니다", RED)
        else:
            caption(cv, "60초 한도는 60초 뒤에야 blue로 넘어가고, 1초 한도는 1초 만에 넘어갑니다", GOOD)
        fr.append(cv.done())
    return fr

# ============================================================ availability
def fig_avail():
    fr = []
    N = 128
    rows = [("99%", "투 나인", "약 3.65일", 5256.0, (250, 170, 150)),
            ("99.9%", "쓰리 나인", "약 8.8시간", 528.0, (250, 205, 120)),
            ("99.99%", "포 나인", "약 53분", 53.0, (150, 210, 160)),
            ("99.999%", "파이브 나인", "약 5분", 5.0, (120, 180, 240))]
    X0 = 330
    scale = 460 / 5256.0
    for i in range(N):
        cv = Cv()
        head(cv, "availability: 1년 중 서비스가 멈추는 시간", "availability가 낮을수록 1년 동안 멈추는 시간이 길다 · 9가 하나 늘 때마다 약 10분의 1 (노드 2장)")
        cv.text(X0, 110, "1년 동안 멈추는 시간", 14, MUTE, True, "lm")
        for kk, (pct, nm, txt, mins, col) in enumerate(rows):
            y = 126 + kk * 80
            st = 10 + kk * 20
            p = smooth((i - st) / 16)
            cv.text(40, y + 14, pct, 28, INK, True, "lm")
            cv.text(40, y + 44, nm, 14, MUTE, False, "lm")
            cv.rr(X0, y, X0 + 460, y + 36, 8, fill=LGRAY, outline=LINE, w=2)
            w = max(4.0, mins * scale) * p
            if w > 1:
                cv.rr(X0, y, X0 + w, y + 36, 6 if w > 12 else 2, fill=col)
            if p > 0.9:
                cv.text(X0 + max(4.0, mins * scale) + 16, y + 12, txt, 20, INK, True, "lm")
                if kk > 0:
                    pill(cv, X0 + max(4.0, mins * scale) + 90, y + 40, "앞 줄의 약 10분의 1", LAMB, WARN, 12, ramp(i, st + 14, 6))
        cv.text(40, 446, "막대 길이는 시간에 비례한다. 99.99%와 99.999%는 너무 짧아 최소 두께로 그렸다.", 13, MUTE, False, "lm")
        if i < 10:
            caption(cv, "availability는 1년 중 서비스를 쓸 수 있었던 시간의 비율입니다")
        elif i < 96:
            caption(cv, "availability가 낮을수록 멈추는 시간이 깁니다 — 99%면 1년에 약 3.65일", INK)
        else:
            caption(cv, "9가 하나 늘 때마다 멈추는 시간이 약 10분의 1로 줄어듭니다", GOOD)
        fr.append(cv.done())
    return fr

if __name__ == "__main__":
    only = sys.argv[2] if len(sys.argv) > 2 else "all"
    if only in ("all", "t"):
        save("figT-시간표.gif", fig_timeline())
    if only in ("all", "a"):
        save("figA-availability.gif", fig_avail())
