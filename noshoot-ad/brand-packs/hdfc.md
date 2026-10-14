# BRAND PACK — HDFC Bank (spec ad; validated project 2026-07-26)
Project root: `G:\GLM\No Shoot Ads\HDFC\` — the worked example for every people-ad /
screen-replace pattern in this skill. Product: XpressWay Festive Treats (pre-approved
loans / cardless EMI style offer). SPEC AD — not a client engagement; legal line
"T&C apply. This is a conceptual spec ad." on the end card.

## PALETTE (locked — flood rule applies)
| Role | Hex | Use |
|---|---|---|
| HDFC RED | #ED232A | Accent ONLY: offer pills, badge, CTA pops |
| HDFC BLUE | #004C8F | DOMINANT — flood the set in this |
| Deep blue | #003B73 | Gradients / dark ends / extrude steps |
| White | #FFFFFF | Text, cards, lockup plate |
- BRAND FLOOD: every set saturated blue with red accents → gens read branded, not stock.
- SUCCESS STATES ARE BLUE, NEVER GREEN (green = the key color + off-brand).
- Wardrobe neutral (white/grey/charcoal) to protect the palette.

## TYPE
- Poppins (ExtraBold/SemiBold/Regular) — UI, cards, body. PostScript: "Poppins-ExtraBold".
- Alfa Slab One — badge / kinetic slam words. PostScript: "AlfaSlabOne-Regular".
- Install BEFORE running AE scripts (fonts silently fall back otherwise) — see DOWNLOADS.md.

## VO (Sarvam Bulbul v3 — reference/vo-pipeline.md)
- Cast: rohan (lead male VO), neha (female alt), mani / kabir (auditioned alts).
- Language: en-IN code-mix. Acronyms PLAIN ("HDFC", "EMI") — spaced caps = robotic.
- pitch/loudness rejected by API — pace only.

## ASSET PATHS (project-local)
- Script/plan: `SCRIPT.md`, `PRODUCTION.md`, `shot-prompts.md`, `AE-BUILD.md`, `DOWNLOADS.md`
- VO: `VO\out\final\*.wav` (locked takes; durations = timeline ground truth)
- Masters: `Assets\To Be Edited\Shot_NN.mov` + `_CUT_SHEET.md` (4K60 ProRes 422 Proxy)
- Tracker: `Tools\` chain + `_track\screen_track.json` + `TRACK-NOTES.md`
  (measured green #05C912 → Keylight Screen Colour; taps 1.87 / 3.87 / 5.47s)
- AE: `AE-SCRIPT.jsx` (13 graphics comps, v1.2) + `AE-SCRIPT-OTS.jsx` (OTS_Shot7/8/9, v1.2)
- Logos: official SVGs per DOWNLOADS.md — AE can't script-import SVG; human drops in.

## STRUCTURE NOTES
- Reference pacing: ICICI Cardless EMI ad (energy/pacing only — original compositions).
- Vignette casting: separate strangers per shot; no recurring cast.
- Phone screens: solid green gen → AE replace. One 8s OTS master cut into shots 7/8/9.
- Characters never speak on camera; VO = inner voice.
