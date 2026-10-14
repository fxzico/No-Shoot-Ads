---
name: noshoot-ad
description: >
  Universal no-shoot AI commercial engine. Produces broadcast-grade product ads with ZERO
  filming — any category: ice cream, food/beverage, apparel, electronics, cosmetics, jewelry,
  footwear, home goods, auto. Pipeline: Nano Banana Pro (hero image) + Veo/Omni (motion) +
  ComfyUI on RTX 4060 (product-lock / relight / roto / upscale fix-layer) + Premiere/AE (post).
  Bakes in the prompt doctrine: DETAILED image prompt, SHORT motion prompt. Self-improving —
  every session appends learnings. Loads brand packs (e.g. Vadilal) on demand.
  Use when the user wants to create a product ad / commercial / promo video without a shoot,
  or says "make a no-shoot ad", "/noshoot-ad", or names a product + "ad/video/commercial".
---

# NO-SHOOT AD ENGINE (universal)

Broadcast-grade product commercials, no camera, no shoot. Any category. Recreate a
reference ad's pacing/energy — original compositions, never shot-for-shot copies.

## ENVIRONMENT (verified)
- I run in Git Bash on the user's Windows PC with disk access: `G:`=/g, `C:`=/c.
  I can read/write files, run ComfyUI headless, launch agents. (Old "sandbox/no access" claim = wrong.)
- I cannot watch video/hear audio directly — but I CAN QC via ffmpeg frame extraction.
  Timecodes/gen results otherwise come from the user.
- GPU: RTX 4060 8GB · Ryzen 7 7700X · 32GB RAM.
- ComfyUI: `C:\Users\USER\Confy UI\ComfyUI_windows_portable\ComfyUI`
- Verify rig: `nvidia-smi --query-gpu=name,memory.total --format=csv,noheader`

## USER TOOLS
- Google Flow: Nano Banana Pro (image hero) · Veo 3 (video primary) · Omni (backup).
- ComfyUI (4060) = FIX-LAYER ONLY — never hero gen, never long/HD video.
- Premiere + AE — user is strong; composite/text/color/sound/edit live here.
- No Kling by default → route those shots to Veo (unless user confirms Kling access).

**Model selection (2026-08-18 upgrade):** See `reference/model-selection-matrix.md` for when 
to use Soul 2.0 (people/realism), GPT 2.0 (text-heavy), Reve (branding), or other alternatives 
instead of Nano Banana Pro. Default stack (Nano Banana + Veo) remains validated for portfolio work.

## ROLE SPLIT (do not blur)
| Layer | Tool |
|---|---|
| Hero product truth (reused, label-critical) | Real 3D model (Blender via agents) |
| Hero frame one-off, sharp label | Nano Banana Pro (feed real PNG) |
| Motion: splash/pour/camera/fabric/actor | Veo 3 (Omni backup) |
| Product-lock, relight, roto, upscale, cleanup | ComfyUI |
| Composite, text, MG, color, sound, cut | Premiere/AE |

Shot needs 8GB+ or clean HD video → Veo, not ComfyUI.

## V4B DOCTRINE (the quality bar — full version: reference/v4b-doctrine.md)
1. **AI = ~60% of output.** Every gen is a plate for post; budget 40% for craft.
2. **Product truth = real 3D model** when hero/reused/label-critical. Image-gen fine for one-offs.
3. **Structure & hooks first** — lock outcome + 1-2s hook + narrative spine BEFORE generating.
4. **Known AI failure modes = non-negotiable QC** → failure-modes-qc.md.
5. **Open models + own control layer** (their LTX/Qwen+control ≈ our ComfyUI fix-layer). Validated.

## V4B PORTFOLIO INTELLIGENCE (11 ads reverse-engineered 2026-08-13)
**Source:** V4B's ₹1L-deal client portfolio. Full analysis: `Videos for refrence/_analysis/v4b-signature-moves.md`

