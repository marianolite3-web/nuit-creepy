# -*- coding: utf-8 -*-
"""Épisode du jour : choisit l'histoire suivante, génère la vidéo, publie (sauf mode test)."""
import os, sys, json, glob, argparse, datetime, subprocess
ap = argparse.ArgumentParser(); ap.add_argument("--mode", default="post", choices=["test", "post", "force"]); a = ap.parse_args()
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
stories = sorted(glob.glob(os.path.join(ROOT, "stories", "ep*.json")))
sp = os.path.join(ROOT, "state", "state.json")
state = json.load(open(sp)) if os.path.exists(sp) else {"next": 0, "last_date": "", "history": []}
today = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
key = os.environ.get("ZERNIO_API_KEY", "").strip()
posting = a.mode in ("post", "force") and bool(key)
if posting and a.mode == "post" and state.get("last_date") == today:
    print("Déjà publié aujourd'hui (%s) : rien à faire." % today); sys.exit(0)
if posting and a.mode == "post":
    sys.path.insert(0, HERE); from pacing import allowed_today
    ok, done, allowed = allowed_today(state.get("history", []), int(os.environ.get("MAX_PER_MONTH", "20") or 0), datetime.datetime.now(datetime.timezone.utc))
    if not ok:
        print("Rythme gratuit : %d posts ce mois (%d autorisés à ce jour) : on saute aujourd'hui." % (done, allowed)); sys.exit(0)
if a.mode in ("post", "force") and not key: print("Pas de clé ZERNIO_API_KEY : passage en mode test (rien ne sera publié).")
idx = state["next"] % len(stories); path = stories[idx]; sj = json.load(open(path))
out = os.path.join(ROOT, "out", os.path.basename(path).replace(".json", ".mp4")); os.makedirs(os.path.dirname(out), exist_ok=True)
print("Histoire : %s (%d/%d)" % (os.path.basename(path), idx + 1, len(stories)))
if os.environ.get("EP_DRY"):  # test rapide : mini vidéo factice
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "color=c=black:s=180x320:d=1", "-pix_fmt", "yuv420p", out], check=True)
else:
    subprocess.run([sys.executable, os.path.join(HERE, "make_episode.py"), path, out], check=True, cwd=ROOT)
caption = (sj.get("caption", "") + " " + sj.get("tags", "")).strip()
open(out.replace(".mp4", ".txt"), "w").write(caption)
if posting:
    sys.path.insert(0, HERE); import post
    res = post.publish(out, caption, ai_label=True)
    state["next"] += 1; state["last_date"] = today; state["history"] = (state.get("history", []) + [{"story": os.path.basename(path), "date": today}])[-60:]
    json.dump(state, open(sp, "w"), ensure_ascii=False, indent=1); print("PUBLIÉ.")
else:
    print("TEST : vidéo générée dans out/, rien publié.")
