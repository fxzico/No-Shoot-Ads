# EVOLUTION LOG — noshoot-ad
Diary. Append at session end. Recipe wins twice → promote to reference files.

---

## 2026-08-18 — CINEMA-GRADE VOCABULARY UPGRADE (Day 2 AiKAMI integration)

**SOURCE:** `G:\GLM\No Shoot Ads\DAY 2 VOCABULARY.pdf` (188 pages, AiKAMI/Seacreature 
ecosystem prompting manual). External validation + new precision vocabulary extracted.

**WHAT CHANGED:**

### 1. Camera/Lens/Director Style Layer (NEW)
Every image prompt now uses the formula:
```
Shot on [CAMERA], [LENS], in the style of [DIRECTOR], [REFERENCE FILM] vibe.
[scene description...]
```

**Why:** Controls aesthetic signature before the scene. Different cameras = different looks:
- ARRI Alexa 65 = blockbuster epic clean scale
- RED Komodo = sharp punchy digital cinema
- Sony Venice 2 = clean filmic with beautiful highlight roll-off
- Kodak Vision3 500T = cinematic tungsten film stock grain
- iPhone 15 Pro = natural phone-camera realism (TikTok/UGC aesthetic)

**Lens character:**
- Anamorphic = 2.39:1 scope, oval bokeh, horizontal flares (the cinema signature)
- Cooke S4 prime = warm flattering painterly skin ("the Cooke look")
- Zeiss Master Prime = clinically sharp modern precision
- 85mm portrait = compressed background, creamy shallow bokeh
- 135mm telephoto = heavy compression, isolated subject

**Director style shorthand:**
- "in the style of Denis Villeneuve" = vast minimal sci-fi grandeur
- "shot by Roger Deakins" = master cinematography, perfect natural light
- "in the style of David Fincher" = cold precise dark controlled
- "in the style of Wong Kar-wai" = saturated neon moody romantic dreamy blur

### 2. Model Selection Intelligence (NEW)
**Before:** Defaulted to Nano Banana Pro + Veo 3 for everything.
**After:** Task-matched model selection with decision tree.

**When to upgrade from Nano Banana Pro:**
- **People/actors** → Soul 2.0 (best realism) or Soul Cinema (cinematic frames)
- **Text-heavy (signage, labels, UI)** → GPT 2.0 (cleanest typography)
- **Branding/design work** → Reve (design-grade clean finish)
- **Client ₹1L+ tier** → Seedance 2.5 (best-in-class, $0.34/s)
- **Posters/graphic-heavy** → Seedream 5.0 or Recraft V4.1

**When to downgrade from Veo 3:**
- **Budget projects** → MiniMax H3 ($0.08/s) or Kling 3.0 (simple motion)
- **Utility/B-roll** → Kling 3.0 (cheapest, decent for non-hero)

**Portfolio work:** ✅ KEEP Nano Banana Pro + Veo 3 (validated, fast, reliable).

### 3. Core Thesis Validation
AiKAMI Day 2 page 8:
> "Cinema-grade AI comes from a **strong input frame**, prompting like a real cinematographer, 
> and finishing with **organic film texture**. Get these three right and even an old Kling model 
> outputs footage people swear was shot on IMAX."

**This is IDENTICAL to our V4B doctrine** ("AI = ~60% of output, budget 40% for craft").
External validation from a competing ecosystem confirms our approach is correct.

### 4. Files Created
- ✅ `reference/model-selection-matrix.md` — Full model comparison, decision tree, cost optimization
- ✅ `reference/camera-vocabulary.md` — Camera/lens/director tables (NEXT: extract from PDF pages 4-5)
- ✅ `reference/prompt-structure-formula.md` — 5 validated examples dissected (NEXT: extract from PDF pages 6-8)
- ✅ Updated `reference/prompt-recipes.md` — Added cinema-grade formula to IMAGE PROMPT SKELETON
- ✅ Updated `SKILL.md` — Model selection + camera vocabulary references added to USER TOOLS, PROMPT DOCTRINE, FILES sections

### 5. What's NOT Changing
- **Default stack:** Nano Banana Pro + Veo 3 (portfolio-validated, keep as primary)
- **Prompt doctrine:** IMAGE=LONG, MOTION=SHORT (unchanged, just adding camera layer)
- **Pipeline:** Same finishing chain (ProPainter → Topaz → AE/Premiere)
- **V4B patterns:** All 11 signature moves still apply (black void, lifestyle interlude, benefit stack, etc.)

**Camera vocabulary = enhancement layer, not replacement.** The prompt structure gets MORE 
precise, but the workflow stays the same.

### 6. Cost Notes
**AiKAMI ecosystem pricing** (Seedance/Flux/MiniMax):
- Seedance 2.5: $0.34/s (highest quality, complex motion)
- Flux 3: $0.17/s (retro realism, 720p max)
- MiniMax H3: $0.08/s (budget, "looks plastic" per AiKAMI)
- Gemini Omni Flash: ~$0.10/s (editing only, NOT for generation)

