#!/usr/bin/env python3
"""Render 1080x1920 animated Instagram story clips with Malayalam text.

usage: story_video.py FONT_DIR OUT_DIR
"""
import math
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, FPS = 1080, 1920, 30
FONT_DIR, OUT = Path(sys.argv[1]), Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)
BOLD = str(FONT_DIR / "manjari700.ttf")
REG = str(FONT_DIR / "ml400.ttf")
HANDLE = "@manifestora_ai"
rng = np.random.default_rng(7)


def font(path, size):
    return ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.RAQM)


def gradient(stops):
    """stops: list of (y_fraction, (r,g,b)) -> HxWx3 float array."""
    ys = np.linspace(0, 1, H)
    col = np.zeros((H, 3))
    fr = [s[0] for s in stops]
    for c in range(3):
        col[:, c] = np.interp(ys, fr, [s[1][c] for s in stops])
    return np.repeat(col[:, None, :], W, axis=1)


def mountains(seed, base_y, amp, color, alpha=255):
    r = np.random.default_rng(seed)
    img = Image.new("RGBA", (W + 200, H), (0, 0, 0, 0))
    pts, x = [], 0
    y = base_y
    while x <= W + 200:
        y = base_y - amp * (0.5 + 0.5 * math.sin(x / (180 + seed * 7))) - r.uniform(0, amp * 0.6)
        pts.append((x, y))
        x += r.integers(40, 110)
    pts += [(W + 200, H), (0, H)]
    ImageDraw.Draw(img).polygon(pts, fill=color + (alpha,))
    return img


def stars(n):
    return [(rng.uniform(0, W), rng.uniform(0, H * 0.62), rng.uniform(1.2, 3.4),
             rng.uniform(0, 2 * math.pi), rng.uniform(1.5, 4)) for _ in range(n)]


def wrap(draw, text, f, maxw):
    lines, cur = [], ""
    for word in text.split(" "):
        t = (cur + " " + word).strip()
        if draw.textlength(t, font=f) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


def text_layer(blocks):
    """blocks: list of (text, fontpath, size, color, y_center, maxw). Returns RGBA."""
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    for text, fp, size, color, yc, maxw in blocks:
        f = font(fp, size)
        lines = []
        for para in text.split("\n"):
            lines += wrap(d, para, f, maxw)
        lh = int(size * 1.45)
        y = yc - lh * len(lines) // 2
        for ln in lines:
            tw = d.textlength(ln, font=f)
            d.text(((W - tw) / 2, y), ln, font=f, fill=color)
            y += lh
    shadow = layer.split()[3].filter(ImageFilter.GaussianBlur(10))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sh.putalpha(shadow.point(lambda a: int(a * 0.75)))
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    out.alpha_composite(sh, (0, 6))
    out.alpha_composite(layer)
    return out


def glow(radius, color, strength=1.0):
    s = radius * 4
    g = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    yy, xx = np.mgrid[0:s, 0:s]
    dist = np.sqrt((xx - s / 2) ** 2 + (yy - s / 2) ** 2) / (s / 2)
    a = np.clip(1 - dist, 0, 1) ** 2.2 * 255 * strength
    arr = np.zeros((s, s, 4), np.uint8)
    arr[..., :3] = color
    arr[..., 3] = a.astype(np.uint8)
    return Image.fromarray(arr, "RGBA")


def crescent(r):
    s = r * 2 + 4
    m = Image.new("L", (s, s), 0)
    d = ImageDraw.Draw(m)
    d.ellipse((2, 2, s - 2, s - 2), fill=255)
    d.ellipse((2 + r * 0.55, 2 - r * 0.2, s - 2 + r * 0.55, s - 2 - r * 0.2), fill=0)
    img = Image.new("RGBA", (s, s), (255, 226, 160, 0))
    img.putalpha(m.filter(ImageFilter.GaussianBlur(1)))
    return img


def ease(t):
    return 0.5 - 0.5 * math.cos(math.pi * min(max(t, 0), 1))


def render(name, seconds, scene):
    n = int(seconds * FPS)
    p = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium",
         "-crf", "20", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(OUT / f"{name}.mp4")],
        stdin=subprocess.PIPE)
    for i in range(n):
        frame = scene(i / FPS, seconds)
        p.stdin.write(frame.convert("RGB").tobytes())
        if i == int(n * 0.7):
            frame.convert("RGB").save(OUT / f"{name}.jpg", quality=88)
    p.stdin.close()
    p.wait()
    print("wrote", name)


def fade_in(layer, t, start, dur=0.9):
    a = ease((t - start) / dur)
    if a >= 1:
        return layer
    l = layer.copy()
    l.putalpha(layer.split()[3].point(lambda v: int(v * a)))
    return l


def handle_layer():
    return text_layer([(HANDLE, REG, 34, (255, 236, 200, 200), 1540, 900)])


HL = None


# ---- scene builders -------------------------------------------------------

