#!/usr/bin/env python3
"""
HDFC XpressWay spec ad - Bulbul v3 VO generator + QC (Sarvam AI)
Usage:
  python generate_vo.py                 -> generate ALL locked lines to out\
  python generate_vo.py --fix           -> regen only the rejected lines (M1 M2 N1 N3 N5)
  python generate_vo.py --line N5       -> regen a single line
  python generate_vo.py --acro          -> acronym variant bank (9 takes) to out\alts\
  python generate_vo.py --audition      -> voice casting samples
  python generate_vo.py --qc            -> analyze + trim everything into out\final\
Key: SARVAM_API_KEY env var or VO/.env
Docs: https://docs.sarvam.ai/api-reference-docs/text-to-speech/api/rest-api

ACRONYM LESSON (2026-07-18): spaced caps like "E M I" force letter-spell mode =
ROBOTIC staccato read (user-rejected). Bulbul v3 is trained on BFSI acronyms
(EMI, bank names) — write "EMI" / "HDFC" PLAIN for a natural connected read.
Phonetic respelling ("Ee-Em-Eye") kept as --alts fallback only.
Same for emphasis: caps "SO" was read as letters S-O — write "so" plain.
"""
import argparse, base64, os, sys, time, wave, array, shutil

try:
    import requests
except ImportError:
    sys.exit("pip install requests")

API_URL = "https://api.sarvam.ai/text-to-speech"
MODEL = "bulbul:v3"
LANG = "en-IN"
SAMPLE_RATE = 24000  # bulbul v3 max; fine for VO under music
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
FINAL = os.path.join(OUT, "final")
ALTDIR = os.path.join(OUT, "alts")

# ---------------- CASTING (v1 vignette plan — ACTIVE) ----------------
# varun = horror voice, never use.
VOICE_M1  = "rohan"   # man in mobile store  (mohit REJECTED by user: flat read)
VOICE_F1  = "neha"    # woman in boutique - take APPROVED, do not regen
VOICE_M2  = "mani"    # man at watch counter - voice approved by user
VOICE_NAR = "kabir"   # narrator - approved on N2/N3/N4 delivery

# ---------------- AD LINES (id, voice, text, pace) ----------------
# Acronyms PLAIN (see lesson above). No all-caps emphasis words.
LINES = [
    ("M1", VOICE_M1,  "Ugh... this phone is so old. Should I get a new one?",          1.0),
    ("F1", VOICE_F1,  "Ooh! And I want this jacket!",                                  1.1),
    ("M2", VOICE_M2,  "Just a designer watch for me, please.",                         1.0),
    # N1/N5 LOCKED by user 2026-07-18: flowing letters @ pace 1.30 — "radio ad"
    # energy (user grew up on radio spots). out\N1/N5_kabir.wav ARE the approved
    # b_pace130 WAVs (copied, not regenerated).
    ("N1", VOICE_NAR, "aitch dee eff see Bank XpressWay is here!",                     1.30),
    ("N2", VOICE_NAR, "Get a credit card in no time, with festive offers on cards...", 1.05),
    # N3 LOCKED by user 2026-07-18: the a_flowing take itself was approved —
    # out\N3_kabir.wav IS that WAV (copied, not regenerated).
    ("N3", VOICE_NAR, "...and easy ee em eye options. Instantly!",                     1.0),
    ("N4", VOICE_NAR, "Festive treats, festive cheer, instantly here!",                1.05),
    ("N5", VOICE_NAR, "aitch dee eff see Bank presents XpressWay.",                    1.30),
]
FIX_IDS = ["M1", "M2", "N1", "N3", "N5"]  # rejected takes; F1/N2/N4 approved as-is

# ACRONYM VARIANT BANK (--acro): plain "HDFC"/"EMI" ALSO rejected by ear, so test
# every remaining respelling. Sarvam's pronunciation dictionary is just text
# substitution pre-synthesis (no phoneme alphabet) — identical to inline respelling,
# so inline is the whole game. Candidates per line:
#   a_flowing = lowercase phonetic words -> inherit normal sentence prosody (top pick)
#   b_hyphen  = capitalized hyphenated phonetic
#   c_dotted  = dotted initialism (often read with natural "U.S."-style rhythm)
ACRO = [
    ("N1", "a_flowing", VOICE_NAR, "aitch dee eff see Bank XpressWay is here!",     1.0),
    ("N1", "b_hyphen",  VOICE_NAR, "Etch-Dee-Eff-See Bank XpressWay is here!",      1.0),
    ("N1", "c_dotted",  VOICE_NAR, "H.D.F.C. Bank XpressWay is here!",              1.0),
    ("N3", "a_flowing", VOICE_NAR, "...and easy ee em eye options. Instantly!",     1.0),
    ("N3", "b_hyphen",  VOICE_NAR, "...and easy Ee-Em-Eye options. Instantly!",     1.0),
    ("N3", "c_dotted",  VOICE_NAR, "...and easy E.M.I. options. Instantly!",        1.0),
    ("N5", "a_flowing", VOICE_NAR, "aitch dee eff see Bank presents XpressWay.",    1.0),
    ("N5", "b_hyphen",  VOICE_NAR, "Etch-Dee-Eff-See Bank presents XpressWay.",     1.0),
    ("N5", "c_dotted",  VOICE_NAR, "H.D.F.C. Bank presents XpressWay.",             1.0),
]

