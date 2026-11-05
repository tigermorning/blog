import sys
from make_figs_d3_p import head, nbox, pill, fade, ramp
from make_gifs_p import *


def lerp(a, b, t):
    return a + (b - a) * t


def frames_of(steps, draw):
    out = []
    for n, prm in steps:
        for j in range(n):
            p = smooth(j / max(1, n - 1))
            out.append(draw(prm, p, len(out)))
    return out


# ============================================================ 5-1 약속은 어디에 둘까
def fig_memory_db():
    def draw(prm, p, i):
        cv = Cv()
        head(cv, "약속은 어디에 둘까: server 메모리와 DB",
             "blue(v1)와 green(v2)는 같은 프로그램을 돌리는 container 둘이다 · 약속 = \"내일 아침 8시에 물 마시기\" (노드 5장 설명 기준)")
        ph = prm["phase"]
        pill(cv, 180, 126, "약속을 server 메모리에 두면" if ph == 1 else "약속을 DB에 두면",
             LRED if ph == 1 else LGREEN, RED if ph == 1 else GOOD, 15)
        route = prm["route"]
        # 사용자와 약속 목록 화면
        user(cv, 70, 250)
        cv.rr(24, 310, 120, 372, 10, fill=WHITE, outline=LINE, w=2)
        cv.text(72, 326, "내 약속 목록", 12, MUTE, False, "mm")
        ul = prm["ulist"]
        cv.text(72, 351, ul, 18, GOOD if ul == "1개" else RED, True, "mm")
        nbox(cv, 190, 215, 290, 285, ["Nginx"], WHITE, TEAL, INK, 19)
        cv.arrow(104, 250, 186, 250, MUTE, 3, 10)
        # server 둘
        for nm, y0, col, key in (("blue", 120, BLUE, "blue"), ("green", 300, GREEN, "green")):
            on = route == key
            server_box(cv, 430, y0, 590, y0 + 130, nm, "v1 · 받는 중" if nm == "blue" and on else ("v2 · 받는 중" if on else ("v1" if nm == "blue" else "v2")),
                       col, "active" if on else "dim")
            # 메모리 칸
            my = y0 + 62
            cv.rr(442, my, 578, my + 56, 8, fill=WHITE, outline=LINE, w=2)
            cv.text(450, my + 8, "메모리", 11, MUTE, False, "lm")
            a = prm["bmem"] if nm == "blue" else prm["gmem"]
            a = lerp(a[0], a[1], p)
            if a > 0.02:
                card(cv, 510, my + 34, AMBER, a, 120)
        if route in ("blue", "green"):
            ty = 170 if route == "blue" else 365
            col = BLUE if route == "blue" else GREEN
            cv.arrow(294, 240 if route == "blue" else 262, 426, ty, col, 4, 12)
        # 재시작 표시
        rs = prm.get("restart", 0)
        if rs:
            pill(cv, 510, 104, "docker restart blue", LAMB, WARN, 13)
            if p > 0.5:
                xmark(cv, 510, 207, 12, RED, 5)
        # DB
        if ph == 2:
            cylinder(cv, 800, 190, 330, 96, DB_A, "DB")
            for y0, key in ((185, "blue"), (365, "green")):
                act = route == key
                cv.dash(594, y0, 752, 250 if key == "blue" else 285, MUTE if act else LINE, 3 if act else 2)
            da = lerp(prm["dbcard"][0], prm["dbcard"][1], p)
            if da > 0.02:
                card(cv, 800, 366, AMBER, da, 130)
                cv.text(800, 392, "DB 안의 약속", 12, MUTE, False, "mm")
        caption(cv, prm["cap"], prm["col"])
        return cv.done()

    P1 = dict(phase=1)
    steps = [
        (8, dict(P1, route="blue", bmem=(0, 1), gmem=(0, 0), ulist="1개", cap="blue가 받을 때 약속을 만들면, 약속은 blue의 메모리에 저장됩니다", col=INK)),
        (14, dict(P1, route="blue", bmem=(1, 1), gmem=(0, 0), ulist="1개", cap="blue의 메모리에 약속이 있고, 사용자 화면에도 보입니다", col=INK)),
        (16, dict(P1, route="green", bmem=(1, 1), gmem=(0, 0), ulist="없음", cap="green으로 전환하면 약속이 안 보입니다 — 약속은 blue 안에 그대로 있습니다", col=RED)),
        (14, dict(P1, route="blue", bmem=(1, 1), gmem=(0, 0), ulist="1개", cap="blue로 돌아오면 다시 보입니다 — 사라진 것이 아니었습니다", col=GOOD)),
        (20, dict(P1, route="blue", bmem=(1, 0), gmem=(0, 0), ulist="없음", restart=1, cap="blue를 재시작하면 메모리가 비워져 약속이 진짜로 사라집니다", col=RED)),
    ]
    P2 = dict(phase=2)
    steps += [
        (8, dict(P2, route="blue", bmem=(0, 0), gmem=(0, 0), dbcard=(0, 0), ulist="없음", cap="이번에는 약속을 blue와 green이 함께 보는 DB에 둡니다", col=INK)),
        (12, dict(P2, route="blue", bmem=(0, 0), gmem=(0, 0), dbcard=(0, 1), ulist="1개", cap="blue가 받은 약속이 DB에 저장됩니다", col=INK)),
        (14, dict(P2, route="green", bmem=(0, 0), gmem=(0, 0), dbcard=(1, 1), ulist="1개", cap="green으로 전환해도 같은 DB를 읽어서 약속이 보입니다", col=GOOD)),
        (14, dict(P2, route="blue", bmem=(0, 0), gmem=(0, 0), dbcard=(1, 1), ulist="1개", restart=1, cap="blue를 재시작해도 약속은 DB에 그대로 있습니다", col=GOOD)),
        (22, dict(P2, route="blue", bmem=(0, 0), gmem=(0, 0), dbcard=(1, 1), ulist="1개", cap="server가 요청 사이에 사용자 정보를 안 가지니 어느 server든 이어받습니다 (무상태)", col=GOOD)),
    ]
    return frames_of(steps, draw)


