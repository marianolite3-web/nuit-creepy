# -*- coding: utf-8 -*-
import json, math, os, numpy as np, scipy.signal as ss
from scipy.io import wavfile
SR = 44100
WORK = os.environ.get("EP_WORK", "work")
TL = json.load(open(os.path.join(WORK, "timeline.json"))); V = np.load(os.path.join(WORK, "voices.npz"))
SEGS = TL["segments"]; SEGBY = {s["id"]: s for s in SEGS}
T = TL["total"] + 1.0; N = int(T * SR)
rng = np.random.RandomState(11)

def tv(n): return np.arange(n, dtype=np.float32) / SR
def lp(x, fc, o=2): b, a = ss.butter(o, fc / (SR / 2), "low"); return ss.lfilter(b, a, x).astype(np.float32)
def hp(x, fc, o=2): b, a = ss.butter(o, fc / (SR / 2), "high"); return ss.lfilter(b, a, x).astype(np.float32)
def bp(x, lo, hi, o=2): b, a = ss.butter(o, [lo / (SR / 2), hi / (SR / 2)], "band"); return ss.lfilter(b, a, x).astype(np.float32)
def norm(x, p=1.0): m = np.abs(x).max(); return (x / m * p).astype(np.float32) if m > 0 else x

sfxL = np.zeros(N, np.float32); sfxR = np.zeros(N, np.float32)
bus = {k: np.zeros(N, np.float32) for k in ("n", "v", "vs")}
def put(arr, sig, t, g=1.0):
    i = int(round(t * SR))
    if i < 0: sig = sig[-i:]; i = 0
    n = min(len(sig), N - i)
    if n > 0: arr[i:i + n] += sig[:n] * g
def add(sig, t, g=1.0, pan=0.0):
    a = (pan + 1) * math.pi / 4; put(sfxL, sig, t, g * math.cos(a)); put(sfxR, sig, t, g * math.sin(a))

# ---------------------------------------------------------------- sons
def knock(seed=0):
    r = np.random.RandomState(seed); n = int(0.6 * SR); t = tv(n)
    body = sum(a * np.sin(2 * np.pi * f * t + r.rand() * 6) * np.exp(-t / tau) for f, a, tau in ((92, 1.0, 0.07), (148, 0.55, 0.05), (231, 0.35, 0.035), (370, 0.2, 0.02)))
    click = bp(r.randn(n), 700, 3200) * np.exp(-t / 0.010)
    return norm(body * 0.9 + click * 0.5)
def ping(f1=1046.5, f2=1568.0, d=0.1):
    n = int(0.7 * SR); t = tv(n); x = np.sin(2 * np.pi * f1 * t) * np.exp(-t / 0.14)
    t2 = np.clip(t - d, 0, None); x2 = np.sin(2 * np.pi * f2 * t2) * np.exp(-t2 / 0.18) * (t >= d)
    return norm(x * 0.6 + x2 * 0.6)
def buzz():
    n = int(0.9 * SR); t = tv(n); x = np.zeros(n, np.float32)
    for st in (0.0, 0.34):
        m = (t >= st) & (t < st + 0.24); u = t - st
        car = np.tanh(2.2 * np.sin(2 * np.pi * 168 * t)) * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 31 * t)))
        x += car * m * np.minimum(1, u * 120) * np.minimum(1, (st + 0.24 - t) * 80)
    return norm(lp(x, 900))
def pop():
    n = int(0.12 * SR); t = tv(n); f = 1500 - 700 * t / 0.12
    return norm(np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.02))
def powerdown():
    n = int(2.4 * SR); t = tv(n); f = 34 + 150 * np.exp(-t / 0.30)
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.9)
    nz = lp(rng.randn(n), 700) * np.exp(-t / 0.3) * 0.9
    clunk = np.sin(2 * np.pi * 62 * t) * np.exp(-t / 0.05) * np.minimum(1, t * 400)
    return norm(x + nz + clunk)
def thump(f0=52, d=0.22):
    n = int(d * SR); t = tv(n)
    return (np.sin(2 * np.pi * (f0 + 12 * np.exp(-t / 0.04)) * t) * np.exp(-t / 0.055) + 0.35 * lp(rng.randn(n), 160) * np.exp(-t / 0.03)).astype(np.float32)
def riser(d=0.7):
    n = int(d * SR); t = tv(n); u = t / d
    nz = rng.randn(n).astype(np.float32); out = np.zeros(n, np.float32)
    for lo, hi in ((300, 900), (900, 2400), (2400, 6000)):
        out += bp(nz, lo, hi) * np.clip((u - (lo / 6000)) * 2.2, 0, 1)
    tone = np.sin(2 * np.pi * np.cumsum(200 + 1400 * u ** 2) / SR) * 0.5
    return norm((out * 0.7 + tone) * (u ** 1.7) * np.minimum(1, (d - t) * 60 + 0.0 + 1))
