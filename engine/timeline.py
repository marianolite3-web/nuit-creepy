# -*- coding: utf-8 -*-
"""story.json -> timeline.json + voices.npz (voix FR Piper, alignement mot à mot)."""
import json, io, wave, re, sys, os
import numpy as np, scipy.signal as ss
from piper import PiperVoice
from piper.config import SynthesisConfig

SR = 44100
WORK = os.environ.get("EP_WORK", "work")
MODEL = os.environ.get("PIPER_MODEL", "assets/fr-siwis-medium.onnx")
story = json.load(open(os.path.join(WORK, "story.json")))
voice = PiperVoice.load(MODEL, config_path=MODEL + ".json")

def synth(text, ls=1.1):
    cfg = SynthesisConfig(length_scale=ls, noise_scale=0.55, noise_w_scale=0.7)
    buf = io.BytesIO()
    with wave.open(buf, "wb") as w: voice.synthesize_wav(text, w, syn_config=cfg)
    buf.seek(0)
    with wave.open(buf, "rb") as r:
        a = np.frombuffer(r.readframes(r.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        assert r.getframerate() == 22050
    return ss.resample_poly(a, 2, 1).astype(np.float32)

def trim(a, thr=0.012, pad=0.02):
    idx = np.where(np.abs(a) > thr)[0]
    if len(idx) == 0: return a
    return a[max(0, idx[0] - int(pad * SR)): min(len(a), idx[-1] + int(pad * SR))]
def bq(kind, fc, order=2): return ss.butter(order, np.array(fc) / (SR / 2), kind)
def stretch(a, f):
    from math import gcd
    up, down = int(round(100 / f)), 100; g = gcd(up, down)
    return ss.resample_poly(a, up // g, down // g).astype(np.float32)
def norm(a, peak=0.9):
    m = np.abs(a).max(); return a / m * peak if m > 0 else a

def proc(kind, a):
    a = trim(a)
    if kind == "n":
        b, aa = bq("high", 70); a = ss.lfilter(b, aa, a)
        b, aa = bq("low", 260); a = a + 0.35 * ss.lfilter(b, aa, a)
        return norm(np.tanh(a * 1.8) / np.tanh(1.8), 0.9)
    if kind == "v":
        a1 = stretch(a, 0.93); a2 = stretch(a, 0.86); d = int(0.014 * SR)
        out = np.zeros(max(len(a1), len(a2) + d), np.float32); out[:len(a1)] += a1 * 0.8; out[d:d + len(a2)] += a2 * 0.5
        b, aa = bq("high", 170); out = ss.lfilter(b, aa, out)
        b, aa = bq("low", 1700, 3); out = ss.lfilter(b, aa, out)
        out = np.tanh(out * 2.2) / np.tanh(2.2)
        return norm(out[:len(a1) + d], 0.8)
    if kind == "vs":
        a1 = stretch(a, 0.74); a2 = stretch(a, 0.5)
        out = np.zeros(len(a2), np.float32); out[:len(a1)] += a1 * 0.85; out += a2 * 0.55
        b, aa = bq("low", 3200, 3); out = ss.lfilter(b, aa, out)
        out = np.tanh(out * 2.5) / np.tanh(2.5)
        return norm(out[:len(a1) + int(0.1 * SR)], 0.95)
    raise ValueError(kind)

def speech_spans(a, win=0.01, thr_rel=0.05, min_gap=0.11):
    n = int(win * SR); env = np.sqrt(np.convolve(a ** 2, np.ones(n) / n, "same"))[::n]
    sp = env > env.max() * thr_rel; spans, s = [], None
    for i, v in enumerate(sp):
        if v and s is None: s = i
        if not v and s is not None: spans.append([s * win, i * win]); s = None
    if s is not None: spans.append([s * win, len(sp) * win])
    merged = []
    for q in spans:
        if merged and q[0] - merged[-1][1] < min_gap: merged[-1][1] = q[1]
        else: merged.append(q)
    return merged

def tokens_of(text):
    toks = []
    for i, p in enumerate(text.split("*")):
        for w in p.split():
            if not re.search(r"\w", w) and toks: toks[-1] = (toks[-1][0] + w, toks[-1][1]); continue
            toks.append((w, i % 2 == 1))
    return toks
def clean_caption(w):
    w = re.sub(r"[,.:;…]+$", "", w).strip(); w = re.sub(r"^[«»\"]+|[«»\"]+$", "", w); return w.upper()
def phon_weight(w):
    t = re.sub(r"[^\w'’-]", "", w) or w
    try: return max(2, sum(len(s) for s in voice.phonemize(t)))
    except Exception: return max(2, len(t))
def align_words(text, a):
    toks = tokens_of(text); spans = speech_spans(a); total = sum(e - s for s, e in spans)
    wts = np.array([phon_weight(w) for w, _ in toks], float); cum = np.concatenate([[0], np.cumsum(wts)]) / wts.sum() * total
    def real(c, end):
        acc = 0
        for s, e in spans:
            L = e - s
            if c < acc + L - 1e-9 or (end and c <= acc + L + 1e-9): return s + (c - acc)
            acc += L
        return spans[-1][1]
    return [dict(w=clean_caption(w), key=k, t0=real(cum[i], False), t1=real(cum[i + 1], True)) for i, (w, k) in enumerate(toks)]

# ----------------------------------------------------------------- histoire -> segments
def clock_secs(s): h, m, x = [int(v) for v in s.split(":")]; return h * 3600 + m * 60 + x
def clock_str(x): x = int(x) % 86400; return "%02d:%02d:%02d" % (x // 3600, (x // 60) % 60, x % 60)
st = story; P = st["places"]; EV = st["clock"]["event"]; HK = st["clock"]["hook"]
C = lambda base, off: clock_str(clock_secs(base) + off)
S = []
def seg(id, scene, loc, clock, events, tail=0.3, **kw): S.append(dict(id=id, scene=scene, loc=loc, clock=clock, events=events, tail=tail, **kw))

seg("salon", "salon", P["hook"], HK, [("wait", 0.7), ("say", "n", st["hook"][0]), ("say", "n", st["hook"][1]), ("wait", 0.3)], tail=0.2)
ev = [("do", "buzz"), ("wait", 0.9), ("say", "n", st["buzz"][0]), ("say", "n", st["buzz"][1])]
for i, r in enumerate(st["rules"]):
    ev += [("do", "msg", dict(who=st["group"]["sender"], text=r[0], **({"key": True} if i == len(st["rules"]) - 1 else {}))), ("say", "n", r[1])]
seg("tel1", "phone", P["hook"], C(HK, 9), ev + [("wait", 0.5)], tail=0.2)
seg("noir", "salon", P["hook"], C(EV, -4), [("say", "n", st["blackout"]), ("wait", 0.25), ("do", "blackout"), ("wait", 1.5),
    ("do", "knock"), ("wait", 0.75), ("do", "knock"), ("wait", 0.75), ("do", "knock"), ("wait", 0.9), ("say", "n", st["knocks"]), ("wait", 0.3)], tail=0.2, blackout=True)
seg("porte", "door", P["door"], C(EV, 14), [("wait", 0.3), ("say", "v", st["voice"]), ("wait", 0.2), ("say", "n", st["who"]),
    ("do", "banner", dict(who=st["contra"][0], text=st["contra"][1])), ("say", "n", st["contra"][2]), ("wait", 0.5)], tail=0.1)
seg("choix", "door", P["door"], C(EV, 31), [("do", "choice_show"), ("say", "n", st["ask"]), ("wait", 0.7), ("do", "choice_pick", dict(i=0)), ("wait", 0.25),
    ("say", "n", st["pick"]), ("wait", 0.3)], tail=0.1, banner_keep=True)
seg("judas", "peephole", P["door"], C(EV, 38), [("say", "n", st["peep"][0]), ("wait", 0.35), ("say", "n", st["peep"][1]), ("wait", 0.35),
    ("say", "n", st["peep"][2]), ("wait", 0.55), ("do", "voice_scare"), ("say", "vs", st["scare"]), ("wait", 0.1)], tail=0.0)
seg("mort", "death", P["door"], C(EV, 47), [("do", "death"), ("wait", 1.25)], tail=0.0)
seg("rewind", "rewind", "", C(EV, 47), [("do", "rewind"), ("wait", 0.25), ("say", "n", "On *rembobine*."), ("wait", 0.9)], tail=0.0, rewind_from="judas_end", rewind_to="choix_start")
seg("chambre1", "bedroom", P["bed"], C(EV, 31), [("do", "choice_show"), ("say", "n", st["retry"]), ("do", "choice_pick", dict(i=1)), ("wait", 0.7),
    ("do", "knock"), ("wait", 0.9), ("do", "knock"), ("wait", 1.5), ("do", "leave"), ("say", "n", st["leave"]), ("wait", 1.0)], tail=0.1)
seg("tel2", "phone", P["bed"], C(EV, 64), [("do", "buzz"), ("wait", 0.85), ("say", "n", st["buzz"][0]),
    ("do", "msg", dict(who=st["twist"][0], text=st["twist"][1], key=True)), ("say", "n", st["twist"][2]), ("wait", 0.6)], tail=0.1, phone2=True)
seg("chambre2", "bedroom2", P["bed"], C(EV, 75), [("say", "n", st["end"][0]), ("wait", 0.6), ("do", "knock3"), ("wait", 1.25),
    ("do", "monster"), ("say", "n", st["end"][1]), ("wait", 0.55), ("do", "glitch"), ("wait", 0.55)], tail=0.0)
seg("fin", "cta", "", "", [("wait", 0.4), ("say", "n", st["cta"][0]), ("wait", 0.2), ("do", "cta_reply"), ("say", "n", st["cta"][1]), ("wait", 1.4)], tail=0.0)

cursor = 0.0; timeline = dict(segments=[], total=0.0); audio = {}; n_line = 0
for sd in S:
    seg_start = cursor; cues, lines = [], []; t = seg_start
    for e in sd["events"]:
        k = e[0]
        if k == "wait": t += e[1]
        elif k == "do": cues.append(dict(name=e[1], t=t, **(e[2] if len(e) > 2 else {})))
        elif k == "say":
            kind, text = e[1], e[2]; dry = proc(kind, synth(text.replace("*", ""))); words = align_words(text, dry)
            for w in words: w["t0"] += t; w["t1"] += t
            dur = len(dry) / SR; lid = f"l{n_line:02d}"; n_line += 1; audio[lid] = dry
            lines.append(dict(id=lid, kind=kind, text=text.replace("*", ""), t0=t, t1=t + dur, words=words)); t += dur + (0.16 if kind == "n" else 0.1)
    end = t + sd["tail"]
    d = dict(id=sd["id"], scene=sd["scene"], loc=sd["loc"], clock=sd["clock"], start=seg_start, end=end, cues=cues, lines=lines)
    for k in ("blackout", "banner_keep", "phone2", "rewind_from", "rewind_to"):
        if k in sd: d[k] = sd[k]
    timeline["segments"].append(d); cursor = end
timeline["total"] = cursor
byid = {s["id"]: s for s in timeline["segments"]}
for s in timeline["segments"]:
    if s["scene"] == "rewind": s["src_from"] = byid["judas"]["end"] - 0.05; s["src_to"] = byid["choix"]["start"] + 0.2
json.dump(timeline, open(os.path.join(WORK, "timeline.json"), "w"), ensure_ascii=False, indent=1)
np.savez_compressed(os.path.join(WORK, "voices.npz"), **audio)
print("TIMELINE OK  durée %.2fs  lignes %d" % (timeline["total"], n_line))
