# PROMPT RECIPES — doctrine expanded

Core split (never violate): **IMAGE (Nano Banana) = LONG, DETAILED. MOTION (Veo/Omni) = SHORT, PHYSICAL.**

**NEW (2026-08-18):** Cinema-grade vocabulary layer added — see `camera-vocabulary.md` 
and `prompt-structure-formula.md` for full camera/lens/director reference tables. Every 
image prompt now starts with camera body + lens + director style to control aesthetic signature.

## BENCHMARK LOOK — bake into EVERY image prompt (HDFC-proven, fixes "stock photo" gens)
A palette-correct gen can still read as a flat stock photo. Reference-grade ads are
DESIGNED SETS shot like TV commercials. Force all four, they are not optional:
1. **DESIGNED SET, never a flat wall** — brand-color architectural panels (fluted/slatted),
   niches and built-in shelves styled with props, a window with soft daylight, textured
   surfaces. Environment fills the frame as design, not backdrop.
2. **CINEMATIC LIGHTING** — soft key + rim/hair light for separation + practical accents
   (LED cove strips, recessed downlights, a neon glow line); pools of light with falloff.
   Dimensional and glossy, NOT flat even lighting.
3. **DEPTH & LAYERING** — foreground framing element in soft focus (rack, counter edge,
   doorway), midground subject, background set depth; shallow DoF, creamy bokeh.
4. **RICH COLOR + POLISH** — environment saturated in the DOMINANT brand color, bright and
   glowing (never murky); accent color as pops only; "ARRI Alexa + Master Prime, high-end
   commercial grade, photoreal, 8k" finish language.
BRAND FLOOD RULE: flood the whole set in the dominant brand hex so gens read BRANDED,
not stock. Wardrobe neutral (white/grey/charcoal) to protect the palette.
COMPOSITION RULE (kills the dead void): subject on a third; the OTHER side = designed set
(styled niche/panel/window), NOT empty wall — AE text overlays the design and carries its
own shadow/pop for legibility.

## PEOPLE-AD GLOBAL RULES (HDFC-proven; inherit into every people prompt)
- Characters NEVER speak on camera: "mouth closed, natural relaxed expression" in every
  prompt + "mouth opening, talking" in every negative. VO = inner voice. Kills lip-sync risk.
- NO readable text anywhere in a gen (signage, posters, tags, dials, TV content, phone UI) —
  all type is AE. Text appears → regen, never retouch.
- Phone/TV screens = "solid bright green screen" for AE replace (see screen-replace.md);
  or abstract glow for background screens.
- Key action inside the middle 9:16 column (the vertical rebuild punches in).
- "natural skin texture with visible pores, no beauty-filter smoothing" in every prompt.
- Vignette casting: separate strangers per shot; face-match only where unavoidable —
  generate the TIGHTER shot first, feed its pick as ref for the wider one.

## IMAGE PROMPT SKELETON — CINEMA-GRADE (updated 2026-08-18)
```
Shot on [CAMERA], [LENS], in the style of [DIRECTOR], [REFERENCE FILM] vibe.

[SHOT SIZE + ANGLE] of [SUBJECT exact], made of [MATERIAL/SURFACE detail].
[LABEL TEXT verbatim, quoted] clearly legible on [where].
[Spatial relationship: subject on third, designed set on other side].

Lighting: [key type + direction + soft/hard], [fill], [rim], [practicals]. 
[Scale, negative space, depth layers, atmosphere]. Mood [x].

Background: [designed set detail / architectural elements / layering]. 
Palette: [dominant brand hex flood] + [accent hex]. 
[Texture beats: condensation, crumbs, sheen, weave...].

Photoreal, ARRI Alexa + Master Prime, high-end commercial grade, 8k.
```
Name the MATERIAL, give LIGHT DIRECTION (ComfyUI must match it), quote label text exactly,
add category texture cues. Over-specify; 60-120 words fine.

## MOTION PROMPT SKELETON (≤2 sentences)
`[Subject] [does ONE physical action with named physics]. Camera [ONE move].`
Weight/viscosity/speed words, no beauty adjectives. Long motion prompts → morph/drift.
Good: `Thick caramel ribbon pours and folds slowly onto the scoop, high viscosity. Camera slow push-in.`