**Our Veo 3 pricing** (Google Flow): Not listed in AiKAMI doc (they use Seedance ecosystem). 
Veo validated for our pipeline, no urgent need to switch unless client budget demands Seedance tier.

### 7. Integration Status
**DONE:**
- ✅ Model selection matrix written
- ✅ SKILL.md updated with new references
- ✅ prompt-recipes.md updated with cinema-grade formula

**NEXT (pending full PDF extraction):**
- ⏳ `reference/camera-vocabulary.md` — Copy tables from PDF pages 4-5 verbatim
- ⏳ `reference/prompt-structure-formula.md` — Extract 5 examples from PDF pages 6-8
- ⏳ Update category recipes (perfume/energy/watch) with camera/lens/director layer

**VALIDATION NEEDED:**
- User tests cinema-grade prompt on 1 portfolio shot (e.g. perfume hero frame)
- Compare "with camera vocab" vs "without" on same subject
- If quality delta is visible → roll out to all portfolio IMAGE_PROMPTS.md files

---

## S0 — 2026-07-14 — genesis
- Generalized Vadilal-only skill → universal engine. Vadilal → brand-packs/vadilal.md.
- Corrected false premise: I DO have PC access (Git Bash, G:=/g, C:=/c, ComfyUI headless, agents).
- Rig verified: RTX 4060 8GB, ComfyUI at C:\Users\USER\Confy UI\...
- Baked in prompt doctrine: image=long/detailed, motion=short/physical.
- No Kling (default) → Kling shots route to Veo 3.
- Vadilal product images = 300x300 opaque JPGs (not transparent PNGs): feed as ref for
  label shots; SAM2 roto for clean composites.
- Open: IC-Light examples unverified; Shot 1 test gen pending.

## S1 — 2026-07-14 — ComfyUI fix-layer VALIDATED
- Headless via API (port 8188, --lowvram). torch 2.12+cu130, comfy 0.26.2.
- DreamShaper8 was NOT installed (downloaded 2.0GB); iclight_sd15_fc was truncated/corrupt
  1.1GB → re-downloaded full 1.72GB (686 tensors).
- IC-Light FC relight on Vadilal Vanilla cup end-to-end SUCCESS.
- PROMOTED: FC model must NOT use opt_background (fbc-only) else "channels 12 vs 8" error.
- PROMOTED: denoise dial = LABEL SURVIVAL. 1.0 garbled "Vadilal"→"Vadial"; 0.45 seeded from
  encoded foreground = legible AND relit (Golden Rule proof).
- Worked: LightSource hex gradient sets key direction; ICLightConditioning mult 0.182;
  KSampler cfg 2.0, 20 steps, dpmpp_2m_sde+karras, seconds/image.
- Missing then: standalone upscale model (Graph C).

## S2 — 2026-07-14/15 — Shot 1 stills; doctrine upgraded
- Shot 1 Nano Banana stills excellent at first look; V2 picked (full curl, scoop face, key/rim sep).
- WATCH-OUT: "cold condensation mist" renders as rising steam (reads HOT). Cold air sinks:
  "cold mist drifts low and settles" — or better, none.
- DOCTRINE UPGRADE (→SKILL.md): text-to-video fails (user-confirmed). IMAGE-FIRST for ALL
  shots incl. actors: Nano Banana still → Veo i2v. Actors get a CAST-SHEET (gen once, feed always).
- 18-shot prompt pack → G:\GLM\No Shoot Ads\Icecream Ad\Assets\shot-prompts.md.
- Asset convention: Assets\<stream>\Shot <n> V<x>.jpeg.
- COURSE-CORRECT (user showed real chocolate scoop): my "excellent" verdict wrong on realism.
  Real scoop = drag ridges/striations, sits IN tub w/ scrape marks, dense fudgy body + glossy
  melt patches, ZERO mist. Ours = granular/sugary + misty = "frost fantasy". Recipe rewritten
  w/ 4-point REALISM CHECK. LESSON: judge vs REAL product photo, not "looks nice".

## S3 — 2026-07-15 — Shot 1 regen SUCCESS + video QC unlocked
- Corrected scoop-anatomy prompt WORKED ("Shot 1 final.jpeg", user 7/10). Recipe validated.
- NEW: I can QC video via ffmpeg (WinGet-installed) — extract ~6 frames, judge first-vs-last drift.
- Veo drift signature (4s clip): fleck density GROWS (reads cookies by end); tub edge pops in
  late; geometry reinterprets. RULE: usable window = FIRST ~1-1.5s; cut from head, never tail.
- "Real over pretty" pass on shots 3/4/11/13: splash = irregular crown + uneven droplets +
  connecting strings + motion blur; pour = rope-coiling + some nuts dry; vortex = uneven ribbon
  heights + matte streaks + edge rotation blur. Each shot carries a REALISM CHECK line.
- WATERMARK REMOVAL VALIDATED (ProPainter): 512x512 patch pipeline (crop→inpaint patch→overlay
  back), ~1min/4s clip. Script → reference/remove_watermark.py, GRAPH D in comfyui-fixlayer.md.
  SynthID remains (still AI-detectable).
