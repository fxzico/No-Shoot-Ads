#!/usr/bin/env python3
"""
Visual QC for the screen track: draws the solved quad onto the plate.

Green quad edges + corner crosshairs + frame/tap readout burned in. If the
outline sticks to the screen edges through all three taps, the track is good
and the corner-pin data is safe to use.

Writes _track/track_overlay.mp4
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / "Assets" / "To Be Edited"
SRC = BASE / "Shot_07_09_OTS.mov"
TRACK = BASE / "_track" / "screen_track.json"
OUT = BASE / "_track" / "track_overlay.mp4"

VW, VH = 1280, 720


def line(buf, p0, p1, col, w=2):
    """Bresenham-ish line via linear interpolation, thickened."""
    x0, y0 = p0
    x1, y1 = p1
    n = int(max(abs(x1 - x0), abs(y1 - y0)) * 2) + 2
    for t in np.linspace(0, 1, n):
        x, y = int(round(x0 + (x1 - x0) * t)), int(round(y0 + (y1 - y0) * t))
        for dy in range(-w, w + 1):
            for dx in range(-w, w + 1):
                px, py = x + dx, y + dy
                if 0 <= px < VW and 0 <= py < VH:
                    buf[py, px] = col


def cross(buf, p, col, r=9, w=2):
    x, y = int(round(p[0])), int(round(p[1]))
    line(buf, (x - r, y), (x + r, y), col, w)
    line(buf, (x, y - r), (x, y + r), col, w)


def main():
    if not TRACK.exists():
        sys.exit("run track_screen.py first")
    d = json.loads(TRACK.read_text())
    track = d["track"]
    sx, sy = VW / d["master_res"][0], VH / d["master_res"][1]
    tap_frames = {t["contact_frame"] for t in d["taps"]}
    tap_windows = [(t["start_frame"], t["end_frame"]) for t in d["taps"]]

    rd = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-i", str(SRC), "-vf", f"scale={VW}:{VH}",
         "-pix_fmt", "rgb24", "-f", "rawvideo", "-"],
        stdout=subprocess.PIPE, bufsize=VW * VH * 3 * 4)
    wr = subprocess.Popen(
        ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{VW}x{VH}", "-r", "60", "-i", "-",
         "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", str(OUT)],
        stdin=subprocess.PIPE)

    n = VW * VH * 3
    RED = np.array([255, 40, 40], np.uint8)
    CYAN = np.array([40, 255, 255], np.uint8)
    WHITE = np.array([255, 255, 255], np.uint8)

    i = 0
    try:
        while True:
            raw = rd.stdout.read(n)
            if len(raw) < n:
                break
            buf = np.frombuffer(raw, np.uint8).reshape(VH, VW, 3).copy()
            if i < len(track):
                q = track[i]
                pt = {k: (q[k][0] * sx, q[k][1] * sy) for k in ("tl", "tr", "br", "bl")}
                touching = any(a <= i <= b for a, b in tap_windows)
                col = RED if touching else CYAN
                for a, b in (("tl", "tr"), ("tr", "br"), ("br", "bl"), ("bl", "tl")):
                    line(buf, pt[a], pt[b], col, 2)
                for k in pt:
                    cross(buf, pt[k], WHITE, 9, 1)
                # frame counter: a simple bar whose length encodes progress
                barw = int(VW * (i / max(1, len(track) - 1)))
                buf[VH - 14:VH - 6, :barw] = CYAN
                if i in tap_frames:
                    buf[:18, :] = RED       # flash the top edge on contact
            wr.stdin.write(buf.tobytes())
            i += 1
    finally:
        rd.stdout.close()
        wr.stdin.close()
        rd.wait()
        wr.wait()

    print(f"wrote {OUT}  ({i} frames)")
    print("cyan quad = clean, red quad = thumb contact, red flash = tap frame")


if __name__ == "__main__":
    main()