## JSON MOTION PROMPTS FOR VEO/OMNI — CANONICAL SCHEMA (user-mandated, R5)
Veo parses structured prompts more reliably. Paste JSON as the motion prompt (still
attached). FIXED field order, same schema for Veo and Omni:
```json
{
  "description": "ONE physical action sentence. Not a mood, not a list.",
  "camera": { "movement": "ONE move", "style": "lens/framing" },
  "motion": { "subject": "what MAY move (allowlist — everything else holds still)",
              "speed": "...", "physics": "weight, contact, lag, falloff" },
  "consistency": "preserve <face>, <wardrobe>, <hero prop>, <set> exactly as the input image",
  "negative_prompt": "failure modes BY NAME (baselines below + shot-specific risks)",
  "audio": { "sfx": "natural only", "music": "none", "speech": "none" },
  "duration_seconds": 4,
  "aspect_ratio": "16:9"
}
```
Field rules that earned their place:
- `motion.subject` is an ALLOWLIST — naming what may move implies the rest holds still.
- `consistency` = highest-value field. Name face + wardrobe + hero prop + set BY NAME,
  not "the input image".
- PEOPLE BASELINE negatives (every person shot): "face morphing, identity change, extra
  fingers, mouth opening, talking, background shift, new objects, flicker".
- MULTI-PERSON adds: "faces merging or swapping between family members".
- GREEN-SCREEN adds: "screen changing colour, UI or icons or text appearing on the screen,
  green screen flickering or gradient shifting, reflections crossing the screen".
- `audio.speech` ALWAYS "none" (nobody talks on camera) · `audio.music` ALWAYS "none"
  (music is a Premiere layer).
- `duration_seconds` ≥ 4 even for a 1.5s cut — Veo's head is cleanest; generate long,
  use the head. `aspect_ratio` "16:9" — the 9:16 is a post rebuild, never a re-gen.
- Trim intent NEVER goes in the JSON (the model reads it as direction). Keep a plain
  `USE:` line under the block: "first 1.5s @25fps". Long master plates are the exception —
  their USE says "all 8s, cut into three".
- Under USE add a `CHECK:` line — that shot's reject list for QC.
Worked packs: Vadilal _VEO_JSON_PROMPTS.md (17 clips) · HDFC shot-prompts.md (8 blocks).

## FRAME-PAIR METHOD (start+end frame — every physics shot)
Flow accepts start AND end frames. Kills drift, forces intended physics.
1. Generate START frame (full detailed prompt).
2. Make END frame by EDITING the start in Nano Banana (never fresh): "Same scene, same lighting,
   same camera. [only the physics outcome changed]. Everything else identical."
3. Feed both + one-line motion prompt.
Use: splashes, pours, scoop pulls, fabric drops, swirls. Skip: camera-only shots.

## LIQUID PHYSICS DICTIONARY (thick foods — from failed splash gens)
The liquid NOUN decides the physics:
- "caramel sauce"/"syrup" → WATER/GLASS physics (tall thin translucent crowns). WRONG for cream.
- "thick opaque caramel cream", "melted toffee with heavy cream", "shrikhand-like mango cream"
  → LOW heavy opaque crowns, blunt lobes, sagging strings. RIGHT.
- Always add "completely opaque, zero translucency" for dairy splashes.
- Thick-crown anatomy: LOW + blunt lobes + fat droplets + short sagging strings.
- Cream viscosity: "pourable like double cream" (soft slumping coils) not "mayonnaise" (stiff
  porcelain). Add "micro bubbles, subtle flow lines, soft sheen not hard gloss".
- Watch: "lassi" pulls glassy crown tips.

## HDR-COMMERCIAL TELL (grade discipline)
Over-bright everything-lit = AI ad look. Pro food ads: moderate light, deep shadows, muted grade.
- "single hard key" / "one key + natural falloff"; "deep controlled shadows";
  "background falling to near-black at edges"; "muted professional color grade" —
  saturation lives in the PRODUCT. Speculars only on ridges/edges.
GRAVITY SANITY: subject must obey gravity — a scoop sits IN its splash pool, never hovers.
Floating element = reject before judging texture.

## CATEGORY RECIPES

### Ice cream / frozen — REAL SCOOP ANATOMY (user-corrected; follow exactly)
1. Drag ridges/striations on ball + tub from the scoop's path (#1 realism cue).
2. Scoop sits IN the tub, scrape marks around — never on a powdery surface.
3. Body dense + fudgy, matte with glossy MELT patches — NOT granular/crystalline.
4. NO mist/frost haze — zero atmosphere; mist = AI tell, reads as steam.
MOTION: `The scoop drags forward slowly, dense cream curling and tearing against the tub. Camera slow push-in.`

