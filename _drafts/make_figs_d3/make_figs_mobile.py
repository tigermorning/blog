"""노션 보고서(모바일 앱 1일차: Expo로 휴대폰 앱 만들기)용 움직이는 그림 5장 + 요약 포스터.
make_gifs.py 의 팔레트·그리기 도구를 그대로 쓴다.  색 규칙: 웹·개발 = 청록(BLUE), 앱·빌드 = 앰버(AMBER), 그 밖 = 회색.
사용: python make_figs_mobile.py <출력 폴더> [1~5|poster|all]
"""
import sys
import os

OUT_DIR = sys.argv[1]
ONLY = sys.argv[2] if len(sys.argv) > 2 else "all"
sys.argv = [sys.argv[0], OUT_DIR]
from make_gifs import *  # noqa: F401,F403  W, H, Cv, 색, header, caption, save, smooth, mix, font
from PIL import Image  # noqa: F401


def lerp(a, b, t):
    return a + (b - a) * t


def mv(i, a, d, x0, x1):
    """프레임 a~a+d 사이에 x0→x1 로 움직인다. 구간 밖이면 None"""
    p = (i - a) / d
    if p < 0 or p >= 1:
        return None
    return lerp(x0, x1, smooth(p))


def box(cv, x0, y0, x1, y1, title, sub="", state="idle", tsize=20):
    fill, edge, tc = WHITE, LINE, INK
    if state == "web":
        fill, edge = LBLUE, BLUE
    elif state == "app":
        fill, edge = LAMB, AMBER
    elif state == "dim":
        fill, edge, tc = LGRAY, LINE, MUTE
    elif state == "bad":
        fill, edge, tc = LRED, RED, (150, 40, 36)
    cv.rr(x0, y0, x1, y1, 14, fill=fill, outline=edge, w=3 if state in ("web", "app", "bad") else 2)
    cy = (y0 + y1) / 2 - (10 if sub else 0)
    cv.fit((x0 + x1) / 2, cy, title, tsize, (x1 - x0) - 16, tc, True, "mm")
    if sub:
        cv.fit((x0 + x1) / 2, cy + 26, sub, 15, (x1 - x0) - 14, MUTE if state != "bad" else (150, 40, 36), False, "mm")


def pill(cv, cx, cy, t, fill, color, sz=16):
    w = cv.d.textlength(t, font=font(sz, True)) / S + 26
    cv.rr(cx - w / 2, cy - 15, cx + w / 2, cy + 15, 15, fill=fill)
    cv.text(cx, cy, t, sz, color, True, "mm")


def packet(cv, x, y, t, fill, edge, color):
    w = cv.d.textlength(t, font=font(15, True)) / S + 22
    cv.rr(x - w / 2, y - 14, x + w / 2, y + 14, 8, fill=fill, outline=edge, w=2)
    cv.text(x, y, t, 15, color, True, "mm")


def phone(cv, x, y, w, h, fill=WHITE, edge=INK):
    cv.rr(x, y, x + w, y + h, 24, fill=fill, outline=edge, w=3)
    cv.rr(x + w / 2 - 22, y + 8, x + w / 2 + 22, y + 14, 3, fill=edge)


