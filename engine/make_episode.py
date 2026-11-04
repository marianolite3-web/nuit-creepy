# -*- coding: utf-8 -*-
"""python engine/make_episode.py stories/ep001.json out/ep001.mp4  -> vidéo complète (voix + son + image)."""
import sys, os, json, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
story, out = sys.argv[1], sys.argv[2]
work = os.path.abspath(os.environ.get("EP_WORK", "work")); os.makedirs(work, exist_ok=True); os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
shutil.copy(story, os.path.join(work, "story.json"))
env = dict(os.environ, EP_WORK=work)
def run(*a): subprocess.run([sys.executable, os.path.join(HERE, a[0])] + list(a[1:]), check=True, env=env, cwd=os.getcwd())
run("timeline.py"); run("sfx.py"); run("render_video.py")
tl = json.load(open(os.path.join(work, "timeline.json"))); T = tl["total"]
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", os.path.join(work, "video.mp4"), "-i", os.path.join(work, "mix.wav"), "-map", "0:v", "-map", "1:a",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-af", "afade=t=out:st=%.2f:d=0.9" % (T - 0.95), "-shortest", "-movflags", "+faststart", out], check=True)
print("EPISODE OK", out, "%.1fs" % T)
