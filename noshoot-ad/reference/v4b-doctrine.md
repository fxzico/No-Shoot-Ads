# V4B DOCTRINE — reverse-engineered from v4b.ai's own channel (@v4b-ai, 151 videos, 2024-09→2026-07)

Transcripts via yt-dlp; raw archive: reference/_transcripts/. Claims cited to video IDs.
HEADLINE: v4b's moat is NOT better prompts — it's CRAFT on top of AI. Adopt the process.

## 1. THE 60/40 RULE — AI is an ingredient, not the dish
"Our in-house AI generates only about 60% of the final output." [LKbHqTRjKLw]
Gen-AI alone = "preset, predictive, not creative": plastic faces, bad lip-sync, "products that
are always wrong". Their AI output ships as production-software file types — plates, never
finals. → Treat every gen as a plate to fix; budget 40% for craft (3D, relight, roto, retime,
comp, grade, sound). "The difference between generated and crafted content."

## 2. PRODUCT TRUTH = REAL 3D MODEL
Thesis of their newest video: "Infinite Content with One Accurate 3D Product Model" [OZFeTg7ttHI].
"Our 3D experts craft flawless, detailed products using professional 3D software" [LKbHqTRjKLw].
"Using product images, we create precise 3D-models" for marketplace content [UU2IJY31X8k].
Ice-cream hero scoop: "extremely difficult... due to melting, timing, texture control...
here captured flawlessly every time" [aw6_9OWpoIg].
- One accurate model → any angle/light/scene, label correct every time. No re-rolling.
- Build 3D when: product is the star in ≥3 shots · label/geometry must stay pixel-accurate
  and drifts in gen · need angles the photos don't cover.
- Our route: Blender via agents, texture from real photos, render passes, then treat renders
  like any plate. Image-gen stays valid for one-off/background/macro moments.
- Decide per shot: hero & reused → 3D; incidental → image.

## 3. STACK = OPEN MODELS + OWN CONTROL LAYERS
"Built on... LTX, Qwen... unified through our own control layers and custom pipelines —
control over every frame." [LKbHqTRjKLw] "Offline, secure, fully controlled."
→ Exactly our ComfyUI + ControlNet/IC-Light strategy. Not a compromise — the same move,
smaller GPU. Favor local/controllable steps for anything brand-critical.

## 4. STRUCTURE & HOOKS — "a video is not a collection of clips"
"It's structured. It's flow... a defined science... conversion-focused hooks." [LKbHqTRjKLw]
→ Before any shot: lock the OUTCOME (awareness/consideration/add-to-cart), the HOOK (first
1-2s), the narrative SPINE. Shots serve the spine. See ecom-listing-format.md.

## 5. NAMED AI FAILURE MODES (their BTS = our QC)
Their BTS films show the broken frames: "fingers just merging... eyes moving in random
directions... lips out of place" [8aJe9wfxxwA]; "text on product distorted. Either the product
is huge or the hand" [pvhYzW_EBu8]; "hand passes through kettle, lips move while steam stands
frozen" [udhWaNFQ8dg]. Their conclusion each time: "post-production filled AI's gaps."
REJECT-ON-SIGHT: merged/extra fingers · drifting eyes · lip-sync off · text-on-product
distorted · scale wrong · clipping · physics desync · morph/warp. → failure-modes-qc.md.

## 6. DELIVERABLE TYPES v4b sells
1. Cinematic ad film (15-60s, sensory, music-led). 2. eCom/D2C listing video (biggest bucket;
turntable + callouts → ecom-listing-format.md). 3. Explainer/service (VO-driven). 4. Manual/
brochure → video ("turn boring brochures... into sharp videos" [BHiPfKxBCQE]). 5. AI
spokesperson & BTS/case-study content.

## 7. AD-COPY STYLE (Brooklyn Creamery = our reference)
"Mango sunshine. / Strawberry nights. / Vanilla dreams. / Chocolate highs. / One more bite. /
I close my eyes. / Every flavor takes me somewhere nice." [aw6_9OWpoIg][OZFeTg7ttHI]
Pattern: `[Flavor] + [one-word mood/time noun]` × N, cut on beat, 4-6 word payoff tagline.
Sensory, concrete, no feature-speak in a cinematic ad.

## ACTIONABLE DELTA
1. Strategy/Hook phase before generation (§4). 2. 3D model as first-class product-truth path
(§2). 3. All gens = plates for post, 40% craft budget (§1). 4. eCom listing format added (§6).
5. QC = named failure modes; text-on-product is why we lock/3D (§5). 6. Keep investing in the
ComfyUI control layer (§3).
