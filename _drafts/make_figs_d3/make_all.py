import sys
sys.argv = [sys.argv[0], sys.argv[1]]
from make_gifs import *

UX, UY = 80, 295
NX0, NY0, NX1, NY1 = 260, 250, 380, 340
BX0, BY0, BX1, BY1 = 560, 150, 780, 255
GX0, GY0, GX1, GY1 = 560, 320, 780, 425
BCY, GCY = (BY0 + BY1) / 2, (GY0 + GY1) / 2
DBX = 895
BSLOT = (670, BY1 - 28)
GSLOT = (670, GY1 - 28)
DBCARD = (DBX, 392)

T1B, T2, F2, T3, ADD, T4A, G1, R1, T4B, G2, R2, END = 26, 70, 130, 142, 168, 198, 226, 240, 258, 290, 304, 334
DEAD_G, DETECT_G = 46, 58

def stage_of(i):
    if i < T2: return 0
    if i < T3: return 1
    if i < T4A: return 2
    return 3

def dest(s0):
    dec = s0 + 8; m = s0 // 6
    if dec < T1B: return "blue"
    if dec < T2: return "green" if (m % 2 == 1 and dec < DETECT_G) else "blue"
    if dec < F2: return "blue"
    if dec < ADD: return "green"
    if dec < T4A: return "green" if m % 2 == 1 else "blue"
    if dec < G1: return "blue"
    if dec < T4B: return "green"
    if dec < G2: return "blue"
    return "green"

