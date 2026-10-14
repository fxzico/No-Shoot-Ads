#!/usr/bin/env python
"""Veo watermark removal — ProPainter patch pipeline (validated 2026-07-15).
Usage:  python remove_watermark.py <input.mp4> [output.mp4]
Assumes: ComfyUI running on 127.0.0.1:8188 with ProPainter + VHS nodes,
watermark = Veo spark in bottom-right (default patch/mask coords below).
Strategy: crop a 512x512 patch around the mark -> ProPainter video inpaint
(temporal fill) -> overlay the healed patch back. Full-res untouched elsewhere.
"""
import json, subprocess, sys, os, time, urllib.request

S = "http://127.0.0.1:8188"
COMFY = r"C:\Users\USER\Confy UI\ComfyUI_windows_portable"
COMFY_IN  = os.path.join(COMFY, "ComfyUI", "input")
COMFY_OUT = os.path.join(COMFY, "ComfyUI", "output")

# Veo 1080p spark location (bottom-right). Patch top-left + mask center in patch coords.
PATCH_X, PATCH_Y, PATCH_W, PATCH_H = 1408, 568, 512, 512
MASK_CX, MASK_CY, MASK_R = 332, 337, 55

def run(cmd): subprocess.run(cmd, check=True)

def main():
    src = sys.argv[1]
    dst = sys.argv[2] if len(sys.argv) > 2 else src.replace(".mp4", "_clean.mp4")

    # 1) crop patch
    patch = os.path.join(COMFY_IN, "wm_patch.mp4")
    run(["ffmpeg","-v","error","-i",src,"-vf",f"crop={PATCH_W}:{PATCH_H}:{PATCH_X}:{PATCH_Y}",
         "-c:v","libx264","-crf","12","-pix_fmt","yuv420p",patch,"-y"])

    # 2) frame count (mask must repeat once per frame)
    n = int(subprocess.check_output(["ffprobe","-v","error","-count_frames","-select_streams","v:0",
         "-show_entries","stream=nb_read_frames","-of","csv=p=0",patch]).strip())

    # 3) mask
    from PIL import Image, ImageDraw
    m = Image.new("L",(PATCH_W,PATCH_H),0)
    ImageDraw.Draw(m).ellipse([MASK_CX-MASK_R,MASK_CY-MASK_R,MASK_CX+MASK_R,MASK_CY+MASK_R],fill=255)
    m.save(os.path.join(COMFY_IN,"wm_mask.png"))

    # 4) ProPainter graph
    wf = {
      "1":{"class_type":"VHS_LoadVideo","inputs":{"video":"wm_patch.mp4","force_rate":0,
           "custom_width":0,"custom_height":0,"frame_load_cap":0,"skip_first_frames":0,"select_every_nth":1}},
      "2":{"class_type":"LoadImage","inputs":{"image":"wm_mask.png"}},
      "4":{"class_type":"RepeatImageBatch","inputs":{"image":["2",0],"amount":n}},
      "5":{"class_type":"ImageToMask","inputs":{"image":["4",0],"channel":"red"}},
      "6":{"class_type":"ProPainterInpaint","inputs":{"image":["1",0],"mask":["5",0],
           "width":PATCH_W,"height":PATCH_H,"mask_dilates":8,"flow_mask_dilates":8,
           "ref_stride":10,"neighbor_length":10,"subvideo_length":40,"raft_iter":20,"fp16":"enable"}},
      "7":{"class_type":"VHS_VideoCombine","inputs":{"images":["6",0],"frame_rate":24,"loop_count":0,
           "filename_prefix":"wm_removed_patch","format":"video/h264-mp4","pingpong":False,"save_output":True}},
    }
    req = urllib.request.Request(S+"/prompt", data=json.dumps({"prompt":wf}).encode(),
                                 headers={"Content-Type":"application/json"})
    pid = json.loads(urllib.request.urlopen(req,timeout=30).read())["prompt_id"]
    print("queued", pid)

    healed = None
    for _ in range(240):
        time.sleep(5)
        h = json.loads(urllib.request.urlopen(S+f"/history/{pid}",timeout=15).read())
        if pid in h:
            g = h[pid].get("outputs",{}).get("7",{}).get("gifs",[])
            if g: healed = g[0]["fullpath"]; break
            if h[pid]["status"]["status_str"]=="error": sys.exit("ProPainter error: "+json.dumps(h[pid]["status"])[:800])
    if not healed: sys.exit("timed out")

    # 5) overlay healed patch back at original position
    run(["ffmpeg","-v","error","-i",src,"-i",healed,"-filter_complex",
         f"[0:v][1:v]overlay={PATCH_X}:{PATCH_Y}:shortest=1",
         "-c:v","libx264","-crf","16","-pix_fmt","yuv420p","-c:a","copy",dst,"-y"])
    print("CLEAN:", dst)

if __name__ == "__main__":
    main()
