import sys
from make_figs_d3_p import head, nbox, pill, fade, ramp
from make_gifs_p import *

CODE = [
    "upstream active_app {",
    "  zone active_app 64k;",
    "  server blue:8080;",
    "  server green:8080;",
    "}",
    "",
    "server {",
    "  listen 80;",
    "  location / {",
    "    proxy_pass http://active_app;",
    "  }",
    "}",
]
LY0, LH = 128, 26

def ly(i):
    return LY0 + LH * i

# ================================================================ upstream 구조
def fig_upstream():
    fr = []
    N = 118
    steps = [
        (0, 12, None, None, "", ""),
        (12, 30, (6, 11), "gray", "server { }", "요청을 받는 쪽. 80번 포트로 들어온 요청을 location 블록이 처리한다"),
        (30, 52, (9, 9), "amber", "proxy_pass", "받은 요청을 대신 넘기라는 지시. 이 줄이 프록시 동작을 지정한다"),
        (52, 76, (0, 4), "teal", "upstream active_app { }", "넘겨줄 서버 목록. proxy_pass가 이 이름을 가리킨다"),
        (76, 96, (2, 3), "teal", "server 줄", "목록 안의 실제 서버(blue, green). 규칙에 따라 요청 하나당 한 곳을 고른다"),
        (96, 118, (1, 1), "gray", "zone 줄", "upstream 블록 안의 한 줄. 이 목록의 순서와 실패 기록을 공유 메모리에 둔다"),
    ]
    hl = {"gray": (74, 70, 64), "amber": (104, 76, 22), "teal": (22, 86, 76)}
    capt = {0: "프록시와 upstream은 설정 파일에서 서로 다른 줄입니다", 1: "server 블록은 요청이 들어오는 입구입니다",
            2: "proxy_pass가 프록시 동작을 지정합니다", 3: "그 이름이 가리키는 upstream이 서버 목록입니다",
            4: "목록 안의 server 줄이 실제로 요청을 받습니다", 5: "zone은 upstream 블록 안의 설정 한 줄입니다"}
    for i in range(N):
        cv = Cv()
        head(cv, "upstream은 프록시와 같은가", "Nginx 설정 파일 안에서 두 개념이 놓인 자리")
        cv.rr(40, 108, 500, 452, 14, fill=DARK)
        cur = 0
        for k, st in enumerate(steps):
            if st[0] <= i < st[1]:
                cur = k
        st = steps[cur]
        if st[2]:
            a, b = st[2]
            cv.rr(50, ly(a) - 13, 490, ly(b) + 13, 6, fill=hl[st[3]])
        for k, t in enumerate(CODE):
            col = (225, 220, 210) if (st[2] and st[2][0] <= k <= st[2][1]) else (176, 168, 156)
            cv.text(62, ly(k), t, 15, col, False, "lm", True)
        # connector proxy_pass -> upstream
        if i >= 52:
            a = ramp(i, 52, 8)
            c = fade(AMBER, a)
            cv.line(496, ly(9), 530, ly(9), c, 4)
            cv.line(530, ly(9), 530, ly(0), c, 4)
            cv.arrow(530, ly(0), 498, ly(0), c, 4, 12)
            cv.text(545, (ly(0) + ly(9)) / 2, "이름 active_app으로 연결", 14, fade(WARN, a), True, "lm")
        # legend
        if i >= 30:
            pill(cv, 760, 146, "프록시 = proxy_pass 줄 (동작)", LAMB, WARN, 16, ramp(i, 30, 6))
        if i >= 52:
            pill(cv, 760, 192, "upstream = 서버 목록 (블록)", LBLUE, GOOD, 16, ramp(i, 52, 6))
        # callout
        if st[4]:
            kind = {"gray": (LGRAY, MUTE), "amber": (LAMB, AMBER), "teal": (LBLUE, BLUE)}[st[3]]
            cv.rr(570, 300, 960, 440, 14, fill=kind[0], outline=kind[1], w=3)
            cv.fit(765, 330, st[4], 22, 360, INK, True, "mm", )
            words = st[5]
            # 두 줄로 나눠 쓰기
            mid = len(words) // 2
            sp = words.find(" ", mid)
            l1, l2 = (words[:sp], words[sp + 1:]) if sp > 0 else (words, "")
            cv.fit(765, 378, l1, 16, 360, INK, False, "mm")
            cv.fit(765, 406, l2, 16, 360, INK, False, "mm")
        caption(cv, capt[cur], INK if cur != 5 else GOOD)
        fr.append(cv.done())
    return fr