def failed_1b(s0):
    return (T1B <= s0 and s0 + 8 < DETECT_G and (s0 // 6) % 2 == 1 and s0 + 24 > DEAD_G)

def single_target(i):
    """upstream 한 줄일 때 가리키는 서버와 그 줄이 바뀐 시점"""
    segs = [(T2, "blue"), (F2, "green"), (T4A, "blue"), (G1, "green"), (T4B, "blue"), (G2, "green")]
    cur = None; start = 0
    for s, t in segs:
        if i >= s:
            cur, start = t, s
    return cur, start

def active_targets(i):
    if i < T1B: return None
    if i < DETECT_G: return ["blue", "green"]
    if i < F2: return ["blue"]
    if i < ADD: return ["green"]
    if i < T4A: return ["blue", "green"]
    if i < G1: return ["blue"]
    if i < T4B: return ["green"]
    if i < G2: return ["blue"]
    return ["green"]

def tracker(cv, i):
    names = ["이중화", "블루그린", "Nginx", "무상태"]
    cur = stage_of(i)
    x = 40
    for k, n in enumerate(names):
        w = cv.d.textlength(n, font=font(16, True)) / S + 30
        if i >= END - 14:
            fill, col = GOOD, WHITE
        elif k == cur:
            fill, col = TEAL, WHITE
        elif k < cur:
            fill, col = LTEAL, TEAL
        else:
            fill, col = LGRAY, MUTE
        cv.rr(x, 102, x + w, 134, 16, fill=fill)
        cv.text(x + w / 2, 118, n, 16, col, True, "mm")
        x += w + 10

def caption_for(i):
    table = [
        (0, 14, "서버가 한 대면 모든 요청이 그 서버 하나로 갑니다", INK),
        (14, 26, "그 한 대가 고장 나면 → 전부 실패 (단일 장애점)", RED),
        (26, 46, "서버를 두 벌로, 앞에는 로드밸런서 (이중화)", INK),
        (46, 58, "한쪽이 고장 → 알아채기 전 잠깐은 실패가 납니다", RED),
        (58, 70, "알아챈 뒤에는 남은 서버가 계속 처리 → 서비스는 안 멈춤", GOOD),
        (70, 94, "블루그린: 지금은 blue(v1)가 받는 중 — 새 버전은 옆 green에 준비합니다", INK),
        (94, 114, "green에 새 버전(v2)을 다 올립니다 — 사용자는 모릅니다", INK),
        (114, 130, "전환하기 전에 green이 정상인지 먼저 확인합니다 (헬스체크)", INK),
        (130, 142, "설정 한 줄 + reload → 방향만 blue에서 green으로 (끊긴 요청 0건)", TEAL),
        (142, 160, "Nginx: 방향을 정하는 장치 — 서버가 한 줄이면 리버스 프록시", INK),
        (160, 168, "목록에 서버를 한 줄 더 하면 …", WARN),
        (168, 198, "→ 로드밸런서: 여러 서버에 나눠 보냄 (같은 Nginx, 설정만 다름)", TEAL),
        (198, 206, "무상태: 지금까지 대화(약속)는 서버 메모리에 있었습니다", INK),
        (206, G1, "blue에서 약속을 만들었습니다 → blue 메모리에 저장", INK),
        (G1, R1, "방향을 green으로 바꾸니 → 약속이 안 보입니다 (blue 안에는 그대로)", RED),
        (R1, T4B, "blue를 재시작하면 → 약속이 진짜로 사라집니다", RED),
        (T4B, 270, "해결: 기억을 서버 밖의 DB에 둡니다", TEAL),
        (270, G2, "약속이 DB에 저장됩니다", INK),
        (G2, R2, "green으로 전환해도 → 같은 DB를 읽어 약속이 보입니다", GOOD),
        (R2, 320, "blue를 재시작해도 → DB에 그대로 남아 있습니다", GOOD),
        (320, END + 1, "기억을 서버가 아니라 DB가 가지면, 서버는 언제 바뀌어도 됩니다 (무상태)", GOOD),
    ]
    for a, b, t, c in table:
        if a <= i < b:
            return t, c
    return "", INK

def draw_cfg(cv, i):
    if i < T2:
        return
    cv.rr(110, 352, 520, 452, 10, fill=DARK)
    cc = (200, 215, 225)
    cv.text(124, 362, "upstream active_app {", 13, cc, False, "la", True)
    two = ADD <= i < T4A
    if two:
        cv.text(124, 382, "  server blue:8080;", 13, cc if i >= ADD + 30 else AMBER, False, "la", True)
        cv.text(124, 402, "  server green:8080;", 13, cc, False, "la", True)
        cv.text(124, 422, "}", 13, cc, False, "la", True)
        if ADD <= i < ADD + 10:
            cv.text(508, 362, "→ reload", 13, AMBER, True, "ra")
    else:
        tgt, start = single_target(i)
        hl = (i - start) < 10 and i >= F2
        cv.text(124, 382, "  server %s:8080;" % tgt, 13, AMBER if hl else cc, False, "la", True)
        cv.text(124, 402, "}", 13, cc, False, "la", True)
        if hl:
            cv.text(508, 362, "→ reload", 13, AMBER, True, "ra")
        if i >= T4A and (i - start) < 10:
            cv.text(508, 362, "→ reload", 13, AMBER, True, "ra")

def memory_slot(cv, x0, y0, x1, y1, label):
    cv.rr(x0 + 10, y1 - 48, x1 - 10, y1 - 10, 6, fill=LGRAY, outline=LINE, w=1)
    if label:
        cv.text((x0 + x1) / 2, y1 - 29, label, 12, MUTE, False, "mm")

def scene_all():
    frames = []
    spawns = [0, 6, 12, 18] + list(range(T1B, END - 18, 6))
    for i in range(END):
        cv = Cv()
        cv.circ(52, 46, 24, fill=TEAL)
        cv.text(52, 46, "8", 26, WHITE, True, "mm")
        cv.text(92, 18, "무중단 배포, 한눈에 보기", 28, INK, True)
        cv.text(92, 56, "무중단을 이루는 네 가지 조각을 하나씩 더해 가며 본다", 15, MUTE)
        cv.line(40, 94, 960, 94, LINE, 2)
        tracker(cv, i)

        user(cv, UX, UY)
        nginx_on = i >= T1B
        # ---- arrows
        if not nginx_on:
            cv.arrow(UX + 40, UY, BX0 - 4, BCY, LINE, 3)
        else:
            cv.arrow(UX + 40, UY, NX0 - 4, UY, LINE, 3)
            act = active_targets(i)
            for nm, cy in (("blue", BCY), ("green", GCY)):
                if nm in act:
                    colr = BLUE if nm == "blue" else GREEN
                    if nm == "green" and DEAD_G <= i < DETECT_G:
                        colr = RED
                    cv.arrow(NX1, UY, BX0 - 4, cy, colr, 5, 14)
                else:
                    cv.dash(NX1, UY, BX0 - 4, cy, LINE, 2)
        # ---- nginx (점이 상자 안에서는 가려지도록 점을 그린 뒤에 호출한다)
        def draw_nginx():
            if not nginx_on:
                return
            pulse = T3 <= i < T3 + 18
            cv.rr(NX0, NY0, NX1, NY1, 14, fill=LTEAL, outline=AMBER if pulse else TEAL, w=6 if pulse else 4)
            cv.text((NX0 + NX1) / 2, NY0 + 26, "Nginx", 22, TEAL, True, "mm")
            sub = "로드밸런서" if i < T3 else ""
            if sub:
                cv.text((NX0 + NX1) / 2, NY0 + 54, sub, 15, INK, False, "mm")
        if T1B <= i < T1B + 14:
            chip(cv, 210, 205, "+ 로드밸런서, + 서버 한 대", LTEAL, TEAL)
        if T3 <= i < T4A:
            role_lb = i >= ADD + 8
            t = "로드밸런서" if role_lb else "리버스 프록시"
            chip(cv, 262 - (0 if role_lb else 6), 205, t, LTEAL if role_lb else LAMB, TEAL if role_lb else (150, 90, 0))
        # ---- blue box
        if i < 14:
            bs, bt = "active", "단일 장애점"
        elif i < T1B:
            bs, bt = "dead", "고장"
        elif i < T2:
            bs, bt = "active", "정상"
        elif i < F2:
            bs, bt = "active", "v1 · 운영 중"
        elif i < ADD:
            bs, bt = "dim", "v1 · 대기 (롤백용)"
        elif i < T4A:
            bs, bt = "active", "v1"
        else:
            tgt, _ = single_target(i)
            restart1 = R1 <= i < R1 + 10
            restart2 = R2 <= i < R2 + 10
            if restart1 or restart2:
                bs, bt = "warn", "재시작!"
            elif tgt == "blue":
                bs, bt = "active", "v1"
            else:
                bs, bt = "dim", "v1"
        server_box(cv, BX0, BY0, BX1, BY1, "blue", bt, BLUE, bs)
        # ---- green box
        if nginx_on:
            if i < DEAD_G:
                gs, gt = "active", "정상"
            elif i < T2:
                gs, gt = "dead", "고장"
            elif i < 94:
                gs, gt = "dim", "(새 버전 올릴 자리)"
            elif i < 114:
                gs, gt = "dim", "v2 올리는 중…"
            elif i < F2:
                gs, gt = "dim", "v2 준비 완료"
            elif i < ADD:
                gs, gt = "active", "v2 · 운영 중"
            elif i < T4A:
                gs, gt = "active", "v2"
            else:
                tgt, _ = single_target(i)
                gs, gt = ("active", "v2") if tgt == "green" else ("dim", "v2")
            server_box(cv, GX0, GY0, GX1, GY1, "green", gt, GREEN, gs)
            if 94 <= i < 114:
                pr = smooth((i - 94) / 20)
                cv.rr(580, 400, 760, 412, 6, fill=LGRAY, outline=LINE, w=1)
                cv.rr(580, 400, 580 + 180 * pr, 412, 6, fill=GREEN)
            if 114 <= i < F2:
                cv.rr(792, 346, 952, 392, 10, fill=LTEAL, outline=GREEN, w=2)
                cv.text(872, 369, "헬스체크: 정상", 17, GOOD, True, "mm")
        # ---- memory slots (stage 4)
        if i >= T4A:
            if i < T4B:
                bl = "메모리"
                if i >= R1 + 8: bl = "(비어 있음)"
                gl = "(비어 있음)" if i >= G1 + 2 else "메모리"
            else:
                bl = gl = "(상태 없음)"
            memory_slot(cv, BX0, BY0, BX1, BY1, bl if not (T4A + 8 <= i < R1 + 8 and i < T4B) and not (i >= R2 + 12 and i >= T4B) else "")
            memory_slot(cv, GX0, GY0, GX1, GY1, gl if not (i >= G2 + 2 and i >= T4B) else "")
        # ---- DB (stage 4b)
        if i >= T4B:
            cylinder(cv, DBX, 238, 350)
            cv.text(DBX, 362, "Supabase", 12, MUTE, False, "mm")
            touch_b = (270 <= i < 282) or (R2 + 12 <= i < R2 + 24)
            touch_g = (G2 <= i < G2 + 14)
            cv.line(BX1, BCY, DBX - 44, 285, TEAL if touch_b else LINE, 3)
            cv.line(GX1, GCY, DBX - 44, 305, TEAL if touch_g else LINE, 3)
            if i >= 282:
                card(cv, DBCARD[0], DBCARD[1], TEAL, 1.0, 104)
        # ---- config panel
        draw_cfg(cv, i)
        # ---- dots
        succ = fail = 0
        for s0 in spawns:
            p = (i - s0) / 24
            if s0 < T1B:
                if i < T1B and 0 <= p <= 1:
                    x = UX + 40 + (BX0 - 4 - UX - 40) * p
                    y = UY + (BCY - UY) * p
                    if i >= 14 and p > 0.85:
                        xmark(cv, UX + 40 + (BX0 - 4 - UX - 40) * 0.85, UY + (BCY - UY) * 0.85)
                    else:
                        dot(cv, x, y, BLUE if i < 14 else RED)
                continue
            d = dest(s0)
            cy = BCY if d == "blue" else GCY
            pts = [(UX + 40, UY), (NX0, UY), (BX0 - 4, cy)]
            fl = failed_1b(s0)
            if T1B <= s0 < T2 and s0 + 24 <= i:
                if fl: fail += 1
                else: succ += 1
            if fl:
                if 0 <= p <= 0.9:
                    x, y = along(pts, [8, 16], p)
                    dot(cv, x, y, GREEN if i < DEAD_G else RED)
                elif 0.9 < p <= 1.2:
                    x, y = along(pts, [8, 16], 0.9)
                    xmark(cv, x, y)
            elif 0 <= p <= 1:
                x, y = along(pts, [8, 16], p)
                dot(cv, x, y, BLUE if d == "blue" else GREEN)
        if T1B <= i < T2 + 8:
            counter(cv, succ, fail)
        if F2 <= i < T3:
            cv.text(960, 108, "끊긴 요청 0건", 20, GOOD, True, "ra")
        draw_nginx()
        # ---- stage 4a card flight / presence
        if T4A + 8 <= i < T4A + 18:
            q = smooth((i - (T4A + 8)) / 10)
            pts = [(UX + 40, UY), (NX0, UY), (BX0 + 60, BCY), BSLOT]
            x, y = along(pts, [3, 4, 2], q)
            card(cv, x, y)
        elif T4A + 18 <= i < R1:
            card(cv, BSLOT[0], BSLOT[1], AMBER, 1.0, 100)
        elif R1 <= i < R1 + 8:
            a = 1 - (i - R1) / 8
            card(cv, BSLOT[0], BSLOT[1], RED, a, 100)
            xmark(cv, BSLOT[0], BSLOT[1], 12, RED, 4)
        if G1 + 4 <= i < T4B:
            cv.text(670, GY1 + 14, "약속이 안 보임", 15, RED, True, "mm")
        if G1 + 6 <= i < R1:
            cv.text(670, BY1 + 13, "blue 안에는 그대로 있음", 13, MUTE, False, "mm")
        # ---- stage 4b card flight / reads
        if 270 <= i < 282:
            q = smooth((i - 270) / 12)
            pts = [(UX + 40, UY), (NX0, UY), (BX0 + 60, BCY), (DBX - 30, 285), DBCARD]
            x, y = along(pts, [3, 4, 2, 3], q)
            card(cv, x, y)
        if G2 + 2 <= i:
            a = smooth((i - (G2 + 2)) / 8)
            card(cv, GSLOT[0], GSLOT[1], TEAL, a, 100)
            if i < R2:
                cv.text(670, GY1 + 14, "약속이 보임", 15, GOOD, True, "mm")
        if R2 + 12 <= i:
            a = smooth((i - (R2 + 12)) / 8)
            card(cv, BSLOT[0], BSLOT[1], TEAL, a, 100)
        # ---- caption
        t, c = caption_for(i)
        caption(cv, t, c)
        frames.append(cv.done())
    return frames

if __name__ == "__main__":
    fr = scene_all()
    save("00_통합.gif", fr)
    pv = os.path.join(OUT, "preview")
    for idx in (10, 20, 40, 52, 66, 100, 120, 136, 150, 190, 215, 232, 245, 262, 285, 296, 312, 330):
        fr[idx].save(os.path.join(pv, "all_%03d.png" % idx))
