"""fig-2-배포방식.gif 만 프레임 간격을 늘려 다시 저장한다(그림 내용은 그대로).
사용: python regen_slow_methods.py <출력폴더> [프레임 간격 ms, 기본 200]"""
import os
import sys

from PIL import Image

import make_figs_d3h as h
import make_gifs_p as g

OUT = sys.argv[1]
DUR = int(sys.argv[2]) if len(sys.argv) > 2 else 200

frames = h.fig_methods()
stride = max(1, len(frames) // 14)
sample = Image.new("RGB", (g.W, g.H * len(frames[::stride])))
for k, f in enumerate(frames[::stride]):
    sample.paste(f, (0, k * g.H))
pal = sample.quantize(colors=255, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE)
q = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in frames]
durs = [DUR] * len(frames)
durs[0] = 1200
durs[-1] = 3500
path = os.path.join(OUT, "fig-2-배포방식.gif")
q[0].save(path, save_all=True, append_images=q[1:], duration=durs, loop=0, disposal=1, optimize=False)
print(path, len(frames), "frames", os.path.getsize(path) // 1024, "KB", "총", round(sum(durs) / 1000, 1), "초")
