#!/usr/bin/env python
"""Flow (labs.google) image-generation automation via CDP attach.
Attaches to the USER'S OWN Chrome (their Google login) started with:
    chrome --remote-debugging-port=9222
Usage:
    python flow_automate.py status                     # can we attach? what page is open?
    python flow_automate.py shoot "<prompt>" [n]       # type prompt, generate, wait, download n outputs
    python flow_automate.py batch <prompts.json>       # run a list: [{"name":"shot3","prompt":"..."}]
Downloads land in FLOW_OUT (default: G:\\GLM\\No Shoot Ads\\Icecream Ad\\Assets\\auto).
NOTE: Flow's UI changes often — selectors below are best-effort and meant to be
iterated live. Run `status` first; if selectors miss, dump the DOM with `dom`.
"""
import sys, os, json, time
from playwright.sync_api import sync_playwright

CDP = "http://127.0.0.1:9223"
OUT = os.environ.get("FLOW_OUT", r"G:\GLM\No Shoot Ads\Icecream Ad\Assets\auto")
# SETUP (learned 2026-07-15):
# - Chrome 136+ IGNORES --remote-debugging-port on the default profile -> must use a
#   dedicated --user-data-dir automation profile (one-time Google login there).
# - Port 9222 is often taken by Adobe UXP (Premiere) -> we use 9223.
# Launch command:
#   "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9223
#     --user-data-dir="C:\Users\USER\.claude\skills\noshoot-ad\chrome-automation-profile"
#     "https://labs.google/fx/tools/flow/project/<PROJECT_ID>"

def attach(p):
    browser = p.chromium.connect_over_cdp(CDP)
    ctx = browser.contexts[0]
    page = next((pg for pg in ctx.pages if "labs.google" in pg.url), None)
    if page is None:
        page = ctx.new_page(); page.goto(
            "https://labs.google/fx/tools/flow", wait_until="domcontentloaded")
    return browser, page

def cmd_status():
    with sync_playwright() as p:
        try:
            b, page = attach(p)
        except Exception as e:
            print("ATTACH FAILED:", e)
            print("Start Chrome with: chrome --remote-debugging-port=9222"); return
        print("attached OK"); print("url:", page.url); print("title:", page.title())

def cmd_dom():
    with sync_playwright() as p:
        b, page = attach(p)
        # dump candidate interactive elements to find selectors
        els = page.eval_on_selector_all(
            "textarea, [contenteditable='true'], button",
            "els => els.slice(0,60).map(e => ({tag:e.tagName, text:(e.innerText||e.placeholder||'').slice(0,80), aria:e.getAttribute('aria-label')}))")
        print(json.dumps(els, indent=1)[:4000])

def find_promptbox(page):
    for sel in ["textarea", "[contenteditable='true']",
                "[aria-label*='prompt' i]", "[placeholder*='describe' i]"]:
        el = page.query_selector(sel)
        if el: return el
    raise RuntimeError("prompt box not found — run `dom` and update selectors")

def cmd_shoot(prompt, n=2):
    os.makedirs(OUT, exist_ok=True)
    with sync_playwright() as p:
        b, page = attach(p)
        box = find_promptbox(page)
        box.click(); page.keyboard.press("Control+A"); page.keyboard.type(prompt, delay=8)
        # generate: try common triggers
        for sel in ["button[aria-label*='generate' i]", "button:has-text('Generate')",
                    "button[type='submit']"]:
            btn = page.query_selector(sel)
            if btn: btn.click(); break
        else:
            page.keyboard.press("Control+Enter")
        print("generation triggered, waiting for results...")
        t0 = time.time()
        # heuristic wait: watch for new <img> elements appearing
        before = page.eval_on_selector_all("img", "els => els.length")
        while time.time() - t0 < 300:
            time.sleep(5)
            now = page.eval_on_selector_all("img", "els => els.length")
            if now > before:
                time.sleep(8)  # let the full batch land
                break
        # screenshot the result grid as a review contact-sheet
        shot = os.path.join(OUT, f"contact_{int(time.time())}.png")
        page.screenshot(path=shot, full_page=False)
        print("contact sheet:", shot)
        print("(review it; if outputs look right, download via UI or extend this script "
              "with the download-button selector from `dom`)")

def cmd_batch(path):
    jobs = json.load(open(path, encoding="utf-8"))
    for j in jobs:
        print("=== ", j["name"], " ===")
        cmd_shoot(j["prompt"], j.get("n", 2))
        time.sleep(3)

if __name__ == "__main__":
    a = sys.argv[1:] or ["status"]
    if a[0] == "status": cmd_status()
    elif a[0] == "dom": cmd_dom()
    elif a[0] == "shoot": cmd_shoot(a[1], int(a[2]) if len(a) > 2 else 2)
    elif a[0] == "batch": cmd_batch(a[1])
    else: print(__doc__)
