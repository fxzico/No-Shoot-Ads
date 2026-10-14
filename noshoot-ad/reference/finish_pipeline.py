#!/usr/bin/env python
"""FINISHING ORCHESTRATOR — Vadilal (2026-07-16)
Stage 1: ProPainter HQ de-watermark (1080p, max quality)  -> *_clean.mp4
Stage 2: QC frame dumps of every healed corner            -> qc/ folder
Stage 3: Topaz TVAI 4K/60 ProRes 422 Proxy                -> To Be Edited/Clip_XX.mov
Progress -> _pipeline_log.txt (tail it anytime).
"""
import os, sys, glob, time, subprocess, json, urllib.request

V   = r"G:\GLM\No Shoot Ads\Icecream Ad\Assets\Final Videos"
OUT = r"G:\GLM\No Shoot Ads\Icecream Ad\Assets\To Be Edited"
QC  = os.path.join(V, "qc")
LOG = os.path.join(V, "_pipeline_log.txt")
HQ  = r"C:\Users\USER\.claude\skills\noshoot-ad\reference\remove_watermark_hq.py"
TVAI_FF = r"C:\Program Files\Topaz Labs LLC\Topaz Video AI\ffmpeg.exe"
os.environ["TVAI_MODEL_DIR"] = r"C:/ProgramData/Topaz Labs LLC/Topaz Video AI/models"
os.environ["TVAI_MODEL_DATA_DIR"] = r"C:/ProgramData/Topaz Labs LLC/Topaz Video AI/models"

# the picked takes (Clip_02 -> v2; 17 pending regen)
CLIPS = ["Clip_01","Clip_02_v2","Clip_03","Clip_04","Clip_07","Clip_08","Clip_09",
         "Clip_10","Clip_11","Clip_12","Clip_13","Clip_14","Clip_15","Clip_16","Clip_17"]

def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    open(LOG,"a",encoding="utf-8").write(line+"\n")

def run(cmd, **kw):
    return subprocess.run(cmd, check=True, capture_output=True, text=True, **kw)

def stage1_propainter():
    sys.path.insert(0, os.path.dirname(HQ))
    import importlib.util
    spec = importlib.util.spec_from_file_location("hq", HQ)
    hq = importlib.util.module_from_spec(spec); spec.loader.exec_module(hq)
    for c in CLIPS:
        src = os.path.join(V, c+".mp4"); dst = os.path.join(V, c+"_clean.mp4")
        if os.path.exists(dst): log(f"S1 skip {c} (done)"); continue
        t0=time.time()
        try:
            hq.clean(src, dst)
            log(f"S1 OK {c} ({int(time.time()-t0)}s)")
        except Exception as e:
            log(f"S1 FAIL {c}: {str(e)[:200]}")

def stage2_qc():
    os.makedirs(QC, exist_ok=True)
    for c in CLIPS:
        src = os.path.join(V, c+"_clean.mp4")
        if not os.path.exists(src): continue
        n = int(subprocess.check_output(["ffprobe","-v","error","-count_frames","-select_streams","v:0",
             "-show_entries","stream=nb_read_frames","-of","csv=p=0",src]).strip())
        for tag, fr in [("first",2),("mid",n//2),("last",n-3)]:
            out = os.path.join(QC, f"{c}_{tag}.png")
            subprocess.run(["ffmpeg","-v","error","-i",src,
                "-vf",f"select='eq(n\\,{fr})',crop=640:640:1280:440","-vsync","vfr",
                "-frames:v","1",out,"-y"],check=False)
    log("S2 QC corners dumped -> qc/")

def stage3_topaz():
    os.makedirs(OUT, exist_ok=True)
    for c in CLIPS:
        src = os.path.join(V, c+"_clean.mp4")
        if not os.path.exists(src): log(f"S3 skip {c} (no clean)"); continue
        final_name = ("Clip_02" if c=="Clip_02_v2" else c) + ".mov"
        dst = os.path.join(OUT, final_name)
        if os.path.exists(dst): log(f"S3 skip {c} (done)"); continue
        t0=time.time()
        try:
            run([TVAI_FF,"-hide_banner","-y","-i",src,
                 "-vf","tvai_up=model=prob-3:scale=2:estimate=20,tvai_fi=model=apo-8:fps=60",
                 "-c:v","prores_ks","-profile:v","0","-pix_fmt","yuv422p10le",
                 "-c:a","copy", dst])
            log(f"S3 OK {final_name} ({int((time.time()-t0)/60)}min)")
        except subprocess.CalledProcessError as e:
            log(f"S3 FAIL {c}: {(e.stderr or '')[-300:]}")

if __name__ == "__main__":
    log("=== PIPELINE START ===")
    stage1_propainter()
    stage2_qc()
    stage3_topaz()
    log("=== PIPELINE COMPLETE ===")
