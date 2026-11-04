# -*- coding: utf-8 -*-
from common import *
from scenes_a import cached, box_grad, tint, limb, blit_into, bg_salon

# ------------------------------------------------------------------ PORTE
def bg_door():
    img = vgrad((32, 25, 56), (12, 10, 24)).copy()
    img[940:] = vgrad((26, 19, 38), (6, 6, 12))[940:]
    cv2.line(img, (0, 940), (W, 940), B((8, 6, 14)), 6)
    cv2.rectangle(img, (184, 222), (536, 944), B((12, 9, 20)), -1)
    img[250:944, 215:505] = box_grad(694, 290, (108, 77, 56), (70, 48, 36))
    for (y0, y1) in ((285, 520), (565, 895)):
        cv2.rectangle(img, (242, y0), (478, y1), B((58, 38, 29)), 4)
        cv2.line(img, (247, y0 + 4), (474, y0 + 4), B((132, 96, 68)), 2); cv2.line(img, (247, y0 + 4), (247, y1 - 4), B((132, 96, 68)), 2)
    circle(img, 360, 362, 12, (176, 156, 106)); circle(img, 360, 362, 8, (8, 8, 14)); circle(img, 357, 359, 2, (220, 230, 255))
    rrect(img, 334, 420, 386, 460, 6, (196, 176, 112)); sp = tsprite(STORY["plate"], 30, (60, 44, 26), weight=600)
    h, w = sp.shape[:2]; blit_into(img, sp, 360 - w // 2, 440 - h // 2)
    circle(img, 468, 645, 17, (205, 166, 84)); rrect(img, 432, 637, 488, 655, 9, (214, 176, 94)); circle(img, 462, 640, 5, (250, 226, 160))
    rrect(img, 330, 150, 390, 164, 6, (232, 192, 122))
    def tr(t, ox, oy): poly(t, [(215 + ox, 944 + oy), (505 + ox, 944 + oy), (610 + ox, 1100 + oy), (110 + ox, 1100 + oy)], (255, 170, 84))
    blend_draw(img, 0, 940, W, 1110, 0.30, tr)
    return img

def hero_back(img, t, x=64, y=760, scared=0.0):
    br = 2 * math.sin(t * 2.0)
    poly(img, [(-30, 1280), (-30, 880 + br), (10, 842 + br), (120, 850 + br), (190, 900 + br), (230, 1280)], (26, 126, 116))
    poly(img, [(110, 856 + br), (190, 906 + br), (230, 1280), (170, 1280)], (18, 88, 82))
    ellipse(img, x + 6, y + 30 + br, 92, 84, (22, 104, 98))
    circle(img, x, y + br, 70, (52, 44, 90)); circle(img, x, y + br, 67, (9, 9, 14))

def scene_door(lt, seg):
    t = seg["start"] + lt
    img = cached("door", bg_door).copy()
    add_glow(img, 360, 952, 300, (255, 170, 84), 0.55)
    add_glow(img, 360, 170, 260, (255, 200, 120), 0.35)
    cv2.rectangle(img, (215, 936), (505, 944), B((255, 218, 156)), -1)
    sway = 4 * math.sin(t * 1.5); sway2 = 3 * math.sin(t * 1.1 + 1)
    ellipse(img, 316 + sway, 948, 26, 9, (6, 5, 10)); ellipse(img, 404 + sway2, 948, 26, 9, (6, 5, 10))
    hero_back(img, t)
    return img

# ------------------------------------------------------------------ JUDAS
PC = 640
def peep_map():
    ys, xs = np.mgrid[0:PC, 0:PC].astype(np.float32)
    dx = (xs - PC / 2) / (PC / 2); dy = (ys - PC / 2) / (PC / 2); r2 = dx * dx + dy * dy
    k = 0.75
    return (dx * (1 + k * r2) * (PC / 2) + PC / 2).astype(np.float32), (dy * (1 + k * r2) * (PC / 2) + PC / 2).astype(np.float32)
def peep_mask():
    ys, xs = np.mgrid[0:PC, 0:PC].astype(np.float32)
    r = np.sqrt((xs - PC / 2) ** 2 + (ys - PC / 2) ** 2)
    m = np.clip((300 - r) / 5.0, 0, 1)
    vig = np.clip(1.05 - 0.55 * (r / 300) ** 2.4, 0, 1)
    return (m * vig)[..., None].astype(np.float32)
def bg_peep():
    img = box_grad(H, W, (14, 10, 12), (8, 6, 8)).copy()
    for i in range(40):
        x = int(hrand(i, 1) * W); cv2.line(img, (x, 0), (x + int(hrand(i, 2) * 20 - 10), H), B((22, 15, 14)), 1 + int(hrand(i, 3) * 3))
    return img
def peep_world():
    cv = box_grad(PC, PC, (180, 150, 104), (96, 74, 50)).copy()
    cv[430:] = box_grad(PC - 430, PC, (84, 64, 44), (40, 30, 22))
    cv2.line(cv, (0, 430), (PC, 430), B((60, 44, 30)), 5)
    for x0 in (50, 500):
        cv2.rectangle(cv, (x0, 130), (x0 + 100, 430), B((110, 82, 56)), -1); cv2.rectangle(cv, (x0, 130), (x0 + 100, 430), B((70, 50, 36)), 5)
        cv2.rectangle(cv, (x0 + 16, 160), (x0 + 84, 270), B((96, 70, 48)), 3)
    return cv

def scene_peephole(lt, seg):
    t = seg["start"] + lt
    img = cached("peepbg", bg_peep).copy()
    cv = cached("peepworld", peep_world).copy()
    mx, my = cached("peepmap", peep_map); mk = cached("peepmask", peep_mask)
    sc = cues(seg, "voice_scare"); tc = sc[0]["t"] if sc else 1e9
    u = t - tc
    grow = ease_in(lt / max(0.1, (tc - seg["start"]))) if u < 0 else 1.0
    s = 0.12 + 0.78 * grow if u < 0 else 1.0
    add_glow(cv, 320, 30, 240, (255, 236, 190), 0.9)
    scale = 1.0 + (0.38 * ease_out(u / 0.14) if u >= 0 else 0.06 * grow)
    hx = 320 + 16 * math.sin(t * 1.3) + (hrand(int(t * 30)) - 0.5) * 14 * (u >= 0)
    hy = 320 + 6 * math.sin(t * 0.9)
    poly(cv, [(150, 640), (205, 450), (435, 450), (490, 640)], tuple(STORY.get("outfit", (164, 132, 214)))); poly(cv, [(270, 450), (370, 450), (320, 560)], (236, 230, 244))
    line(cv, (320, hy + 70), (320, 460), (8, 8, 12), 26)
    R = 100 * scale
    circle(cv, hx, hy, R + 3, (60, 46, 40)); circle(cv, hx, hy, R, (8, 8, 12))
    for sx in (-1, 1):
        circle(cv, hx + sx * 42 * scale, hy - 24 * scale, 24 * scale, (250, 250, 255)); circle(cv, hx + sx * 40 * scale, hy - 22 * scale, 7 * scale, (8, 8, 12))
    a = (62 + 128 * s) * scale; b = (40 + 34 * s) * scale
    ellipse(cv, hx, hy + 30 * scale, a, b, (248, 248, 252), 0, 8, 172, max(3, int(9 * scale)))
    if s > 0.45:
        for kk in np.linspace(-0.82, 0.82, 15):
            px = hx + a * kk; py = hy + 30 * scale + b * math.sqrt(1 - kk * kk)
            line(cv, (px, py), (px, py - 13 * scale), (248, 248, 252), 3)
    cv = cv2.remap(cv, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    out = (cv.astype(np.float32) * mk).astype(np.uint8)
    cx, cy = 360, 560; x0, y0 = cx - PC // 2, cy - PC // 2
    roi = img[y0:y0 + PC, x0:x0 + PC]
    m1 = (mk > 0.001).astype(np.float32) * np.clip(mk * 8, 0, 1)
    roi[:] = (roi * (1 - m1) + out * m1).astype(np.uint8)
    circle(img, cx, cy, 306, (150, 122, 74), 12); circle(img, cx, cy, 316, (18, 12, 8), 10)
    ellipse(img, cx, cy, 306, 306, (230, 200, 130), 0, 200, 250, 5)
    return img

# ------------------------------------------------------------------ MORT
def scene_death(lt, seg):
    t = seg["start"] + lt; fi = int(t * 30)
    img = np.full((H, W, 3), B((7, 4, 9)), np.uint8)
    for i in range(14):
        y0 = int(hrand(fi, i, 1) * H); h = 2 + int(hrand(fi, i, 2) * 6); x0 = int(hrand(fi, i, 3) * W * 0.6); w = int(60 + hrand(fi, i, 4) * 420)
        cv2.rectangle(img, (x0, y0), (x0 + w, y0 + h), B((40 + int(hrand(fi, i, 5) * 80), 10, 20)), -1)
    sp = tsprite("T'ES MORT", 120, RED, 700, 0)
    jx = (hrand(fi, 9) - 0.5) * 16 * (1 if hrand(fi, 10) > 0.4 else 0)
    if hrand(fi, 11) > 0.35: blit_c(img, tsprite("T'ES MORT", 120, (70, 220, 255), 700, 0), 360 + 9 + jx, 560 + 3, 0.55)
    blit_c(img, sp, 360 + jx, 560)
    lab = tsprite("VIES", 26, (170, 166, 200), weight=500, track=8); blit_c(img, lab, 360, 735)
    for i, x in enumerate((296, 360, 424)):
        if i == 0: circle(img, x, 800, 17, (60, 10, 20)); circle(img, x, 800, 17, RED, 4)
        else: circle(img, x, 800, 17, (230, 230, 245), 4)
    line(img, (282, 786), (310, 814), RED, 5); line(img, (310, 786), (282, 814), RED, 5)
    return img

# ------------------------------------------------------------------ CHAMBRE
def bg_bedroom():
    img = vgrad((22, 20, 54), (8, 8, 22)).copy()
    img[930:] = vgrad((16, 14, 36), (4, 4, 10))[930:]
    cv2.line(img, (0, 930), (W, 930), B((6, 6, 16)), 6)
    x0, y0, x1, y1 = 256, 240, 440, 520
    img[y0:y1, x0:x1] = box_grad(y1 - y0, x1 - x0, (28, 36, 96), (84, 110, 190))
    circle(img, 380, 300, 18, (236, 240, 255))
    for xb in (x0, (x0 + x1) // 2 - 4, x1 - 8): cv2.rectangle(img, (xb, y0), (xb + 8, y1), B((14, 12, 34)), -1)
    for yb in (y0, (y0 + y1) // 2 - 4, y1 - 8): cv2.rectangle(img, (x0, yb), (x1, yb + 8), B((14, 12, 34)), -1)
    def beam(t, ox, oy): poly(t, [(256 + ox, 520 + oy), (440 + ox, 520 + oy), (740 + ox, 940 + oy), (180 + ox, 940 + oy)], (150, 176, 255))
    blend_draw(img, 0, 500, W, 950, 0.06, beam)
    cv2.rectangle(img, (40, 250), (194, 740), B((10, 8, 20)), -1); cv2.rectangle(img, (52, 262), (182, 740), B((44, 34, 62)), -1)
    cv2.rectangle(img, (66, 290), (168, 480), B((36, 27, 52)), 3); circle(img, 170, 520, 7, (190, 160, 90))
    cv2.rectangle(img, (500, 226), (694, 720), B((10, 8, 22)), -1)
    return img

def eye_w(img, cx, cy, look, r=15):
    circle(img, cx, cy, r, (250, 250, 255)); circle(img, cx + look * 5, cy, r * 0.28, (10, 10, 16))

def monster(img, cx, cy, sc, s, t):
    arm = (96, 82, 170)
    for sx in (-1, 1):
        pts = [(cx + sx * 40 * sc, cy + 50 * sc), (cx + sx * 104 * sc, cy + 170 * sc + 8 * math.sin(t * 5 + sx)), (cx + sx * 84 * sc, cy + 300 * sc)]
        for a, b in zip(pts[:-1], pts[1:]): line(img, a, b, arm, int(18 * sc) + 5)
        for a, b in zip(pts[:-1], pts[1:]): line(img, a, b, (3, 3, 6), int(18 * sc))
    poly(img, [(cx - 44 * sc, cy + 30 * sc), (cx + 44 * sc, cy + 30 * sc), (cx + 56 * sc, cy + 300 * sc), (cx - 56 * sc, cy + 300 * sc)], (3, 3, 6))
    circle(img, cx, cy, 52 * sc + 3, arm); circle(img, cx, cy, 52 * sc, (3, 3, 6))
    for sx in (-1, 1):
        ellipse(img, cx + sx * 21 * sc, cy - 10 * sc, 8 * sc, 15 * sc, (255, 255, 255))
    add_glow(img, cx, cy - 10 * sc, 90 * sc, (200, 200, 255), 0.5)
    a = (26 + 40 * s) * sc; b = (14 + 14 * s) * sc
    ellipse(img, cx, cy + 14 * sc, a, b, (255, 255, 255), 0, 8, 172, max(2, int(5 * sc)))

def scene_bedroom(lt, seg, mode):
    t = seg["start"] + lt
    img = cached("bedroom", bg_bedroom).copy()
    add_glow(img, 348, 390, 320, (96, 120, 240), 0.22)
    ks = [c["t"] for c in cues(seg, "knock")] + [c["t"] + d for c in cues(seg, "knock3") for d in (0, 0.3, 0.6)]
    lv = cues(seg, "leave"); tl = lv[0]["t"] if lv else 1e9
    visitor = (mode == 1 and t < tl)
    if visitor:
        fl = 1.0 if t < tl - 0.5 else (1.0 if hrand(int(t * 24)) > 0.4 else 0.2)
        cv2.rectangle(img, (40, 250), (194, 740), B((255, 190, 110)), 3)
        add_glow(img, 117, 745, 130, (255, 170, 84), 0.55 * fl)
    # placard
    mo = cues(seg, "monster"); tm = mo[0]["t"] if mo else 1e9
    um = t - tm
    gap = 10 if mode == 2 else 0
    if mode == 2: gap = lerp(10, 78, ease_out(um / 0.5)) if um >= 0 else 10
    cv2.rectangle(img, (505, 232), (689, 720), B((4, 3, 10)), -1)
    if mode == 2 and um >= 0:
        sc = lerp(0.65, 1.35, ease_in_out_(um / 1.1)); s = clamp(um / 0.9)
        monster(img, 597 + (hrand(int(t * 30)) - 0.5) * 3, 380 + 40 * (sc - 0.65), sc, s, t)
    # portes de placard
    dw = int(round(92 - gap))
    cv2.rectangle(img, (500, 226), (500 + 92, 722), B((40, 30, 66)), -1); cv2.rectangle(img, (500, 226), (592, 722), B((22, 16, 40)), 4)
    cv2.rectangle(img, (689 - dw, 226), (689, 722), B((40, 30, 66)), -1); cv2.rectangle(img, (689 - dw, 226), (689, 722), B((22, 16, 40)), 4)
    # lit
    rrect(img, 20, 722, 700, 930, 30, (56, 50, 112)); line(img, (30, 770), (690, 770), (92, 84, 160), 4)
    rrect(img, 470, 650, 694, 742, 36, (92, 86, 156))
    scared = 1.0
    look = 0.0
    if mode == 1: look = -1.0 if visitor else 0.0
    if mode == 2: look = 1.0 if um > -0.8 else -1.0
    hy = 672 + (2 * math.sin(t * 5) if scared else 0)
    circle(img, 586, hy, 54, (60, 52, 108)); circle(img, 586, hy, 51, (10, 10, 16))
    for ex in (566, 606): eye_w(img, ex, hy - 4, look)
    line(img, (552, hy - 26), (578, hy - 32), (235, 235, 245), 3); line(img, (596, hy - 32), (622, hy - 26), (235, 235, 245), 3)
    rrect(img, 330, 716 + 2 * math.sin(t * 5), 700, 940, 30, (60, 54, 122)); line(img, (340, 758), (690, 758), (96, 88, 170), 3)
    ellipse(img, 520, 722, 18, 13, (10, 10, 16))
    add_glow(img, 586, 672, 150, (130, 150, 255), 0.12)
    return img

def ease_in_out_(x): return ease_io(x)

# ------------------------------------------------------------------ CTA
def scene_cta(lt, seg):
    t = seg["start"] + lt
    img = cached("door", bg_door).copy()
    img = cv2.convertScaleAbs(img, alpha=0.22)
    add_glow(img, 360, 640, 520, (110, 70, 220), 0.22)
    pop = back_out(lt / 0.35)
    blit_c(img, tsprite(STORY["cta_title"][0], 100, WHITE, 700, 6), 360, 250, 1.0, 0.9 + 0.1 * pop)
    blit_c(img, tsprite(STORY["cta_title"][1], 160, RED, 700, 6), 360, 395, 1.0, 0.9 + 0.1 * pop)
    for (cx, col, num, lab, d) in ((215, (255, 138, 40), "1", STORY["cta_opts"][0], 0.15), (505, (66, 112, 255), "2", STORY["cta_opts"][1], 0.3)):
        k = back_out((lt - d) / 0.35)
        if k <= 0: continue
        add_glow(img, cx, 640, 190, col, 0.5 * k)
        circle(img, cx, 640, 92 * k, col); circle(img, cx, 640, 92 * k, (255, 255, 255), 3)
        blit_c(img, tsprite(num, 120, WHITE, 700, 0), cx, 640, 1.0, k)
        blit_c(img, tsprite(lab, 46, WHITE, 600, 3), cx, 780, k, 1.0)
    rp = cues(seg, "cta_reply"); tr = rp[0]["t"] if rp else 1e9
    if t >= tr:
        k = back_out((t - tr) / 0.3)
        rrect(img, 360 - 280 * k, 858, 360 + 280 * k, 926, 34, RED)
        if k > 0.8: blit_c(img, tsprite("RÉPONDS EN COMMENTAIRE", 38, WHITE, 600, 0, track=2), 360, 892)
    blit_c(img, tsprite("NUIT %d · DEMAIN" % (STORY["night"] + 1), 30, (180, 176, 214), 500, 0, track=7), 360, 1160, 0.95 if int(t * 2) % 2 == 0 else 0.7)
    return img
