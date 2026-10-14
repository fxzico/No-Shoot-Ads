# PIPELINE PLAYBOOK — the master checklist (any brand, any topic)
Validated twice end-to-end: Vadilal (product/food, 2026-07-16) and HDFC XpressWay
(finance/people, 2026-07-26). Follow the phases IN ORDER. Each phase names its
detailed reference file — load that file when you reach the phase.

THE ONE-LINE PIPELINE:
VO first → prompts (still + JSON motion) → Nano Banana stills → Veo i2v →
rename to Shot_NN at intake → ProPainter de-watermark → Topaz 4K60 ProRes →
cut sheet → AE (scripted comps + screen replace) → Premiere conform → grade/mix
→ 9:16 rebuild → export.

## PHASE 0 — PROJECT SCAFFOLD (5 min, do it before anything creative)
Create the standard folder tree — every later step assumes these names:
```
<Project>\
  SCRIPT.md            the story, beat by beat (plain English)
  PRODUCTION.md        timeline bible: timecode table, VO durations, workflow order
  shot-prompts.md      one block per generation (image prompt + motion JSON + USE + CHECK)
  AE-BUILD.md          polish spec for every AE comp (what the script can't decide)
  AE-SCRIPT.jsx        ExtendScript that builds all AE comps (reference/ae-automation.md)
  DOWNLOADS.md         fonts/logos/SFX to fetch, with URLs
  VO\                  generate_vo.py + .env + out\ (final\ = locked takes)
  Generations\Images\  raw Nano Banana picks, per shot
  Generations\Video\   raw Veo/Omni downloads (model-named, pre-rename)
  Assets\Brand\        official logo SVG/PNG
  Assets\Fonts\        campaign fonts (install before AE scripts)
  Assets\SFX\          pulled from D:\ashis dar pack
  Assets\To Be Edited\ finished 4K60 ProRes masters + _CUT_SHEET.md (Premiere imports THIS)
  Tools\               project-specific python (tracker etc.)
  Reference\           reference-ad frames, badge/logo screenshots
```

## PHASE 1 — CREATIVE LOCK (before any generation)
1. Pick the reference ad (pacing/energy ONLY — original compositions, legal rule).
   User supplies frames/timecodes → build the shot table in PRODUCTION.md.
2. Write SCRIPT.md: story in one line, then beat-by-beat table (time / see / hear).
3. LOCK THE PALETTE: 2–3 brand hex codes + white. Write "PALETTE LOCK" into every
   doc header. Flood the SET in the dominant brand color (the branded-not-stock
   trick); accent color = pops only. Wardrobe neutral. Success states = brand
   color, never green if green isn't brand.
4. Decide the vignette structure: separate strangers per shot beats one recurring
   cast (each shot can fail/regen alone). Face-match only where unavoidable —
   generate the tighter shot FIRST, feed its pick as ref to the wider one.
5. People-ad doctrine: characters NEVER speak on camera (mouths closed, VO = inner
   voice) → zero lip-sync risk. All phone/TV screens gen as SOLID GREEN → AE replace.
6. NO readable text in any gen (finance version of the label rule): no signage,
   posters, UI, logos. ALL type is AE. Text sneaks in → regen, don't fix.

## PHASE 2 — VO FIRST (before video; picture conforms to VO rhythm)
Full steps: reference/vo-pipeline.md. Summary:
1. Copy VO\generate_vo.py template, edit the LINES list to the new script.
2. `python generate_vo.py --audition` → pick voices per role by ear.
3. Generate → `--qc` (auto tail-clip check + silence trim) → user ear-locks each
   take → locked WAVs COPIED into out\final\ (never blind-regen: takes vary per run).
4. Measure real durations → rewrite PRODUCTION.md timecode table to the WAVs.
   Rule: one narrator can't overlap itself; sum of lines + breathing room = the
   real cut length. Fight for air, not compression.
5. Premiere: lay VO + music FIRST, mark shot boundaries on the VO track.

## PHASE 3 — SHOT PROMPTS (write ALL before generating ANY)
Full format: reference/prompt-recipes.md (§BENCHMARK LOOK, §JSON MOTION).
Per shot, shot-prompts.md carries exactly four parts:
1. IMAGE — long Nano Banana prompt. Must bake in the four benchmark-look forcers
   (designed set / cinematic light / depth layers / rich color + polish) and the
   global rules (palette flood, no text, mouth closed, middle-column framing, skin
   texture).
2. MOTION — the canonical 8-field JSON (description / camera / motion /
   consistency / negative_prompt / audio / duration_seconds / aspect_ratio).
   duration ≥4s always; speech always "none"; music always "none".
