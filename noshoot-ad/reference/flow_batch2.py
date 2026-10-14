#!/usr/bin/env python
"""Flow batch driver v2 — WITH reference-image feeding (calibrated 2026-07-15).
Feeds uploaded media as Nano Banana references, then prompts.

Flow mechanics (learned live):
- input[type='file'] (accept=image/*, multiple) uploads straight to project media.
- '+' button (FIRST button in the 'Nano Banana' toolbar) opens the media menu;
  clicking an item by filename attaches it as a reference chip.
- Reference chips are CONSUMED by a generation (auto-clear after submit).
- Uploads keep their filename in the menu -> upload finals once, select by name.

KNOWN FAILURE MODES (batch-2 postmortem, 2026-07-15) — FIX BEFORE HEAVY REUSE:
1. RESULT ATTRIBUTION IS BY IMG-DIFF ONLY. New <img> srcs are diffed globally, so a
   slow previous gen or a media-panel refresh bleeds images into the WRONG job.
   Batch-2 saved several files under wrong names (shot7_V1 actually held shot 2's
   couple; shot2_V1/V2 held Kesar-Pista tub lineups; shot9/12/15/16 were mislabeled).
   ALWAYS content-verify by eye before renaming to *_Final. Better fix: scope the
   img-diff to the newest generation card container, not the whole page.
2. REF THUMBNAILS ECHO AS <img>. Uploading N refs adds N 300x300 thumbs that the
   differ counts as results (shot5_V1..V4 were just the fed tub JPGs echoed back).
   Fix: skip download when img natural size <= 600px (PIL check post-download works too).
3. MULTI-REF IDENTITY DRIFT. With 2+ face refs + product ref, Nano Banana often
   invents NEW faces (batch-2 pair/shot2/shot12 casts were strangers, incl. a
   white-couple bleed from the v4b reference world). Single-face jobs held identity
   fine. Fix: chain pairs from the LOCKED PAIR image (one ref), not two solos;
   re-attach refs EVERY run; verify faces before accepting.
4. Veo/NB safety: person + consumption action + brand label in one prompt sometimes
   swaps to generic actors. Keep brand cup in a separate insert shot when possible.

jobs.json entry:
  {"name":"shot2", "promptFile":"...", "outdir":"...", "runs":1,
   "refs":["G:\\\\...\\\\Shot_0_CastW_Final.jpg", "G:\\\\...\\\\Shot_0_CastM_Final.jpeg"]}
"""
import sys, os, time, json
from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9223"
GETIMGS = "els => els.map(e => e.src).filter(s => s && s.startsWith('http'))"
FIND_BAR_BTN = """(idx) => {
    const chips = [...document.querySelectorAll('button')];
    const bar = chips.find(b => (b.innerText||'').includes('Nano Banana'));
    if (!bar) return null;
    const container = bar.closest('div[class]').parentElement;
    const btns = [...container.querySelectorAll('button')];
    return idx === 'last' ? btns[btns.length-1] : btns[0];
}"""

uploaded = set()

def upload(page, path):
    if path in uploaded: return
    fi = page.query_selector("input[type='file']")
    fi.set_input_files(path)
    time.sleep(6)
    uploaded.add(path)
    print("  uploaded:", os.path.basename(path))

def attach_ref(page, path):
    name = os.path.basename(path)
    plus = page.evaluate_handle(FIND_BAR_BTN, "first").as_element()
    plus.click(); time.sleep(1.5)
    item = page.get_by_text(name, exact=False).first
    try:
        item.click(timeout=5000); time.sleep(1)
        print("  attached ref:", name)
        return True
    except Exception:
        page.keyboard.press("Escape")
        print("  REF NOT FOUND in menu:", name)
        return False

def gen_once(page, prompt, refs, outdir, name, start_idx):
    before = set(page.eval_on_selector_all("img", GETIMGS))
    for r in refs:
        upload(page, r)
    for r in refs:
        attach_ref(page, r)
    ed = page.query_selector("[data-slate-editor='true']")
    ed.click(force=True); time.sleep(0.8)
    page.keyboard.press("Control+A"); page.keyboard.press("Delete")
    page.keyboard.insert_text(prompt); time.sleep(1.5)
    btn = page.evaluate_handle(FIND_BAR_BTN, "last").as_element()
    btn.click()
    t0 = time.time(); new = []
    while time.time() - t0 < 360:
        time.sleep(8)
        cur = set(page.eval_on_selector_all("img", GETIMGS))
        if cur - before:
            time.sleep(12)
            new = list(set(page.eval_on_selector_all("img", GETIMGS)) - before)
            break
    saved = []
    for i, url in enumerate(new[:8]):
        try:
            resp = page.request.get(url)
            if resp.ok:
                fp = os.path.join(outdir, f"{name}_V{start_idx+i}.jpeg")
                open(fp, "wb").write(resp.body()); saved.append(os.path.basename(fp))
        except Exception as e:
            print("  dl fail:", str(e)[:60])
    return saved

def main():
    jobs = json.load(open(sys.argv[1], encoding="utf-8"))
    with sync_playwright() as p:
        b = p.chromium.connect_over_cdp(CDP)
        page = next(pg for pg in b.contexts[0].pages if "flow/project" in pg.url)
        page.bring_to_front()
        for job in jobs:
            os.makedirs(job["outdir"], exist_ok=True)
            prompt = open(job["promptFile"], encoding="utf-8").read().strip()
            idx = job.get("startIdx", 1)
            for r in range(job.get("runs", 1)):
                print(f"=== {job['name']} run {r+1}/{job.get('runs',1)} ===")
                saved = gen_once(page, prompt, job.get("refs", []), job["outdir"], job["name"], idx)
                print("  saved:", ", ".join(saved) if saved else "NOTHING")
                idx += max(len(saved), 2)
                time.sleep(4)
    print("BATCH2 DONE")

if __name__ == "__main__":
    main()