# HDFC SPEED BANK (--hdfc): flowing style approved (see N3) but the HDFC letters
# still felt slow/off. Pace is per-LINE (no per-word control), so the whole line
# gets the energy bump — fine for an announcer read. c_ tries "hetch" (the
# Indian-English H) in case the letter SOUND, not the speed, is what feels wrong.
HDFC_PACE = [
    ("N1", "a_pace115", VOICE_NAR, "aitch dee eff see Bank XpressWay is here!",   1.15),
    ("N1", "b_pace130", VOICE_NAR, "aitch dee eff see Bank XpressWay is here!",   1.30),
    ("N1", "c_hetch120", VOICE_NAR, "hetch dee eff see Bank XpressWay is here!",  1.20),
    ("N5", "a_pace115", VOICE_NAR, "aitch dee eff see Bank presents XpressWay.",  1.15),
    ("N5", "b_pace130", VOICE_NAR, "aitch dee eff see Bank presents XpressWay.",  1.30),
    ("N5", "c_hetch120", VOICE_NAR, "hetch dee eff see Bank presents XpressWay.", 1.20),
]

AUDITION_TEXT = {
    "M1":  ("Ugh... this phone is so old. Should I get a new one?", ["mohit", "rohan", "sunny"]),
    "F1":  ("Ooh! And I want this jacket!", ["neha", "kavya", "tanya"]),
    "M2":  ("Just a designer watch for me, please.", ["mani", "kabir", "anand"]),
    "NAR": ("HDFC Bank presents XpressWay. Festive treats, festive cheer, instantly here!", ["kabir", "aditya", "amit"]),
}

def get_key():
    k = os.environ.get("SARVAM_API_KEY")
    if not k:
        env = os.path.join(HERE, ".env")
        if os.path.exists(env):
            for ln in open(env, encoding="utf-8"):
                if ln.strip().startswith("SARVAM_API_KEY"):
                    k = ln.split("=", 1)[1].strip().strip('"').strip("'")
    if not k:
        sys.exit("Set SARVAM_API_KEY env var or put SARVAM_API_KEY=... in VO\\.env")
    return k

def tts(key, text, speaker, pace=1.0):
    # bulbul:v3 rejects pitch/loudness params (API 400) — pace only.
    body = {
        "text": text,
        "target_language_code": LANG,
        "speaker": speaker,
        "model": MODEL,
        "pace": pace,
        "speech_sample_rate": SAMPLE_RATE,
    }
    r = requests.post(API_URL, json=body,
                      headers={"api-subscription-key": key, "Content-Type": "application/json"},
                      timeout=60)
    if r.status_code != 200:
        raise RuntimeError(f"{speaker}: HTTP {r.status_code}: {r.text[:300]}")
    return base64.b64decode(r.json()["audios"][0])

def save_wav(raw, path):
    if raw[:4] == b"RIFF":
        open(path, "wb").write(raw)
    else:  # raw pcm fallback
        with wave.open(path, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SAMPLE_RATE)
            w.writeframes(raw)

# ---------------- QC ----------------
def load_samples(path):
    with wave.open(path, "rb") as w:
        sr, sw, ch, n = w.getframerate(), w.getsampwidth(), w.getnchannels(), w.getnframes()
        raw = w.readframes(n)
    if sw != 2:
        return None, sr
    a = array.array("h"); a.frombytes(raw)
    if ch > 1:
        a = a[::ch]
    return a, sr

def wav_stats(path):
    """duration, speech bounds, tail-clip detection (energy still high at end of
    file = last word chopped, like the rejected N5 take)."""
    a, sr = load_samples(path)
    if a is None:
        return None
    dur = len(a) / sr
    peak = max(1, max(max(a), -min(a)))
    thr = int(0.02 * peak)  # 2% of peak = speech start/end
    first = next((i for i, s in enumerate(a) if abs(s) >= thr), 0)
    last = len(a) - 1 - next((i for i, s in enumerate(reversed(a)) if abs(s) >= thr), 0)
    tail_n = max(1, int(sr * 0.10))  # final 100ms of the FILE
    tail_peak = max(abs(s) for s in a[-tail_n:])
    clipped = tail_peak > 0.20 * peak
    return {"dur": dur, "sr": sr, "first": first, "last": last,
            "speech": (last - first) / sr, "tail_pct": 100.0 * tail_peak / peak,
            "clipped": clipped, "arr": a}

