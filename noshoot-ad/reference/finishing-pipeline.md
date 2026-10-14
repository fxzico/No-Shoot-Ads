# FINISHING PIPELINE — validated end-to-end x2 (Vadilal 2026-07-16 · HDFC 2026-07-26)
Raw Veo clips → Premiere-ready masters. ORDER FIXED: dewatermark at 1080p FIRST, upscale LAST
(upscaling first amplifies inpaint flaws; the upscaler smooths the healed patch on the way up).
Numbers below reproduced unchanged on a second project — they are project-independent
for Veo 1080p output.

## STAGE 0 — INTAKE + RENAME (the naming IS the pipeline)
1. Copy picks to `Final Videos\Shot_NN.mp4` — timeline shot numbers, span names for
   multi-shot plates (`Shot_07_09_OTS.mp4`). The name rides the whole chain:
   Shot_NN.mp4 → Shot_NN_clean.mp4 → To Be Edited\Shot_NN.mov. No rename step at the
   end, no mapping to lose.
2. **VERIFY THE MAPPING VISUALLY before spending GPU**: tile one frame per clip into
   a grid (`ffmpeg` scale+tile), confirm each file shows the shot its name claims.
   Gen filenames are model-authored and easy to misassign.
3. Multi-take shots: extract 4 frames/take, compare motion sanity, face/label drift,
   first-second cleanliness. Pick, log reason.

## STAGE 1 — DE-WATERMARK (ProPainter; ~60-70s per 4s clip, ~190s per 8s @1080p)
Veo spark shows EVEN ON paid Google AI Pro → this pass is standard for every clip.
0. **Coord check first (one ffmpeg pass)**: tile the bottom-right crop of the LAST
   frame of every clip into one grid — spark is faint early, obvious at the tail.
   Coords have been IDENTICAL across projects (1080p: patch 512@1408,568, spark
   ≈332,337 in patch, r≈55-60) but confirm before batching.
1. remove_watermark_hq.py (single or --batch). 8GB-validated: 512px patch, WHOLE-CLIP
   temporal window (subvideo_length=n≤120), neighbor 15, ref_stride 6, raft 32, fp16.
   GLITCH LESSON: seams/shimmer come from SHORT windows (40-frame default = seam every
   1.7s), NOT fp16. One window per clip = zero seams. fp32@640px = 12.6GB → OOM on 8GB.
2. QC gate: healed corner at first/mid/last frame, 2x zoom. Reject any smear/boil.

## STAGE 2 — UPSCALE + RETIME (Topaz Video AI; ~2min per 4s clip, ~4min per 8s)
Topaz ships ffmpeg.exe beside the GUI. Env: TVAI_MODEL_DIR + TVAI_MODEL_DATA_DIR → ProgramData.
Validated chain (= GUI "Upscale to 4K + 60fps", ProRes 422 Proxy):
`ffmpeg -i in.mp4 -vf "tvai_up=model=prob-3:scale=2:estimate=20,tvai_fi=model=apo-8:fps=60" -c:v prores_ks -profile:v 0 -pix_fmt yuv422p10le -c:a copy out.mov`
Output: 3840x2160 · 60fps · prores yuv422p10le · ~160MB per 4s clip → To Be Edited\Shot_NN.mov.
MODEL LESSON: Chronos chr-2 HALLUCINATES on macro texture → NEVER chr-2 for product macro.
Apollo apo-8 = clean. estimate=20 for stable Proteus.

## ⚠ GPU CONTENTION (cost 10min to learn — one job at a time)
ProPainter and Topaz both want the 4060. Overlapped: 70s clip → 690s (10x) and Topaz
stalled at 0.03x. The 8GB card fits exactly ONE of these at a time — run stages strictly
sequentially. Before starting Topaz, free ComfyUI's VRAM without restarting:
`POST http://127.0.0.1:8188/free {"unload_models":true,"free_memory":true}` (7.6GB → 819MB).

## STAGE 3 — PACK-SHOT COMPOSITE (labels can never be generated — Golden Rule 1)
1. 4x-UltraSharp upscale the real product photos.
2. SAM2 cutouts: GroundingDinoSAM2Segment(prompt="<product> cup", threshold=0.3,
   keep_model_loaded=true) → ORIGINAL image + mask → RGBA. (JoinImageWithAlpha can silently
   output empty alpha — verify at import.)
3. Stage: gen backgrounds read as "rooms" — PROCEDURAL gradient cyclorama wins (PIL: wall
   gradient + darker glossy floor + cove + warm radial key pool).
4. Composite: contact shadow (blurred ellipse) + flipped/darkened/faded reflection + cup. 4K still.
5. Motion: ffmpeg zoompan push-in (z='1+0.04*on/180' d=1 s=3840x2160 fps=60, oversized source)
   → ProRes 4K60. Or hand the still to the editor for a keyframed move.

## STAGE 4 — HANDOFF (the cut sheet is the contract)
To Be Edited\ = every Shot_NN.mov + `_CUT_SHEET.md` containing: master specs line
(3840x2160 · 60fps · ProRes 422 Proxy · source chain), file table (file / shot / source
clip / src dur / USE), the use-the-head rule, per-shot AE slot list, VO final paths +
measured durations, SFX map, timeline-fps note (60fps masters = slow-mo/tracking headroom,
cut at delivery fps), deliverables spec. Template: HDFC\Assets\To Be Edited\_CUT_SHEET.md.

## OPS
- S1+S2 as one background script (finish_pipeline.py), log to _pipeline_log.txt.
- RESTART ComfyUI before a ProPainter batch — stale relight session holds 7GB+ and OOMs it
  (mid-run, prefer the /free POST above).
- ffprobe "moov atom not found" on newest .mov = still writing; wait.
- Every stage gate: verify CONTENT (frames), not exit codes.
