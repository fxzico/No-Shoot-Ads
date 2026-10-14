# FAILURE MODES & QC — reject on sight
From v4b's own BTS videos (they show the broken frames): [8aJe9wfxxwA][pvhYzW_EBu8][udhWaNFQ8dg].
"AI doesn't get it right the first time or the second or the 10th." Fix is always post.

## ARTIFACTS (reject if any survive to final)
| Artifact | Fix |
|---|---|
| Merged/extra/missing fingers | reroll; roto/inpaint hand; hide hand behind product |
| Eyes drifting / mismatched gaze | reroll; AE eye stabilize; avoid long eye holds |
| Lip-sync off | dedicated lip-sync pass; shorten on-camera dialogue; cutaways |
| **Text-on-product distorted** (THE big one) | lock label (ControlNet) / real 3D model / comp real label in AE |
| Product-vs-hand scale wrong | reroll with scale ref; composite at correct size |
| Objects clipping through each other | reroll; roto separation; reframe to hide overlap |
| Physics desync (steam/liquid frozen while subject moves) | reroll motion (short physical prompt); replace element in post |
| Morph/warp between frames | shorten motion prompt to one action + one camera move |

Validates our rules: text-distortion → Golden Rule 1 + geometry lock + 3D · physics/morph →
short physical motion prompts · hands/eyes/lip-sync → 3-4 variants + post not optional.

## STANDARD QC PASS (before calling any shot done)
1. Label legible, correct spelling (100% zoom). 2. Hands: count fingers, check contact points.
3. Face: gaze steady, lip-sync locked. 4. Scale reads true. 5. Nothing clips through anything.
6. Dynamics move consistently with subject. 7. No morph/warp across the clip. 8. Light
direction consistent shot-to-shot. 9. (Listing) muted-readable, safe-area, loop seam clean.
