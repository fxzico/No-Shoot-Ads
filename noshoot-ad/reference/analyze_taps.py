#!/usr/bin/env python3
"""
Thumb-tip analysis + screen colour sampling for the OTS plate.

Green-area coverage turned out to be a weak tap signal (2-4% swings - that is
the thumb drifting across the glass, not necessarily contacting). Thumb TIP
HEIGHT is the real signal: during a tap the thumb extends UP into the screen,
so the topmost non-green intrusion rising from the bottom edge spikes.

Also samples the true screen green (median of the clean interior) so Keylight
gets the measured colour instead of a guessed one.

Updates _track/screen_track.json in place with:
  thumb_tip[]        per-frame tip height, 0 = bottom of screen, 1 = top
  taps[]             re-derived from tip peaks
  screen_colour      measured RGB + hex for Keylight's Screen Colour
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

AW, AH = 960, 540
FPS = 60.0


def frames(path, w, h):
    cmd = ["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"scale={w}:{h}",
           "-pix_fmt", "rgb24", "-f", "rawvideo", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, bufsize=w * h * 3 * 4)
    n = w * h * 3
    try:
        while True:
            buf = p.stdout.read(n)
            if len(buf) < n:
                break
            yield np.frombuffer(buf, np.uint8).reshape(h, w, 3)
    finally:
        p.stdout.close()
        p.wait()


def green_mask(f):
    r = f[:, :, 0].astype(np.int16)
    g = f[:, :, 1].astype(np.int16)
    b = f[:, :, 2].astype(np.int16)
    return (g - np.maximum(r, b) > 45) & (g > 90)


def quad_mask(q, w, h):
    """
    Boolean mask of the screen interior, inset slightly to dodge edge fringe.
    Corners run tl->tr->br->bl which in image coords (y down) is a positive
    winding, so the interior is the non-negative side of every edge.
    """
    c = (q["tl"] + q["tr"] + q["br"] + q["bl"]) / 4.0
    pts = [c + (q[k] - c) * 0.94 for k in ("tl", "tr", "br", "bl")]
    ys, xs = np.mgrid[0:h, 0:w]
    inside = np.ones((h, w), bool)
    for i in range(4):
        a, b = pts[i], pts[(i + 1) % 4]
        cross = (b[0] - a[0]) * (ys - a[1]) - (b[1] - a[1]) * (xs - a[0])
        inside &= cross >= 0
    return inside


def main():
    if not TRACK.exists():
        sys.exit("run track_screen.py first")
    d = json.loads(TRACK.read_text())
    track = d["track"]
    sc = AW / d["master_res"][0]          # master -> analysis scale

    tips, covers, samples = [], [], []
    for i, f in enumerate(frames(SRC, AW, AH)):
        if i >= len(track):
            break
        q = {k: np.array(track[i][k]) * sc for k in ("tl", "tr", "br", "bl")}
        g = green_mask(f)

        # sample the clean interior for the screen colour (upper-middle, never
        # occluded) - small box ~30% down the screen centreline
        top_mid = (q["tl"] + q["tr"]) / 2
        bot_mid = (q["bl"] + q["br"]) / 2
        p = top_mid + (bot_mid - top_mid) * 0.30
        x, y = int(p[0]), int(p[1])
        box = f[max(0, y - 6):y + 7, max(0, x - 6):x + 7].reshape(-1, 3)
        if len(box):
            samples.append(np.median(box, axis=0))

        # thumb = anything inside the screen quad that is not green
        inside = quad_mask(q, AW, AH)
        intrusion = inside & ~g
        area = inside.sum()
        covers.append(round(float(intrusion.sum() / max(1, area)), 4))

        # tip height: how far UP the screen the intrusion reaches, 0..1.
        # Project intruding pixels onto the screen's own vertical axis so the
        # measure is independent of the phone's tilt.
        ys_i, xs_i = np.nonzero(intrusion)
        if len(ys_i) > 40:
            axis = bot_mid - top_mid
            L2 = float(axis @ axis)
            t = ((xs_i - top_mid[0]) * axis[0] + (ys_i - top_mid[1]) * axis[1]) / max(1e-6, L2)
            tips.append(round(float(1.0 - np.percentile(t, 3)), 4))
        else:
            tips.append(0.0)
        if i % 120 == 0:
            print(f"  frame {i}...", flush=True)

    tips_a = np.array(tips)
    # smooth, then find peaks that clear the local baseline
    k = np.ones(5) / 5
    sm = np.convolve(np.pad(tips_a, 2, mode="edge"), k, mode="valid")
    base = np.percentile(sm, 25)
    thr = base + max(0.04, (sm.max() - base) * 0.45)

    taps, i = [], 1
    while i < len(sm) - 1:
        if sm[i] >= thr and sm[i] >= sm[i - 1] and sm[i] > sm[i + 1]:
            j = i
            while j < len(sm) - 1 and sm[j + 1] >= thr:
                j += 1
            peak = i + int(np.argmax(sm[i:j + 1]))
            taps.append({
                "contact_frame": int(peak),
                "contact_sec": round(peak / FPS, 3),
                "tip_height": round(float(sm[peak]), 3),
                "start_frame": int(i), "end_frame": int(j),
            })
            i = j + 6
        else:
            i += 1

    col = np.median(np.array(samples), axis=0).astype(int)
    hexcol = "#%02X%02X%02X" % tuple(col)

    d["thumb_tip"] = tips
    d["thumb_cover"] = covers
    d["taps"] = taps
    d["tap_threshold"] = round(float(thr), 4)
    d["screen_colour"] = {"rgb": [int(c) for c in col], "hex": hexcol,
                          "normalised": [round(float(c) / 255, 4) for c in col]}
    TRACK.write_text(json.dumps(d, indent=1))

    print(f"\nscreen green measured: {hexcol}  rgb{tuple(int(c) for c in col)}")
    print(f"peak thumb coverage of screen: {max(covers) * 100:.1f}%")
    print(f"thumb-tip baseline {base:.3f}, tap threshold {thr:.3f}")
    print(f"\n{len(taps)} taps from thumb-tip peaks:")
    for n, t in enumerate(taps, 1):
        print(f"  tap {n}: frame {t['contact_frame']:3d} = {t['contact_sec']:5.2f}s "
              f"  tip reaches {t['tip_height'] * 100:.0f}% up the screen")

    print("\nthumb-tip curve (1 col = 8 frames, height up the screen):")
    for s in range(0, len(sm), 8):
        v = sm[s:s + 8].max()
        mark = " <-- TAP" if any(s <= t["contact_frame"] < s + 8 for t in taps) else ""
        print(f"{s:4d} {s / 60:5.2f}s |{'#' * int(v * 60):<42}| {v:.2f}{mark}")


if __name__ == "__main__":
    main()
