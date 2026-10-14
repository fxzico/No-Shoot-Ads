# SHOT GRAMMAR — v4b's editing patterns (9 verified shot-by-shot sources)

User-supplied breakdowns, IDs verified vs channel dump / yt-dlp. The layer transcripts
can't give: shot type, camera move, timing, cut rhythm. Only REPEATING patterns kept.

Sources: [1WRllmDEyyE] Borosil Waffle Maker 59s/23sh · [B-i7QRIZvvA] ICICI Pru explainer
150s/19sh · [5iZc-bYZnDI] J&T app walkthrough 40s/16sh · [FA1tgILMs8g] NARS beauty 34s/22sh ·
[LC4EVrQ3Iig]* Everlift Night Cream 51s/22sh · [yTocfHd5V6s]* DBS Women's Day 89s/17sh ·
[jpT0icEFqCM]* Tesla 30s/14sh · [vTGPSZ8uYT8] Aqua Lumière perfume 19s/8sh ·
[M42N2K7OjL8] Showreel 105s/60sh. (* = "Manan Gala", v4b founder's channel.)

⚠️ 26 other breakdowns in the same batch were FABRICATED and refused. ALWAYS verify an ID's
real title before ingesting: `grep "|ID|" channel_list_raw.txt`.

## P1 — PRODUCT-VIDEO SPINE (~30-60s D2C ad)
1. Detail-macro opener (shots 1-4, ~1s each): ECU logo/texture/controls, fast cuts, moving camera.
2. Presenter establish (WS/MS): AI human enters — the LONGEST single shot (7s vs 1s macros). Anchor.
3. Demo/use beats (CU/MCU, static): one action per shot; the action provides the motion.
4. Turntable/360 hero: the money beat, recurs MID and LATE. Cheap to vary, reads premium.
5. Result payoff (CU/ECU): finished thing, hero-lit.
6. Presenter close + logo card (~3-4s hold).

## P2 — CUT RHYTHM ("cut on information")
Openers ~1s/shot · presenter/claim shots 3-7s · demo beats 1-3s · avg ≈2.5s/shot (product ad);
explainer slides hold 10-19s. Pace = f(information density): fast for texture, slow for reading.

## P3 — CAMERA VOCABULARY
Tilt/pan = reveal logo/form · track = glide across panel/lips · push-in = emphasis ·
zoom out = context reveal · 360 turntable = hero beat · static = demos, talk, text cards.
RULE: product gets the moving camera; actions & talk get the static camera. Motion = camera
OR subject, rarely both (matches our short-motion-prompt doctrine).

## P4 — AI-PRESENTER FORMAT
Presenter MCU/MS on clean brand bg, returns 3-5×; between beats: macros, demos, kinetic text.
Presenter shots = where lip-sync/hands/eyes must be perfect → failure-modes-qc.md.
Beauty ad = presenter as connective tissue; explainer = narrator beside slides.

## P5 — KINETIC TEXT / GRAPHIC BEATS
Bold short on-brand typography as its own shot ("IT'S NOT GOING ANYWHERE"), lands on a beat,
holds 1-2s. Final shot ALWAYS a clean logo card on solid bg (non-negotiable closer).
On-screen text carries the sell (works muted) → ecom-listing-format.md.

## FORMAT NOTES
- Product/D2C ad: macro-hook → presenter → demo → turntable → payoff → logo. ~30s, 20+ shots.
- Explainer: presenter narrates beside full-screen slides (10-19s holds), title-card transitions.
- App walkthrough: presenter bookends; middle = screen-UI captures, camera pans/zooms across
  the UI, one feature per 2-3s beat, split-screen presenter+UI.

## P6 — NARRATIVE-ARC CINEMATIC (Night Cream, 51s/22sh)
Product enters LATE — shot 11 of 22 (~40% in). 1) World/problem, no product (night city, tired
commute). 2) Product reveal = glamour CU slow dolly IN the story. 3) Use + transformation +
macro-CGI proof beat (skin cells repairing — mechanism visualized). 4) Payoff mirror: the SAME
world transformed (day/night mirror). 5) Packshot close. Orange/teal, 2-4s shots.
= the spine for a cinematic brand cut.

## P7 — NO-PRESENTER PRODUCT CINEMATIC (Tesla, 30s/14sh)
1) Static detail suite 0-9s: anatomy, one detail per ~1.5s. 2) Motion suite 9-24s: escalating
scale detail→street→aerial. 3) Rest + logo. Statics for anatomy, tracking/aerials for emotion.
(Maps to: 3D/locked hero for statics, Veo for motion suite.)

## P8 — LUXURY MOOD FILM (Perfume, 19s/8sh)
Fewest shots, longest holds, no VO, no feature text till end. Product opens AND closes. Middle =
one committed elemental brand-world (ocean) a model inhabits. Every prop on-theme.