**Core signatures (90%+ adoption):**
- **Black void open** (0-2s pure black, premium framing) — 10/11 ads. Exception: Tesla (white void for tech aesthetic).
- **Shot length = emotion intensity** — Product 2.0-2.5s, premium 3.0s, CSR 4.4s, testimonial 6.0s, tribute 10s+.
- **Image-first pipeline** — Every motion shot starts as Nano Banana still → Veo i2v. Text-to-video = failure.
- **Lifestyle interlude** (7/11 ads) — 25-40% of ad with ZERO product shots (actor in context, pure vibe).
- **Benefit stack** (6/11) — 1 perfect product shot → rotating text overlays → 8-12s content from 1 image.
- **Brand color flood** (5/11) — 8-12s actor/product on SOLID brand color bg (orange, green, blue), no texture.

**New techniques unlocked:**
- **Triple-panel lifestyle grid** — 1 face gen'd across 3 contexts (gym, outdoor, office). 1x cost → 3x variety.
- **Product PNG composite** — Real product photo → mask → composite on solid color OR gen scene. Beats pure gen (labels stay accurate).
- **Venetian blind slat lighting** — Horizontal sunlight stripes = instant cinema. Easy prompt, trained aesthetic.
- **Text timing hierarchy** — Visual first (0-17%), benefit claims (17-70%), brand last (85-100%). Never reverse.

**Category playbooks:**
- **Skincare positioning** — Luxury 0% product shots (actor only), mid-tier 60%, mass 80%.
- **Automotive dual** — Tech/EV = white void + specs. Prestige/luxury = black void + emotion.
- **Health/nutrition** — Material truth macro (4s powder) → triple-panel lifestyle (17s) → PNG benefit stack (5s).
- **FMCG bars/snacks** — Ingredient surround (product + bowls of chocolate/almonds/PB), not lifestyle actors.

**Cost benchmark:** $0.01/second avg ($0.30 per 30s ad). 50,000x cheaper than traditional shoot while maintaining broadcast quality.

**The unlock:** V4B isn't using better AI — they're using better CREATIVE SYSTEMS. All patterns now encoded in `reference/shot-grammar.md` (P12-P28), `prompt-recipes.md` (V4B sections), `category-cheatsheet.md` (V4B tables).

## PROMPT DOCTRINE (apply to every shot)
- **IMAGE prompt (Nano Banana) = LONG & DETAILED**: subject, material, label text verbatim,
  lighting+direction, lens/DoF, background, palette (hex), mood, angle. The still is the casting.
- **MOTION prompt (Veo/Omni) = SHORT & PHYSICAL**: one movement sentence + one camera sentence.
  Name physics (viscosity, weight, speed). Long motion prompts → drift/morph.
- Image prompt describes; motion prompt commands.
- **IMAGE-FIRST, ALWAYS (proven 2026-07-14):** text-to-video fails. Every shot — actors included —
  starts as a Nano Banana still → Veo image-to-video. Templates: reference/prompt-recipes.md.

**Cinema-grade vocabulary (2026-08-18 upgrade):** Every image prompt now uses the formula:
`Shot on [CAMERA], [LENS], in the style of [DIRECTOR], [REFERENCE FILM] vibe.`
This controls aesthetic signature before the detailed scene description. See `reference/camera-vocabulary.md` 
for complete camera body/lens/director style tables, and `reference/prompt-structure-formula.md` 
for 5 validated examples with dissection. Product category → camera match guide included.

**Photorealistic human characteristics (2026-08-20 upgrade — MANDATORY FOR ALL HUMAN SUBJECTS):**
AI-generated faces default to unrealistic perfection. Every human portrait MUST include natural 
imperfections to read as real people, not synthetic. Apply to ALL character/actor prompts:

- **Facial asymmetry**: Eyes at different heights, varying eyelid depths, different eye sizes, 
  eyebrows with uneven arch heights and thickness, jawline asymmetry (one side stronger/more angular), 
  cheekbones with different prominence
- **Skin texture & imperfections**: Visible pores (especially nose bridge, forehead, cheeks, T-zone), 
  beauty marks, moles, freckles, minor blemishes, healed acne scars with texture, age spots (mature 
  characters), fine lines, crow's feet, nasolabial folds, under-eye bags/circles showing natural features