def death_hit():
    n = int(1.6 * SR); t = tv(n)
    boom = np.sin(2 * np.pi * (45 + 40 * np.exp(-t / 0.08)) * t) * np.exp(-t / 0.55)
    clu = sum(np.sin(2 * np.pi * f * t) for f in (311, 330, 466, 622)) * np.exp(-t / 0.5) * 0.18
    nz = bp(rng.randn(n), 200, 5000) * np.exp(-t / 0.12) * 0.9
    return norm(np.tanh(2.0 * (boom + clu + nz)))
def glitch_hit(d=0.6):
    n = int(d * SR); t = tv(n); nz = rng.randn(n).astype(np.float32)
    nz = np.round(nz * 6) / 6
    gate = (np.repeat(rng.rand(n // 600 + 2) > 0.45, 600)[:n]).astype(np.float32)
    sub = np.sin(2 * np.pi * np.cumsum(110 - 80 * t / d) / SR) * np.exp(-t / 0.3)
    return norm(bp(nz, 400, 7000) * gate * np.exp(-t / 0.35) * 0.8 + sub)
def rewind_sfx(d):
    n = int(d * SR); t = tv(n); u = t / d
    f = 160 * (1 + 10 * u ** 2); tone = np.sin(2 * np.pi * np.cumsum(f) / SR + 0.6 * np.sin(2 * np.pi * 13 * t))
    nz = bp(rng.randn(n), 600, 5200) * (0.5 + 0.5 * np.sin(2 * np.pi * 9 * t))
    flut = 1 + 0.3 * np.sin(2 * np.pi * 21 * t)
    env = np.minimum(1, t * 40) * np.minimum(1, (d - t) * 25)
    return norm((tone * 0.5 + nz * 0.6) * flut * env)
def monster_sting():
    n = int(1.8 * SR); t = tv(n)
    clu = sum(np.sin(2 * np.pi * f * t) for f in (233, 247, 349, 370, 587)) * np.exp(-t / 0.7) * 0.2
    scr = np.tanh(3 * np.sin(2 * np.pi * np.cumsum(2400 - 1500 * np.clip(t / 0.5, 0, 1)) / SR)) * np.exp(-t / 0.35) * 0.55
    sub = np.sin(2 * np.pi * 40 * t) * np.exp(-t / 0.7)
    nz = bp(rng.randn(n), 300, 6000) * np.exp(-t / 0.18)
    return norm(np.tanh(2.0 * (clu + scr + sub * 0.9 + nz * 0.7)))
def whoosh(d=0.2, g=1.0):
    n = int(d * SR); t = tv(n); return norm(bp(rng.randn(n), 900, 4200) * np.sin(np.pi * t / d) ** 2) * g
def step():
    n = int(0.25 * SR); t = tv(n); return norm(lp(rng.randn(n), 380) * np.exp(-t / 0.045) + np.sin(2 * np.pi * 70 * t) * np.exp(-t / 0.05))

# ---------------------------------------------------------------- voix
for s in SEGS:
    for l in s["lines"]:
        put(bus[l["kind"]], V[l["id"]], l["t0"], 1.0)

# ---------------------------------------------------------------- cues -> sfx
for s in SEGS:
    add(whoosh(0.22, 0.5), s["start"] - 0.05, 0.10)
    for c in s["cues"]:
        n, t = c["name"], c["t"]
        if n == "buzz": add(buzz(), t, 0.55, 0.1); add(ping(), t + 0.05, 0.2, 0.0)
        elif n == "msg": add(pop(), t, 0.35)
        elif n == "banner": add(ping(880, 1320, 0.09), t, 0.25)
        elif n == "blackout": add(powerdown(), t, 0.9)
        elif n == "knock": add(knock(int(t * 10)), t, 0.95, -0.35)
        elif n == "knock3":
            for i, d in enumerate((0, 0.3, 0.6)): add(knock(50 + i), t + d, 1.0, 0.3)
        elif n == "choice_show": add(whoosh(0.3, 0.8), t, 0.18)
        elif n == "choice_pick": add(pop(), t, 0.5)
        elif n == "voice_scare": add(riser(0.8), t - 0.8, 0.5)
        elif n == "death": add(death_hit(), t, 1.0)
        elif n == "rewind": add(rewind_sfx(s["end"] - s["start"] - 0.05), t, 0.55)
        elif n == "leave":
            add(step(), t, 0.25, -0.5); add(step(), t + 0.6, 0.18, -0.7); add(step(), t + 1.2, 0.12, -0.9)
        elif n == "monster": add(monster_sting(), t, 1.0)
        elif n == "glitch": add(glitch_hit(0.6), t, 0.9)
        elif n == "cta_reply": add(ping(), t, 0.22)
    for l in s["lines"]:
        if l["kind"] == "n":
            for w in l["words"]:
                if w["key"]: add(thump(70, 0.12), w["t0"], 0.14)

# battements de coeur
def heart(t0, t1):
    tt = t0
    while tt < t1:
        u = (tt - t0) / (t1 - t0); period = 60 / (62 + 44 * u)
        for off, g in ((0, 1.0), (period * 0.27, 0.65)): add(thump(), tt + off, 0.34 * g, 0)
        tt += period
heart(SEGBY["noir"]["start"] + 1.7, SEGBY["mort"]["start"])
heart(SEGBY["chambre1"]["start"], SEGBY["fin"]["start"] - 0.3)

# ---------------------------------------------------------------- drone
t = tv(N)
pad = (0.5 * np.sin(2 * np.pi * 55 * t + 0.8 * np.sin(2 * np.pi * 0.13 * t)) + 0.32 * np.sin(2 * np.pi * 82.41 * t + 0.6 * np.sin(2 * np.pi * 0.09 * t + 1)) +
       0.25 * np.sin(2 * np.pi * 116.5 * t + 0.5 * np.sin(2 * np.pi * 0.07 * t + 2)) + 0.12 * np.sin(2 * np.pi * 164.8 * t))
pad = np.tanh(pad * 1.5)
wind = lp(rng.randn(N).astype(np.float32), 380) * (0.55 + 0.45 * np.sin(2 * np.pi * 0.07 * t))
hi = np.sin(2 * np.pi * 1760 * t) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.23 * t))
KEY = dict(salon=(.22, .28), tel1=(.28, .32), noir=(.35, .6), porte=(.6, .65), choix=(.7, .78), judas=(.8, 1.0), mort=(0, 0), rewind=(.2, .25),
           chambre1=(.5, .58), tel2=(.5, .55), chambre2=(.6, 1.0), fin=(.35, .15))
xs, ys = [], []
for s in SEGS:
    a, b = KEY[s["id"]]; xs += [s["start"] + 0.001, s["end"] - 0.001]; ys += [a, b]
inten = np.interp(t, xs, ys).astype(np.float32)
mute = np.ones(N, np.float32); ms = SEGBY["mort"]; i0, i1 = int(ms["start"] * SR), int(ms["end"] * SR); mute[i0:i1] = 0
mute = lp(mute, 30, 1)
drone = (pad * 0.20 * (0.4 + 0.6 * inten) + wind * 0.10 * (0.6 + 0.4 * inten) + hi * 0.012 * inten ** 2) * mute
# coupure du drone au black-out
bo = [c["t"] for s in SEGS for c in s["cues"] if c["name"] == "blackout"][0]
duck_bo = np.ones(N, np.float32); duck_bo[int(bo * SR):int((bo + 1.4) * SR)] = 0.08; duck_bo = lp(duck_bo, 6, 1)
drone *= duck_bo

# ---------------------------------------------------------------- reverbs & mix
def make_ir(dur, seed, fc):
    r = np.random.RandomState(seed); n = int(dur * SR); ir = r.randn(n) * np.exp(-np.arange(n) / SR * 5.0 / dur)
    ir = lp(ir.astype(np.float32), fc); k = int(0.012 * SR); ir[:k] *= np.linspace(0, 1, k); return ir / np.sqrt((ir ** 2).sum())
def rv(x, dur, seed, fc=4200):
    return ss.fftconvolve(x, make_ir(dur, seed, fc))[:N].astype(np.float32), ss.fftconvolve(x, make_ir(dur, seed + 1, fc))[:N].astype(np.float32)

nL, nR = rv(bus["n"], 0.9, 1); vL, vR = rv(bus["v"], 1.8, 3, 2600); sL, sR = rv(bus["vs"], 2.6, 5, 2200)
mono_sfx = (sfxL + sfxR) * 0.5; xL, xR = rv(mono_sfx, 1.5, 7, 3600)
voiceL = 0.85 * bus["n"] * 0.707 + 0.12 * nL + 0.7 * bus["v"] * 0.9 + 0.35 * vL + 0.95 * bus["vs"] * 0.707 + 0.5 * sL
voiceR = 0.85 * bus["n"] * 0.707 + 0.12 * nR + 0.7 * bus["v"] * 0.5 + 0.35 * vR + 0.95 * bus["vs"] * 0.707 + 0.5 * sR
vox_env = lp(np.abs(bus["n"] + bus["v"] + bus["vs"]), 6, 1)
duck = 1 - 0.5 * np.clip(vox_env * 5, 0, 1)
L = voiceL + (sfxL + 0.16 * xL) * duck * 0.9 + drone * duck
R = voiceR + (sfxR + 0.16 * xR) * duck * 0.9 + drone * duck
end = TL["total"]; fade = np.clip((end + 0.5 - t) / 0.7, 0, 1); L *= fade; R *= fade
pk = max(np.abs(L).max(), np.abs(R).max())
L = np.tanh(L * 1.15) / np.tanh(1.15); R = np.tanh(R * 1.15) / np.tanh(1.15)
pk = max(np.abs(L).max(), np.abs(R).max()); g = 0.89 / pk
st = np.stack([L * g, R * g], axis=1)
wavfile.write(os.path.join(WORK, "mix.wav"), SR, (st * 32767).astype(np.int16))
print("OK", round(T, 2), "s  peak", round(float(pk), 2), "rms", round(float(np.sqrt((st ** 2).mean())), 3))
