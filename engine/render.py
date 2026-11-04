# -*- coding: utf-8 -*-
import sys, subprocess, time, os
from common import *
from scenes_a import scene_salon, scene_phone, tint, cached, wrap
from scenes_b import *

SEG_SCENES = dict(salon=scene_salon, phone=scene_phone, door=scene_door, peephole=scene_peephole, death=scene_death, cta=scene_cta)

def art_at(t):
    seg = seg_at(t); lt = t - seg["start"]; sc = seg["scene"]
    if sc == "bedroom": return scene_bedroom(lt, seg, 1)
    if sc == "bedroom2": return scene_bedroom(lt, seg, 2)
    if sc == "rewind": return scene_rewind(lt, seg)
    return SEG_SCENES[sc](lt, seg)

def glitch(img, k, seed):
    for i in range(int(3 + 8 * k)):
        y0 = int(hrand(seed, i, 1) * H); h = int(8 + hrand(seed, i, 2) * (40 + 120 * k)); dx = int((hrand(seed, i, 3) - 0.5) * 2 * (20 + 90 * k))
        img[y0:y0 + h] = np.roll(img[y0:y0 + h], dx, axis=1)
    d = int(2 + 10 * k); b, g, r = cv2.split(img)
    return cv2.merge([np.roll(b, d, axis=1), g, np.roll(r, -d, axis=1)])

def scene_rewind(lt, seg):
    d = seg["end"] - seg["start"]; u = clamp(lt / d)
    src = lerp(seg["src_from"], seg["src_to"], u)
    img = art_at(src); fi = int((seg["start"] + lt) * 30)
    img = tint(img, (1.2, 1.0, 0.82))
    img[::3] = (img[::3] * 0.74).astype(np.uint8)
    for i in range(7):
        y0 = int(hrand(fi, i, 1) * H); h = int(14 + hrand(fi, i, 2) * 80); dx = int((hrand(fi, i, 3) - 0.5) * 140)
        img[y0:y0 + h] = np.roll(img[y0:y0 + h], dx, axis=1)
    by = int((u * 2.6 * H + 200) % H); noise = (np.random.RandomState(fi).rand(26, W, 1) * 90).astype(np.uint8)
    img[by:by + 26] = cv2.add(img[by:by + 26], np.repeat(noise, 3, axis=2)[:H - by])
    img = cv2.GaussianBlur(img, (0, 0), 1.1)
    return img

# ---------- éléments d'interface
LINES = [l for s in SEGS for l in s["lines"]]
CAPS = []
for l in LINES:
    ws = l["words"]
    for i, w in enumerate(ws):
        nxt = ws[i + 1]["t0"] if i + 1 < len(ws) else w["t1"] + 0.14
        until = min(nxt, w["t1"] + 0.35) if i + 1 < len(ws) else w["t1"] + 0.14
        CAPS.append((w["t0"], until, w["w"], w["key"], l["kind"]))

def draw_caption(img, t):
    for t0, until, txt, key, kind in CAPS:
        if t0 <= t < until:
            col = RED if key else WHITE
            if kind == "v": col = (RED if key else (178, 198, 255))
            if kind == "vs": col = (255, 70, 96) if key else (255, 214, 220)
            spr = tsprite(txt, 90, col, 700, 6)
            k = 0.8 + 0.2 * back_out((t - t0) / 0.1)
            jx = jy = 0
            if kind in ("v", "vs"): jx = (hrand(int(t * 30), 1) - 0.5) * (5 if kind == "v" else 12); jy = (hrand(int(t * 30), 2) - 0.5) * 4
            blit_c(img, spr, 360 + jx, 985 + jy, 1.0, k)
            return

SHADE = None
def apply_shade(img):
    global SHADE
    if SHADE is None:
        y = np.linspace(0, 1, 330, dtype=np.float32)[:, None, None]
        SHADE = (1 - 0.6 * np.clip(np.sin(np.pi * y), 0, 1) ** 0.8).repeat(W, axis=1)
    roi = img[830:1160]; roi[:] = (roi * SHADE).astype(np.uint8)

def header(img, seg, t, clock_override=None):
    if seg["scene"] == "cta": return
    if clock_override is None: cs = clock_secs(seg["clock"]) + (t - seg["start"] if seg["scene"] != "death" else 0)
    else: cs = clock_override
    loc = seg["loc"] if seg["scene"] != "rewind" else STORY["places"]["door"]
    lab = tsprite(f"NUIT {STORY['night']} · {loc}", 21, (206, 202, 236), weight=500, track=5)
    blit_c(img, lab, 360 + 8, 66); 
    if int(t) % 2 == 0 or seg["scene"] == "rewind": circle(img, 360 - lab.shape[1] / 2 - 8, 66, 5, RED)
    txt = clock_str(cs)
    blit_c(img, tsprite(txt, 68, WHITE, weight=500, track=3), 360, 122)

