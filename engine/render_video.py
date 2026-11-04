# -*- coding: utf-8 -*-
"""Rend les images [a,b) en mp4 (ffmpeg). Sans argument : toute la vidéo -> work/video.mp4"""
import sys, subprocess, time, os
from render import *
N = int(TL["total"] * FPS) + 1
a = int(sys.argv[1]) if len(sys.argv) > 1 else 0
b = min(int(sys.argv[2]), N) if len(sys.argv) > 2 else N
out = sys.argv[3] if len(sys.argv) > 3 else os.path.join(WORK, "video.mp4")
cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
       "-c:v", "libx264", "-preset", "veryfast", "-crf", "24", "-g", "30", "-pix_fmt", "yuv420p", out]
p = subprocess.Popen(cmd, stdin=subprocess.PIPE); t0 = time.time()
for i in range(a, b): p.stdin.write(render_frame(i / FPS).tobytes())
p.stdin.close(); p.wait()
print("RENDER OK", a, b, "frames", N, "en %.0fs" % (time.time() - t0))
