#!/usr/bin/env python
"""Flow batch driver — CALIBRATED 2026-07-15 (working end-to-end).
Runs a queue of prompts through Flow (Nano Banana), downloads each batch.

SETUP (one-time):
  "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9223
    --user-data-dir="C:\\Users\\USER\\.claude\\skills\\noshoot-ad\\chrome-automation-profile"
    "https://labs.google/fx/tools/flow/project/<PROJECT_ID>"
  (login once in that window; profile persists)

CALIBRATION NOTES (Flow UI, July 2026):
- Prompt box = Slate editor: [data-slate-editor='true'] — click(force=True), then
  keyboard.insert_text(). Placeholder span intercepts normal clicks.
- input[aria-label='Editable text'] at the top is the PROJECT TITLE — do not type there.
- Submit = last <button> in the toolbar containing the 'Nano Banana' chip (arrow icon).
- Default output = 2 images per run ("x2" chip). Run same prompt again for more variants.
- New images appear as googleusercontent <img> in the grid; download via page.request.get
  (authenticated). Poll img srcs before/after.

Usage:
  python flow_batch.py jobs.json
  jobs.json: [{"name":"castW","promptFile":"p.txt","outdir":"G:\\\\...","runs":2}, ...]
"""
import sys, os, time, json
from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9223"
GETIMGS = "els => els.map(e => e.src).filter(s => s && s.startsWith('http'))"
FIND_ARROW = """() => {
    const chips = [...document.querySelectorAll('button')];
    const bar = chips.find(b => (b.innerText||'').includes('Nano Banana'));
    if (!bar) return null;
    const container = bar.closest('div[class]').parentElement;
    const btns = [...container.querySelectorAll('button')];
    return btns[btns.length - 1];
}"""

def gen_once(page, prompt, outdir, name, start_idx):
    before = set(page.eval_on_selector_all("img", GETIMGS))
    ed = page.query_selector("[data-slate-editor='true']")
    ed.click(force=True); time.sleep(0.8)
    page.keyboard.press("Control+A"); page.keyboard.press("Delete")
    page.keyboard.insert_text(prompt); time.sleep(1.5)
    btn = page.evaluate_handle(FIND_ARROW).as_element()
    if btn: btn.click()
    else: page.keyboard.press("Enter")
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
            r = page.request.get(url)
            if r.ok:
                fp = os.path.join(outdir, f"{name}_V{start_idx+i}.jpeg")
                open(fp, "wb").write(r.body()); saved.append(os.path.basename(fp))
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
                saved = gen_once(page, prompt, job["outdir"], job["name"], idx)
                print("  saved:", ", ".join(saved) if saved else "NOTHING (check UI)")
                idx += max(len(saved), 2)
                time.sleep(4)
    print("BATCH DONE")

if __name__ == "__main__":
    main()