## P9 — CGI-INTERNALS BEAT
Mechanism cutaway (mattress layers, skin cells, vaporizer exploding) placed right after the
claim — "see how" beats "trust me". One 2-4s beat. 3D/AE job in our stack (Veo can't do
accurate internals).

## P10 — SPLIT-SCREEN DENSITY
2-3 panels compress parallel info (product+lifestyle+texture; feature matrices; before/after).
Used at openers and feature beats. Cheap in AE, high perceived value. Never for the hero reveal.

## P11 — ANIMATED BRAND STORY (DBS, 89s/17sh)
Stylized character lives a mini-narrative; product (app) appears as a STORY PROP in tight
phone-screen CUs (real UI 3× in ~15s), not a packshot. Metaphor close + frame-story device
(storybook). Long holds ~5s. For brand-feeling/occasion briefs, not conversion.
UI-in-story beats feature lists for app trust.

## SHOWREEL CATALOG ([M42N2K7OjL8], 60 shots)
Confirms grammar at scale: macro food scoops · product+floating ingredients · lifestyle-use
beats · kinetic-text cards · CGI internals · green-screen/AI BTS shown openly as proof.
Same Night Cream ad reused across manifesto/showreel/standalone → THEY RE-CUT ONE HERO
PRODUCTION INTO MANY CONTENTS. Do the same.

## V4B PORTFOLIO PATTERNS (11 ads, 2026-08-13 analysis)

