# MODEL SELECTION MATRIX — Match Model to Task

**Source:** AiKAMI Day 2 Vocabulary + V4B validation (2026-08-18 integration)

Different models excel at different tasks. **Stop using one model for everything.** Your input frame quality decides 80% of the final output — pick the right tool for the job.

---

## IMAGE GENERATION MODELS

### Soul 2.0 (Best Realism)
**Best for:** Photorealistic human characters, natural skin, believable lighting
**Use when:** People ads (finance, service, lifestyle), actors, faces, skin texture
**Strengths:** The realism king for human subjects
**Weakness:** Not ideal for products, text, or stylized work

### Soul Cinema (Cinematic Frames)
**Best for:** Film-grade cinematic stills, dramatic lighting, movie-still composition
**Use when:** Hero frames that need to look "shot on camera", high-end product reveals
**Strengths:** Filmic color, cinematic composition, premium feel
**Weakness:** May be overkill for utility shots or rough drafts

### Nano Banana Pro / Nano Banana 2 (General Editing)
**Best for:** Inserting subjects, fixing flaws, swapping outfits/locations, refining details
**Use when:** Our **current default** — surgical editing, product hero frames, iterations
**Strengths:** Versatile, reliable, fast, good balance of control and quality
**Weakness:** Not the best at typography or extreme realism

### GPT 2.0 (Text-Heavy Images & General Editing)
**Best for:** Signage, posters, labels, UI, lots of readable text, cleanest typography
**Use when:** Pack shots with visible labels, signage in environments, UI screens
**Strengths:** Text rendering is dramatically better than other models
**Weakness:** Product shapes may be less reliable than Nano Banana
**⚠️ LABEL RULE STILL APPLIES:** Even with GPT 2.0, gen'd labels on branded products = legal risk. Use for blank mockups → composite real labels in AE.

### Reve (Branding, Design & Clean Images)
**Best for:** Branding, product design, advertisements, posters, clean finish
**Use when:** Design-grade work, clean minimal aesthetic, brand identity shots
**Strengths:** Polished professional finish, design-oriented
**Weakness:** May lack texture/grain for cinematic work

### Seedream 5.0 (Poster Images)
**Best for:** Posters, labels, UI, lots of readable text, good color combinations
**Use when:** Graphic-heavy work, poster design, packaging mockups
**Strengths:** Color palette + typography combo
**Weakness:** May not suit photorealistic product shots

### Recraft V4.1 (Posters & Illustrations)
**Best for:** Refined poster details, artistic designs, branding
**Use when:** Illustration-heavy work, stylized branding, design decks
**Strengths:** Artistic polish, illustration quality
**Weakness:** Not for photorealistic products

### Midjourney (Artistic Images)
**Best for:** Vivid aesthetic, variety of styles, experimentation
**Use when:** Mood boards, concept exploration, stylized work
**Strengths:** Aesthetic range, prompt flexibility
**Weakness:** Less control for precise product work

---

## VIDEO GENERATION MODELS

### Veo 3 (Google Flow — Our Current Default)
**Best for:** Crisp 1080p outputs, i2v workflow, reliable motion, fast iteration
**Use when:** **EVERY shot in our current pipeline** (validated workflow)
**Strengths:** Image-to-video reliability, reasonable cost, good motion physics
**Weakness:** Not listed in AiKAMI doc (they use Seedance ecosystem)
**Status:** ✅ **KEEP AS PRIMARY** — validated pipeline, known failure modes

### Seedance 2.0 (High-End Alternative)
**Best for:** Crisp 1080p & 2K outputs, Hollywood-level complex shots, VFX
**Cost:** Higher than most models (not specified, but $0.34/s for 2.5)
**Use when:** Complex motion, high production value, client-facing hero shots
**Strengths:** Complex motion handling, professional quality
**Weakness:** Higher cost than Veo

### Seedance 2.5 (Best Realistic & Complex)
**Best for:** Best realistic and complex outputs, state-of-the-art, best acting/prompt adherence, best video editing/manipulation
**Cost:** Highest ($0.34/s)
**Use when:** Absolute highest quality needed, complex actor performances
**Strengths:** Best-in-class realism, acting, editing capability
**Weakness:** Most expensive

### Kling 3.0 (Budget Option)
**Best for:** Crisp 1080p when no complex motion is needed, simple outputs
**Cost:** Lowest generation cost
**Use when:** Budget-constrained projects, simple motion shots
**Strengths:** Cheapest option, decent quality for simple work
**Weakness:** Cannot handle complex motion
**⚠️ Our workflow:** User doesn't have default Kling access — route to Veo instead unless confirmed