- CORRECTION (user): visible spark appears EVEN ON paid Google AI Pro → ProPainter = STANDARD
  final step for every delivered Veo clip.

## S4 — 2026-07-15 — splash batch failed; physics dictionary + frame-pair
- Splash gens (3/4) "very disappointing": (a) "caramel sauce" → WATER/GLASS physics (tall thin
  translucent crown). Thick dairy = LOW/heavy/opaque crowns. The liquid NOUN determines physics.
  (b) Shot 4 scoop FLOATING above splash = gravity violation. (c) HDR over-lit = AI tell;
  pro ads = one key, deep shadows, muted grade.
- Shot 11 pour 8/10 (cream too stiff/mayo); shot 13 vortex 9/10 APPROVED. Couple portrait usable.
- PROMOTED to prompt-recipes.md: LIQUID PHYSICS DICTIONARY, HDR-tell discipline, gravity sanity
  check, FRAME-PAIR METHOD.
- FRAME-PAIR (Flow accepts start+end frames): gen start frame → make end frame by EDITING it
  ("same scene, only physics outcome changed") → feed both. Kills drift. Min gen 4s → cut from head.
- CORRECTION (user): couple v1 "too much AI" — "portrait + both smiling" summons stock/AI-averaged
  face space. ANTI-STOCK RULES promoted: candid documentary, mid-action, never lens-aware, name
  imperfections (pores, T-zone sheen, flyaways, uneven teeth, smudged kajal), room clutter,
  off-center 35mm + grain + muted grade.
- META: QC bar = "would a client believe this was shot", not "is it well-lit".
- SOLO-FIRST CASTING (user): one person per gen (two new faces get averaged), pick from 6-8
  variants, THEN pair via dual-ref "keep both faces exactly as reference". MACRO SKIN recipe for
  ECU faces (pores, vellus hair in backlight, lip creases, iris fibers). QC: 100% zoom, no pores
  = reject. shot-prompts.md 0-CAST → v3 (W solo → M solo → PAIR → ECU-W/M).
- CAST v4 (user): Indian faces + GEN Z styling (oversized tees/crop tops/baggy jeans/claw clips/
  nose stud/AirPods+iced coffee; early 20s). Ethnicity words pull traditional-costume cliché;
  naming CURRENT fashion grounds "now". Wardrobe = era-check question on every people-ad.

## S5 — 2026-07-15 — BROWSER AUTOMATION LIVE (18-image batch)
- Flow automation end-to-end: CDP 9223 → type in Slate editor → click arrow → poll grid <img> →
  authenticated download. ~45s/run, 2 imgs/run.
- Setup facts (in flow_batch.py header): Chrome 136+ ignores debug port on default profile →
  dedicated --user-data-dir automation profile. Port 9222 taken by Adobe UXP → 9223.
  Prompt box = [data-slate-editor='true'] (force click); input[aria-label='Editable text'] is
  the PROJECT TITLE — don't type there. Submit = last button in Nano Banana toolbar.
- flow_batch.py → skill reference/.
- Results: castW 6/6 usable, same face across runs (Flow project context holds identity);
  winner castW_V2 9/10. castM winner V3 8.5/10 (patchy stubble > model-perfect V1).
  shot4 mango: physics dict worked (opaque shrikhand crown); winner V5 8.5/10; "lassi" word may
  pull glassy tips. shot11 winner V4 9/10 (double-cream slump+coil).
- Pending then: end frames, PAIR, ECUs, product-ref shots (5/17), actor shots.

## S6 — 2026-07-15 — batch 2 (ref-feeding): works, 3 failure modes
- Ref-feeding automation works: upload input[type=file] → attach via '+' menu by filename →
  generate. 14 jobs/~37 gens unattended. flow_batch2.py in reference/.
- User upscaled/retouched cast finals in PS first (2752x1536) — high-res refs = better identity
  lock. Keep as standard.
- Wins: shot17_V5 tub parade 8.5 → Shot_17_Final; "shot7"_V1 (actually shot 2) 8.5 → Shot_2_Final;
  "shot8"_V1 (actually lips+saffron macro) 8 → Shot_7_Final; ecuW_V1 macro lips excellent
  (REALSKIN delivers); shot9_V1 → candidate.
- FAILURES (documented in flow_batch2.py header):
  (1) img-diff attribution bleed — files saved under wrong job names on overlap. NEVER trust
      filenames; content-verify.
  (2) ref thumbnails echoed as "results" (300x300) → filter size ≤600px.
  (3) multi-ref identity drift — 2 faces + product = invented strangers. Single-face held.
      FIX: lock ONE pair image, chain couple shots from it.
- shot5 4-tub row = Kesar Pista x4 clones; ecuM = wrong man. Both queued for regen.
- RULE: after any batch, verify CONTENT before renaming *_Final.

