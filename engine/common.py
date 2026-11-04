# -*- coding: utf-8 -*-
import numpy as np, cv2, math, functools, json, os
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 720, 1280, 30
HERE = os.path.dirname(os.path.abspath(__file__))
A = os.environ.get("EP_ASSETS", os.path.join(HERE, "..", "assets"))
OSWALD = os.path.join(A, "Oswald.ttf")
def _font(cands):
    for c in cands:
        if os.path.exists(c): return c
    raise FileNotFoundError(cands[0])
SANS = _font(["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"])
SANSB = _font(["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"])

def B(c): return (int(c[2]), int(c[1]), int(c[0]))
RED = (228, 30, 60); ORANGE = (255, 138, 40); TEAL = (40, 196, 176); WHITE = (246, 246, 250)
AMBER = (255, 178, 96); INK = (9, 9, 14); LILAC = (170, 150, 255)

def clamp(x, a=0.0, b=1.0): return a if x < a else b if x > b else x
def lerp(a, b, t): return a + (b - a) * t
def ease_out(x): x = clamp(x); return 1 - (1 - x) ** 3
def ease_in(x): x = clamp(x); return x ** 3
def ease_io(x): x = clamp(x); return 3 * x * x - 2 * x ** 3
def back_out(x, s=1.9): x = clamp(x) - 1; return x * x * ((s + 1) * x + s) + 1
def hrand(*a):  # bruit déterministe 0..1
    h = 0
    for v in a: h = (h * 1000003 + int(v * 1000) + 12345) & 0xFFFFFFFF
    h ^= h >> 13; h = (h * 0x5bd1e995) & 0xFFFFFFFF; h ^= h >> 15
    return (h & 0xFFFF) / 65535.0

@functools.lru_cache(None)
def ofont(size, weight=700):
    f = ImageFont.truetype(OSWALD, size)
    try: f.set_variation_by_axes([weight])
    except Exception: pass
    return f
@functools.lru_cache(None)
def sfont(size, bold=False): return ImageFont.truetype(SANSB if bold else SANS, size)

