#!/usr/bin/env python3
"""
Green-screen corner tracker + tap detector for the OTS phone plate.

Streams the master through ffmpeg, isolates the green screen per frame, solves
the 4 screen corners, and detects the thumb taps. Writes:
  - _track/screen_track.json     per-frame corners in master coords + tap times
  - _track/track_overlay.mp4     visual QC - solved quad drawn on the plate

WHY EDGE FITTING, NOT EXTREME POINTS
The thumb bites into the screen's bottom-right during each tap. Extreme-point
corner search follows the bite and the corner collapses inward (measured: 185px
of false travel). Instead we fit a line to each of the four edges and intersect
them. The thumb corrupts a minority of the points on two edges, so trimmed
least-squares rejects it and the corner stays put through the occlusion.

TAP DETECTION
Green pixel count drops when the thumb covers the screen. The dips are the taps.
Those frame numbers drive the UI ripple/button-press sync, so the graphics hit
on the same frame the thumb actually lands.

numpy only - no OpenCV.
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "Assets" / "To Be Edited" / "Shot_07_09_OTS.mov"
OUT = HERE.parent / "Assets" / "To Be Edited" / "_track"

AW, AH = 960, 540                 # analysis res
MASTER_W, MASTER_H = 3840, 2160
SCALE = MASTER_W / AW
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


def largest_blob(mask):
    h, w = mask.shape
    parent = {}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    labels = np.zeros((h, w), np.int32)
    nxt = 1
    for y in range(h):
        row = mask[y]
        if not row.any():
            continue
        xs = np.flatnonzero(row)
        splits = np.flatnonzero(np.diff(xs) > 1)
        starts = np.concatenate(([0], splits + 1))
        ends = np.concatenate((splits, [len(xs) - 1]))
        for s, e in zip(starts, ends):
            x0, x1 = xs[s], xs[e]
            above = labels[y - 1, x0:x1 + 1] if y > 0 else np.zeros(0, np.int32)
            hits = np.unique(above[above > 0])
            if len(hits) == 0:
                lab = nxt
                parent[lab] = lab
                nxt += 1
            else:
                lab = int(hits[0])
                for o in hits[1:]:
                    union(lab, int(o))
            labels[y, x0:x1 + 1] = lab
    if nxt == 1:
        return mask
    flat = np.zeros(nxt, np.int32)
    for lab in range(1, nxt):
        flat[lab] = find(lab)
    resolved = flat[labels]
    counts = np.bincount(resolved.ravel())
    counts[0] = 0
    return resolved == counts.argmax()


def fit_trimmed(u, v, keep=0.7, iters=4):
    """
    Robust line fit v = a*u + b via trimmed least squares.
    Drops the worst-residual points each pass so a thumb bite on part of an
    edge can't drag the line. Returns (a, b).
    """
    u = np.asarray(u, float)
    v = np.asarray(v, float)
    idx = np.arange(len(u))
    a, b = 0.0, float(v.mean()) if len(v) else 0.0
    for _ in range(iters):
        if len(idx) < 8:
            break
        a, b = np.polyfit(u[idx], v[idx], 1)
        res = np.abs(a * u + b - v)
        cut = max(8, int(len(u) * keep))
        idx = np.argsort(res)[:cut]
    return float(a), float(b)


def solve_top(mask):
    """
    Solve ONLY the top edge and the upper part of the left/right edges.

    The thumb rests low on the glass for most of the take, so the bottom edge
    and the lower side-edges are unusable - measuring them is what produced
    218px of false corner travel. The top 55% of the screen is never occluded
    (the plate was generated with 'thumb stays low, never covers centre'), so
    we fit there and reconstruct the bottom corners rigidly. Returns TL, TR and
    the edge direction vectors.
    """
    ys, xs = np.nonzero(mask)
    if len(xs) < 500:
        return None
    y0, y1 = ys.min(), ys.max()
    x0, x1 = xs.min(), xs.max()
    hgt, wid = y1 - y0, x1 - x0
    if hgt < 40 or wid < 20:
        return None

    # left/right edges from the CLEAN upper band only
    ry0, ry1 = int(y0 + hgt * 0.08), int(y0 + hgt * 0.55)
    rows, lx, rx = [], [], []
    for y in range(ry0, ry1 + 1):
        r = np.flatnonzero(mask[y])
        if len(r) < 5:
            continue
        rows.append(y)
        lx.append(r[0])
        rx.append(r[-1])
    if len(rows) < 20:
        return None
    al, bl = fit_trimmed(rows, lx)
    ar, br_ = fit_trimmed(rows, rx)

    # top edge from columns (first green pixel per column - never occluded)
    cx0, cx1 = int(x0 + wid * 0.08), int(x1 - wid * 0.08)
    cols, ty = [], []
    for x in range(cx0, cx1 + 1):
        c = np.flatnonzero(mask[:, x])
        if len(c) < 5:
            continue
        cols.append(x)
        ty.append(c[0])
    if len(cols) < 10:
        return None
    at, bt = fit_trimmed(cols, ty)

    def isect(a_side, b_side, a_edge, b_edge):
        den = 1.0 - a_side * a_edge
        if abs(den) < 1e-9:
            return None
        x = (b_side + a_side * b_edge) / den
        return [float(x), float(a_edge * x + b_edge)]

    tl = isect(al, bl, at, bt)
    tr = isect(ar, br_, at, bt)
    if tl is None or tr is None:
        return None
    # side-edge directions (unit, pointing down the screen)
    dl = np.array([al, 1.0]); dl /= np.linalg.norm(dl)
    dr = np.array([ar, 1.0]); dr /= np.linalg.norm(dr)
    return {"tl": tl, "tr": tr, "dl": dl.tolist(), "dr": dr.tolist(),
            "y_max": float(y1)}


def rigid_bottom(tops, ref_i):
    """
    Reconstruct BL/BR from the clean TL/TR by treating the screen as rigid.

    On the reference frame (the least-occluded one) we measure how far the
    bottom corners sit down each side edge, expressed as a multiple of the top
    edge length. That ratio is a property of the phone, not the frame, so we
    reapply it every frame. Occlusion then cannot move the bottom corners at
    all - they are implied by the top edge, which the thumb never touches.
    """
    ref = tops[ref_i]
    w_ref = np.linalg.norm(np.array(ref["tr"]) - np.array(ref["tl"]))
    # bottom of the green blob on the reference frame, projected onto each edge
    span = ref["y_max"] - ref["tl"][1]
    kl = (span / max(1e-6, ref["dl"][1])) / w_ref
    kr = (span / max(1e-6, ref["dr"][1])) / w_ref

    out = []
    for t in tops:
        tl = np.array(t["tl"]); tr = np.array(t["tr"])
        w = np.linalg.norm(tr - tl)
        bl = tl + np.array(t["dl"]) * (kl * w)
        br = tr + np.array(t["dr"]) * (kr * w)
        out.append({"tl": tl.tolist(), "tr": tr.tolist(),
                    "br": br.tolist(), "bl": bl.tolist()})
    return out, (kl + kr) / 2.0


def smooth(seq, win=5):
    if win < 2:
        return seq
    out = [{k: list(v) for k, v in f.items()} for f in seq]
    half = win // 2
    for k in ("tl", "tr", "br", "bl"):
        for axis in (0, 1):
            vals = np.array([f[k][axis] for f in seq], float)
            pad = np.pad(vals, half, mode="edge")
            sm = np.convolve(pad, np.ones(win) / win, mode="valid")
            for i, f in enumerate(out):
                f[k][axis] = float(sm[i])
    return out


def find_taps(areas):
    """Green area dips = thumb on glass. Return (start, min, end) frame runs."""
    a = np.array(areas, float)
    base = np.median(a)
    dip = (base - a) / base > 0.02       # >2% of the screen covered
    if not dip.any():
        return []
    idx = np.flatnonzero(dip)
    runs = np.split(idx, np.flatnonzero(np.diff(idx) > 4) + 1)
    taps = []
    for r in runs:
        if len(r) < 3:
            continue
        lo = int(r[0] + np.argmin(a[r[0]:r[-1] + 1]))
        taps.append({
            "start_frame": int(r[0]), "contact_frame": lo, "end_frame": int(r[-1]),
            "contact_sec": round(lo / FPS, 3),
            "max_cover_pct": round(float((base - a[r].min()) / base * 100), 1),
        })
    return taps


def main():
    if not SRC.exists():
        sys.exit(f"missing source: {SRC}")
    OUT.mkdir(parents=True, exist_ok=True)

    tops, areas, missing = [], [], []
    for i, f in enumerate(frames(SRC, AW, AH)):
        m = green_mask(f)
        areas.append(int(m.sum()))
        if m.sum() < 500:
            missing.append(i)
            tops.append(None)
            continue
        q = solve_top(largest_blob(m))
        if q is None:
            missing.append(i)
        tops.append(q)
        if i % 120 == 0:
            print(f"  frame {i}...", flush=True)

    last = next((c for c in tops if c), None)
    if last is None:
        sys.exit("no green screen found")
    for i, c in enumerate(tops):
        if c is None:
            tops[i] = dict(last)
        else:
            last = c

    # reference frame = most green visible = least thumb
    ref_i = int(np.argmax(areas))
    track, k_ratio = rigid_bottom(tops, ref_i)
    track = smooth(track, win=5)
    full = [{k: [v[0] * SCALE, v[1] * SCALE] for k, v in f.items()} for f in track]

    stats = {}
    for k in ("tl", "tr", "br", "bl"):
        xs = np.array([f[k][0] for f in full])
        ys = np.array([f[k][1] for f in full])
        stats[k] = {"x_range_px": round(float(xs.max() - xs.min()), 1),
                    "y_range_px": round(float(ys.max() - ys.min()), 1),
                    "mean": [round(float(xs.mean()), 1), round(float(ys.mean()), 1)]}

    taps = find_taps(areas)

    q0 = full[0]
    sw = float(np.linalg.norm(np.array(q0["tr"]) - np.array(q0["tl"])))
    sh = float(np.linalg.norm(np.array(q0["bl"]) - np.array(q0["tl"])))

    (OUT / "screen_track.json").write_text(json.dumps({
        "source": SRC.name, "frames": len(full), "fps": FPS,
        "master_res": [MASTER_W, MASTER_H], "analysis_res": [AW, AH],
        "reference_frame": ref_i, "height_over_width_ratio": round(k_ratio, 4),
        "screen_px_at_frame0": [round(sw, 1), round(sh, 1)],
        "screen_aspect": round(sh / sw, 4),
        "dropout_frames": missing, "movement": stats, "taps": taps,
        "green_area_px": areas, "track": full,
    }, indent=1))

    print(f"\ntracked {len(full)} frames, {len(missing)} dropouts")
    print(f"reference frame (least occluded): {ref_i}")
    print("corner travel across the 8s take (master px, 3840 wide):")
    for k, v in stats.items():
        print(f"  {k}:  x {v['x_range_px']:6.1f}   y {v['y_range_px']:6.1f}")
    print(f"\nscreen at frame 0: {sw:.0f} x {sh:.0f} px, aspect {sh / sw:.3f}")
    print(f"detected {len(taps)} thumb taps:")
    for i, t in enumerate(taps, 1):
        print(f"  tap {i}: contact frame {t['contact_frame']:3d} "
              f"= {t['contact_sec']:5.2f}s   covers {t['max_cover_pct']:.0f}% of screen")
    print(f"\nwrote {OUT / 'screen_track.json'}")


if __name__ == "__main__":
    main()