def night_scene(blocks, moon_xy=(780, 420), text_start=0.6):
    base = Image.fromarray(gradient([(0, (6, 8, 28)), (0.55, (20, 22, 60)),
                                     (0.85, (70, 45, 70)), (1, (120, 70, 60))]).astype(np.uint8)).convert("RGBA")
    far = mountains(3, 1500, 160, (24, 20, 40))
    near = mountains(5, 1720, 200, (10, 8, 18))
    st = stars(170)
    moon = crescent(70)
    mg = glow(110, (255, 210, 140), 0.55)
    txt = text_layer(blocks)

    def scene(t, total):
        img = base.copy()
        d = ImageDraw.Draw(img)
        for x, y, r, ph, sp in st:
            a = 0.45 + 0.55 * (0.5 + 0.5 * math.sin(ph + t * sp))
            c = int(255 * a)
            d.ellipse((x - r, y - r, x + r, y + r), fill=(c, c, int(c * 0.92), 255))
        mx, my = moon_xy[0], moon_xy[1] - t * 6
        img.alpha_composite(mg, (int(mx - mg.width / 2), int(my - mg.height / 2)))
        img.alpha_composite(moon, (int(mx - moon.width / 2), int(my - moon.height / 2)))
        img.alpha_composite(far, (int(-100 + t * 6), 0))
        img.alpha_composite(near, (int(-100 - t * 10), 0))
        img.alpha_composite(fade_in(txt, t, text_start))
        img.alpha_composite(fade_in(HL, t, text_start + 0.6))
        return img
    return scene


def dawn_scene(blocks, warmth=0.0, text_start=0.6, rise=True):
    top = (int(30 + 60 * warmth), int(40 + 40 * warmth), int(90 - 20 * warmth))
    base = Image.fromarray(gradient([(0, top), (0.45, (220, 120, 80)),
                                     (0.68, (250, 175, 90)), (1, (120, 60, 40))]).astype(np.uint8)).convert("RGBA")
    sun_g = glow(260, (255, 200, 110), 0.9)
    m1 = mountains(11, 1380, 140, (150, 80, 70), 220)
    m2 = mountains(13, 1540, 180, (80, 40, 45))
    m3 = mountains(17, 1760, 220, (30, 16, 22))
    mist = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(mist).rectangle((0, 1390, W, 1470), fill=(255, 220, 190, 70))
    mist = mist.filter(ImageFilter.GaussianBlur(40))
    txt = text_layer(blocks)

    def scene(t, total):
        img = base.copy()
        sy = 1300 - (t / total) * 220 if rise else 1130
        d = ImageDraw.Draw(img)
        img.alpha_composite(sun_g, (int(540 - sun_g.width / 2), int(sy - sun_g.height / 2)))
        d.ellipse((540 - 70, sy - 70, 540 + 70, sy + 70), fill=(255, 236, 190, 255))
        img.alpha_composite(m1, (int(-100 + t * 5), 0))
        img.alpha_composite(mist, (int(t * 12) - 40, 0))
        img.alpha_composite(m2, (int(-100 - t * 7), 0))
        img.alpha_composite(m3, (int(-100 + t * 11), 0))
        # soft dark band behind text for legibility
        img.alpha_composite(fade_in(txt, t, text_start))
        img.alpha_composite(fade_in(HL, t, text_start + 0.6))
        return img
    return scene


if __name__ == "__main__":
    HL = handle_layer()
    GOLD, CREAM = (255, 214, 140, 255), (255, 246, 230, 255)
    clips = [
        ("1-open", 5, night_scene([("ഇന്ന് ഒരു ചോദ്യം മാത്രം", BOLD, 92, GOLD, 900, 860)])),
        ("2-question", 6, dawn_scene([("മറ്റുള്ളവർ നിന്നെ വിശ്വസിക്കാൻ\nനീ കാത്തിരിക്കുകയാണോ?", BOLD, 66, CREAM, 720, 900)])),
        ("3-message", 6, dawn_scene([("Trust തുടങ്ങേണ്ടത്\nഉള്ളിൽ നിന്നാണ്.", BOLD, 86, CREAM, 640, 900),
                                     ("നിനക്ക് നിന്നോട് തന്നെ.", BOLD, 70, GOLD, 900, 900)], warmth=0.6)),
        ("4-poll", 8, dawn_scene([("ഇന്ന് നീ നിന്നെ\nവിശ്വസിക്കുന്നുണ്ടോ?", BOLD, 84, CREAM, 560, 900)],
                                 warmth=0.3, rise=False, text_start=0.3)),
        ("5-close", 6, night_scene([("ഇന്ന് 3 തവണ പറയ്:", BOLD, 70, CREAM, 700, 900),
                                    ("\"ഞാൻ എന്നെ\nവിശ്വസിക്കുന്നു.\"", BOLD, 96, GOLD, 940, 900)],
                                   moon_xy=(540, 380))),
    ]
    only = set(sys.argv[3:])
    for name, sec, sc in clips:
        if not only or name in only:
            render(name, sec, sc)
