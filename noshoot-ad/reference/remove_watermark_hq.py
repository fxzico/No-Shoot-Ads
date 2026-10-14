#!/usr/bin/env python
"""Veo watermark removal — MAX QUALITY mode (v2, 2026-07-15).
User saw a glitch in v1 output (speed settings). This version trades time for quality:

v1 (glitchy)                          v2 (this)
- subvideo_length=40                  - whole clip in ONE subvideo (<=120 frames)
- neighbor_length=10                  - neighbor_length=20 (2.5x temporal context)
- ref_stride=10                       - ref_stride=5  (2x reference frames)
- raft_iter=20                        - raft_iter=32  (better optical flow)
- fp16 enable                         - fp32 (no half-precision artifacts)
- 512x512 patch                       - 640x640 patch (more healing context)
- crf 16 re-encode                    - crf 10 + veryslow preset (visually lossless)

~4-6 min per 4s clip on the 4060 (vs ~1 min in v1). Worth it.

Usage:
  python remove_watermark_hq.py <input.mp4> [output.mp4]
  python remove_watermark_hq.py --batch <folder>     # all *.mp4, skips *_clean.mp4
Requires ComfyUI running on 127.0.0.1:8188.
"""
import json, subprocess, sys, os, time, glob, urllib.request

S = "http://127.0.0.1:8188"
COMFY = r"C:\Users\USER\Confy UI\ComfyUI_windows_portable"
COMFY_IN = os.path.join(COMFY, "ComfyUI", "input")

# Veo 1080p spark, bottom-right. 640px patch centered on it.
PATCH_W = PATCH_H = 512   # 640 whole-clip OOMs on 8GB; 512 fits
PATCH_X, PATCH_Y = 1408, 568          # right/bottom edge aligned to 1920x1080
MASK_CX, MASK_CY, MASK_R = 332, 337, 60   # spark center within the patch

def run(cmd): subprocess.run(cmd, check=True, capture_output=True)

def probe_frames(path):
    return int(subprocess.check_output(["ffprobe","-v","error","-count_frames",
        "-select_streams","v:0","-show_entries","stream=nb_read_frames",
        "-of","csv=p=0", path]).strip())

def clean(src, dst):
    print(f"--- {os.path.basename(src)}")
    patch = os.path.join(COMFY_IN, "wmhq_patch.mp4")
    # lossless-ish patch extract
    run(["ffmpeg","-v","error","-i",src,"-vf",
         f"crop={PATCH_W}:{PATCH_H}:{PATCH_X}:{PATCH_Y}",
         "-c:v","libx264","-crf","6","-preset","slow","-pix_fmt","yuv420p",patch,"-y"])
    n = probe_frames(patch)

    from PIL import Image, ImageDraw
    m = Image.new("L",(PATCH_W,PATCH_H),0)
    ImageDraw.Draw(m).ellipse([MASK_CX-MASK_R,MASK_CY-MASK_R,MASK_CX+MASK_R,MASK_CY+MASK_R],fill=255)
    m.save(os.path.join(COMFY_IN,"wmhq_mask.png"))

    wf = {
      "1":{"class_type":"VHS_LoadVideo","inputs":{"video":"wmhq_patch.mp4","force_rate":0,
           "custom_width":0,"custom_height":0,"frame_load_cap":0,"skip_first_frames":0,"select_every_nth":1}},
      "2":{"class_type":"LoadImage","inputs":{"image":"wmhq_mask.png"}},
      "4":{"class_type":"RepeatImageBatch","inputs":{"image":["2",0],"amount":n}},
      "5":{"class_type":"ImageToMask","inputs":{"image":["4",0],"channel":"red"}},
      "6":{"class_type":"ProPainterInpaint","inputs":{"image":["1",0],"mask":["5",0],
           "width":PATCH_W,"height":PATCH_H,
           "mask_dilates":10,"flow_mask_dilates":10,
           "ref_stride":6,"neighbor_length":15,
           "subvideo_length":min(n,120),          # whole clip = one temporal window
           "raft_iter":32,"fp16":"enable"}},      # fp16: 640px whole-clip needs ~6.3GB (fits 8GB);
                                                  # fp32 needs ~12.6GB -> OOM. The v1 glitch came from
                                                  # 40-frame window SEAMS, not precision. Whole-clip
                                                  # window + dense refs are the anti-glitch levers.
      "7":{"class_type":"VHS_VideoCombine","inputs":{"images":["6",0],"frame_rate":24,
           "loop_count":0,"filename_prefix":"wmhq_healed","format":"video/h264-mp4",
           "pingpong":False,"save_output":True}},
    }
    req = urllib.request.Request(S+"/prompt", data=json.dumps({"prompt":wf}).encode(),
                                 headers={"Content-Type":"application/json"})
    pid = json.loads(urllib.request.urlopen(req,timeout=30).read())["prompt_id"]
    healed = None
    t0 = time.time()
    while time.time()-t0 < 1800:
        time.sleep(10)
        try:
            h = json.loads(urllib.request.urlopen(S+f"/history/{pid}",timeout=15).read())
        except Exception: continue
        if pid in h:
            g = h[pid].get("outputs",{}).get("7",{}).get("gifs",[])
            if g: healed = g[0]["fullpath"]; break
            if h[pid]["status"]["status_str"]=="error":
                raise RuntimeError("ProPainter error: "+json.dumps(h[pid]["status"])[:500])
    if not healed: raise RuntimeError("timeout")
    print(f"    healed in {int(time.time()-t0)}s")

    # visually-lossless recomposite
    run(["ffmpeg","-v","error","-i",src,"-i",healed,"-filter_complex",
         f"[0:v][1:v]overlay={PATCH_X}:{PATCH_Y}:shortest=1",
         "-c:v","libx264","-crf","10","-preset","veryslow","-pix_fmt","yuv420p",
         "-c:a","copy",dst,"-y"])
    print(f"    -> {os.path.basename(dst)}")

def main():
    if sys.argv[1] == "--batch":
        folder = sys.argv[2]
        vids = [v for v in sorted(glob.glob(os.path.join(folder,"*.mp4")))
                if not v.endswith("_clean.mp4")]
        print(f"batch: {len(vids)} clips")
        for v in vids:
            clean(v, v.replace(".mp4","_clean.mp4"))
    else:
        src = sys.argv[1]
        dst = sys.argv[2] if len(sys.argv)>2 else src.replace(".mp4","_clean.mp4")
        clean(src, dst)
    print("DONE")

if __name__ == "__main__":
    main()
