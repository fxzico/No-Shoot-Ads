# COMFYUI FIX-LAYER — RTX 4060 / 8GB
Fix layer, never hero generator. Stills + very short clips only.
Path: `C:\Users\USER\Confy UI\ComfyUI_windows_portable\ComfyUI`

## 8GB RULES
SAM2 = base_plus (never large) · SD1.5 checkpoints (DreamShaper8) for relight, not SDXL ·
tiled upscale · no long video diffusion (Veo's job) · `--lowvram` if OOM.

## GRAPH A — Product-lock + relight (workhorse)
LoadImage(product) → Canny preprocessor → Apply ControlNet(control_canny fp16) →
IC-Light(iclight_sd15_fc) → SAM2(base_plus) mask → ImageCompositeMasked(onto plate) → Save.
Checkpoint DreamShaper8. Match IC-Light direction to the plate's key.

## TESTED API GRAPH — IC-Light FC relight (verified 2026-07-14)
CheckpointLoaderSimple(dreamshaper_8) · LoadImage → ImageScale(512x512 lanczos) → VAEEncode
(= foreground latent) · LightSource(position, start/end hex — sets key direction) ·
LoadAndApplyICLightUnet(iclight_sd15_fc) · CLIPTextEncode pos/neg ·
ICLightConditioning(pos, neg, vae, foreground, multiplier=0.182 — NO opt_background for FC!) ·
KSampler(patched model, latent=foreground latent, cfg 2.0, ~20 steps, dpmpp_2m_sde/karras)
→ VAEDecode → Save.
GOTCHAS:
- FC model + opt_background → "Input channels 12 does not match model in_channels 8" (fbc-only).
- DENOISE = LABEL SURVIVAL: 1.0 garbles ("Vadilal"→"Vadial"); ~0.45 seeded from encoded
  foreground = legible AND relit. For perfect labels add canny lock or comp original label in AE.
- Script: AppData/Local/Temp/claude-scratch-noshoot/iclight_test*.py

## GRAPH B — Cutout/roto for AE
LoadImage → SAM2(base_plus) mask → GrowMask(2-4px) → Save RGBA.
(Prompt-based: GroundingDinoSAM2Segment, threshold 0.3 — see finishing-pipeline.md Stage 3.)

## GRAPH C — Upscale (tiled)
LoadImage → Ultimate SD Upscale (tile 512, DreamShaper8, denoise 0.2). 4x-UltraSharp.pth installed.

## GRAPH D — Veo watermark removal (ProPainter, validated 2026-07-15)
Patch strategy (the 8GB trick): never feed full 1080p — crop 512x512 around the spark
(1080p Veo: patch x=1408 y=568, spark center ≈332,337 in patch, mask r=55), inpaint the patch,
ffmpeg overlay back.
Basic: remove_watermark.py (~1min/4s clip). HQ (STANDARD): remove_watermark_hq.py —
whole-clip temporal window, 512px fp16, neighbor 15, ref_stride 6, raft 32 (~70s/clip) —
see finishing-pipeline.md Stage 1.
Visible spark appears EVEN ON paid Google AI Pro (user-confirmed) → this pass is standard for
every delivered Veo clip. SynthID (invisible) remains — output still detectable as AI.

## INSTALLED / VERIFIED (2026-07-14)
torch 2.12.0+cu130, ComfyUI 0.26.2, RTX 4060 8188MiB. Custom nodes: controlnet_aux,
comfyui-ic-light, VHS, SAM2 x2, KJNodes, essentials. Models: dreamshaper_8 (2.0GB),
iclight_sd15_fc (full 1.72GB — old copy was truncated 1.1GB; validate: filesize =
8 + header_len + max tensor offset), control canny/depth fp16, SAM2 base_plus, 4x-UltraSharp.

## HEADLESS RUN
`cd "/c/Users/USER/Confy UI/ComfyUI_windows_portable" && ./python_embeded/python.exe -s ComfyUI/main.py --listen 127.0.0.1 --port 8188`
POST workflow JSON to `http://127.0.0.1:8188/prompt`. Outputs → ComfyUI/output/ (read back to confirm).
Batch across SKUs: agent loops the API per PNG.

## VERIFY
`nvidia-smi --query-gpu=name,memory.total --format=csv,noheader`
`ls .../ComfyUI/models/checkpoints` · `ls .../ComfyUI/custom_nodes`