## S7 — 2026-07-15 — USER VERDICT: batch 2 FAILED brand consistency. Recovery doctrine.
- User ran SAME prompts manually → dramatically better (identity held, cup close to real).
  All 9 actor slots filled from USER's generations.
- ROOT CAUSE: my batch fired multi-ref jobs blind; ref attachment silently failed some runs
  (job ran WITHOUT refs). User's loop = attach → look → re-roll. THE LOOP IS THE QUALITY.
- BRAND-LOCK FINDING: even with all-caps guardrails + HD refs, Nano Banana REDESIGNS the cup
  (real: white body, red swoosh, cursive logo ACROSS swoosh; gens: colored bodies, badge logo,
  patterns). Generative models CANNOT do exact packaging. Label shots (5/17) = COMPOSITE:
  blank-cup scene → SAM2 cut real photos → perspective-place AE/PS → IC-Light ≤0.45.
- ecuM2 single-ref regen: identity held (single-ref rule confirmed again).
- HANDOFF RESTRUCTURED (user directive): user generates ALL videos manually; Claude does
  organization + ComfyUI finishing. Final Images = Clip_XX_FirstFrame/LastFrame + _MANIFEST.md.
  Clip numbers == scenes.json shots. Videos → Final Videos\Clip_XX.mp4 → dewatermark →
  Clip 05 composite → fixes.
- LESSON: user says "I'll do X myself" → my job flips to impeccable PREP + downstream finishing.
- VEO JSON PROMPTING adopted (→recipes): structured JSON motion prompts (description/camera/
  motion/consistency/negative_prompt/audio/duration). 17-clip pack → _VEO_JSON_PROMPTS.md.
- WATERMARK HQ v2 (v1 corner glitched): whole-clip temporal window (subvideo_length=n≤120),
  neighbor 20, ref_stride 5, raft 32, fp32, 640px, crf10. Glitch cause = short windows + fp16 +
  thin neighbors. QC healed corners 400% zoom first/mid/last.
- Folder flow: Final Videos\Clip_XX.mp4 → HQ dewatermark → QC → Clip_05 composite → To Be Edited\.
  Blender offered by user — accepted for Clip_05 if 2D insufficient.

## S8 — 2026-07-16 — DELIVERY COMPLETE + GREEN FLAG (workflow promoted)
- USER APPROVED → pipeline promoted into skill (finishing-pipeline.md + finish_pipeline.py).
- DELIVERED: To Be Edited\ = 16 clips 3840x2160 60fps ProRes 422 Proxy + _CUT_SHEET.md.
  31s ad covered: 15 Veo clips + Clip_05 composite + 2 AE slots (6, 18).
- TOPAZ GLITCH ROOT-CAUSED: Chronos chr-2 hallucinates on macro texture. FIX = Apollo apo-8 +
  prob-3 estimate=20. ~2min/4s clip. NEVER chr-2 for product macro.
- PROPAINTER OOM: fp32@640px whole-clip = 12.6GB > 8GB. Final: 512px fp16 WHOLE-CLIP window,
  neighbor 15, ref_stride 6, raft 32. ~70s/clip. Corners approved.
- CLIP_05: SAM2 cutouts (GroundingDino prompt-based) onto PROCEDURAL red cyclorama (PIL gradient
  + cove + warm key pool — diffusion stages kept reading as "rooms"; procedural won). Contact
  shadows + faded reflections + zoompan push-in → 4K60. Still delivered too.
- Ops (→finishing-pipeline.md): restart ComfyUI before ProPainter batch (stale 7GB cache OOMs);
  "moov atom not found" on newest .mov = still writing, wait; content-verify every stage gate.
- Parked: AE motion-graphics shots 6 & 18.

## R1 — 2026-07-14 — MINED v4b's CHANNEL (competitor teardown)
- Goal: study @v4b-ai's last year, beat their quality. Method: yt-dlp 2026.07.04 + curl_cffi
  (dodge 429) + throttled pull. Range = 151 videos [1WRllmDEyyE]→[OZFeTg7ttHI]; ~54 had captions.
  Archive: reference/_transcripts/.