### Flux 3 (Retro Realism)
**Best for:** Best raw retro realism, state-of-the-art model, closest to Seedance in realism
**Cost:** Cheaper than Seedance ($0.17/s for standard HD)
**Resolution:** Currently only 720p outputs
**Use when:** Retro aesthetic, natural grain, budget + quality balance
**Strengths:** Retro filmic look, reasonable cost
**Weakness:** 720p max (not ideal for 4K finishing)

### MiniMax H3 (Budget Compromise)
**Cost:** ⅓ of Seedance cost ($0.13/s at 2K, $0.08/s at 768p)
**Use when:** Budget projects, non-hero shots
**Strengths:** Low cost, acceptable for utility shots
**Weakness:** Outputs usually look plastic (per AiKAMI)
**AiKAMI note:** "I personally don't use it"

### Gemini Omni Flash (Video Editing Only)
**Best for:** Decent video editing only (NOT for text-to-video or img-to-video)
**Best for talking heads** (after Seedance)
**Cost:** Most value for money (very cheap ~$0.10/s for 720p)
**Use when:** Post-generation editing, talking head refinement, budget editing
**Strengths:** Cheap editing capability
**Weakness:** Not for primary generation

---

## DECISION TREE — WHICH MODEL TO USE

### FOR IMAGE GENERATION (Hero Frames)

```
START
 ├─ Is it a PERSON (face, actor, human subject)?
 │   ├─ YES → Soul 2.0 (realism) or Soul Cinema (cinematic)
 │   └─ NO → Continue
 │
 ├─ Is there VISIBLE TEXT (signage, labels, UI, posters)?
 │   ├─ YES → GPT 2.0 (best typography) or Seedream 5.0 (posters)
 │   └─ NO → Continue
 │
 ├─ Is it BRANDING / DESIGN work (clean minimal aesthetic)?
 │   ├─ YES → Reve (brand-grade clean finish)
 │   └─ NO → Continue
 │
 ├─ Is it a PRODUCT HERO SHOT (perfume, watch, tech, drink)?
 │   ├─ YES → Nano Banana Pro (our validated default)
 │   └─ NO → Continue
 │
 └─ Is it STYLIZED / ARTISTIC / MOOD BOARD?
     ├─ YES → Midjourney (aesthetic range)
     └─ NO → Nano Banana Pro (general purpose)
```

### FOR VIDEO GENERATION (Motion)

```
START
 ├─ Do we have budget constraints?
 │   ├─ YES → MiniMax H3 ($0.08/s) or Kling 3.0 (simple motion)
 │   └─ NO → Continue
 │
 ├─ Is this a CLIENT-FACING HERO SHOT (₹1L tier work)?
 │   ├─ YES → Seedance 2.5 (best-in-class, $0.34/s)
 │   └─ NO → Continue
 │
 ├─ Is motion COMPLEX (splash, pour, fabric physics, VFX)?
 │   ├─ YES → Seedance 2.0 or Veo 3
 │   └─ NO → Continue
 │
 ├─ Is this a PORTFOLIO/PORTFOLIO REEL shot?
 │   ├─ YES → Veo 3 (our validated workflow)
 │   └─ NO → Continue
 │
 └─ Is this UTILITY / B-ROLL / NON-HERO?
     └─ YES → Veo 3 (reliable default) or Kling 3.0 (if very simple)
```

---

## UPDATED WORKFLOW BY PRODUCT CATEGORY

### Luxury Product Ads (Perfume, Watch, Jewelry)
**Image:** Soul Cinema (cinematic hero) or Nano Banana Pro (fast iteration)
**Video:** Veo 3 (our default) or Seedance 2.0 (if ₹1L+ budget)
**Camera vocab:** ARRI Alexa 65, 85mm portrait, Fincher/Villeneuve style

### Energy Products (Drinks, Sport)
**Image:** Nano Banana Pro (product hero) or Soul 2.0 (if athletes/people)
**Video:** Veo 3 (physics-heavy: splash, pour) or Seedance 2.0 (complex VFX)
**Camera vocab:** RED Komodo/V-Raptor, 24mm wide, Nolan/Tarantino style

### Tech Products (Audio, Electronics)
**Image:** Reve (clean design-grade) or Nano Banana Pro (product hero)
**Video:** Veo 3 (reliable) or Flux 3 (retro tech aesthetic)
**Camera vocab:** Sony Venice 2, 35mm lens, clean modern style

