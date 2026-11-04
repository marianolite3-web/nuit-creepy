# -*- coding: utf-8 -*-
from common import *

_C = {}
def cached(key, fn):
    if key not in _C: _C[key] = fn()
    return _C[key]

def box_grad(h, w, top, bot):
    t = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
    c = np.array(B(top), np.float32) * (1 - t) + np.array(B(bot), np.float32) * t
    return np.repeat(c, w, axis=1).astype(np.uint8)

def tint_lut(mult):
    lut = np.clip(np.arange(256, dtype=np.float32)[:, None] * np.array(mult, np.float32)[None, :], 0, 255).astype(np.uint8)
    return lut.reshape(1, 256, 3)
def tint(img, bgr_mult):  # (b,g,r)
    return cv2.LUT(img, tint_lut(bgr_mult))

def limb(img, pts, th, col=(12, 12, 18), rim=(52, 46, 92)):
    for a, b in zip(pts[:-1], pts[1:]): line(img, a, b, rim, th + 5)
    for a, b in zip(pts[:-1], pts[1:]): line(img, a, b, col, th)

# ------------------------------------------------------------------ SALON
def bg_salon():
    img = vgrad((32, 21, 66), (14, 10, 32)).copy()
    img[830:] = vgrad((22, 15, 44), (7, 6, 16))[830:]
    cv2.line(img, (0, 830), (W, 830), B((10, 8, 22)), 6)
    def d(t, ox, oy): poly(t, [(60 + ox, 560 + oy), (300 + ox, 560 + oy), (560 + ox, 1200 + oy), (120 + ox, 1200 + oy)], (130, 100, 210))
    blend_draw(img, 0, 540, W, 1280, 0.08, d)
    x0, y0, x1, y1 = 60, 230, 300, 560
    sky = box_grad(y1 - y0, x1 - x0, (46, 30, 104), (156, 96, 180))
    for i in range(26):  # étoiles
        sx = int(hrand(i, 1) * (x1 - x0 - 8)) + 4; sy = int(hrand(i, 2) * 150) + 4
        cv2.circle(sky, (sx, sy), 1, (255, 240, 235), -1)
    x = 0; k = 0
    while x < x1 - x0:
        bw = int(26 + hrand(k, 3) * 34); bh = int(50 + hrand(k, 4) * 120)
        cv2.rectangle(sky, (x, y1 - y0 - bh), (x + bw, y1 - y0), (40, 22, 30), -1)
        for wy in range(y1 - y0 - bh + 10, y1 - y0 - 6, 16):
            for wx in range(x + 6, x + bw - 6, 12):
                if hrand(wx, wy) > 0.72: cv2.rectangle(sky, (wx, wy), (wx + 4, wy + 6), (110, 200, 255), -1)
        x += bw + 2; k += 1
    img[y0:y1, x0:x1] = sky
    circle(img, 246, 290, 19, (244, 240, 255))
    for xb in (x0, (x0 + x1) // 2 - 4, x1 - 8): cv2.rectangle(img, (xb, y0), (xb + 8, y1), B((20, 16, 46)), -1)
    for yb in (y0, (y0 + y1) // 2 - 4, y1 - 8): cv2.rectangle(img, (x0, yb), (x1, yb + 8), B((20, 16, 46)), -1)
    cv2.rectangle(img, (x0 - 12, y1), (x1 + 12, y1 + 18), B((44, 34, 86)), -1)
    # horloge murale (cadran)
    circle(img, 610, 300, 46, (190, 186, 215)); circle(img, 610, 300, 41, (24, 20, 44))
    for i in range(12):
        a = math.radians(i * 30); line(img, (610 + 34 * math.sin(a), 300 - 34 * math.cos(a)), (610 + 39 * math.sin(a), 300 - 39 * math.cos(a)), (170, 166, 200), 2)
    # tapis, canapé, lampe
    ellipse(img, 360, 940, 330, 66, (30, 21, 66)); ellipse(img, 360, 940, 270, 46, (40, 29, 88))
    rrect(img, 92, 556, 482, 736, 42, (92, 74, 170))
    line(img, (140, 566), (430, 566), (136, 118, 214), 3); line(img, (287, 586), (287, 722), (74, 58, 140), 4)
    rrect(img, 84, 606, 164, 812, 36, (110, 90, 190))
    rrect(img, 120, 724, 484, 806, 26, (122, 100, 204)); line(img, (140, 730), (462, 730), (160, 140, 232), 3)
    cv2.rectangle(img, (130, 806), (150, 830), B((30, 24, 60)), -1); cv2.rectangle(img, (452, 806), (472, 830), B((30, 24, 60)), -1)
    cv2.rectangle(img, (590, 770), (692, 836), B((58, 42, 96)), -1)
    ellipse(img, 640, 764, 20, 6, (88, 70, 128)); line(img, (640, 764), (640, 676), (72, 62, 112), 6)
    poly(img, [(608, 678), (672, 678), (656, 612), (624, 612)], (216, 172, 112))
    return img

def hero_sit(img, t, phone_on=False, eyes="tired", look=0.0, scared=0.0):
    br = 1.8 * math.sin(t * 2.1)
    hip = (330, 720); knee = (476, 714); ankle = (490, 828)
    # jambe lointaine
    limb(img, [(hip[0] + 8, hip[1] - 6), (knee[0] + 14, knee[1] - 6), (ankle[0] + 16, ankle[1] - 2)], 14, (6, 6, 10), (36, 32, 70))
    ellipse(img, ankle[0] + 30, ankle[1] + 4, 28, 11, (150, 150, 176))
    # bras lointain
    limb(img, [(312, 604 + br), (298, 668), (344, 706)], 13, (6, 6, 10), (36, 32, 70))
    # torse (sweat teal)
    ellipse(img, 308, 590 + br, 40, 26, (24, 128, 118))
    rrect(img, 282, 580 + br, 384, 736, 36, (38, 190, 170))
    def shade(tmp, ox, oy): rrect(tmp, 282 + ox, 580 + br + oy, 318 + ox, 736 + oy, 30, (10, 70, 70))
    blend_draw(img, 280, 578, 330, 740, 0.45, shade)
    line(img, (356, 604 + br), (356, 632 + br), (230, 255, 250), 2); line(img, (366, 604 + br), (366, 626 + br), (230, 255, 250), 2)
    rrect(img, 300, 668 + br, 366, 712 + br, 14, (30, 160, 144), 3)
    # cuisse + tibia + chaussure (jambe proche)
    limb(img, [hip, knee, ankle], 15)
    ellipse(img, ankle[0] + 30, ankle[1] + 6, 30, 12, (214, 214, 230)); ellipse(img, ankle[0] + 34, ankle[1] + 12, 30, 5, (150, 150, 176))
    # bras proche + téléphone
    shoulder = (352, 600 + br); elbow = (394, 668); hand = (426, 630)
    limb(img, [shoulder, elbow, hand], 13)
    ang = math.radians(-14); cx, cy = 438, 608
    pts = []
    for dx, dy in ((-17, -32), (17, -32), (17, 32), (-17, 32)):
        pts.append((cx + dx * math.cos(ang) - dy * math.sin(ang), cy + dx * math.sin(ang) + dy * math.cos(ang)))
    poly(img, pts, (22, 22, 30))
    sp = []
    for dx, dy in ((-14, -29), (14, -29), (14, 29), (-14, 29)):
        sp.append((cx + dx * math.cos(ang) - dy * math.sin(ang), cy + dx * math.sin(ang) + dy * math.cos(ang)))
    poly(img, sp, (214, 228, 255) if phone_on else (30, 30, 46))
    # tête
    hx, hy = 340, 514 + br * 0.6
    circle(img, hx, hy, 51, (62, 52, 104)); circle(img, hx, hy, 48, (10, 10, 16))
    for ex in (332, 366):
        ey = hy - 2
        if scared > 0.3:
            circle(img, ex, ey, 15, (255, 255, 255)); circle(img, ex + look * 4, ey, 4, (10, 10, 16))
            line(img, (ex - 14, ey - 24), (ex + 12, ey - 28 + (4 if ex > 340 else -4)), (235, 235, 245), 3)
        else:
            blink = (t % 3.7) < 0.12
            if blink: line(img, (ex - 11, ey), (ex + 11, ey), (240, 240, 250), 3)
            else:
                ellipse(img, ex, ey, 12, 10, (246, 246, 252)); circle(img, ex + 3 + look * 4, ey + 1, 5, (10, 10, 16))
                ellipse(img, ex, ey - 1, 14, 11, (10, 10, 16), 0, 180, 360)  # paupière
                line(img, (ex - 12, ey - 1), (ex + 12, ey - 1), (230, 230, 245), 3)

def scene_salon(lt, seg):
    t = seg["start"] + lt
    img = cached("salon", bg_salon).copy()
    bo = cues(seg, "blackout"); tb = bo[0]["t"] if bo else None
    level = 1.0
    if tb is not None:
        u = t - tb
        if u >= 0.35: level = 0.0
        elif u > -0.3: level = 1.0 if hrand(int((u + 0.3) * 28)) > 0.5 - 0.5 * clamp((u + 0.3) / 0.65) else 0.12
    phone_on = (seg["id"] == "noir")
    # lumières
    add_glow(img, 640, 640, 340, (255, 168, 78), 0.55 * level)
    add_glow(img, 180, 400, 300, (110, 90, 230), 0.22)
    # horloge
    ang = math.radians(96); line(img, (610, 300), (610 + 22 * math.sin(ang), 300 - 22 * math.cos(ang)), (220, 216, 240), 4)
    ang = math.radians(72); line(img, (610, 300), (610 + 32 * math.sin(ang), 300 - 32 * math.cos(ang)), (220, 216, 240), 3)
    ang = math.radians((t * 6) % 360); line(img, (610, 300), (610 + 35 * math.sin(ang), 300 - 35 * math.cos(ang)), (230, 40, 70), 1)
    scared = 0.0
    look = 0.0
    if seg["id"] == "noir":
        ks = [c["t"] for c in cues(seg, "knock")]
        if ks and t > ks[0]: scared = 1.0
        look = 1.0 if (ks and t > ks[0]) else 0.0
    hero_sit(img, t, phone_on=phone_on, scared=scared, look=look)
    for i in range(16):  # poussière
        px = (hrand(i, 1) * W + 12 * math.sin(t * 0.4 + i)) % W; py = (hrand(i, 2) * 700 + 250 - t * (4 + hrand(i, 3) * 6)) % 700 + 250
        cv2.circle(img, (int(px), int(py)), 1 + int(hrand(i, 4) * 1.5), (200, 190, 230), -1, cv2.LINE_AA)
    dark = lerp(0.2, 1.0, level)
    if dark < 0.999:
        img = cv2.convertScaleAbs(img, alpha=dark)
        img = tint(img, (1.18, 0.95, 0.8))
        add_glow(img, 180, 400, 260, (70, 60, 170), 0.18)
        if phone_on: add_glow(img, 438, 608, 300, (150, 175, 255), 0.95 * (1 - level))
    return img

# ------------------------------------------------------------------ PHONE
PW, PH_ = 460, 860; PX0, PY0 = 130, 215; PAD = 30
SENDER_COL = {STORY["group"]["sender"]: (255, 152, 60), STORY["contra"][0]: (186, 156, 255)}

def wrap(text, font, maxw):
    words = text.split(); lines = []; cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if font.getlength(trial) <= maxw: cur = trial
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

@functools.lru_cache(maxsize=128)
def bubble_sprite(who, text, key=False):
    S = 3
    fb = ImageFont.truetype(SANSB, 17 * S); ft = ImageFont.truetype(SANS, 23 * S)
    maxw = 330 * S
    lines = wrap(text, ft, maxw)
    wmax = max([ft.getlength(l) for l in lines] + [fb.getlength(who)])
    pad = 17 * S
    w = int(wmax + 2 * pad); h = int(pad + 22 * S + len(lines) * 31 * S + pad - 6 * S)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=22 * S, fill=(40, 40, 56, 255))
    d.text((pad, pad - 4 * S), who, font=fb, fill=SENDER_COL.get(who, (200, 200, 220)) + (255,))
    y = pad + 24 * S
    for l in lines:
        d.text((pad, y), l, font=ft, fill=(238, 238, 244, 255)); y += 31 * S
    a = np.asarray(img.resize((w // S, h // S), Image.LANCZOS))
    return np.ascontiguousarray(a[:, :, [2, 1, 0, 3]])

def phone_parts():
    cw, ch = PW + 2 * PAD, PH_ + 2 * PAD
    body = np.zeros((ch, cw, 3), np.uint8); mask = np.zeros((ch, cw), np.uint8)
    rrect(body, PAD, PAD, PAD + PW, PAD + PH_, 66, (17, 17, 24)); rrect(body, PAD, PAD, PAD + PW, PAD + PH_, 66, (60, 60, 82), 3)
    rrect(body, PAD + 11, PAD + 11, PAD + PW - 11, PAD + PH_ - 11, 56, (20, 20, 30))
    cv2.fillPoly(mask, [rr_pts(PAD, PAD, PAD + PW, PAD + PH_, 66)], 255, cv2.LINE_AA, 4)
    cx = PAD + PW // 2
    sx0, sx1 = PAD + 11, PAD + PW - 11
    # ---- barre du haut (en-tête + îlot)
    t3 = np.zeros((ch, cw, 3), np.uint8); ta = np.zeros((ch, cw), np.uint8)
    rrect(t3, sx0, PAD + 11, sx1, PAD + 170, 56, (26, 26, 38))
    cv2.fillPoly(ta, [rr_pts(sx0, PAD + 11, sx1, PAD + 170, 56)], 255, cv2.LINE_AA, 4)
    ta[PAD + 112:] = 0; t3[PAD + 112:] = 0
    cv2.line(t3, (sx0, PAD + 111), (sx1, PAD + 111), B((50, 50, 70)), 1)
    rrect(t3, cx - 58, PAD + 26, cx + 58, PAD + 54, 14, (4, 4, 7))
    poly(t3, [(PAD + 40, PAD + 82), (PAD + 52, PAD + 71), (PAD + 53, PAD + 77), (PAD + 45, PAD + 82), (PAD + 53, PAD + 87), (PAD + 52, PAD + 93)], (230, 50, 80))
    circle(t3, PAD + 100, PAD + 86, 22, (92, 66, 178))
    cv2.rectangle(t3, (PAD + 91, PAD + 74), (PAD + 109, PAD + 98), B((240, 236, 255)), -1)
    for wy in (78, 84, 90):
        for wx in (94, 100, 105): cv2.rectangle(t3, (PAD + wx, PAD + wy), (PAD + wx + 2, PAD + wy + 3), B((92, 66, 178)), -1)
    top = np.dstack([t3, ta])
    def paste(dst4, spr, x, y):
        h, w = spr.shape[:2]; reg = dst4[y:y + h, x:x + w]
        a = spr[..., 3:4].astype(np.float32) / 255.0
        reg[..., :3] = (reg[..., :3] * (1 - a) + spr[..., :3] * a).astype(np.uint8); reg[..., 3] = np.maximum(reg[..., 3], spr[..., 3])
    nm = tsprite(STORY["group"]["name"], 21, (240, 240, 248), sans=True, bold=True); sb = tsprite(STORY["group"]["sub"], 15, (140, 140, 164), sans=True)
    paste(top, nm, PAD + 136, PAD + 64); paste(top, sb, PAD + 136, PAD + 92)
    # ---- barre du bas (saisie)
    b3 = np.zeros((ch, cw, 3), np.uint8); ba = np.zeros((ch, cw), np.uint8)
    yb = PAD + PH_ - 128
    rrect(b3, sx0, PAD + PH_ - 240, sx1, PAD + PH_ - 11, 56, (20, 20, 30))
    cv2.fillPoly(ba, [rr_pts(sx0, PAD + PH_ - 240, sx1, PAD + PH_ - 11, 56)], 255, cv2.LINE_AA, 4)
    ba[:yb] = 0; b3[:yb] = 0
    y0 = PAD + PH_ - 112
    rrect(b3, PAD + 30, y0, PAD + PW - 92, y0 + 52, 26, (38, 38, 52))
    circle(b3, PAD + PW - 52, y0 + 26, 26, (74, 74, 100))
    xs = PAD + PW - 58
    line(b3, (xs, y0 + 36), (xs, y0 + 16), (230, 230, 240), 3); line(b3, (xs, y0 + 16), (xs - 8, y0 + 24), (230, 230, 240), 3); line(b3, (xs, y0 + 16), (xs + 8, y0 + 24), (230, 230, 240), 3)
    rrect(b3, cx - 70, PAD + PH_ - 30, cx + 70, PAD + PH_ - 24, 3, (224, 224, 234))
    bot = np.dstack([b3, ba])
    pm = tsprite("Message", 19, (120, 120, 146), sans=True); paste(bot, pm, PAD + 50, y0 + 12)
    return body, mask, top, bot

def comp_over(base, spr4, ox=0, oy=0):
    a = spr4[..., 3:4].astype(np.float32) / 255.0
    base[:] = (base * (1 - a) + spr4[..., :3] * a).astype(np.uint8)

def bg_phone():
    img = vgrad((30, 20, 62), (9, 8, 22)).copy()
    return img

HIST = [(STORY["group"]["sender"], r[0], False) for r in STORY["rules"]] + [(STORY["contra"][0], STORY["contra"][1], False)]

def scene_phone(lt, seg):
    t = seg["start"] + lt
    img = cached("bg_phone", bg_phone).copy()
    for i, (cx, cy, r, col) in enumerate(((140, 300, 240, (96, 60, 200)), (600, 900, 260, (200, 110, 60)), (560, 260, 200, (60, 90, 220)))):
        add_glow(img, cx + 14 * math.sin(t * 0.3 + i), cy + 12 * math.cos(t * 0.27 + i), r, col, 0.22)
    body, mask, top, bot = cached("phone", phone_parts)
    cvs = body.copy()
    msgs = []
    if seg.get("phone2"):
        for who, text, key in HIST: msgs.append(dict(who=who, text=text, key=key, t=-1e3))
    for c in cues(seg, "msg"): msgs.append(dict(who=c["who"], text=c["text"], key=c.get("key", False), t=c["t"]))
    area_top = PAD + 128; area_bot = PAD + PH_ - 130; area_h = area_bot - area_top
    def total_at(tt):
        y = 0
        for m in msgs:
            if m["t"] <= tt: y += bubble_sprite(m["who"], m["text"]).shape[0] + 14
        nxt = [m for m in msgs if m["t"] - 0.6 <= tt < m["t"]]
        if nxt: y += 58
        return y
    tot = total_at(t)
    last_ev = max([m["t"] for m in msgs if m["t"] <= t] + [m["t"] - 0.6 for m in msgs if m["t"] - 0.6 <= t] + [-1e3])
    off_now = max(0, tot - area_h); off_prev = max(0, total_at(last_ev - 0.01) - area_h) if last_ev > -1e2 else off_now
    off = lerp(off_prev, off_now, ease_out((t - last_ev) / 0.3)) if last_ev > -1e2 else off_now
    y = area_top - off
    for m in msgs:
        spr = bubble_sprite(m["who"], m["text"]); age = t - m["t"]; h = spr.shape[0]
        if age >= 0:
            a = ease_out(age / 0.22); yy = y + (1 - a) * 18
            blit_into(cvs, spr, PAD + 38, int(yy), a)
            if m["key"] and age > 0.35:
                pul = 0.55 + 0.45 * math.sin(age * 7)
                rrect(cvs, PAD + 38 - 4, yy - 4, PAD + 38 + spr.shape[1] + 4, yy + h + 4, 26, (int(255 * (0.6 + 0.4 * pul)), int(130 * (0.6 + 0.4 * pul)), 40), 3)
            y += h + 14
        elif age > -0.6:
            dots = bubble_typing(t)
            blit_into(cvs, dots, PAD + 38, int(y), 1.0); y += 58
    comp_over(cvs, top); comp_over(cvs, bot)
    # secousse de vibration
    sx = sy = 0.0
    for c in cues(seg, "buzz"):
        u = t - c["t"]
        if 0 <= u < 0.7:
            amp = 9 * math.exp(-u * 4.5); sx = amp * math.sin(u * 95); sy = amp * 0.6 * math.cos(u * 80)
            for sgn in (-1, 1):
                for k in range(2):
                    r = 34 + 22 * k
                    ellipse(img, PX0 + PW / 2 + sgn * (PW / 2 + 24 + 20 * k), PY0 + PH_ * 0.45, 12 + 6 * k, r * 1.1, (255, 190, 120), 0, -50 if sgn > 0 else 130, 50 if sgn > 0 else 230, 4)
    ox, oy = int(PX0 - PAD + sx), int(PY0 - PAD + sy)
    add_glow(img, PX0 + PW / 2 + sx, PY0 + PH_ / 2, 520, (120, 100, 230), 0.14)
    h, w = cvs.shape[:2]
    X0 = max(ox, 0); Y0 = max(oy, 0); X1 = min(ox + w, W); Y1 = min(oy + h, H)
    roi = img[Y0:Y1, X0:X1]; m3 = (mask[Y0 - oy:Y1 - oy, X0 - ox:X1 - ox, None].astype(np.float32) / 255.0)
    roi[:] = (roi * (1 - m3) + cvs[Y0 - oy:Y1 - oy, X0 - ox:X1 - ox] * m3).astype(np.uint8)
    # main (doigts + pouce)
    for k, yy in enumerate((600, 668, 736, 804)):
        rrect(img, ox + PAD - 52 + sx * 0, oy + yy, ox + PAD + 18, oy + yy + 36, 18, (24, 24, 36)); rrect(img, ox + PAD - 52, oy + yy, ox + PAD + 18, oy + yy + 36, 18, (90, 90, 118), 2)
    ellipse(img, ox + PAD + PW - 40, oy + PAD + PH_ - 50, 36, 56, (22, 22, 34), -30); ellipse(img, ox + PAD + PW - 40, oy + PAD + PH_ - 50, 36, 56, (210, 120, 60), -30, 200, 300, 3)
    return img

def blit_into(dst, spr, x, y, alpha=1.0):
    h, w = spr.shape[:2]; H_, W_ = dst.shape[:2]
    x0 = max(x, 0); y0 = max(y, 0); x1 = min(x + w, W_); y1 = min(y + h, H_)
    if x1 <= x0 or y1 <= y0: return
    s = spr[y0 - y:y1 - y, x0 - x:x1 - x]; a = s[..., 3:4].astype(np.float32) * (alpha / 255.0)
    roi = dst[y0:y1, x0:x1]; roi[:] = (roi * (1 - a) + s[..., :3] * a).astype(np.uint8)

def bubble_typing(t):
    S = 3; w, h = 90 * S, 46 * S
    img = np.zeros((h, w, 4), np.uint8)
    pil = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(pil)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=22 * S, fill=(40, 40, 56, 255))
    for i in range(3):
        k = 0.5 + 0.5 * math.sin(t * 9 - i * 0.9); r = (5 + 2.2 * k) * S
        cx = (24 + i * 21) * S; d.ellipse((cx - r, h / 2 - r, cx + r, h / 2 + r), fill=(150 + int(80 * k),) * 3 + (255,))
    a = np.asarray(pil.resize((w // S, h // S), Image.LANCZOS)); return np.ascontiguousarray(a[:, :, [2, 1, 0, 3]])