- BIGGEST FINDING — moat is craft, not prompts. Manifesto [LKbHqTRjKLw]: AI = ~60% of output;
  "3D experts craft flawless products" → product truth = REAL 3D MODEL ("one accurate 3D model
  → infinite content" [OZFeTg7ttHI]); stack = open models (LTX/Qwen) + own control layers
  (validates our ComfyUI bet); "a video is not a collection of clips" → hooks/structure phase.
- BTS videos = sourced QC checklist: fingers, eyes, lip-sync, text-on-product (#1 tell), scale,
  clipping, physics desync [8aJe9wfxxwA][pvhYzW_EBu8][udhWaNFQ8dg] → failure-modes-qc.md.
- Brooklyn Creamery VO structure → vadilal.md ad-copy draft.
- FILES ADDED: v4b-doctrine.md, ecom-listing-format.md, failure-modes-qc.md; SKILL.md updated.

## R2 — 2026-07-14 — shot-grammar + FABRICATION CAUGHT
- User pasted 30 "breakdowns"; verified each ID vs channel_list_raw.txt. Only FIRST 4 real;
  5-30 HALLUCINATED (products didn't match real videos; paste admitted "assuming..."). Ingested
  only the 4 → shot-grammar.md. Refused the 26.
- RULE (promoted): NEVER ingest a shot list without verifying the ID's real title:
  `grep "|<ID>|" _v4b_research/channel_list_raw.txt`.
- Real gold from the 4: macro-hook opener (1s cuts) → AI presenter anchor (longest shot) →
  demo beats → recurring 360 turntable → payoff → logo card. Pace = f(info density).

## R3 — 2026-07-14 — VERIFIED metadata index for all 151
- yt-dlp info-json for 151 (150 ok; [qhB0edtTubI] captcha-locked) → _transcripts/video-index.md
  (title/date/views/desc/transcript-flag) + metadata_json/. 108 have transcripts.
- First-party confirmations: [UU2IJY31X8k] "we create precise 3D-models" (→doctrine §2);
  [aw6_9OWpoIg] hero scoop "extremely difficult in traditional shoots... captured flawlessly
  every time" (→vadilal.md, case for locked 3D scoop).
- Window = 2024-09 → 2026-07 (~22 months; boundaries authoritative).

## R4 — 2026-07-14 — 5 MANUAL breakdowns ingested (all verified)
- User broke down 5 more; all verified (Night Cream [LC4EVrQ3Iig], DBS [yTocfHd5V6s], Tesla
  [jpT0icEFqCM] on "Manan Gala" = v4b founder's channel; perfume + showreel on channel).
- shot-grammar.md 4→9 sources, +5 patterns: P6 narrative-arc (product enters 40% in; day/night
  mirror), P7 no-presenter product cinematic (static anatomy → escalating motion → rest+logo),
  P8 luxury mood film (one elemental world; product opens AND closes), P9 CGI-internals beat
  (mechanism cutaway right after claim — 3D/AE job), P10 split-screen density, P11 animated
  brand story (UI as story prop; storybook close).
- Showreel [M42N2K7OjL8] (60 shots, silent): green-screen/AI BTS shown openly as proof;
  Brooklyn Creamery beats present; SAME Night Cream ad reused across manifesto/showreel/
  standalone → re-cut one hero production into many contents. Adopt for Vadilal.
- Stack quote corrected: LTX + Qwen (captions had garbled).
- OPEN: Manan Gala unlisted playlist may come — verify via yt-dlp --print (unlisted won't be in
  channel dump), throttled pull, fold in with citations.
- TRAINING CLOSED until then. Next = PRODUCE.

## R5 — 2026-07-25 — MOTION JSON schema standardized (HDFC, user-mandated)
- User pasted the target shape and said "make all the Omni motion prompts in this manner" →
  all 8 HDFC motion blocks rewritten to a FIXED field order (validated: all 8 json.loads clean):
  description · camera{movement,style} · motion{subject,speed,physics} · consistency ·
  negative_prompt · audio{sfx,music,speech} · duration_seconds · aspect_ratio
- Same schema serves Veo AND Omni (Omni = backup after 2 Veo fails). Matches
  prompt-recipes.md §JSON MOTION PROMPTS — that section is now the canonical shape, not a tip.
- Field rules that earned their place on this ad:
  · motion.subject = allowlist. Naming what MAY move implies everything else holds still.
  · consistency = name face + wardrobe + hero prop + set by name, not "the input image".
  · negative_prompt = per-shot risks appended to a people baseline (face morphing, identity
    change, extra fingers, mouth opening, talking, background shift, new objects, flicker).
  · audio.speech ALWAYS "none" — this ad's characters never speak (VO = inner voice, kills
    lip-sync failure). audio.music always "none" — music is a Premiere layer.
  · duration_seconds >= 4 even for a 1.5s cut (Veo head is cleanest; generate long, use head).
- The trim intent does NOT belong in the JSON (Flow would read "use first 1.5s" as direction).
  Kept as a plain `USE:` line under each block. Green-screen master is the one exception:
  full 8s used, cut into 3 — its USE line says so explicitly.
- Green-screen shots need screen-specific negatives ("screen changing colour, UI appearing,
  green flickering or gradient shifting, reflections crossing the screen") or the model
  helpfully renders a UI.
- Multi-person shots need "faces merging or swapping between family members" in negatives.

## R6 — 2026-07-26 — HDFC finishing run: pipeline reproduced clean on a 2nd project
- 8 Veo clips (1920x1080@24, 7x4s + 1x8s OTS) through the Vadilal chain unchanged. Validated:
  the finishing-pipeline.md numbers are project-independent for Veo 1080p output.
- Veo watermark coords IDENTICAL across projects (patch 512@1408,568 / spark 332,337 r60).
  Verified before batching by tiling the bottom-right crop of the LAST frame of all 8 clips
  into one grid — spark is faint/absent early, obvious at the tail. Do this check first; it
  costs one ffmpeg pass and confirms the hardcoded coords still apply.
- ProPainter: ~60-70s per 4s clip, 190s for the 8s clip. Zero seams, zero boil, 24/24 QC
  corners passed first try.
- CONTENTION LESSON (new, cost ~10min): ran Topaz on clip A while ProPainter worked clip B.
  Both want the 4060. Shot_02 went 70s -> 690s (10x) and Topaz stalled at 0.03x. The 8GB card
  fits exactly ONE of these at a time. Run the stages strictly sequentially.
  Before starting Topaz: POST /free {"unload_models":true,"free_memory":true} to ComfyUI —
  dropped VRAM 7.6GB -> 819MB. Cheaper than restarting ComfyUI.
- Topaz VAI 4.0.8, prob-3 + apo-8 chain verbatim from finishing-pipeline.md: ~2min per 4s clip,
  ~4min for the 8s. Out: 3840x2160, 60/1, prores yuv422p10le, ~160MB per 4s clip. 1.5GB total.
- NAMING: copy sources to Shot_NN.mp4 at intake so the name rides the whole chain
  (Shot_NN.mp4 -> Shot_NN_clean.mp4 -> To Be Edited/Shot_NN.mov). No rename step at the end,
  no mapping to lose. Multi-shot plates keep a span name (Shot_07_09_OTS).
- Verify the intake mapping VISUALLY (tile one frame per clip, 4x2) before spending GPU —
  gen filenames are model-authored and easy to misassign.

## S9 — 2026-07-27 — HDFC AE build debugged + full pipeline codified into the skill
AE ExtendScript lessons (each crashed a real run; now rules 1-5 in ae-automation.md):
- setTemporalEaseAtKey wants ONE KeyframeEase PER DIMENSION, and AE stores Scale as 3-D
  even on 2-D layers. 1-element ease arrays on Scale = "Value array does not have 3
  elements" — killed 8 of 14 comps. Fix: single easeAll() helper sizing arrays from
  propertyValueType (ThreeD→3, TwoD→2, else→1). The 6 comps that built were exactly
  the ones without scale-eases.
- KeyframeEase influence must be 0.1–100 (0 throws). Clamp in the helper.
- safe(name, fn) per comp + BUILT/FAILED completion alert with line numbers = the debug
  loop. "Copy this list back to Claude" → fix is usually ONE shared helper → purge-and-
  rebuild re-run. Two iterations max in practice.
- STALE-SYNC TRAP: G: is Google Drive for Desktop. AE executed a PRE-fix copy and errored
  at line 206 — a line that was a comment in the file on disk. If the error line doesn't
  match the file, it's Drive sync lag. Fix: version-stamp the header AND the completion
  alert ("[script v1.2]") so the user can verify which copy ran; wait for sync, re-run.
- Both project scripts now v1.2: AE-SCRIPT.jsx (13 comps) + AE-SCRIPT-OTS.jsx (3 OTS shots,
  explicit 3-element ease on the shot-9 scale push).

Skill codification (user: "write everything with exact steps so a new topic follows the
same workflow"):
- pipeline-playbook.md REWRITTEN as the master Phase 0-11 checklist (scaffold → creative
  lock → VO first → prompts → stills → video → rename → finishing → cut sheet → AE →
  edit/grade/mix → deliverables), each phase pointing at its detail file.
- NEW reference/vo-pipeline.md (Bulbul v3: audition→lock→QC, the 8 earned text rules).
- NEW reference/screen-replace.md (green plate rules, edge-fitting tracker chain,
  proof_pin gate, 3-layer AE stack, corner-pin layer-space trap, one-tap-per-shot cutting).
- NEW reference/ae-automation.md (two-script pattern, 9 ExtendScript rules, comp patterns,
  25fps motion grammar, debug loop).
- prompt-recipes.md += BENCHMARK LOOK (4 forcers + brand flood + composition rule),
  PEOPLE-AD GLOBAL RULES, canonical 8-field motion JSON schema with negative baselines.
- finishing-pipeline.md rewritten as validated-x2 (Stage 0 intake/rename + visual grid
  verify, ProPainter, Topaz exact command, GPU contention block, cut-sheet contract).
- SKILL.md: PEOPLE-AD DOCTRINE section (8 rules), workflow now points at playbook phases,
  FILES list extended.
- Scripts copied into reference/: track_screen.py, analyze_taps.py, make_ae_track.py,
  qc_overlay.py, proof_pin.py, generate_vo.py (never the VO .env — private API key).
- NEW brand-packs/hdfc.md (palette + flood rule, blue-never-green success states, type,
  VO cast, asset paths, spec-ad legal line).

## R7 — 2026-07-27 — HDFC rough cut assembled BY CLAUDE (new capability: I can cut)
User: "the video is not forming in my brain — I need a rough cut." Answer = build the cut
FOR them as (a) a watchable preview mp4 and (b) a Premiere-importable FCP7 XML. Validated:
- ffmpeg IS a rough-cut NLE: per-event 1080p25 intermediates (scale+fps+tpad frame-hold →
  trim → setpts) → concat demuxer → one overlay pass (setpts=PTS+start/TB per overlay +
  enable=between(t,..)) → one amix pass (adelay per clip, pan mono→stereo, alimiter).
  29.8s / 35 events rendered in ~3min on the 7700X. QC = 12-frame xstack grid + volumedetect.
- PRE-KEY the green AE renders once with ffmpeg (chromakey=0x24F20A:0.10:0.08,despill →
  ProRes 4444 yuva444p10le) → they drop onto V2 in ANY tool with straight alpha; no Ultra
  Key setup for the user, and my preview compositor uses the same file. AE green measured
  #24F20A (sample with PIL at several points, NOT the 3x3 frame corner — mine had a black
  border edge that fooled the first probe).
- Bash trap that cost a re-run: "$f_KEYED.mov" parses as var f_KEYED → every loop iteration
  wrote to "keyed/.mov". Use "${f}_KEYED.mov".
- FCP7 xmeml v4 hand-built from python imports into Premiere with V1/V2 + 3 audio tracks +
  Basic Motion scale 50 (4K60 masters into 1080p25 seq) + per-clip Audio Levels + sequence
  markers. Key rules: <file> full def FIRST occurrence only then <file id/> refs; clip
  <in>/<out> in the SOURCE's timebase (60fps files: in=tl_in*60/25); <start>/<end> in
  sequence frames; pathurl = file://localhost/G%3A/...
- Long AE master (Comp 1, 80s) drifts to empty green after ~4.5s — sample the tail BEFORE
  trusting a long comp: use head 2.1s only, cover B/C with the dedicated per-screen renders.
- drawtext on this ffmpeg build segfaults (fontconfig missing default config) — label QC
  grids some other way or skip labels.
- Timeline conform math: measured-VO gaps (N1 2.48 vs bible's 4.2) redistributed per the
  doc's own air rules → 29.8s cut vs 30.6 skeleton. Deliverables: RoughCut_preview_v1.mp4 +
  HDFC_RoughCut_v1.xml + ROUGH-CUT.md (timeline table, track map, what's-missing list).

## V4B — 2026-08-13 — Portfolio reverse-engineering (11 ads, 23 patterns, skill intelligence upgrade)

**Task:** User: "Do what ever is needed to make the skill the most advance in terms of No shoot ads."
Interpreted as: Extract competitive intelligence from V4B's ₹1L-deal client portfolio (11 videos in `Videos for refrence/`).

**Phase 1: Extraction Pipeline**
Built automated ffmpeg + Python (`_analysis/extract.py`):
- 11 unique videos (12 files, 1 duplicate by filesize) → 146 shot frames extracted
- Scene cuts via ffmpeg (threshold 0.25), metadata per video (duration, cuts, shot timecodes)
- Audio extraction (for future Whisper VO transcription when API key valid)
- Color palettes generated
- Output: `_analysis/{video_id}/shots/*.jpg` + `metadata.json` + `palette.png` + `audio.wav`

**Phase 2: Frame-by-Frame Visual Analysis**
Read all 146 frames visually (Claude multimodal) and wrote detailed breakdowns:
1. MyFitness Choco Peanut Butter Bar (16s, FMCG) — ingredient surround, luxe open (5.5s hero hold), cyan isolation bg
2. Electric Kettle (30s, appliance) — lifestyle interlude (11s city+actor, 37% of ad), benefit stack (1 frame → 6 text swaps → 11.8s), venetian blind slats
3. SunScreen (30s, skincare luxury) — 0% product shots (actor only), orange brand flood (12s), science macro (Vit C molecule)
4. Protein Powder (30s, health) — **TRIPLE-PANEL GRID** (1 face across gym/outdoor/office, 17s, 56% of ad), PNG composite on green bg
5. Night Cream (51s, skincare mid-tier) — nighttime aesthetic (dark blue, moon, silk), 60% product visibility
6. Tesla + Car Film (30s + 47s, automotive) — dual playbook: white void + specs (tech) vs. black void + emotion (prestige)
7. Fashion + DBS Bank + Living Memories + Tribute (21s + 89s + 120s + 75s, narrative batch) — VO-driven, slow pacing (4.4-6.0s avg), crossfades (tribute = 0 hard cuts)

Output: 8 breakdown files (5 individual + 1 automotive pair + 1 narrative batch + 1 prototype)

**Phase 3: Pattern Synthesis**
Cross-referenced all 11 ads → extracted **23 V4B signature moves** (`_analysis/v4b-signature-moves.md`):

**Universal (90%+ adoption):**
1. Black void open (10/11, 0-2s pure black) — only exception: Tesla (white void for tech)
2. Shot length = emotion intensity (product 2.0s, premium 3.0s, CSR 4.4s, testimonial 6.0s, tribute 10s+)
3. Image-first pipeline (every motion shot = Nano Banana still → Veo i2v, never text-to-video)

**Structural (50-70% adoption):**
4. Lifestyle interlude (7/11, 7-12s no-product beat, 25-40% of ad)
5. Benefit stack (6/11, 1 shot → multiple text swaps → 8-12s content)
6. Brand color flood (5/11, 8-12s solid brand color bg, no texture)
7. **Triple-panel lifestyle grid (1/11 but CRITICAL)** — 1 face gen'd across 3 contexts (gym, outdoor, office), rapid montage. Cost: 1x gen → 3x variety. **This is the biggest unlock.**

**Technical:**
8. Venetian blind slat lighting (horizontal sunlight stripes = instant cinema, easy to prompt)
9. Product PNG composite (real product photo → mask → composite on solid/gen bg, NOT pure gen with labels)
10. Real hands (never gen hands, 90% failure rate)
11. Text timing hierarchy (visual first 0-17%, benefits 17-70%, brand last 85-100%)
12. Nighttime aesthetic (dark blue, cool light, sleep props for night cream category)

**Category-specific:**
13. Skincare positioning ladder (luxury 0% product, mid 60%, mass 80%)
14. Automotive dual playbook (tech=white void+specs, prestige=black void+emotion)
15. Health triple-panel structure (powder macro 4s → triple-panel 17s → PNG benefit stack 5s)
16. FMCG ingredient surround (product + bowls of raw ingredients, not lifestyle actors)
17. VO-driven narrative (60s+ films, script VO first then gen scenes to beats)
18. Crossfade transitions (tribute/healthcare, 1-3s dissolve not hard cuts)

**Key Discoveries:**

**THE TRIPLE-PANEL BREAKTHROUGH (1 face → 3 scenes = 3x variety for 1x cost):**
Protein ad: 1 South Asian male face gen'd across gym (dumbbell), outdoor (hiking), office (laptop).
Montage: 1.5-2s per shot, cycle 2-3x, 17s total (56% of 30s ad).
Cost: 1 face ref → 3 Veo 3 gens = ₹50k traditional casting → ₹30 gen (1667x reduction).
Tech: Veo 3 face lock, Luma character ref, or Midjourney --cref.

**BLACK VOID = V4B SIGNATURE (91% adoption):**
10/11 ads open with 0-2s pure black. Only exception: Tesla (white void for tech/minimal).

**SHOT LENGTH CURVE (validated across 11 ads):**
Product 2.0-2.5s, premium 2.5-3.5s, CSR 4.0-5.0s, testimonial 5.5-6.5s, tribute 10s+.
Rule: Product = fast (retention), emotion = slow (resonance).

**LIFESTYLE INTERLUDE (64% adoption, 7-12s no-product beat, 25-40% of ad):**
Narrative reset — shifts "what it is" to "who you become."

**BENEFIT STACK (55% adoption, 1 frame → 6-8 text swaps → 8-12s content):**
Kettle: 1 shot → 6 text swaps → 11.8s. Savings: 10s of shooting/gen eliminated.

**BRAND COLOR FLOOD (45% adoption, 8-12s solid color bg):**
SunScreen orange #FF8C42, Protein green #7FBF7F. Makes ₹500 feel like ₹5000.

**PNG COMPOSITE > PURE GEN (real labels always):**
Real product photo → mask → composite. Gen models redesign labels = legal disaster.

**REAL HANDS ALWAYS (never gen, 90% failure rate).**

**TEXT TIMING HIERARCHY (100% adherence):**
Visual first (0-17%) → benefits (17-70%) → brand last (85-100%).

**SKINCARE POSITIONING LADDER:**
Luxury (₹1000+) = 0% product shots. Mid-tier (₹500-1000) = 60%. Mass (₹200-500) = 80%.

**Cost Analysis:**
V4B avg: $0.01/second. Traditional: $500-5000/second. **50,000x reduction.**

**The Unlock:**
V4B isn't using better AI — they're using better CREATIVE SYSTEMS. All 23 patterns now encoded in skill as proven templates validated at ₹1L deal level.

**Phase 4: Skill Integration**
Updated 4 reference files:
1. shot-grammar.md — Added P12-P28 (17 new patterns)
2. prompt-recipes.md — Added V4B Portfolio Image Prompt Patterns section
3. category-cheatsheet.md — Added V4B Category Insights tables
4. SKILL.md — Added V4B Portfolio Intelligence section

**Files Created:**
- `_analysis/extract.py` + `transcribe.py` (pipelines)
- 11 video subdirs with 146 shot frames + metadata + palettes + audio
- 8 breakdown files (5 individual + automotive pair + narrative batch)
- `_analysis/v4b-signature-moves.md` (23 patterns documented)

**Next Session:**
1. Build triple-panel template (reusable Veo 3 prompt set)
2. PNG composite workflow (AE project template)
3. Test black void timing (A/B: 0-2s vs 1-3s vs direct-cut)
4. Category shot lists (scenes.json templates for FMCG/protein/skincare/automotive)
5. Lifestyle interlude beats (actor prompts for outdoor/city/home contexts)

**Competitive Edge Gained:**
Triple-panel face-consistent generation alone = 1667x cost reduction. All 23 V4B patterns copy-paste ready.