### Food/beverage: steam wisps (hot) / condensation beads (cold), garnish crisp, backlight for
drinks, 45° plated. MOTION: `Steam rises and drifts; liquid swirls once. Camera slow orbit left.`
### Apparel: weave/stitch visible, drape, softbox or window light, 4:5/9:16, tag legible.
MOTION: `Fabric flows and settles in a gentle breeze; model turns once. Camera slow dolly.`
Shoes: `Shoe rotates 30° on turntable; laces sway. Camera locked, rack focus.`
### Electronics: brushed metal/glass reflections, screen crisp, rim light, macro ports, logo sharp.
MOTION: `Device rotates slowly, reflections travel; screen glows on. Camera slow arc.`
### Cosmetics/perfume: dew, cream swirl, glass refraction+caustics, beauty light, name legible.
MOTION: `Cream swirls once; a droplet slides down the bottle. Camera slow push-in.`
### Jewelry/watches: sparkle facets, specular hits, velvet/black bg, extreme macro, shallow DoF.
MOTION: `Piece rotates a few degrees, light glints travel. Camera locked macro, rack focus.`
### Home/appliance/auto: 3/4 hero, material realism, badge sharp, key+rim.
MOTION: `Object turns slowly / feature actuates once. Camera slow dolly-in.`

## ACTOR / LIFESTYLE (image-first — text-to-video fails, user-confirmed)
- Never direct t2v. CAST SHEET first: one detailed portrait per actor → feed into every shot.
- Per shot: detailed still → Veo i2v, one action + simple camera.
- People physics: "she lifts the spoon", "his eyes widen slowly" — one beat.

### ANTI-STOCK RULES ("portrait + smiling" = instant AI look)
- BANNED: "portrait", "smiling at the camera", "beautiful", "perfect" (pull AI-averaged face space).
- Prompt a CANDID DOCUMENTARY PHOTOGRAPH: mid-action, looking at each other/off-frame,
  "neither aware of the camera".
- Name imperfections: asymmetric features, pores, T-zone sheen, flyaways, uneven stubble,
  smudged kajal, uneven teeth, wrinkled cotton.
- Name room clutter (2-3 props: newspaper, phone on cushion, water glass). Catalog-clean = AI.
- Wardrobe = ERA-CHECK with client. Ethnicity words pull traditional-costume cliché; if brief is
  young/modern say "Gen Z style" + real garments (oversized graphic tee off one shoulder, crop
  top, baggy jeans, claw-clip bun, nose stud, scrunchie, AirPods + iced coffee props).
  Current-fashion detail reads "original photo, not AI".
- Framing: 35mm documentary, off-center, one limb clipped, one face-side in shadow,
  "gentle film grain, muted documentary color grade".
- Reject: poreless skin, perfect teeth rows, lens-aware gazes, catalog rooms.
- SOLO-FIRST CASTING: never two new faces in one image (model averages them). Cast each alone
  (6-8 variants, pick ONE), then pair via "keep both faces exactly as in the reference images".
- REALSKIN BLOCK (append to EVERY actor image prompt — user-mandated):
  "Realistic skin features: natural skin imperfections, a few faint freckles across the nose
  and cheekbones, one or two tiny pimples or healed blemish marks, visible pore structure,
  mild uneven skin tone with warmer patches, fine vellus hairs catching the light, natural
  under-eye texture. Skin must NOT look airbrushed, smoothed or plastic — like unretouched
  RAW photo skin."
- MACRO SKIN (ECU faces): name micro-detail — pore structure, vellus hairs (peach fuzz) catching
  backlight (single strongest realism trigger), lip vertical creases + dry corners, tone varying
  across face, one healed blemish, iris fibers, inner-eye redness, uneven lashes.
  QC at 100% zoom: no pores/vellus = plastic = reject.

## TEMPERATURE GOTCHA
"condensation mist" renders as rising steam → reads HOT. Frozen products: NO atmosphere at all.
Hot food only: `steam rises and drifts`.

## V4B PORTFOLIO IMAGE PROMPT PATTERNS (₹1L-deal validated)

### BLACK VOID / WHITE VOID OPEN
BLACK (default): `Pure black background #000000, subtle film grain texture, no gradients, no objects,
complete darkness, cinematic void aesthetic`
WHITE (tech/minimal only): `Pure white background #FFFFFF, seamless, soft gradient to light gray #F5F5F5
at edges, clean studio void, Apple aesthetic`
Use: First 0-2s of ad. Black = luxury/mystery (10/11 V4B ads), white = tech/transparency (Tesla only).

### SOLID COLOR BACKGROUNDS (BRAND FLOOD)
```
[Actor/product] on solid [brand_color_hex] seamless background, no texture, no gradient,
flat studio color, even lighting from front, no shadows on background, [brand_color_name]
brand color flood, commercial photography, 4K
```
Examples: Orange #FF8C42 (SunScreen), green #7FBF7F (Protein), dark blue #1A1F3A (Night Cream).
Use: 8-12s sequence (30-40% of 30s ad), beauty portraits or product PNG composite.
Text: White bold sans overlays with benefit claims.