3. USE — plain line outside the JSON: which portion the edit keeps ("first 1.5s
   @25fps"). Never put trim intent inside the JSON.
4. CHECK — shot-specific reject list the user QCs against before accepting.
Also write the GENERATION ORDER list: hero-face shots first (they feed refs),
the long/risky master gen early, independents in any order, hardest-faces last
with extra variants (families melt).

## PHASE 4 — STILLS (Nano Banana Pro)
1. Follow generation order. 3–4 variants per shot minimum; families/multi-face 4+.
2. Label-critical product visible → feed the real product PNG as reference
   (Golden Rule 1). Face continuity → feed the picked still of the anchor shot.
3. QC each still vs its CHECK line + failure-modes-qc.md at 100% zoom:
   fingers, pores (no pores = plastic = reject), text-free, palette held.
4. Save picks: Generations\Images\Shot <n> V<x>.jpeg. The still IS the casting —
   don't animate a frame you wouldn't frame.

## PHASE 5 — VIDEO (Veo 3 image-to-video, Omni backup)
1. Attach the picked still + paste the motion JSON verbatim. NEVER text-to-video.
2. 3–4 variants where motion is risky; Omni after 2 Veo fails.
3. Green-screen phone shots: screen must stay flat green the whole take —
   negatives carry "screen changing colour, UI appearing, green flickering,
   reflections crossing" (reference/screen-replace.md).
4. QC via frame extraction (ffmpeg 6-frame strip): drift check first vs last.
   Veo's head is cleanest — that's why USE lines cut from the head.
5. Download picks → Generations\Video\ (keep the model's filename for now).

## PHASE 6 — RENAME AT INTAKE (before any processing)
Copy picks to Final Videos\Shot_NN.mp4 (span names for multi-shot plates:
Shot_07_09_OTS.mp4). The name rides the whole chain unchanged:
Shot_NN.mp4 → Shot_NN_clean.mp4 → To Be Edited\Shot_NN.mov — no mapping to lose.
VERIFY THE MAPPING VISUALLY before spending GPU: tile one frame per clip into a
grid (ffmpeg), confirm each file shows the shot its name claims. Gen filenames
are model-authored and easy to misassign.

## PHASE 7 — FINISHING (the fixed chain; full: reference/finishing-pipeline.md)
Order is FIXED: de-watermark at 1080p FIRST, upscale LAST.
1. ProPainter de-watermark every Veo clip (spark shows even on paid AI Pro).
   Check watermark coords first: tile last-frame bottom-right crops of all clips.
2. Topaz: prob-3 2x + apo-8 60fps → 3840x2160 60fps ProRes 422 Proxy.
3. ONE GPU JOB AT A TIME — ProPainter and Topaz both want the 4060; overlapping
   them is 10x slower. Free ComfyUI VRAM (POST /free) before Topaz.
4. QC gates between stages: healed corners at 2x zoom, content-verify frames.
Output: Assets\To Be Edited\Shot_NN.mov masters.

## PHASE 8 — CUT SHEET (the Premiere handoff contract)
Write Assets\To Be Edited\_CUT_SHEET.md — the editor (you, next week) opens ONLY
this: master specs line, file table (file / shot / source / duration / USE),
use-the-head rule, per-shot AE slot list, VO final paths + durations, SFX map,
timeline-fps note, deliverables. Template: HDFC\Assets\To Be Edited\_CUT_SHEET.md.

## PHASE 9 — AFTER EFFECTS (scripted builds + hand polish)
Full steps: reference/ae-automation.md + reference/screen-replace.md.
1. Install campaign fonts FIRST (AE reads them at script run).
2. Run AE-SCRIPT.jsx → builds every graphics comp (badge, lockups, floating
   cards, phone UI screens, kinetic text, end card) with safe() isolation —
   failures list per-comp, successes survive.
3. Phone screens: run the tracker chain (track_screen.py → analyze_taps.py →
   make_ae_track.py), QC pin_proof.mp4, then AE-SCRIPT-OTS.jsx builds the
   corner-pinned + Keylight-thumb comps automatically.
4. Hand work the scripts can't do: import brand SVG, product cut-outs into
   card placeholders, roto for behind-subject text, Keylight clip black/white
   by eye, Deep Glow on text/UI (0.15–0.25), light wrap.
5. AE-BUILD.md is the polish spec — timing, easing (25fps-native: 10f moves,
   5f micro), shadows, per-comp notes.

## PHASE 10 — EDIT / GRADE / MIX (Premiere)
1. Sequence at 60fps (masters' rate) or 25fps conformed — the 60fps masters
   exist for slow-mo headroom and AE tracking, not because the cut needs 60.
2. Conform cuts to the VO track laid in Phase 2; cuts land on music beats.
3. Grade (Looks): warmth lives in FOOTAGE only; graphics stay strict palette.
   Match all gens to the warmest shot.
4. Grain: subtle 35mm overlay on GENERATED shots only (unifies AI plastic) —
   never on UI/end-card comps. RSMB never on text layers (halos).
5. Mix: VO ducking, SFX from D:\ashis dar pack (whoosh per fly-in, UI ticks,
   OTP chime, success ding, impact hit on end card). Music: no-copyright pool,
   beat-map markers BEFORE conforming.
6. QC vs failure-modes-qc.md + timing <0.1s per shot.

## PHASE 11 — DELIVERABLES
16:9 1920x1080 master + 9:16 1080x1920 REBUILD (reframe gens — middle column
was kept safe; REBUILD text/UI comps natively at 1080x1920, never crop text).
More ratios (1:1, 4:5) per brand pack. h264/aac for delivery; ProRes stays archive.

## DOES THIS SHOT NEED COMFYUI? (unchanged decision tree)
Label drifted and must stay legible → lock. Light mismatch with plate → IC-Light.
Cutout needed → SAM2 roto. Soft/low-res → tiled upscale. Otherwise no — Veo/AE.

## SESSION END
Append learnings to evolution-log.md. Recipe proves itself twice → promote here.