- **Natural expression lines**: Dynamic wrinkles from years of expressions, forehead lines (horizontal), 
  frown lines between eyebrows, smile lines around mouth, age-appropriate character lines
- **Dental/alignment differences**: Front teeth with slight overlap, minor natural gaps, tooth 
  rotation/alignment imperfection, age-related tooth wear and discoloration (mature characters), 
  natural tooth color variation
- **Hair & grooming details**: Uneven hair density/texture, beard with patches of varying growth, 
  flyaway hairs around hairline, individual grey hairs in varying distribution (age-appropriate), 
  natural hair texture showing individual strands
- **Other micro-details**: Visible blood vessels in eye sclera (subtle red veins), natural nail 
  length variation, knuckle texture, age spots on hands (mature characters), lip texture and 
  vertical lines, subtle lip asymmetry

**Template example:** "...Indian male, 27 years old, sharp angular jawline with subtle asymmetry 
(left side slightly stronger), visible skin texture including pores on nose and cheeks, small 
beauty mark near right jawline, eyebrows with natural asymmetry (right sits 2mm higher), subtle 
crow's feet from natural expressions, eyes showing natural asymmetry (left eye slightly more open), 
photorealistic human imperfections..."

This upgrade applies to: casting portraits, actor shots, testimonial faces, lifestyle scenes with 
people. SKIP for: products, food, environments, abstract compositions. The goal: characters read 
as real humans photographed, not AI-generated perfection.

## GOLDEN RULES
1. Label visible → real product image = only truth. PACK SHOTS: gen models WILL redesign
   packaging → composite pipeline (blank-cup scene → SAM2 cut real photo → place in AE/PS →
   IC-Light relight denoise ≤0.45). Never deliver pure-gen branded pack shots.
2. Gen is lossy → 3-4 variants per shot, pick best.
3. **Verify-regenerate loop IS the quality**: attach refs → generate → LOOK → re-roll.
   A batch that doesn't check its own output is a slot machine.
4. ONE face reference at a time. Multi-ref = identity drift. Cast solo → lock ONE pair image → chain.
5. Lock geometry with real photo + ControlNet before relight. Never text-gen an accuracy-critical shape.
6. Match light direction (IC-Light) between bg and product or the composite reads fake.
7. Cut on audio beats, to reference timecodes.
8. 8GB discipline: SAM2 base_plus; stills/very short clips only in ComfyUI. ONE GPU job
   at a time (ProPainter ∥ Topaz = 10x slowdown).
9. Legal: reference ads = pacing/energy only. Original compositions.

## PEOPLE-AD DOCTRINE (finance/service ads — HDFC-validated)
1. VO FIRST: lock voice track (reference/vo-pipeline.md), then cut picture to it.
2. Characters NEVER speak on camera (mouths closed, VO = inner voice) → zero lip-sync risk.
3. NO readable text in any gen — signage/UI/logos are ALL AE. (The label rule, generalized.)
4. Phone/TV screens gen as SOLID GREEN → AE screen replace (reference/screen-replace.md).
5. One long master gen cut into N shots = continuity for free.
6. BRAND FLOOD: whole set saturated in dominant brand color; accent color = pops; wardrobe
   neutral. Fixes "palette-correct but reads stock".
7. Vignette structure (separate strangers) > recurring cast — shots fail independently.
8. AE comps built by ExtendScript, not by hand (reference/ae-automation.md).

## WORKFLOW (per project — full checklist: reference/pipeline-playbook.md)
0. Scaffold the standard folder tree (playbook Phase 0). Strategy & format; lock outcome,
   hook, spine.
1. Intake: category, brand assets, reference ad, duration, ratios, message. Load brand pack.
2. Deconstruct reference (user timecodes/frames) → PRODUCTION.md timeline + scenes.json.
3. VO first when narrated (vo-pipeline.md) → conform timeline to measured WAVs.
4. Write ALL prompts (shot-prompts.md): benchmark-look image prompt + canonical motion JSON
   + USE + CHECK per shot. Generation order: anchor faces first, long masters early.