# ============================================================ 5-2 같은 DB를 쓰는 두 버전
def fig_schema():
    def draw(prm, p, i):
        cv = Cv()
        head(cv, "DB를 붙인 뒤의 위험: 두 버전이 같은 표를 읽는다",
             "예시: 표의 열 이름 하나를 바꾸는 경우 (식당 비유의 \"메뉴\" 칸을 \"음식\"으로)")
        ph = prm["phase"]
        pill(cv, 200, 126, "한 번에 바꾸면" if ph == 1 else "나눠서 바꾸면 (확장-축소)",
             LRED if ph == 1 else LGREEN, RED if ph == 1 else GOOD, 15)
        # server 둘
        bst, gst = prm["b"], prm["g"]
        for nm, y0, col, st in (("blue", 150, BLUE, bst), ("green", 310, GREEN, gst)):
            state = "dim" if st[0] == "off" else "active"
            server_box(cv, 60, y0, 240, y0 + 110, nm, "옛 버전 (v1)" if nm == "blue" else "새 버전 (v2)", col, state)
            cv.text(150, y0 + 84, st[1], 14, st[2], True, "mm")
        # 표
        TX0, TY0 = 430, 170
        cols = prm["cols"]
        cw = 120
        cv.text(TX0, TY0 - 22, "DB의 표", 14, MUTE, True, "lm")
        for k, (nm, tag) in enumerate(cols):
            x0 = TX0 + k * cw
            fill = WHITE
            if tag == "new":
                fill = mix(LGREEN, WHITE, 1 - p) if prm.get("anim") else LGREEN
            if tag == "chg":
                fill = mix(LAMB, WHITE, 1 - p) if prm.get("anim") else LAMB
            if tag == "del":
                fill = mix(LRED, WHITE, 1 - p)
            cv.rr(x0, TY0, x0 + cw, TY0 + 44, 4, fill=fill, outline=LINE, w=2)
            cv.text(x0 + cw / 2, TY0 + 22, nm, 18, INK, True, "mm")
            for r in range(2):
                cv.rr(x0, TY0 + 44 + r * 40, x0 + cw, TY0 + 84 + r * 40, 4, fill=WHITE, outline=LINE, w=2)
                cv.text(x0 + cw / 2, TY0 + 64 + r * 40, "…", 16, MUTE, False, "mm")
        # 읽기 화살표
        for y0, st, col in ((150, bst, BLUE), (310, gst, GREEN)):
            if st[0] == "off":
                continue
            ok = st[0] == "ok"
            c = col if ok else RED
            ty = TY0 + 22 if y0 == 150 else TY0 + 110
            cv.arrow(244, y0 + 55, TX0 - 8, ty, c, 4, 12)
            if not ok:
                xmark(cv, (244 + TX0) / 2, (y0 + 55 + ty) / 2, 11, RED, 5)
        if prm.get("note"):
            cv.rr(430, 390, 900, 440, 10, fill=LAMB, outline=AMBER, w=2)
            cv.fit(665, 415, prm["note"], 15, 440, WARN, True, "mm")
        caption(cv, prm["cap"], prm["col"])
        return cv.done()

    OK = ("ok", "\"메뉴\" 열을 읽는 중 (정상)", GOOD)
    steps = [
        (12, dict(phase=1, cols=[("메뉴", ""), ("시간", "")], b=("ok", "\"메뉴\" 열을 읽음 (정상)", GOOD), g=("ok", "\"메뉴\" 열을 읽음 (정상)", GOOD),
                  cap="DB는 하나, server는 두 벌 — 두 버전이 같은 표를 읽습니다", col=INK)),
        (14, dict(phase=1, anim=True, cols=[("음식", "chg"), ("시간", "")], b=("ok", "\"메뉴\" 열을 읽음 (정상)", GOOD), g=("ok", "\"음식\" 열로 바꿈", WARN),
                  cap="새 버전(green)이 열 이름을 \"메뉴\"에서 \"음식\"으로 바꿉니다", col=WARN)),
        (18, dict(phase=1, cols=[("음식", ""), ("시간", "")], b=("bad", "\"메뉴\" 열을 못 찾음", RED), g=("ok", "\"음식\" 열을 읽음 (정상)", GOOD),
                  cap="전환 중에는 두 버전이 모두 일하는데, 옛 버전(blue)은 \"메뉴\" 열을 읽지 못합니다", col=RED)),
        (22, dict(phase=1, cols=[("음식", ""), ("시간", "")], b=("bad", "\"메뉴\" 열을 못 찾음", RED), g=("off", "(롤백해서 내림)", MUTE),
                  note="롤백해도 DB는 이미 \"음식\"으로 바뀐 상태라 blue가 계속 실패합니다",
                  cap="롤백은 프로그램 버전만 되돌릴 뿐, DB의 표는 그대로입니다", col=RED)),
        (12, dict(phase=2, cols=[("메뉴", ""), ("시간", "")], b=("ok", "\"메뉴\" 열을 읽음 (정상)", GOOD), g=("ok", "\"메뉴\" 열을 읽음 (정상)", GOOD),
                  cap="같은 상황을 나눠서 바꿔 봅니다 (확장-축소 패턴)", col=INK)),
        (14, dict(phase=2, anim=True, cols=[("메뉴", ""), ("음식", "new"), ("시간", "")], b=("ok", "옛 열 \"메뉴\"로 동작 (정상)", GOOD), g=("ok", "\"메뉴\" 열을 읽음 (정상)", GOOD),
                  cap="1. 새 열 \"음식\"을 추가만 합니다 — 옛 버전은 옛 열로 그대로 동작합니다", col=GOOD)),
        (18, dict(phase=2, cols=[("메뉴", ""), ("음식", ""), ("시간", "")], b=("ok", "옛 열 \"메뉴\"로 동작 (정상)", GOOD), g=("ok", "두 열을 함께 사용 (정상)", GOOD),
                  cap="2. 두 열을 함께 쓰는 새 버전을 배포합니다 — 전환도 롤백도 안전합니다", col=GOOD)),
        (22, dict(phase=2, cols=[("메뉴", "del"), ("음식", ""), ("시간", "")], b=("off", "(다 내려감)", MUTE), g=("ok", "\"음식\" 열을 읽음 (정상)", GOOD),
                  cap="3. 이전 버전이 다 내려간 뒤에야 옛 열 \"메뉴\"를 삭제합니다", col=GOOD)),
    ]
    # 마지막 단계에서 옛 열이 실제로 사라지도록 마지막 6프레임은 열 목록에서 제거
    out = frames_of(steps, draw)
    tail = dict(phase=2, cols=[("음식", ""), ("시간", "")], b=("off", "(다 내려감)", MUTE), g=("ok", "\"음식\" 열을 읽음 (정상)", GOOD),
                cap="3. 이전 버전이 다 내려간 뒤에야 옛 열 \"메뉴\"를 삭제합니다", col=GOOD)
    for k in range(14):
        out.append(draw(tail, 1.0, len(out)))
    return out


if __name__ == "__main__":
    only = sys.argv[2] if len(sys.argv) > 2 else "all"
    if only in ("all", "m"):
        save("fig5-1-메모리와DB.gif", fig_memory_db())
    if only in ("all", "s"):
        save("fig5-2-열이름변경.gif", fig_schema())