### P12 — BLACK VOID OPEN (10/11 = 91% adoption)
0-2s pure black (#000000 or #0A0A0A) before first visual. Premium framing, palette cleanser
from feed chaos. EXCEPTION: Tesla (white void for tech/minimalist aesthetic). Never skip this
unless brand is explicitly Apple-adjacent tech positioning.

### P13 — SHOT LENGTH = EMOTIONAL INTENSITY
Product ads (FMCG, appliances): 2.0-2.5s avg (TikTok retention).
Premium products: 2.5-3.5s avg (confidence pacing).
CSR/cause films: 4.0-5.0s avg (documentary empathy).
Testimonial: 5.5-6.5s avg (deep emotion).
Tribute/memorial: 10s+ or zero cuts (reverence).
RULE: Product = fast (retention), emotion = slow (resonance). Never reverse.

### P14 — LIFESTYLE INTERLUDE (64% of product ads)
7-12s block (25-40% of total ad) with ZERO product shots. Actor in context, environment, vibe only.
Placement: 20-60% mark (after product truth, before benefit stack).
Purpose: Narrative reset — shifts "what it is" to "who you become."
Examples: Kettle 11s city+actor (37%), SunScreen 7.5s outdoor (25%), Protein 17s triple-panel (56%).
Use for: Premium positioning (₹500+), lifestyle categories, aspirational buyers.
Skip for: Utility products, B2B (unless work-life narrative), ads <15s.

### P15 — BENEFIT STACK (STATIC HERO + TEXT SWAPS) (55% adoption)
ONE perfect product shot (3-5s) + rotating text overlays (1.5-2.5s each) = 8-12s content from 1 image.
Formula: Base_duration + (Num_swaps × Text_duration).
Text: White bold geometric sans (Montserrat/Sora/DM Sans), two-line breaks for rhythm, left/right-third
positioning (never center). Fade-in 0.3s, hold 1.5-2.0s, fade-out 0.3s.
Examples: Kettle (1 shot → 6 text swaps → 11.8s), Tesla (1 turntable → 4 specs → 20s).

### P16 — BRAND COLOR FLOOD (45% adoption)
8-12s sequence, ENTIRE background = SOLID brand color (no texture, no gradient).
Gen: Veo 3 "actor on solid [hex] background" OR PNG product composite on AE solid layer.
Duration: 30-40% of ad (for 30s format).
Text overlays: Benefit claims in white or contrasting color.
Examples: SunScreen (orange #FF8C42, 12s portraits), Protein (green #7FBF7F, product PNG).
Why: Color BECOMES product. Maximum brand imprint. Makes ₹500 product FEEL like ₹5000.

### P17 — TRIPLE-PANEL LIFESTYLE GRID (NEW TECHNIQUE)
ONE face gen'd across THREE contexts (gym, outdoor, office) — rapid montage, 1.5-2s per shot, 2-3 cycles.
Pipeline: 1 face ref → Veo 3 with 3 prompts (same face, different scene/wardrobe/bg).
Cost: 3x scene variety for SAME gen cost vs. casting 3 actors.
Text per scene: GYM="STRENGTH", OUTDOOR="ENERGY", OFFICE="FOCUS".
Example: Protein ad (17s, 56% of 30s ad, 1 actor in 3 lifestyles).
Use for: Multi-use-case products (protein, energy, multivitamins), "complete lifestyle" positioning.

### P18 — TEXT TIMING HIERARCHY (100% adherence)
VISUAL FIRST, CLAIM SECOND. Never reverse.
Benefit claim (first): 17-25% into ad, 1.5-2.5s duration.
Feature callouts: 30-70%, 1.5-2s each.
Brand name (last): 85-100%, 2-5s hold.
Exception: Brand films (CSR/tribute) show brand at 90-95%, not 85%.
Why: Early text = "skip this ad." Visual credibility first, then claims.

### P19 — VENETIAN BLIND SLAT LIGHTING
Horizontal sunlight stripes across actor face (window blind shadows). Trained aesthetic in all AI
models, signals "cinematic" instantly. Easy prompt: "venetian blind sunlight slats across face."
QC: Slats must be parallel, evenly spaced, NOT morphing between frames.

### P20 — PRODUCT PNG COMPOSITE (NOT IN-SCENE SHOOT)
Real product photo (white bg) → mask → composite on solid color OR gen'd scene.
Pipeline: Shoot product on white seamless (<1h) → Remove.bg/SAM2 → AE composite on solid layer
or Midjourney bg → IC-Light relight if needed.
Why: Gen models redesign labels. Real photo = label accuracy. Composite = background flexibility.
Use for: Products with visible branding (bottles, jars, boxes), mid-tier positioning (₹500-2000).

### P21 — REAL HANDS (NEVER GEN HANDS)
When hands appear, they're REAL (actor shoot or stock), never AI-gen. Gen hands = 90% failure rate
(morphing fingers, wrong joints, broken physics). If shot needs hands: shoot real OR use stock footage.

### P22 — NIGHTTIME AESTHETIC (NIGHT CREAM CATEGORY)
Dark blue palette (#1A1F3A to #2C3E50), cool lighting (5500-6500K), sleep props (silk pillows, moon, stars).
Use for: Products used AT NIGHT (night cream, sleep supplements, bedtime tea).
Why: Visual language matches usage context. Golden hour for night cream = cognitive dissonance.

### P23 — VO-DRIVEN STRUCTURE (NARRATIVE FILMS 60s+)
Script VO FIRST, then gen scenes to VO beats — not reverse.
Workflow: Write VO script → record/gen VO → beatmap key phrases → gen scenes timed to VO → cut picture to locked VO.
Why: Picture can flex, VO cannot. Locking VO first = tight sync.
Use for: CSR films, testimonials, brand documentaries (all 60s+, not product ads).

### P24 — CROSSFADE TRANSITIONS (TRIBUTE/HEALTHCARE)
1-3s dissolve overlap between shots (not 0-frame hard cut).
Use for: Tribute films, memorials, healthcare, elderly care — subjects requiring RESPECT.
Skip for: Product ads (hard cuts = energy), fast montages, comedy/action.

### P25 — SKINCARE POSITIONING LADDER
Luxury (₹1000+): 0% product visibility, 100% actor lifestyle + portraits (SunScreen model).
Mid-tier (₹500-1000): 60% product + 40% actor mix (Night Cream model).
Mass (₹200-500): 80%+ product hero, 20% actor.
Rule: Luxury sells FEELING (glowing skin), not OBJECT (cream jar). Position brand first, then decide %.

### P26 — AUTOMOTIVE DUAL PLAYBOOK
TECH/SPEC (Tesla): White void studio, 3D car turntable (1 RPM), spec callouts (range, 0-60, tech),
minimal 3-word tagline. Target: Logic-first buyers (EV, early adopters).
PRESTIGE/EMOTION (Luxury): Black void, cinematic environments (mountain road, city night), fast montage
(exterior/interior/details), emotion text (FREEDOM, POWER). Target: Aspiration-first (status buyers).

### P27 — FMCG INGREDIENT SURROUND
Hero product surrounded by RAW INGREDIENTS in bowls (chocolate, almonds, peanut butter) — not lifestyle props.
Why: Cheaper than actors, more authentic than stock, tells flavor story without VO.
Technique: Shoot/buy ingredient bowls → shoot product on same surface → composite OR shoot together → light consistently.
Use for: Food/bev where ingredients = story (protein bars, supplements, snacks). Skip for: processed foods.

### P28 — ONE FRAME, MANY USES (EFFICIENCY PATTERN)
1 perfect shot → multiple text swaps → 8-12s content from 1 image/render.
Examples: Kettle (1 shot → 6 swaps → 11.8s), Tesla (1 render → 4 specs → 20s).
Cost equation: Kettle saved 10s of shooting/gen by exploiting 1 hero frame.
Use for: Products with 3+ features, static acceptable (not fashion/cars needing motion variety).

## USE
Building scenes.json: pick the matching format spine, fill with P3 moves + P2 rhythm.
Deviate on content, keep the pacing skeleton.

V4B portfolio (P12-P28) adds: black void opens, lifestyle interludes, benefit stacks, brand color
floods, triple-panel grids, text timing hierarchy. These are PROVEN patterns from ₹1L deals —
start here, then iterate per brand.