# ---------------------------------------------------------------- 그림 1. 웹은 열 때마다 받고 앱은 이미 들어 있다
def scene1():
    frames = []
    N = 88
    for i in range(N):
        cv = Cv()
        header(cv, 1, "웹은 열 때마다 받고, 앱은 이미 들어 있다", "화면 코드가 어디에 있느냐가 웹과 앱의 가장 큰 차이")
        app_phase = i >= 42
        pill(cv, 120, 124, "웹 (칠판 수업)", LBLUE, GOOD)
        pill(cv, 130, 276, "앱 (가방 속 교과서)", LAMB, WARN)
        # --- 웹 줄
        st_web = "dim" if app_phase else "web"
        box(cv, 60, 140, 250, 240, "브라우저(학생)", "받은 글대로 화면을 그려요", st_web)
        box(cv, 430, 140, 640, 186, "웹 서버(선생님)", "", st_web, 18)
        box(cv, 430, 196, 640, 242, "백엔드(사무실)", "", "dim" if app_phase else "idle", 18)
        cv.dash(430, 163, 252, 163, BLUE if not app_phase else LINE, 2)
        cv.dash(430, 219, 252, 219, LINE, 2)
        # --- 앱 줄
        st_app = "app" if app_phase else "dim"
        box(cv, 60, 292, 250, 392, "폰 안의 앱 파일", "화면 코드가 미리 들어 있어요", st_app)
        box(cv, 430, 292, 640, 338, "웹 서버", "", "dim", 18)
        cv.text(660, 315, "화면 코드는 안 받아요", 16, MUTE, True, "lm")
        box(cv, 430, 348, 640, 394, "백엔드(사무실)", "", "idle" if app_phase else "dim", 18)
        cv.dash(430, 371, 252, 371, AMBER if app_phase else LINE, 2)
        # --- 움직이는 조각
        for a in (4, 22):
            x = mv(i, a, 14, 430, 250)
            if x is not None:
                packet(cv, x, 163, "화면 코드", LBLUE, BLUE, GOOD)
        for a in (12, 30):
            x = mv(i, a, 14, 430, 250)
            if x is not None:
                packet(cv, x, 219, "데이터", WHITE, LINE, INK)
        for a in (46, 62):
            x = mv(i, a, 14, 430, 250)
            if x is not None:
                packet(cv, x, 371, "데이터", WHITE, AMBER, WARN)
        if 22 <= i < 42:
            pill(cv, 700, 163, "다시 열면 또 받아요", LBLUE, GOOD)
        if i < 20:
            cap = "웹: 주소를 열면 서버에서 화면 코드를 받아 와요"
        elif i < 42:
            cap = "다시 열면 또 받아요. 서버만 고치면 모든 사용자가 새 화면을 봐요"
        elif i < 62:
            cap = "앱: 화면 코드는 이미 폰 안의 앱 파일에 들어 있어요"
        else:
            cap = "움직이는 것은 데이터뿐이에요. 백엔드는 웹과 같은 것을 써요"
        caption(cv, cap, GOOD if i < 42 else WARN)
        frames.append(cv.done())
    return frames


# ---------------------------------------------------------------- 그림 2. 화면을 고치면 웹은 모두, 앱은 업데이트한 폰만
def scene2():
    frames = []
    N = 84

    def flip(i, a, d):
        return smooth((i - a) / d)

    for i in range(N):
        cv = Cv()
        header(cv, 2, "화면을 고쳤을 때, 웹은 모두 바뀌고 앱은 옛 버전이 남는다", "같은 수정을 내보냈을 때 사용자 폰에서 일어나는 일")
        cv.line(500, 108, 500, 452, LINE, 2)
        pill(cv, 270, 124, "웹 (칠판 수업)", LBLUE, GOOD)
        pill(cv, 740, 124, "앱 (가방 속 교과서)", LAMB, WARN)
        # 서버/스토어 상자
        newv = flip(i, 14, 14)
        w_fill = mix(WHITE, LBLUE, newv)
        a_fill = mix(WHITE, LAMB, newv)
        cv.rr(130, 150, 410, 206, 14, fill=w_fill, outline=BLUE if newv > 0.5 else LINE, w=3)
        cv.fit(270, 178, "웹 서버: 새 글로 교체" if newv > 0.5 else "웹 서버: 화면 1판", 19, 250, INK, True, "mm")
        cv.rr(600, 150, 880, 206, 14, fill=a_fill, outline=AMBER if newv > 0.5 else LINE, w=3)
        cv.fit(740, 178, "앱 가게: 새 책(2판)" if newv > 0.5 else "앱 가게: 책(1판)", 19, 250, INK, True, "mm")
        # 폰 3대
        for k, cx in enumerate((190, 270, 350)):
            t = flip(i, 30 + k * 2, 12)
            body = mix(LGRAY, LBLUE, t)
            phone(cv, cx - 34, 250, 68, 130, body, BLUE if t > 0.5 else MUTE)
            cv.text(cx, 330, "2판" if t > 0.5 else "1판", 22, GOOD if t > 0.5 else MUTE, True, "mm")
        # 앱 폰 3대: 첫 번째만 업데이트
        for k, cx in enumerate((660, 740, 820)):
            if k == 0:
                t = flip(i, 56, 10)
            else:
                t = 0
            body = mix(LGRAY, LAMB, t)
            phone(cv, cx - 34, 250, 68, 130, body, AMBER if t > 0.5 else MUTE)
            cv.text(cx, 330, "2판" if t > 0.5 else "1판", 22, WARN if t > 0.5 else MUTE, True, "mm")
        for k, cx in enumerate((190, 270, 350)):
            cv.text(cx, 398, "사용자 %d" % (k + 1), 14, MUTE, True, "mm")
        for k, cx in enumerate((660, 740, 820)):
            cv.text(cx, 398, "사용자 %d" % (k + 1), 14, MUTE, True, "mm")
        if i >= 30 and i < 56:
            pill(cv, 740, 430, "아직 아무도 업데이트 안 함", LGRAY, MUTE, 15)
        if i >= 56:
            pill(cv, 740, 430, "업데이트한 사용자 1명만 2판", LAMB, WARN, 15)
        if i >= 30:
            pill(cv, 270, 430, "열 때마다 받아서 모두 2판", LBLUE, GOOD, 15)
        if i < 14:
            cap = "모두 1판을 쓰고 있어요"
        elif i < 44:
            cap = "새 화면을 내보냈어요. 웹은 서버에 올리는 순간 모든 사용자가 새 화면을 봐요"
        elif i < 56:
            cap = "앱은 앱 파일 안에 화면 코드가 있어서 폰에 있는 1판은 그대로예요"
        else:
            cap = "사용자가 업데이트해야 바뀌고, 안 한 폰에는 옛 앱이 계속 남아요"
        caption(cv, cap, GOOD if i < 44 else WARN)
        frames.append(cv.done())
    return frames