# ================================================================ zone
def fig_zone():
    fr = []
    PB = 84
    N = 182
    UX, UY = 80, 300
    W1 = (200, 160, 380, 235)
    W2 = (200, 270, 380, 345)
    WY = (197, 307)
    SRV = {"blue": (700, 140, 900, 220), "green": (700, 300, 900, 380)}
    SCY = {"blue": 180, "green": 340}
    SHM = (430, 190, 590, 320)
    A_req = [(6, 0, "blue"), (22, 1, "blue"), (38, 0, "green"), (54, 1, "green")]
    B_req = [(92, 0, "blue"), (108, 1, "green"), (124, 0, "blue"), (140, 1, "green")]
    for i in range(N):
        cv = Cv()
        head(cv, "zone 줄은 무엇을 하나", "작업 프로세스(worker process) 둘이 요청을 나눠 받을 때 '다음 차례'를 누가 세는가")
        phase_b = i >= PB
        chip(cv, 40, 104, "zone 줄 있음" if phase_b else "zone 줄 없음",
             LBLUE if phase_b else LRED, GOOD if phase_b else RED)
        user(cv, UX, UY)
        cv.arrow(UX + 40, UY, 196, UY, LINE, 3)
        cv.rr(180, 130, 620, 420, 14, fill=LGRAY, outline=TEAL, w=3)
        cv.text(196, 144, "Nginx", 18, TEAL, True, "lm")
        # shared memory
        if phase_b:
            a = ramp(i, PB, 8)
            cv.rr(SHM[0], SHM[1], SHM[2], SHM[3], 12, fill=fade(LBLUE, a), outline=fade(BLUE, a), w=3)
            cv.text(510, 214, "공유 메모리", 16, fade(INK, a), True, "mm")
            cv.text(510, 238, "zone active_app", 13, fade(MUTE, a), False, "mm", True)
        # counters
        reqs = B_req if phase_b else A_req
        def nxt(c):
            return ["blue", "green"][c % 2]
        if not phase_b:
            c1 = sum(1 for s, w, d in A_req if w == 0 and s + 16 <= i)
            c2 = sum(1 for s, w, d in A_req if w == 1 and s + 16 <= i)
            labs = [nxt(c1), nxt(c2)]
        else:
            ct = sum(1 for s, w, d in B_req if s + 13 <= i)
            labs = None
        for wi, box in enumerate((W1, W2)):
            cv.rr(box[0], box[1], box[2], box[3], 12, fill=WHITE, outline=MUTE, w=3)
            cv.text((box[0] + box[2]) / 2, box[1] + 20, "작업 프로세스 %d" % (wi + 1), 16, INK, True, "mm")
            if not phase_b:
                l = labs[wi]
                pill(cv, (box[0] + box[2]) / 2, box[3] - 18, "다음 차례: " + l, LBLUE if l == "blue" else LGREEN,
                     BLUE_T if l == "blue" else GREEN_T, 14)
            else:
                pill(cv, (box[0] + box[2]) / 2, box[3] - 18, "공유 메모리에 물어봄", LGRAY, MUTE, 13)
                cv.dash(box[2], (box[1] + box[3]) / 2, SHM[0], 255 if wi == 0 else 255, LINE, 2)
        if phase_b:
            cv.text(510, 280, "다음 차례: " + nxt(ct), 15, BLUE_T if nxt(ct) == "blue" else GREEN_T, True, "mm")
        for nm, b in SRV.items():
            col = BLUE if nm == "blue" else GREEN
            server_box(cv, b[0], b[1], b[2], b[3], nm, "정상", col, "active")
        # requests
        for (s, w, d) in reqs:
            if phase_b:
                L1, L2, L3 = 10, 10, 12
                dec = s + 13
            else:
                L1, L2, L3 = 10, 6, 12
                dec = s + 16
            tot = L1 + L2 + L3
            p = (i - s) / tot
            if 0 <= p <= 1:
                wy = WY[w]
                pts = [(UX + 40, UY), (W1[0], wy), (W1[2], wy), (SRV[d][0], SCY[d])]
                x, y = along(pts, [L1, L2 + 8, L3], p)
                dot(cv, x, y, (BLUE if d == "blue" else GREEN) if i >= dec else MUTE)
                if phase_b and s + 8 <= i <= s + 16:
                    cv.line(W1[2] if False else (W1[2]), wy, SHM[0], 255, BLUE, 3)
        # result strip
        cv.text(196, 440, "응답 순서:", 15, INK, True, "lm")
        arrv = [(s + (22 if not phase_b else 28), d) for (s, w, d) in reqs if s + (22 if not phase_b else 28) <= i]
        for k, (t0, d) in enumerate(arrv):
            cv.circ(310 + k * 34, 440, 11, fill=BLUE if d == "blue" else GREEN, outline=WHITE, w=2)
        if i < 6:
            caption(cv, "요청 4개가 작업 프로세스 둘에 번갈아 들어옵니다 (예시)")
        elif i < 76:
            caption(cv, "zone 없음: 프로세스마다 '다음 차례'를 따로 셉니다", INK)
        elif i < PB:
            caption(cv, "응답 순서 blue, blue, green, green: 고르지 않게 보일 수 있습니다", WARN)
        elif i < 92:
            caption(cv, "zone 줄을 더하면: 작업 프로세스들이 공유 메모리를 함께 씁니다", INK)
        elif i < 168:
            caption(cv, "zone 있음: '다음 차례'를 공유 메모리에서 함께 셉니다", GOOD)
        else:
            caption(cv, "응답 순서 blue, green, blue, green: 번갈아 나뉩니다", GOOD)
        fr.append(cv.done())
    return fr

if __name__ == "__main__":
    only = sys.argv[2] if len(sys.argv) > 2 else "all"
    if only in ("all", "9"):
        save("fig9-upstream구조.gif", fig_upstream())
    if only in ("all", "10"):
        save("fig10-zone.gif", fig_zone())