5. Per shot: still (3-4 variants) → Veo i2v → QC vs CHECK line.
6. Rename to Shot_NN at intake, verify mapping visually → finishing chain
   (finishing-pipeline.md): ProPainter → Topaz 4K60 ProRes → _CUT_SHEET.md.
7. AE: fonts → AE-SCRIPT.jsx builds comps → tracker + AE-SCRIPT-OTS.jsx for screens
   (ae-automation.md, screen-replace.md) → hand polish per AE-BUILD.md.
8. Premiere: conform to VO/music beats, grade (warmth in footage, graphics strict palette),
   grain on gens only, mix with SFX map.
9. QC vs failure-modes-qc.md + timing <0.1s. Export 16:9 + 9:16 REBUILD (+1:1, 4:5 per pack).

## FILES (load as needed)
- `reference/pipeline-playbook.md` — **THE MASTER CHECKLIST** (Phases 0-11, exact steps,
  folder scaffold). Start every project here.
- `reference/camera-vocabulary.md` — **CINEMA-GRADE PROMPTING (NEW 2026-08-18)**: Camera 
  bodies (ARRI Alexa 65, RED Komodo, Sony Venice 2), lenses (85mm portrait, anamorphic, 
  Cooke S4), director styles (Villeneuve, Fincher, Deakins). Product category → camera match guide.
- `reference/prompt-structure-formula.md` — **VALIDATED PROMPT FORMULA (NEW 2026-08-18)**: 
  5 dissected examples from AiKAMI Day 2 Vocabulary. Shows how to combine camera/lens/director 
  with scene/technical/color layers. Template checklists for product/people/environment shots.
- `reference/model-selection-matrix.md` — **WHEN TO USE WHICH MODEL (NEW 2026-08-18)**: 
  Soul 2.0 (people), GPT 2.0 (text-heavy), Reve (branding), Seedance (client ₹1L+), cost 
  optimization by tier. Decision tree + quick reference card.
- `reference/vo-pipeline.md` — Sarvam Bulbul v3 TTS: audition → lock → QC loop, text rules.
- `reference/screen-replace.md` — green-screen phone/TV → tracked AE UI (no Mocha/SAM2).
- `reference/ae-automation.md` — ExtendScript project builders: patterns + crash rules.
- `reference/finishing-pipeline.md` — validated post chain (rename → ProPainter → Topaz
  4K60 ProRes → cut sheet). Read before any finishing work.
- `reference/v4b-doctrine.md` — quality bar with citations.
- `reference/failure-modes-qc.md` — reject-on-sight artifact checklist.
- `reference/ecom-listing-format.md` — conversion/listing spine.
- `reference/shot-grammar.md` — v4b editing patterns (11 verified patterns).
- `reference/prompt-recipes.md` — benchmark look, canonical motion JSON, category recipes.
- `reference/comfyui-fixlayer.md` — node graphs, 8GB settings, headless run.
- `reference/scenes-template.json` — blank shot-blueprint schema.
- `reference/category-cheatsheet.md` — hero shot per product type.
- `reference/generate_vo.py` — VO template script (copy into <Project>\VO\).
- `reference/track_screen.py + analyze_taps.py + make_ae_track.py + qc_overlay.py +
  proof_pin.py` — screen-tracker chain (copy into <Project>\Tools\).
- `reference/_transcripts/` — v4b transcript archive + video-index.md (151 verified) + metadata_json/.
- `evolution-log.md` — append every session.
- `brand-packs/<brand>.md` — brand colors, products, text swaps, asset paths.

## SELF-IMPROVEMENT PROTOCOL
At session end, append to evolution-log.md: winning prompts verbatim, bad gens+fix, new recipes,
rig changes. Recipe proves itself twice → promote into reference files.

## RESUME PROTOCOL
On load: skim SKILL.md + evolution-log.md. Detect brand → load pack. Ask "which shot / what
product?" Deliver per shot: detailed image prompt → short Veo motion prompt → (if label)
ComfyUI relight steps → AE placement note. Session end → Self-Improvement Protocol.