# ---------------------------------------------------------------- 그림 3. 빌드: 소스 코드가 앱 파일이 되기까지
def scene3():
    frames = []
    steps = [("① 코드 받기", "소스 코드 폴더", "소스 코드", "gray"),
             ("② 패키지 설치", "필요한 라이브러리", "소스 + 라이브러리", "gray"),
             ("③ 번들로 묶기", "내 코드를 파일 하나로", "번들 하나", "gray"),
             ("④ 컴파일", "폰이 읽는 숫자 말로 번역", "번역된 코드", "amber"),
             ("⑤ 서명", "개발자 키로 도장", "서명된 앱 파일", "amber")]
    caps = ["내 소스 코드로 시작해요. 폰은 이 폴더를 그대로 설치하지 못해요",
            "코드가 쓰는 패키지를 모두 설치해요",
            "내 코드(JavaScript)는 컴파일하지 않고 번들 하나로 묶기만 해요",
            "폰의 CPU가 실행하는 기계어로 바꿔요. 안드로이드는 Android SDK, iOS는 Xcode(맥)가 필요해요",
            "개발자 키로 서명해요. 서명이 없으면 폰과 스토어가 설치를 거부해요"]
    per = 14
    N = per * 5 + 24
    xs = [40 + k * 185 for k in range(5)]
    for i in range(N):
        cv = Cv()
        header(cv, 3, "빌드: 소스 코드가 앱 파일이 되기까지", "사람이 쓴 코드를 폰이 설치하고 실행할 수 있는 파일로 만드는 다섯 단계")
        cur = min(4, i // per)
        for k, (t, sub, tok, kind) in enumerate(steps):
            on = i >= k * per and i < N
            reached = i >= k * per
            state = "idle"
            if reached:
                state = "app" if kind == "amber" else "web"
            if k == cur and i < per * 5:
                pass
            box(cv, xs[k], 128, xs[k] + 160, 228, t, sub, state, 19)
            if k < 4:
                cv.arrow(xs[k] + 162, 178, xs[k + 1] - 4, 178, LINE if i < (k + 1) * per else (AMBER if kind == "amber" else BLUE), 3, 10)
        # 움직이는 토큰
        pos = min(i, per * 5 - 1) / per
        k0 = int(pos)
        k1 = min(4, k0 + 1)
        f = smooth(pos - k0) if k0 < 4 else 1
        cx = lerp(xs[k0] + 80, xs[k1] + 80, f)
        cur_k = min(4, int(round(pos - 0.2)))
        label = steps[min(4, k0 if f < 0.5 else k1)][2]
        kind = steps[min(4, k0 if f < 0.5 else k1)][3]
        packet(cv, cx, 268, label, LAMB if kind == "amber" else LBLUE, AMBER if kind == "amber" else BLUE, WARN if kind == "amber" else GOOD)
        cv.line(60, 268, 940, 268, LINE, 1)
        # 단계 아래 메모
        if i >= 3 * per:
            pill(cv, xs[3] + 80, 312, "폰 회사 도구가 필요", LAMB, WARN, 14)
            cv.text(xs[3] + 80, 342, "Android SDK · Xcode(맥)", 14, MUTE, True, "mm")
        if i >= 4 * per:
            pill(cv, xs[4] + 80, 312, "도장(서명) 열쇠", LAMB, WARN, 14)
            cv.text(xs[4] + 80, 342, "Expo 클라우드가 보관", 14, MUTE, True, "mm")
        if i >= 5 * per:
            t = smooth((i - 5 * per) / 8)
            cv.rr(300, 372, 700, 446, 16, fill=mix(WHITE, LAMB, t), outline=AMBER, w=4)
            cv.fit(500, 400, "앱 파일: APK · AAB · IPA", 24, 360, INK, True, "mm")
            cv.fit(500, 428, "폰에 설치하거나 스토어에 올릴 수 있어요", 15, 360, MUTE, False, "mm")
        cap = caps[cur] if i < per * 5 else "완성: 이 파일 안에 내 코드가 고정돼요. 코드를 고치면 다시 빌드해야 해요"
        caption(cv, cap, WARN if (cur >= 3 or i >= per * 5) else GOOD)
        frames.append(cv.done())
    return frames


# ---------------------------------------------------------------- 그림 4. 저장하면 폰 화면이 바뀐다
def scene4():
    frames = []
    N = 86
    old = "첫 메시지를 보내 보세요."
    new = "오늘 한 만큼만 찍어요."
    for i in range(N):
        cv = Cv()
        header(cv, 4, "저장하면 폰 화면이 바뀐다", "개발할 때는 노트북이 코드를 보내고, 폰의 Expo Go가 실행한다")
        # 노트북
        cv.rr(40, 130, 330, 392, 14, fill=DARK, outline=MUTE, w=3)
        cv.text(60, 148, "src/app/index.tsx", 14, AMBER, True, "la", True)
        for k in range(4):
            cv.rr(60, 184 + k * 26, 60 + (150 if k % 2 == 0 else 110), 196 + k * 26, 5, fill=(78, 72, 66))
        typed = int(len(new) * smooth((i - 10) / 14)) if i >= 10 else 0
        show = old if typed == 0 else (new[:typed] + ("" if typed >= len(new) else "▌"))
        cv.rr(52, 296, 318, 330, 6, fill=(70, 64, 58) if i < 24 else (40, 96, 88))
        cv.fit(185, 313, show, 17, 250, WHITE, True, "mm")
        cv.rr(40, 392, 330, 408, 6, fill=(60, 56, 52))
        # 저장 칩
        if 22 <= i < 36:
            pill(cv, 185, 112, "저장 (Ctrl+S)", LAMB, WARN, 15)
        # Metro
        glow = smooth((i - 26) / 8) * (1 - smooth((i - 44) / 8))
        box(cv, 410, 200, 600, 300, "Metro", "번들로 묶어요", "web" if glow > 0.3 else "idle", 22)
        cv.text(505, 322, "개발 서버(노트북 안)", 14, MUTE, True, "mm")
        cv.arrow(332, 250, 408, 250, BLUE if i >= 24 else LINE, 3, 10)
        x = mv(i, 24, 8, 340, 400)
        if x is not None:
            packet(cv, x, 228, "저장됨", LBLUE, BLUE, GOOD)
        # 폰
        phone(cv, 720, 118, 200, 300, WHITE, INK)
        flip = smooth((i - 52) / 6)
        cv.rr(732, 150, 908, 404, 10, fill=mix(LGRAY, LBLUE, flip))
        cv.text(820, 190, "Expo Go", 14, MUTE, True, "mm")
        cv.fit(820, 276, new if flip > 0.5 else old, 17, 150, INK, True, "mm")
        if 52 <= i < 64:
            cv.circ(820, 276, lerp(30, 86, smooth((i - 52) / 12)), outline=BLUE, w=3)
        # 와이파이로 전달
        cv.dash(602, 250, 718, 250, BLUE if 34 <= i < 56 else LINE, 3)
        x = mv(i, 36, 16, 610, 706)
        if x is not None:
            packet(cv, x, 228, "바뀐 번들", LBLUE, BLUE, GOOD)
        if 34 <= i < 56:
            pill(cv, 660, 190, "와이파이", LBLUE, GOOD, 14)
        if i >= 58:
            pill(cv, 820, 436, "다시 설치 없이 몇 초 안에", LBLUE, GOOD, 14)
        caps = [(0, "화면에 «첫 메시지를 보내 보세요.»가 보여요. 코드의 이 문구를 바꿔 볼게요"),
                (10, "① 노트북에서 문구를 고치고 저장해요"),
                (26, "② Metro(개발 서버)가 바뀐 코드를 번들로 묶어요"),
                (36, "③ 와이파이로 폰의 Expo Go에 보내요"),
                (52, "④ Expo Go가 화면을 새로 그려요. 앱을 다시 만들거나 설치하지 않았어요")]
        cap = [c for s, c in caps if i >= s][-1]
        caption(cv, cap, GOOD)
        frames.append(cv.done())
    return frames


# ---------------------------------------------------------------- 그림 5. Expo Go로 연 앱 vs 설치한 앱
def scene5():
    frames = []
    N = 92
    for i in range(N):
        cv = Cv()
        header(cv, 5, "같은 수정, 다른 결과: Expo Go vs 설치한 앱", "코드를 1판에서 2판으로 고쳤을 때 두 폰에서 일어나는 일")
        # 노트북 코드
        v2 = i >= 14
        cv.rr(360, 108, 640, 158, 12, fill=DARK, outline=MUTE, w=3)
        cv.fit(500, 133, "코드 수정: 2판으로 변경" if v2 else "코드: 1판", 18, 250, AMBER if v2 else WHITE, True, "mm")
        # 두 폰
        pill(cv, 200, 190, "Expo Go로 연 앱", LBLUE, GOOD)
        pill(cv, 800, 190, "설치한 앱 (빌드한 파일)", LAMB, WARN)
        flipL = smooth((i - 36) / 8)
        phone(cv, 110, 215, 180, 235, mix(LGRAY, LBLUE, flipL), BLUE)
        cv.text(200, 332, "2판" if flipL > 0.5 else "1판", 34, GOOD if flipL > 0.5 else MUTE, True, "mm")
        cv.text(200, 372, "앱 화면", 14, MUTE, True, "mm")
        phone(cv, 710, 215, 180, 235, LAMB, AMBER)
        cv.text(800, 332, "1판", 34, WARN, True, "mm")
        cv.text(800, 372, "앱 파일 안의 옛 코드", 14, MUTE, True, "mm")
        # 왼쪽 연결: 번들이 전달됨
        cv.dash(362, 158, 262, 232, BLUE if i >= 24 else LINE, 3)
        x = mv(i, 26, 14, 360, 270)
        if x is not None:
            y = lerp(160, 228, smooth((i - 26) / 14))
            packet(cv, x, y, "번들", LBLUE, BLUE, GOOD)
        # 오른쪽 연결: 끊김
        cv.dash(638, 158, 738, 232, LINE, 3)
        if i >= 26:
            xx, yy = lerp(638, 700, 0.5), lerp(158, 232, 0.5)
            xmark(cv, xx, yy, 11, RED, 4)
        if i >= 46:
            pill(cv, 800, 412, "다시 빌드해야 바뀌어요", LRED, (150, 40, 36), 15)
        if i >= 70:
            t = smooth((i - 70) / 10)
            phone(cv, 710, 215, 180, 235, mix(LAMB, LBLUE, t), AMBER)
            cv.text(800, 332, "2판" if t > 0.5 else "1판", 34, GOOD if t > 0.5 else WARN, True, "mm")
            cv.text(800, 372, "새로 빌드한 앱 파일", 14, MUTE, True, "mm")
            pill(cv, 800, 412, "빌드 횟수 1회 사용", LAMB, WARN, 15)
        if i < 14:
            cap = "두 폰 모두 1판이에요. 이제 노트북에서 코드를 2판으로 고쳐요"
        elif i < 36:
            cap = "Expo Go는 개발 서버에서 바뀐 번들을 받아 와요"
        elif i < 70:
            cap = "Expo Go는 곧바로 2판이 돼요. 설치한 앱은 앱 파일 안의 코드가 고정돼서 그대로예요"
        else:
            cap = "설치한 앱에 반영하려면 다시 빌드해서 새 앱 파일로 바꿔야 하고, 그때마다 빌드 횟수를 써요"
        caption(cv, cap, GOOD if i < 70 else WARN)
        frames.append(cv.done())
    return frames


# ---------------------------------------------------------------- 요약 포스터 (한 장)
def poster():
    cv = Cv()
    cv.text(500, 38, "오늘의 세 가지 질문", 34, INK, True, "mm")
    cv.text(500, 72, "비유: 웹은 «칠판 수업», 앱은 «가방 속 교과서»", 18, MUTE, False, "mm")
    cv.line(40, 92, 960, 92, LINE, 2)
    cols = [("1  웹과 앱은 어디가 다른가", BLUE, LBLUE), ("2  앱은 왜 빌드가 필요한가", AMBER, LAMB),
            ("3  개발 중에는 어떻게 도는가", BLUE, LBLUE)]
    for k, (title, edge, fill) in enumerate(cols):
        x0 = 40 + k * 310
        cv.rr(x0, 108, x0 + 290, 448, 18, fill=fill, outline=edge, w=4)
        cv.fit(x0 + 145, 138, title, 21, 266, INK, True, "mm")
        cv.line(x0 + 20, 160, x0 + 270, 160, edge, 2)
    # 1. 칠판 vs 교과서
    x0 = 40
    box(cv, x0 + 20, 180, x0 + 130, 228, "선생님", "웹 서버", "web", 18)
    box(cv, x0 + 160, 180, x0 + 270, 228, "학생", "브라우저", "web", 18)
    cv.arrow(x0 + 130, 204, x0 + 160, 204, BLUE)
    cv.fit(x0 + 145, 250, "열 때마다 칠판에 새로 적어 줘요", 15, 262, GOOD, True, "mm")
    box(cv, x0 + 70, 280, x0 + 220, 336, "가방 속 교과서", "화면 코드가 이미 안에", "app", 17)
    cv.fit(x0 + 145, 360, "설치할 때 한 번 들어와요", 15, 262, WARN, True, "mm")
    cv.fit(x0 + 145, 408, "→ 고치면 앱은 새 책을 받아야 해요", 16, 266, WARN, True, "mm")
    # 2. 원고 -> 교과서
    x0 = 350
    for n, (t, st) in enumerate([("원고", "idle"), ("번역", "app"), ("도장", "app")]):
        bx = x0 + 18 + n * 92
        box(cv, bx, 190, bx + 78, 236, t, "", st, 18)
        if n < 2:
            cv.arrow(bx + 78, 213, bx + 92, 213, AMBER)
    cv.fit(x0 + 145, 262, "소스 코드 → 폰이 읽는 말로 번역", 15, 262, INK, True, "mm")
    cv.fit(x0 + 145, 284, "→ 검정 도장(서명)을 찍어요", 15, 262, INK, True, "mm")
    box(cv, x0 + 70, 306, x0 + 220, 362, "앱 파일", "설치할 수 있는 한 권", "app", 18)
    cv.fit(x0 + 145, 408, "→ 이 과정이 «빌드»예요", 16, 266, WARN, True, "mm")
    # 3. 노트북 -> 와이파이 -> 폰
    x0 = 660
    box(cv, x0 + 15, 190, x0 + 105, 250, "노트북", "고치고 저장", "web", 17)
    box(cv, x0 + 185, 190, x0 + 275, 250, "폰", "Expo Go", "web", 17)
    cv.arrow(x0 + 105, 220, x0 + 185, 220, BLUE)
    cv.fit(x0 + 145, 200, "와이파이", 14, 80, GOOD, True, "mm")
    cv.fit(x0 + 145, 290, "고친 코드만 보내 주면", 16, 262, INK, True, "mm")
    cv.fit(x0 + 145, 316, "폰이 바로 화면을 새로 그려요", 16, 262, INK, True, "mm")
    cv.fit(x0 + 145, 362, "(시험 인쇄본을 읽는 기계)", 15, 262, MUTE, True, "mm")
    cv.fit(x0 + 145, 408, "→ 저장하면 폰이 바로 바뀌어요", 16, 266, GOOD, True, "mm")
    cv.rr(40, 466, 960, 528, 14, fill=WHITE, outline=LINE, w=2)
    cv.fit(500, 497, "내 실습: 루틴 도장(도장 3칸 + 진동 + 폰 저장) — 껐다 켜도 도장이 남았어요", 20, 880, INK, True, "mm")
    im = cv.done()
    path = os.path.join(OUT_DIR, "C1-요약포스터.png")
    im.save(path)
    print("C1-요약포스터.png", os.path.getsize(path) // 1024, "KB")


def seqfig():
    cv = Cv()
    cv.text(500, 30, "앱이 켜질 때 백엔드와 주고받는 순서", 28, INK, True, "mm")
    xs = {"앱": 150, "백엔드": 500, "로그인 서비스(Supabase)": 850}
    for t, x in xs.items():
        box(cv, x - 110, 52, x + 110, 94, t, "", "app" if t == "앱" else "web", 18)
        cv.line(x, 94, x, 548, LINE, 2)
    L = "로그인 서비스(Supabase)"
    rows = [("앱", "백엔드", "① 설정을 알려 주세요  (/api/config)", BLUE, 1),
            ("백엔드", "앱", "로그인 서비스 주소 · 공개용 열쇠 · 캐릭터 선택지", GOOD, 1),
            ("앱", L, "② 게스트로 로그인할래요  (익명 로그인)", BLUE, 1),
            (L, "앱", "③ 토큰(«이 번호의 사람»이라는 증표) — 폰 안에 저장", GOOD, 1),
            ("앱", "백엔드", "④ 토큰 + 내 정보·캐릭터·지난 대화 주세요", BLUE, 1),
            ("백엔드", L, "이 토큰, 누구 건가요?", BLUE, 1),
            ("백엔드", "앱", "그 사람의 데이터만 돌려줘요", GOOD, 1),
            ("앱", "백엔드", "⑤ 메시지 보낼게요  (/api/chat)", BLUE, 1),
            ("백엔드", "앱", "조각으로 이어서: 글자 조각(delta) → 약속 알림(reminder)|→ 기억 정리(memory) → 끝(done)", GOOD, 2)]
    for n, (a, b, t, c, nl) in enumerate(rows):
        y = 132 + n * 46
        cv.arrow(xs[a], y, xs[b], y, c)
        mx = (xs[a] + xs[b]) / 2
        mw = abs(xs[a] - xs[b]) - 16
        if nl == 2:
            l1, l2 = t.split("|")
            cv.fit(mx, y - 30, l1, 14, mw, INK, True, "mm")
            cv.fit(mx, y - 14, l2, 14, mw, INK, True, "mm")
        else:
            cv.fit(mx, y - 14, t, 14, mw, INK, True, "mm")
    im = cv.done()
    path = os.path.join(OUT_DIR, "D2-앱과백엔드순서.png")
    im.save(path)
    print("D2-앱과백엔드순서.png", os.path.getsize(path) // 1024, "KB")


JOBS = {"1": ("A1-웹은받고앱은들어있다.gif", scene1), "2": ("A2-고쳤을때.gif", scene2),
        "3": ("A3-빌드컨베이어.gif", scene3), "4": ("A4-저장하면폰이바뀐다.gif", scene4),
        "5": ("A5-ExpoGo와설치한앱.gif", scene5)}

for k, (nm, fn) in JOBS.items():
    if ONLY in ("all", k):
        save(nm, fn())
if ONLY in ("all", "poster"):
    poster()
if ONLY in ("all", "seq"):
    seqfig()