@functools.lru_cache(maxsize=4096)
def tsprite(text, size, color=WHITE, weight=700, stroke=0, scol=(0, 0, 0), track=0, sans=False, bold=False):
    f = sfont(size, bold) if sans else ofont(size, weight)
    asc, desc = f.getmetrics(); pad = stroke + 3
    w = sum(f.getlength(ch) + track for ch in text) if track else f.getlength(text)
    img = Image.new("RGBA", (int(w) + 2 * pad + 2, asc + desc + 2 * pad), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if track:
        x = pad
        for ch in text:
            d.text((x, pad), ch, font=f, fill=tuple(color) + (255,), stroke_width=stroke, stroke_fill=tuple(scol) + (255,))
            x += f.getlength(ch) + track
    else:
        d.text((pad, pad), text, font=f, fill=tuple(color) + (255,), stroke_width=stroke, stroke_fill=tuple(scol) + (255,))
    return np.ascontiguousarray(np.asarray(img)[:, :, [2, 1, 0, 3]])

def blit(dst, spr, x, y, alpha=1.0):
    x = int(round(x)); y = int(round(y))
    h, w = spr.shape[:2]
    x0 = max(x, 0); y0 = max(y, 0); x1 = min(x + w, W); y1 = min(y + h, H)
    if x1 <= x0 or y1 <= y0 or alpha <= 0: return
    alpha = min(alpha, 1.0)
    s = spr[y0 - y:y1 - y, x0 - x:x1 - x]
    a = s[..., 3:4].astype(np.float32) * (alpha / 255.0)
    roi = dst[y0:y1, x0:x1]
    roi[:] = (roi * (1.0 - a) + s[..., :3] * a).astype(np.uint8)

def blit_c(dst, spr, cx, cy, alpha=1.0, scale=1.0):
    if abs(scale - 1.0) > 1e-3:
        spr = cv2.resize(spr, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA if scale < 1 else cv2.INTER_LINEAR)
    h, w = spr.shape[:2]
    blit(dst, spr, cx - w / 2, cy - h / 2, alpha)

@functools.lru_cache(None)
def vgrad(top, bot):
    t = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    c = np.array(B(top), np.float32) * (1 - t) + np.array(B(bot), np.float32) * t
    return np.ascontiguousarray(np.repeat(c, W, axis=1).astype(np.uint8))

@functools.lru_cache(None)
def glow_sprite(r, color):
    y, x = np.mgrid[-r:r, -r:r].astype(np.float32)
    g = np.clip(1 - np.sqrt(x * x + y * y) / r, 0, 1) ** 2.2
    return np.ascontiguousarray((g[..., None] * np.array(B(color), np.float32)).astype(np.uint8))

def add_glow(img, cx, cy, r, color, k=1.0):
    if k <= 0.01: return
    r = int(r); spr = glow_sprite(r, tuple(color))
    if abs(k - 1.0) > 1e-3: spr = cv2.convertScaleAbs(spr, alpha=k)
    x0 = int(cx - r); y0 = int(cy - r); h, w = spr.shape[:2]
    H_, W_ = img.shape[:2]
    X0 = max(x0, 0); Y0 = max(y0, 0); X1 = min(x0 + w, W_); Y1 = min(y0 + h, H_)
    if X1 <= X0 or Y1 <= Y0: return
    roi = img[Y0:Y1, X0:X1]
    cv2.add(roi, np.ascontiguousarray(spr[Y0 - y0:Y1 - y0, X0 - x0:X1 - x0]), dst=roi)

def rr_pts(x0, y0, x1, y1, r, n=8):
    r = min(r, (x1 - x0) / 2, (y1 - y0) / 2); pts = []
    for cx, cy, a0 in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0), (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
        for k in range(n + 1):
            a = math.radians(a0 + 90 * k / n); pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return np.round(np.array(pts, np.float32) * 16).astype(np.int32)

def rrect(img, x0, y0, x1, y1, r, color, thick=-1):
    pts = rr_pts(x0, y0, x1, y1, r)
    if thick < 0: cv2.fillPoly(img, [pts], B(color), cv2.LINE_AA, 4)
    else: cv2.polylines(img, [pts], True, B(color), thick, cv2.LINE_AA, 4)

def blend_draw(img, x0, y0, x1, y1, alpha, fn):
    x0 = max(int(x0), 0); y0 = max(int(y0), 0); x1 = min(int(x1) + 1, W); y1 = min(int(y1) + 1, H)
    if x1 <= x0 or y1 <= y0 or alpha <= 0: return
    roi = img[y0:y1, x0:x1]; tmp = roi.copy()
    fn(tmp, -x0, -y0)
    cv2.addWeighted(tmp, alpha, roi, 1 - alpha, 0, roi)

def circle(img, cx, cy, r, color, thick=-1):
    cv2.circle(img, (int(round(cx * 16)), int(round(cy * 16))), int(round(r * 16)), B(color), thick, cv2.LINE_AA, 4)
def ellipse(img, cx, cy, ax, ay, color, ang=0, a0=0, a1=360, thick=-1):
    cv2.ellipse(img, (int(round(cx * 16)), int(round(cy * 16))), (int(round(ax * 16)), int(round(ay * 16))), ang, a0, a1, B(color), thick, cv2.LINE_AA, 4)
def line(img, p0, p1, color, th):
    cv2.line(img, (int(round(p0[0] * 16)), int(round(p0[1] * 16))), (int(round(p1[0] * 16)), int(round(p1[1] * 16))), B(color), int(th), cv2.LINE_AA, 4)
def poly(img, pts, color):
    cv2.fillPoly(img, [np.round(np.array(pts, np.float32) * 16).astype(np.int32)], B(color), cv2.LINE_AA, 4)

def clock_secs(s):
    h, m, sec = [int(x) for x in s.split(":")]; return h * 3600 + m * 60 + sec
def clock_str(x):
    x = int(x) % 86400; return "%02d:%02d:%02d" % (x // 3600, (x // 60) % 60, x % 60)

WORK = os.environ.get("EP_WORK", "work")
TL = json.load(open(os.path.join(WORK, "timeline.json")))
STORY = json.load(open(os.path.join(WORK, "story.json")))
SEGS = TL["segments"]
SEGBY = {s["id"]: s for s in SEGS}
def seg_at(t):
    for s in SEGS:
        if s["start"] <= t < s["end"]: return s
    return SEGS[-1]
def cues(seg, name): return [c for c in seg["cues"] if c["name"] == name]
def all_cues(name): return [c for s in SEGS for c in s["cues"] if c["name"] == name]