### Fashion/Apparel
**Image:** Soul 2.0 (people/models) or Soul Cinema (cinematic lifestyle)
**Video:** Seedance 2.5 (best acting/fabric physics) or Veo 3 (default)
**Camera vocab:** Kodak Portra 400, 35mm film, Deakins/Cuarón style

### People Ads (Finance, Service, Lifestyle)
**Image:** Soul 2.0 (photorealistic actors) or Soul Cinema (cinematic)
**Video:** Seedance 2.5 (best acting) or Veo 3 (budget-conscious)
**Camera vocab:** Sony Venice 2, shot by Roger Deakins

### Pack Shots with Visible Labels
**Image:** GPT 2.0 (text rendering) → but still composite real labels in AE
**Video:** Veo 3 (product lock via ControlNet in ComfyUI fixlayer)
**⚠️ LABEL LAW:** Even GPT 2.0 will redesign brands — blank gen → real label composite

### UGC / TikTok Style Ads
**Image:** Soul 2.0 (natural people) with "shot on iPhone 15 Pro" prompt
**Video:** Veo 3 or Flux 3 (retro natural grain)
**Camera vocab:** iPhone 15 Pro, candid phone-camera realism

---

## COST OPTIMIZATION STRATEGY

### Portfolio / Spec Work (Our 5-film reel)
**Image:** Nano Banana Pro (fast, reliable, known workflow)
**Video:** Veo 3 (validated pipeline, reasonable cost)
**Why:** Speed + reliability > absolute max quality for portfolio proofs

### Client Work ₹50k–₹1L (Mid-Tier)
**Image:** Soul Cinema (hero frames) + Nano Banana Pro (utility)
**Video:** Veo 3 primary, Seedance 2.0 for money shots only
**Why:** Balance quality + cost, splurge on 2-3 hero shots

### Client Work ₹1L+ (Premium Tier)
**Image:** Soul Cinema (all hero frames) + GPT 2.0 (text-heavy)
**Video:** Seedance 2.5 (best-in-class for all hero shots)
**Why:** Client paying premium, deliver premium — no compromises

### Utility Shots / B-Roll (Always Budget)
**Image:** Nano Banana Pro (fast iteration)
**Video:** Kling 3.0 (if simple) or MiniMax H3 (if budget tight)
**Why:** These shots support the hero, don't need hero-tier quality

---

## INTEGRATION WITH EXISTING SKILL

**Current default:** Nano Banana Pro (image) + Veo 3 (video)
**Status:** ✅ **KEEP THIS FOR PORTFOLIO WORK** — validated, fast, reliable

**When to upgrade:**
- People/actors in shot → Soul 2.0 / Soul Cinema
- Visible text/signage → GPT 2.0 (but still composite real brands)
- Client paying ₹1L+ → Seedance 2.5 for hero shots
- Design/branding work → Reve (clean finish)

**When to downgrade:**
- Utility shots, B-roll → Kling 3.0 (simple motion)
- Budget-constrained client → MiniMax H3 or Flux 3

**Never change:** The doctrine (IMAGE-FIRST, LONG image prompt, SHORT motion prompt, 
ComfyUI fixlayer only, AE finishing). Only the upstream model changes.

---

## VALIDATION NOTES

**AiKAMI's core thesis (matches our V4B doctrine):**
> "The tool is never the bottleneck — the process is."

Translation: Model choice matters, but:
1. Strong input frame (detailed prompt) > model tier
2. Finishing layer (ProPainter → Topaz → AE) > raw gen quality
3. Known failure-mode QC > blind batch generation

**Our approach:** Veo 3 + Nano Banana Pro is **sufficient for portfolio-grade work** 
when paired with cinema-grade prompting (camera vocab) + finishing pipeline.

Upgrade to Soul/Seedance when client budget allows or when people/acting is critical.

---

## QUICK REFERENCE CARD

| Task | Image Model | Video Model |
|---|---|---|
| **Product hero (portfolio)** | Nano Banana Pro | Veo 3 |
| **Product hero (client ₹1L+)** | Soul Cinema | Seedance 2.5 |
| **People / actors** | Soul 2.0 / Soul Cinema | Seedance 2.5 |
| **Visible text / signage** | GPT 2.0 | Veo 3 |
| **Branding / design** | Reve | Veo 3 |
| **UGC / TikTok vibe** | Soul 2.0 ("iPhone 15 Pro") | Flux 3 |
| **Utility / B-roll** | Nano Banana Pro | Kling 3.0 |

**Default stack (unchanged):** Nano Banana Pro + Veo 3 + ComfyUI fixlayer + Premiere/AE
