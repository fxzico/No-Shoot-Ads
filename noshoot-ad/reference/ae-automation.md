# AE AUTOMATION — ExtendScript project builders (validated HDFC 2026-07-26/27)
Two scripts per project build EVERY graphics comp; the human does polish, not
construction. Working examples: G:\GLM\No Shoot Ads\HDFC\AE-SCRIPT.jsx (26KB,
13 comps) + AE-SCRIPT-OTS.jsx (tracked screen comps). Copy + adapt, don't
rewrite from scratch.

## THE TWO-SCRIPT PATTERN
1. **AE-SCRIPT.jsx** — all standalone graphics comps: badge, logo lockups,
   floating offer cards, phone UI screens, kinetic 3D text, end card.
   Run FIRST (File > Scripts > Run Script File).
2. **AE-SCRIPT-OTS.jsx** (screen-replace projects) — imports the plate, builds
   the corner-pinned + Keylight shot comps from the solved track
   (screen-replace.md). Needs script 1's UI comps → run SECOND.
Companion docs: AE-BUILD.md = per-comp polish spec (timing/easing/shadows);
DOWNLOADS.md = fonts + official SVGs to install BEFORE running.

## HARD-WON EXTENDSCRIPT RULES (each crashed a real run)
1. **setTemporalEaseAtKey wants ONE KeyframeEase PER DIMENSION** — and AE stores
   Scale as 3-D even on 2-D layers. A 1-element ease array on Scale =
   "Value array does not have 3 elements" (killed 8 of 14 comps). Route ALL
   easing through one helper that sizes the array from propertyValueType:
   ThreeD→3, TwoD→2, OneD + spatial→1.
2. **KeyframeEase influence must be 0.1–100** — influence 0 throws. Clamp in
   the helper.
3. **Wrap every comp build in safe(name, fn)** — try/catch per section, collect
   failures, keep building. Completion alert lists BUILT vs FAILED (+ line
   numbers) so one bad comp doesn't hide twelve good ones. Alert says
   "copy this list back to Claude" — that report IS the debug loop.
4. **Purge-and-rebuild on re-run**: script deletes its own folder/comps first →
   idempotent; re-running after a fix rebuilds everything clean.
5. **Version-stamp header AND completion alert** ("[script v1.2]"). Google
   Drive-synced folders serve STALE script copies to AE (real failure:
   "error at line 206" pointing at the PRE-fix file). If the error line doesn't
   match the file on disk, it's a stale sync — wait for Drive, re-run.
6. No Math.random() in builds — deterministic confetti/scatter (index-based
   angles) so every rebuild is identical.
7. AE can't script-import SVG — leave a placeholder plate + "IMPORT X HERE"
   text layer; the human drops the official SVG in after.
8. Third-party effects (Deep Glow, RSMB) can't be assumed installed — script
   applies native effects only; AE-BUILD.md tells the human what to add.
9. Fonts by PostScript name ("Poppins-ExtraBold", "AlfaSlabOne-Regular") —
   install before running or text layers silently fall back.

## COMP PATTERNS THAT WORKED (steal from HDFC AE-SCRIPT.jsx)
- **Badge**: shape-layer circle + polystar/repeater sunburst (24 rays, time*8
  rotation) + dashed-ellipse dotted ring (counter-rotating) + slab text with
  chunky stroke. Trace source image kept as 50%-opacity underlay, recolored to
  palette.
- **Floating offer cards**: one builder function, N content variants. White
  rounded card + grey PRODUCT_IMG_placeholder (human drops a cut-out FROM THE
  SHOT ITSELF for perfect match) + offer pill. popIn/fadeIn stagger.
- **Phone UI screens**: 1080x2340 comps (or tracker-measured aspect); status
  bar, header, content; animation beats keyed to the measured tap times.
- **Faked 3D extrude text**: N text copies stepping darker, offset [3,4]px per
  step, all parented to the face layer — one slam animates the stack. Slam =
  170%→squash 112/88→settle 100, 8 frames.
- **Behind-subject text**: build stack back-to-front (behind words / RED guide
  solid named ROTO_FG_PLATE__replace_me / front words). Human rotos the
  subject (Roto Brush 3; ComfyUI SAM2 if it chatters), drops it on the plate
  layer, unchecks guide. No per-word masking.
- **End card**: badge slams center → shrinks/slides to corner → lockup on white
  pill takes center → card fan → search pill with typewriter expression
  (substr on time) → legal line.
- **Markers everywhere**: every sync point (word land, tap, impact) gets a comp
  marker naming what lands there — the edit slides comps, never re-keys.

## 25FPS-NATIVE MOTION GRAMMAR
Moves 10f, micro-moves 5f, slams land in 5f + 3f settle, pop-in overshoot
106–118%, two-bounce for heavy objects. Comp time 0 = the shot's start on the
master timeline — conform by SLIDING the whole comp.

## THE DEBUG LOOP (what actually happened, kept as procedure)
Run → alert lists FAILED comps with line numbers → paste list to Claude →
fix is usually ONE shared helper (see rules above) → purge-and-rebuild re-run →
BUILT (all). Two iterations max in practice.
