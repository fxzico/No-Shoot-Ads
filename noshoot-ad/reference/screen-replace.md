# SCREEN REPLACE — green-screen phone/TV → AE UI (validated HDFC 2026-07-26)
The full path from "ad needs an app tutorial" to corner-pinned UI comps with the
thumb restored — no Mocha, no SAM2, no paid plugins. Scripts: reference/track_screen.py,
analyze_taps.py, make_ae_track.py (copy into <Project>\Tools\).

## THE DESIGN DECISION (make it at script stage)
One LONG master gen cut into N timeline shots beats N separate gens:
same phone, same hand, same light = continuity for free; only the AE screen
content changes per shot. HDFC: one 8s OTS take → 3 tutorial shots.

## GENERATING THE PLATE
- Still prompt: phone screen = "SOLID BRIGHT GREEN screen, evenly lit, no
  reflections crossing it, clean thin dark bezels"; thumb hovers lower half,
  never covering center.
- Motion JSON negatives MUST carry: "screen changing colour, UI or icons or
  text appearing on the screen, green screen flickering or gradient shifting,
  reflections crossing the screen, thumb covering the centre of the screen,
  phone drifting or rotating out of frame".
- Direct the taps in `description` ("taps twice with a natural pause, then one
  short scroll") — the taps become your UI sync beats.
- FALLBACK if the model won't hold green: gen screen OFF (black glossy), track
  the bezels the same way, use a luma/garbage matte instead of Keylight.

## THE TRACKER CHAIN (run after the plate is finished 4K60)
```bash
cd <Project>\Tools
python track_screen.py && python analyze_taps.py && python make_ae_track.py
```
1. **track_screen.py** — solves the screen's 4 corners per frame by EDGE FITTING
   the green region (numpy only, streams via ffmpeg). Why edges not extreme
   points: the thumb bites into the screen and extreme-point corners follow the
   bite (measured 185–218px false travel); trimmed least-squares line fits
   reject the occlusion. → _track/screen_track.json
   EDIT AT TOP: SRC path, master resolution, FPS.
2. **analyze_taps.py** — finds taps via thumb-TIP HEIGHT inside the screen quad
   (tip rises ~0.32→0.50 per tap; green-coverage dips alone are too weak) and
   samples the true screen green hex. → taps + green into the track json.
3. **make_ae_track.py** — emits screen_track.jsx (read by the AE build script),
   CornerPin_*.txt clipboard files (manual fallback), TRACK-NOTES.md (measured
   numbers, human-readable).

QC BEFORE TRUSTING (both render mp4s into _track\):
```bash
python qc_overlay.py    # solved quad drawn on the plate
python proof_pin.py     # checkerboard corner-pinned through the SAME numbers
```
proof_pin is the real gate: if the checkerboard sticks, AE will stick.

## THE AE STACK (what AE-SCRIPT-OTS.jsx builds per shot — see ae-automation.md)
```
3  plate again on top + Keylight     ← restores the thumb OVER the UI
2  UI comp, corner-pinned, keyed per-frame from the solve
1  plate (bottom)
```
- **The thumb needs NO roto**: it's skin against saturated green — Keylight
  kills the green, the thumb survives as foreground for free. (SAM2 matte =
  insurance for thumbs crossing screen center; don't build it preemptively.)
- Keylight Screen Colour = the MEASURED hex from the tracker (HDFC: #05C912),
  never eyedropped. Screen Matte Clip Black ~8 / Clip White ~92, judge by eye.
- CORNER-PIN COORDINATE TRAP: Corner Pin runs in LAYER space before transform.
  Wrap the UI in a full-frame holder comp pinned at 100% scale centred — layer
  space == comp space, tracked numbers apply as-is. (Scaling the pinned layer
  instead multiplies the corners and the UI flies off screen.)
- Keyframe the pin per plate frame at absolute seconds (comp fps ≠ plate fps is
  fine), LINEAR interpolation — the solve is per-frame truth, easing it lies.
- Comp markers on the detected taps = where the UI beat lands (ripple, button
  press, success draw-on).

## UI COMP DESIGN
- Build at the screen's real aspect (tracker measures it — phone ≈ 2.2–2.35:1;
  e.g. 1080x2340). A few % of corner-pin squeeze is invisible at video size.
- Status bar 9:41 + generic glyphs; app header in brand color; NO real bank/app
  numbers, masked fields ("+91 98XXX XXXXX"); success state in BRAND color.
- Animate to the tap markers: tap 1 → selection ripple, tap 2 → button press
  pulse, tap 3 → success check draw-on + chip slide.

## CUTTING THE MASTER
Give each timeline shot ONE tap, landing LATE in the shot (action commits, then
cut to result). Plate slightly short vs slot → hold the last frame (success
screens are static) or run at 95% speed — at 60fps source both are invisible.