### VENETIAN BLIND SLAT LIGHTING (INSTANT CINEMA)
Append to ANY indoor actor shot:
```
...venetian blind sunlight slats across face and shoulders, horizontal striped shadows from
window blinds, parallel evenly-spaced light stripes, golden hour window light streaming through
blinds, cinematic natural lighting
```
QC: Slats must stay parallel, NOT morph. Common in Veo 3/Luma, easy to prompt, looks expensive.

### NIGHTTIME AESTHETIC (SLEEP/NIGHT PRODUCTS)
```
Dark blue background #1A1F3A to #2C3E50 gradient, cool moonlight 5500-6500K, white silk satin
pillow props, silver crescent moon decoration, small metallic star accents scattered, nighttime
sleep aesthetic, bedroom luxury, cool-toned lighting
```
Use: Night cream, sleep supplements, bedtime tea. NOT for daytime products (cognitive dissonance).

### INGREDIENT SURROUND (FMCG FOOD/HEALTH)
```
[Product hero] centered on warm honey-toned wooden table, surrounded by raw ingredients in bowls:
white ceramic bowl of [ingredient A] top-left, dark wooden bowl of [ingredient B] top-right,
glass bowl of [ingredient C] bottom, soft directional window light from right creating gentle
highlights, shallow depth of field f/2.8, food photography, ingredient storytelling composition
```
Use: Protein bars, supplements, snacks where ingredients = story. Cheaper than actors, authentic.
Example: MyFitness bar + chocolate bowl + almond bowl + peanut butter swirl.

### OUTDOOR/HIKING LIFESTYLE (ACTIVE/ENERGY PRODUCTS)
```
Medium closeup portrait, [actor details], wearing [outdoor gear — navy/teal athletic jacket,
backpack straps visible], mountain landscape background with green hills and misty peaks,
golden hour natural light from right 4500-5000K creating warm skin glow, shallow depth of
field f/2.0, outdoor adventure lifestyle photography, 4K, candid documentary moment
```
Use: Sunscreen, protein, energy drinks. NOT studio — background must read "real location" (even if gen'd).

### TRIPLE-PANEL FACE-CONSISTENT ACTOR (1 FACE, 3 SCENES)
Pipeline: Create ONE face ref, then gen 3 scenes with SAME FACE:
```
FACE REF (gen once, reuse 3x):
"Headshot portrait, South Asian male late 20s, short dark hair, athletic build, natural
skin texture, [REALSKIN BLOCK], neutral expression, even studio lighting, white background"

SCENE 1 (GYM):
"Same man [paste face ref], white tank top, lifting dumbbell mid-curl, gym background with
blurred weights and machines, cool fluorescent lighting, keep face exactly as reference"

SCENE 2 (OUTDOOR):
"Same man [paste face ref], navy athletic jacket with backpack, mountain trail background,
golden hour natural light, keep face exactly as reference"

SCENE 3 (OFFICE):
"Same man [paste face ref], white business casual shirt, working on silver laptop, modern
office interior blurred background, soft diffused light, keep face exactly as reference"
```
Tech: Veo 3 face lock, Luma character ref, or Midjourney `--cref`. 3x scene variety for 1x gen cost.
Use: Multi-use-case products (protein, energy, supplements). Montage: 1.5-2s per shot, cycle 2-3x.

### PRODUCT PNG COMPOSITE (REAL LABEL + GEN/SOLID BG)
Don't prompt this — SHOOT IT, then composite:
1. Real product on white seamless (studio or DIY <1h)
2. Remove.bg or SAM2 mask
3. AE: Place PNG on solid color layer OR Midjourney gen'd scene
4. Optional: IC-Light relight to match scene (denoise ≤0.45)
Use: ANY product with visible label/branding. Gen models redesign labels = legal disaster.

## WHEN A GEN GOES BAD (fix ladder)
0. Veo tail drift (always check): first ~1-1.5s cleanest; texture mutates later. Gen long, cut
   from head. QC: `ffmpeg -i clip.mp4 -vf "select='eq(n,0)+eq(n,24)+eq(n,48)+eq(n,72)',scale=960:-1" -vsync vfr f%d.png`
1. Label garbled → feed the real PNG as reference; regen. (Pack shots → composite, Golden Rule 1.)
2. Motion morphs → motion prompt too long; cut to one action + one camera move.
3. Wrong geometry → photo + ControlNet(canny) lock, then relight.
4. Product light ≠ bg → IC-Light, match plate's key direction.
5. Flat/AI → add ONE physical texture cue.
6. Keep 3-4 variants; pick, don't force.

V4B portfolio patterns (black void, brand flood, venetian slats, nighttime aesthetic, ingredient
surround, triple-panel, PNG composite) are validated at ₹1L deal level — use as starting templates.

Log winning prompts verbatim in ../evolution-log.md.