def draw_choice(img, seg, t):
    sh = cues(seg, "choice_show")
    if not sh: return
    ts = sh[0]["t"]; u = t - ts
    if u < 0: return
    pk = cues(seg, "choice_pick"); tp = pk[0]["t"] if pk else 1e9; idx = pk[0]["i"] if pk else -1
    a = ease_out(u / 0.3)
    blit_c(img, tsprite("SI TU AS CHOISI :", 22, (220, 216, 245), weight=500, track=4), 360, 214 - (1 - a) * 20, a)
    for i, labt in enumerate(STORY["choice"]):
        y0 = 244 + i * 70; x0, x1 = 100, 620
        yy = y0 + (1 - a) * 30
        sel = (t >= tp and i == idx); dim = (t >= tp and i != idx)
        if sel: fill = ORANGE; tc = (30, 14, 4); bd = (255, 190, 120)
        else: fill = (44, 38, 80) if not dim else (28, 24, 52); tc = (214, 208, 246) if not dim else (110, 104, 140); bd = (120, 110, 190) if not dim else (60, 56, 90)
        pop = 1.0 + (0.05 * back_out((t - tp) / 0.2) if sel else 0)
        cx = 360; w2 = (x1 - x0) / 2 * pop
        blend_draw(img, cx - w2 - 2, yy - 2, cx + w2 + 2, yy + 58, a, lambda tmp, ox, oy: (rrect(tmp, cx - w2 + ox, yy + oy, cx + w2 + ox, yy + 56 + oy, 28, fill), rrect(tmp, cx - w2 + ox, yy + oy, cx + w2 + ox, yy + 56 + oy, 28, bd, 2)))
        blit_c(img, tsprite(labt, 31, tc, weight=600, track=2), 360 - (14 if sel else 0), yy + 28, a)
        if sel:
            bx = x1 - 56; by = yy + 28
            cv2.polylines(img, [np.array([[bx - 12, by], [bx - 3, by + 10], [bx + 14, by - 10]], np.int32)], False, B((30, 14, 4)), 5, cv2.LINE_AA)

