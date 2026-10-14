# VO PIPELINE — Sarvam Bulbul v3 (validated HDFC 2026-07-18)
VO-FIRST is the workflow inversion that made HDFC work: lock the voice track,
THEN cut picture to it. (Vadilal was music-first; people-ads with narration are
VO-first.) Template script: reference/generate_vo.py — copy into <Project>\VO\.

## WHY VO FIRST
- TTS reads at its own natural pace; you cannot compress 28s of speech into a
  19s cut. Measure the real WAVs, then set shot boundaries.
- One narrator voice cannot overlap itself; different characters can.
- Natural-pace floor = sum(character lines) + sum(narrator lines) + music-only
  beats. Compute it BEFORE locking the timeline length.

## SETUP (once per machine)
1. Python + `pip install requests`.
2. API key: dashboard.sarvam.ai → API Keys.
3. `<Project>\VO\.env` containing `SARVAM_API_KEY=<key>`.

## THE SCRIPT'S MODES (generate_vo.py)
| Command | What it does |
|---|---|
| `python generate_vo.py --audition` | Each role's test line x 3 candidate voices → out\audition\ |
| `python generate_vo.py` | All LINES → out\<ID>_<voice>.wav (with auto tail-clip QC) |
| `python generate_vo.py --line N2` | Regen one line only |
| `python generate_vo.py --qc` | Duration/clip table + silence-trimmed finals → out\final\ (no API calls) |
| `python generate_vo.py --alts` | Phonetic-respell A/B takes for a stubborn acronym → out\alts\ |

Config lives at the top of the script: VOICE_M1/F1/M2/NAR names + the LINES
list `("ID", VOICE, "text", pace, pitch)`.

## BULBUL v3 RULES (each one earned by a rejected take)
1. **pitch is REJECTED by the API** — pace only. Leave pitch 0.0.
2. **Acronyms PLAIN**: "HDFC", "EMI". Spaced caps ("E M I") force letter-spell
   mode = robotic staccato. Never space caps.
3. **NEVER all-caps for emphasis** — "SO old" gets read as letters S-O.
   Use "..." pauses and word order for stress.
4. Pace 1.30 on hype narrator lines = radio-ad energy (user's taste). 1.0–1.15
   for character lines.
5. Cast that worked: rohan (M lead), neha (F), mani (M2), kabir (narrator).
   Audition anyway — fit is per-script.
6. **Takes vary run to run.** A locked take is COPIED to out\final\, never
   regenerated blind. A regen needs fresh ear-approval.
7. Auto-QC catches tail-clipping (loud audio in last 100ms → auto-regen x3).
8. Cost: negligible — a 30s ad ≈ 450 chars, deep inside free tier.

## THE LOCK LOOP (user in the loop, per line)
generate → user listens → reject (note WHY: robotic / clipped / wrong energy)
→ fix text or pace → regen that --line → re-listen → approve → COPY to final\.
Track rejects in a Rejected\ subfolder — they document what not to do.

## HANDOFF
out\final\*.wav → Premiere. Write the measured durations into PRODUCTION.md
("VO REALITY" block) and conform the shot table to them. The WAV durations are
the timeline's ground truth from this point on.