def trim_to(src, dest, head_ms=50, tail_ms=150):
    """silence-trim into dest, keeping a natural head/tail pad."""
    st = wav_stats(src)
    if st is None:
        shutil.copy2(src, dest)
        return None
    a, sr = st["arr"], st["sr"]
    i0 = max(0, st["first"] - int(sr * head_ms / 1000))
    i1 = min(len(a), st["last"] + int(sr * tail_ms / 1000))
    seg = a[i0:i1]
    with wave.open(dest, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes(seg.tobytes())
    return len(seg) / sr

def gen_line(key, lid, spk, text, pace, dest_dir, tag=""):
    """generate with automatic tail-clip QC: bad take -> regen, up to 3 tries."""
    path = os.path.join(dest_dir, f"{lid}_{spk}{tag}.wav")
    for attempt in range(1, 4):
        save_wav(tts(key, text, spk, pace), path)
        st = wav_stats(path)
        if st is None:
            print(f"  [{lid}] saved (couldn't analyze)")
            return path
        if not st["clipped"]:
            print(f"  [{lid}] {spk}{tag} OK  ({st['dur']:.2f}s, tail {st['tail_pct']:.0f}% of peak)")
            return path
        print(f"  [{lid}] attempt {attempt}: TAIL-CLIPPED (tail {st['tail_pct']:.0f}% of peak) -> regen")
        time.sleep(0.5)
    print(f"  [{lid}] WARNING: still clipped after 3 tries — listen before use")
    return path

def qc_report():
    os.makedirs(FINAL, exist_ok=True)
    print(f"{'id':4} {'voice':7} {'raw':>7} {'speech':>7} {'tail%':>6} {'clip':>5} {'final':>7}")
    total = 0.0
    for lid, spk, text, pace in LINES:
        src = os.path.join(OUT, f"{lid}_{spk}.wav")
        if not os.path.exists(src):
            print(f"{lid:4} {spk:7} MISSING — run: python generate_vo.py --line {lid}")
            continue
        st = wav_stats(src)
        fdur = trim_to(src, os.path.join(FINAL, f"{lid}_{spk}.wav"))
        flag = "CLIP!" if st["clipped"] else "ok"
        print(f"{lid:4} {spk:7} {st['dur']:6.2f}s {st['speech']:6.2f}s {st['tail_pct']:5.1f} {flag:>5} {fdur:6.2f}s")
        total += fdur or 0
    print(f"\ntotal speech (trimmed, back-to-back): {total:.2f}s")
    print(f"finals written to: {FINAL}  <- import THESE into Premiere")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audition", action="store_true")
    ap.add_argument("--acro", action="store_true", help="acronym variant bank (3 styles x N1/N3/N5) -> out\\alts")
    ap.add_argument("--hdfc", action="store_true", help="HDFC speed bank (3 takes x N1/N5) -> out\\alts")
    ap.add_argument("--fix", action="store_true", help="regen only rejected ids: " + " ".join(FIX_IDS))
    ap.add_argument("--qc", action="store_true", help="analyze + trim -> out\\final (no API calls)")
    ap.add_argument("--line", help="regen one line id e.g. M1, N2")
    a = ap.parse_args()

    if a.qc:
        qc_report()
        return

    key = get_key()
    os.makedirs(OUT, exist_ok=True)

    if a.audition:
        adir = os.path.join(OUT, "audition"); os.makedirs(adir, exist_ok=True)
        for role, (text, voices) in AUDITION_TEXT.items():
            print(f"[{role}] \"{text}\"")
            for v in voices:
                try:
                    save_wav(tts(key, text, v), os.path.join(adir, f"{role}_{v}.wav"))
                    print(f"  saved {role}_{v}.wav")
                except Exception as e:
                    print(f"  FAIL {v}: {e}")
                time.sleep(0.4)
        return

    if a.acro:
        os.makedirs(ALTDIR, exist_ok=True)
        for lid, tag, spk, text, pace in ACRO:
            print(f"[{lid} {tag}] \"{text}\"")
            gen_line(key, lid, spk, text, pace, ALTDIR, tag=f"_{tag}")
            time.sleep(0.4)
        print(f"\n9 takes in {ALTDIR} — listen per line (a_flowing / b_hyphen / c_dotted),")
        print("tell me which letter wins per line; I'll lock it into LINES and regen finals.")
        return

    if a.hdfc:
        os.makedirs(ALTDIR, exist_ok=True)
        for lid, tag, spk, text, pace in HDFC_PACE:
            print(f"[{lid} {tag}] pace {pace}: \"{text}\"")
            gen_line(key, lid, spk, text, pace, ALTDIR, tag=f"_{tag}")
            time.sleep(0.4)
        print(f"\n6 takes in {ALTDIR} — a=pace1.15  b=pace1.30  c=hetch@1.20.")
        print("Pick per line (N1 + N5); I'll lock pace/spelling into LINES and finalize.")
        return

    ids = FIX_IDS if a.fix else None
    todo = [l for l in LINES if (a.line and l[0] == a.line.upper()) or (ids and l[0] in ids) or (not a.line and not ids)]
    if not todo:
        sys.exit(f"No line id '{a.line}'. Ids: {', '.join(l[0] for l in LINES)}")
    for lid, spk, text, pace in todo:
        print(f"[{lid}] {spk}: \"{text}\"")
        gen_line(key, lid, spk, text, pace, OUT)
        time.sleep(0.4)
    print("\nNow run: python generate_vo.py --qc   (trims everything into out\\final)")

if __name__ == "__main__":
    main()
