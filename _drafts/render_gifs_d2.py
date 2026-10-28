# SVG 모션 → GIF: 헤드리스 Chrome으로 시간 T의 프레임을 찍고 ffmpeg로 GIF를 만든다.
# 실행: python render_gifs_d2.py  → notion-figs-d2/gif/figN-*.gif
import os, re, subprocess, sys, shutil, tempfile
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "notion-figs-d2")
OUT = os.path.join(SRC, "gif")
TMP = os.path.join(tempfile.gettempdir(), "d2frames")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
FFMPEG = shutil.which("ffmpeg") or r"C:\Users\Aiffel\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin\ffmpeg.exe"
W = 1000  # GIF 가로(px)

# (파일, 반복 길이 L초, fps, march 주기 덮어쓰기)
FIGS = [
    ("fig1-library", 7.2, 10, None),
    ("fig2-where", 0.9, 20, None),
    ("fig3-tag-digest", 6.0, 10, None),
    ("fig4-chain", 7.5, 10, ".75s"),
    ("fig5-promote", 5.0, 10, None),
    ("fig6-revisions", 9.0, 10, None),
    ("fig7-cleanup", 9.0, 10, None),
    ("fig8-size", 6.0, 10, None),
    ("fig4-1-names", 6.0, 10, None),
    ("fig4-2-screen", 7.5, 10, ".75s"),
]

def frame_html(svg_text, T_ms, w, h, march):
    svg_text = re.sub(r'<svg ([^>]*?)width="\d+" height="\d+"', rf'<svg \1width="{w}" height="{h}" style="display:block"', svg_text, count=1)
    if march:
        svg_text = svg_text.replace("animation: march .9s linear infinite", f"animation: march {march} linear infinite")
    return f"""<!doctype html><meta charset="utf-8"><body style="margin:0;background:#fffdf9">{svg_text}
<script>document.getAnimations().forEach(a=>{{a.pause();a.currentTime={T_ms};}});</script></body>"""

def shoot(args):
    name, idx, T_ms, w, h, svg_text, march = args
    d = os.path.join(TMP, name)
    html = os.path.join(d, f"f{idx:03d}.html")
    png = os.path.join(d, f"f{idx:03d}.png")
    with open(html, "w", encoding="utf-8") as f:
        f.write(frame_html(svg_text, T_ms, w, h, march))
    ud = os.path.join(d, f"ud{idx % 6}")
    url = "file:///" + html.replace("\\", "/")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={w},{h}",
                    f"--user-data-dir={ud}-{idx}", f"--screenshot={png}", url],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=150)
    shutil.rmtree(f"{ud}-{idx}", ignore_errors=True)
    return os.path.exists(png)

def main(only=None):
    os.makedirs(OUT, exist_ok=True)
    for name, L, fps, march in FIGS:
        if only and name not in only:
            continue
        svg_text = open(os.path.join(SRC, name + ".svg"), encoding="utf-8").read()
        vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', svg_text)
        vw, vh = int(vb.group(1)), int(vb.group(2))
        w = 1140
        h = round(w * vh / vw)
        d = os.path.join(TMP, name)
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d, exist_ok=True)
        n = int(round(L * fps))
        jobs = [(name, i, 20000 + int(i * 1000 / fps), w, h, svg_text, march) for i in range(n)]
        with ThreadPoolExecutor(max_workers=3) as ex:
            ok = list(ex.map(shoot, jobs))
        print(f"{name}: 프레임 {sum(ok)}/{n} 완료 ({w}x{h})", flush=True)
        if sum(ok) != n:
            print("  실패 프레임이 있어 건너뜀", flush=True)
            continue
        pal = os.path.join(d, "pal.png")
        pat = os.path.join(d, "f%03d.png")
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-framerate", str(fps), "-i", pat,
                        "-vf", f"scale={W}:-1:flags=lanczos,palettegen=stats_mode=diff", pal], check=True)
        gif = os.path.join(OUT, name + ".gif")
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-framerate", str(fps), "-i", pat, "-i", pal,
                        "-lavfi", f"scale={W}:-1:flags=lanczos[x];[x][1:v]paletteuse=dither=bayer:bayer_scale=5",
                        "-loop", "0", gif], check=True)
        print(f"  → {gif} {os.path.getsize(gif)//1024}KB", flush=True)

if __name__ == "__main__":
    main(sys.argv[1:] or None)
