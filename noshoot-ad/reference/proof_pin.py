#!/usr/bin/env python3
"""
Proof render: composites a test UI onto the tracked screen, using the exact
corner numbers AE will use. If this sticks, the AE corner pin will stick.

This is not a deliverable - it exists so the track can be trusted before
anyone opens After Effects. Renders a checkerboard + centre cross + tap flash
through the perspective transform onto the plate.

Writes _track/pin_proof.mp4
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
OUT = BASE / "_track" / "pin_proof.mp4"

VW, VH = 1280, 720
UW, UH = 216, 468          # test UI raster (matches 1080x2340 aspect)


def test_ui():
    """Checkerboard + border + centre cross. Any slip is instantly visible."""
    ui = np.zeros((UH, UW, 3), np.uint8)
    cell = 36
    yy, xx = np.mgrid[0:UH, 0:UW]
    chk = ((yy // cell) + (xx // cell)) % 2 == 0
    ui[chk] = (0, 76, 143)          # HDFC blue #004C8F
    ui[~chk] = (237, 35, 42)        # HDFC red  #ED232A
    b = 5
    ui[:b] = ui[-b:] = ui[:, :b] = ui[:, -b:] = (255, 255, 255)
    cy, cx = UH // 2, UW // 2
    ui[cy - 2:cy + 3, :] = (255, 255, 255)
    ui[:, cx - 2:cx + 3] = (255, 255, 255)
    ui[:14, :] = (255, 255, 255)    # solid top strip = orientation check
    return ui


def homography(src, dst):
    """Solve the 3x3 mapping dst_pixel -> src_pixel (inverse warp)."""
    A, b = [], []
    for (sx, sy), (dx, dy) in zip(src, dst):
        A.append([dx, dy, 1, 0, 0, 0, -sx * dx, -sx * dy])
        b.append(sx)
        A.append([0, 0, 0, dx, dy, 1, -sy * dx, -sy * dy])
        b.append(sy)
    h, *_ = np.linalg.lstsq(np.array(A, float), np.array(b, float), rcond=None)
    return np.append(h, 1.0).reshape(3, 3)


def main():
    if not TRACK.exists():
        sys.exit("run track_screen.py first")
    d = json.loads(TRACK.read_text())
    track = d["track"]
    sx_, sy_ = VW / d["master_res"][0], VH / d["master_res"][1]
    taps = {t["contact_frame"] for t in d["taps"]}
    ui = test_ui()

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
    ys, xs = np.mgrid[0:VH, 0:VW]
    ones = np.ones_like(xs, float)
    i = 0
    try:
        while True:
            raw = rd.stdout.read(n)
            if len(raw) < n:
                break
            frame = np.frombuffer(raw, np.uint8).reshape(VH, VW, 3).copy()
            if i < len(track):
                q = track[i]
                dst = [(q["tl"][0] * sx_, q["tl"][1] * sy_),
                       (q["tr"][0] * sx_, q["tr"][1] * sy_),
                       (q["br"][0] * sx_, q["br"][1] * sy_),
                       (q["bl"][0] * sx_, q["bl"][1] * sy_)]
                src = [(0, 0), (UW - 1, 0), (UW - 1, UH - 1), (0, UH - 1)]
                Hm = homography(src, dst)

                # bounding box of the quad - only warp what we must
                qx = [p[0] for p in dst]
                qy = [p[1] for p in dst]
                x0, x1 = max(0, int(min(qx)) - 2), min(VW, int(max(qx)) + 3)
                y0, y1 = max(0, int(min(qy)) - 2), min(VH, int(max(qy)) + 3)
                if x1 > x0 and y1 > y0:
                    sub_x = xs[y0:y1, x0:x1]
                    sub_y = ys[y0:y1, x0:x1]
                    sub_1 = ones[y0:y1, x0:x1]
                    den = Hm[2, 0] * sub_x + Hm[2, 1] * sub_y + Hm[2, 2] * sub_1
                    den[np.abs(den) < 1e-9] = 1e-9
                    u = (Hm[0, 0] * sub_x + Hm[0, 1] * sub_y + Hm[0, 2] * sub_1) / den
                    v = (Hm[1, 0] * sub_x + Hm[1, 1] * sub_y + Hm[1, 2] * sub_1) / den
                    inside = (u >= 0) & (u < UW - 1) & (v >= 0) & (v < UH - 1)
                    ui_px = ui[np.clip(v.astype(int), 0, UH - 1),
                               np.clip(u.astype(int), 0, UW - 1)]
                    region = frame[y0:y1, x0:x1]
                    region[inside] = ui_px[inside]
                    frame[y0:y1, x0:x1] = region
                if i in taps:
                    frame[:16, :] = (255, 255, 255)
            wr.stdin.write(frame.tobytes())
            i += 1
    finally:
        rd.stdout.close()
        wr.stdin.close()
        rd.wait()
        wr.wait()

    print(f"wrote {OUT}  ({i} frames)")
    print("checkerboard should sit ON the screen and stay locked to the bezels.")
    print("the thumb will be COVERED here - that is expected, this proof has no")
    print("key layer. In AE the keyed plate on top restores it.")


if __name__ == "__main__":
    main()