_banner = {}
def banner_sprite(who, text):
    key = (who, text)
    if key in _banner: return _banner[key]
    S = 3; w, h = 600 * S, 112 * S
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=30 * S, fill=(46, 44, 64, 245), outline=(100, 96, 140, 255), width=2 * S)
    d.rounded_rectangle((18 * S, 22 * S, 82 * S, 86 * S), radius=16 * S, fill=(92, 66, 178, 255))
    d.rectangle((38 * S, 36 * S, 62 * S, 72 * S), fill=(240, 236, 255, 255))
    for wy in (42, 50, 58):
        for wx in (42, 49, 56): d.rectangle((wx * S, wy * S, (wx + 3) * S, (wy + 4) * S), fill=(92, 66, 178, 255))
    d.text((104 * S, 16 * S), STORY["group"]["name"].upper(), font=ImageFont.truetype(SANS, 15 * S), fill=(150, 146, 180, 255))
    d.text((104 * S, 38 * S), who, font=ImageFont.truetype(SANSB, 22 * S), fill=(255, 255, 255, 255))
    d.text((104 * S, 68 * S), text, font=ImageFont.truetype(SANS, 22 * S), fill=(228, 226, 240, 255))
    a = np.asarray(im.resize((w // S, h // S), Image.LANCZOS)); _banner[key] = np.ascontiguousarray(a[:, :, [2, 1, 0, 3]]); return _banner[key]

def draw_banner(img, seg, t):
    b = cues(seg, "banner")
    if not b: return
    c = b[0]; u = t - c["t"]
    if u < 0: return
    spr = banner_sprite(c["who"], c["text"])
    y = lerp(-130, 196, back_out(u / 0.4)) + 2 * math.sin(u * 40) * math.exp(-u * 6)
    out = clamp((seg["end"] - t) / 0.3)
    blit(img, spr, 60, y, out)

KNOCKS = [c["t"] for c in all_cues("knock")] + [c["t"] + d for c in all_cues("knock3") for d in (0, 0.3, 0.6)]
def shake_at(t):
    sx = sy = 0.0
    for tk in KNOCKS:
        u = t - tk
        if 0 <= u < 0.32:
            a = 16 * math.exp(-u * 13); sx += a * math.sin(u * 120); sy += a * 0.7 * math.cos(u * 97)
    for c in all_cues("voice_scare") + all_cues("monster"):
        u = t - c["t"]
        if 0 <= u < 0.5: a = 20 * math.exp(-u * 8); sx += a * math.sin(u * 140); sy += a * math.cos(u * 120)
    return sx, sy

def glitch_at(t):
    k = 0.0
    for c in all_cues("voice_scare"):
        u = t - c["t"]
        if 0 <= u < 0.5: k = max(k, 0.8 * (1 - u / 0.5))
    for c in all_cues("monster"):
        u = t - c["t"]
        if 0 <= u < 0.9: k = max(k, 0.3)
    for c in all_cues("glitch"):
        u = t - c["t"]
        if 0 <= u < 0.6: k = max(k, 1.0 * (1 - u / 0.7))
    for c in all_cues("blackout"):
        u = t - c["t"]
        if -0.05 <= u < 0.3: k = max(k, 0.35)
    if seg_at(t)["scene"] == "death": k = max(k, 0.5)
    return k

TENSE = [(SEGBY["noir"]["start"] + 1.7, SEGBY["mort"]["start"]), (SEGBY["chambre1"]["start"], SEGBY["fin"]["start"] - 0.3)]
VIG = None; REDV = None; GR = None
def post(img, t):
    global VIG, REDV, GR
    if VIG is None:
        ys, xs = np.mgrid[0:H, 0:W].astype(np.float32); r = np.sqrt(((xs - W / 2) / (W / 2)) ** 2 + ((ys - H / 2) / (H / 2)) ** 2) / 1.35
        VIG = np.repeat(np.clip(1 - 0.62 * np.clip(r, 0, 1.2) ** 2.3, 0, 1)[..., None] * 255, 3, axis=2).astype(np.uint8)
        e = np.clip((r - 0.55) / 0.6, 0, 1) ** 1.8
        REDV = np.stack([e * 20, e * 8, e * 210], axis=2).astype(np.uint8)
        rs = np.random.RandomState(7); GR = [np.repeat(rs.normal(128, 9, (H, W, 1)).clip(0, 255).astype(np.uint8), 3, axis=2) for _ in range(6)]
    img = cv2.multiply(img, VIG, scale=1 / 255.0)
    for a, b in TENSE:
        if a <= t < b:
            bpm = lerp(66, 108, (t - a) / max(1, b - a)); ph = (t * bpm / 60) % 1
            pulse = math.exp(-ph * 9) + 0.55 * math.exp(-abs(ph - 0.28) * 22)
            img = cv2.add(img, cv2.convertScaleAbs(REDV, alpha=0.5 * pulse)); break
    img = cv2.addWeighted(img, 1.0, GR[int(t * 15) % 6], 0.5, -64)
    if t < 0.5: img = cv2.convertScaleAbs(img, alpha=ease_out(t / 0.5))
    tot = TL["total"]
    if t > tot - 0.45: img = cv2.convertScaleAbs(img, alpha=clamp((tot - t) / 0.45))
    return img

PALETTES = {"violet": None, "bleu": (1.25, 1.0, 0.78), "rouge": (0.72, 0.9, 1.3), "vert": (0.85, 1.2, 0.88)}
def render_frame(t):
    seg = seg_at(t); img = art_at(t)
    pm = PALETTES.get(STORY.get("palette", "violet"))
    if pm: img = tint(img, pm)
    sx, sy = shake_at(t)
    if abs(sx) + abs(sy) > 0.6:
        img = cv2.warpAffine(img, np.float32([[1, 0, sx], [0, 1, sy]]), (W, H), borderMode=cv2.BORDER_REPLICATE)
    gk = glitch_at(t)
    if gk > 0.02: img = glitch(img, gk, int(t * 30))
    apply_shade(img)
    co = None
    if seg["scene"] == "rewind":
        u = clamp((t - seg["start"]) / (seg["end"] - seg["start"]))
        def ck(tt): s2 = seg_at(tt); return clock_secs(s2["clock"]) + (tt - s2["start"])
        co = lerp(ck(seg["src_from"]), ck(seg["src_to"]), u)
        rrect(img, 26, 196, 270, 248, 24, (18, 18, 28)); rrect(img, 26, 196, 270, 248, 24, (110, 110, 140), 2)
        for dx in (0, 22): poly(img, [(62 + dx, 222), (80 + dx, 210), (80 + dx, 234)], (250, 250, 255))
        blit(img, tsprite("REMBOBINAGE", 22, (240, 240, 250), sans=True, bold=True, track=1), 108, 211)
    header(img, seg, t, co)
    draw_choice(img, seg, t); draw_banner(img, seg, t)
    draw_caption(img, t)
    return post(img, t)

if __name__ == "__main__":
    if sys.argv[1] == "frames":
        names = []
        for tt in [float(x) for x in sys.argv[2].split(",")]:
            t0 = time.time(); f = render_frame(tt); dt = (time.time() - t0) * 1000
            n = os.path.join(WORK, f"f_{tt:05.1f}.png"); cv2.imwrite(n, f); names.append(n); print(tt, seg_at(tt)["id"], "%.0f ms" % dt)
        ims = [cv2.resize(cv2.imread(n), (288, 512)) for n in names]
        rows = [np.hstack(ims[i:i + 6] + [np.zeros_like(ims[0])] * (6 - len(ims[i:i + 6]))) for i in range(0, len(ims), 6)]
        cv2.imwrite(sys.argv[3], np.vstack(rows))
