"""Grava a demonstração da versão atual do EstoqueFácil em Chromium isolado."""
from pathlib import Path
import re
import subprocess
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
RECORDINGS = DOCS / "_recordings"
RECORDINGS.mkdir(exist_ok=True)
html = (ROOT / "index.html").read_text(encoding="utf-8")
css = re.sub(r"@import[^;]+;", "", (ROOT / "src/style.css").read_text(encoding="utf-8"), count=1)
html = re.sub(r'<link rel="stylesheet"[^>]+>', "<style>" + css + "</style>", html)
html = re.sub(r'<script type="module"[^>]+></script>', "", html)
stock = (ROOT / "src/stock.js").read_text(encoding="utf-8").replace("export ", "")
app = re.sub(r"^import .*?;\n", "", (ROOT / "src/app.js").read_text(encoding="utf-8"), count=1, flags=re.M)
javascript = stock + "\n" + app

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
    context = browser.new_context(viewport={"width":1280,"height":720}, record_video_dir=str(RECORDINGS),
                                 record_video_size={"width":1280,"height":720}, accept_downloads=True)
    page = context.new_page()
    page.set_content(html, wait_until="domcontentloaded")
    page.evaluate("""() => {
      const memory = {};
      Object.defineProperty(window, "localStorage", {configurable:true, value:{
        getItem:key => memory[key] ?? null,
        setItem:(key,value) => { memory[key] = String(value); },
        removeItem:key => { delete memory[key]; }
      }});
      const bar = document.createElement("div");
      bar.id = "demoBar";
      bar.style.cssText = "position:fixed;z-index:99999;left:18px;bottom:14px;right:18px;background:rgba(11,35,50,.94);border-left:5px solid #35d9b8;border-radius:8px;color:#fff;font:700 16px Arial,sans-serif;padding:10px 16px;pointer-events:none";
      document.body.append(bar);
    }""")
    page.add_script_tag(content=javascript)
    def caption(text):
        page.locator("#demoBar").evaluate("(el, value) => el.textContent = value", text)
        page.wait_for_timeout(100)

    caption("ESTOQUEFÁCIL 1.1  |  1/6 — VISÃO GERAL")
    page.wait_for_timeout(3500)
    caption("2/6 — PRODUTOS: cadastro de um novo item")
    page.locator('.nav-link[data-view="products"]').click()
    page.locator("#addProduct").click()
    for field, value in [("name","Caçarola antiaderente 22 cm"),("sku","CAC-022"),("price","79.90"),("stock","9"),("minimum","4")]:
        page.locator(f'#productForm [name="{field}"]').fill(value)
    page.wait_for_timeout(2200)
    page.locator('#productForm button[type="submit"]').click()
    page.wait_for_timeout(1500)
    caption("3/6 — ENTRADA: cinco unidades adicionadas")
    page.locator('#productRows button[data-action="move"]').first.click()
    page.locator('#moveForm [name="quantity"]').fill("5")
    page.wait_for_timeout(2000)
    page.locator('#moveForm button[type="submit"]').click()
    page.wait_for_timeout(1500)
    caption("4/6 — SAÍDA: duas unidades retiradas com validação de saldo")
    page.locator('.nav-link[data-view="products"]').click()
    page.locator('#productRows button[data-action="move"]').first.click()
    page.locator('#moveForm [name="type"]').select_option("SAÍDA")
    page.locator('#moveForm [name="quantity"]').fill("2")
    page.wait_for_timeout(600)
    page.locator('#moveForm button[type="submit"]').click()
    page.wait_for_timeout(1500)
    caption("5/6 — ALERTAS E PESQUISA: filtro de estoque baixo")
    page.locator('.nav-link[data-view="products"]').click()
    page.locator("#onlyLow").check()
    page.wait_for_timeout(2200)
    page.locator("#onlyLow").uncheck()
    page.locator("#searchInput").fill("frigideira")
    page.wait_for_timeout(1300)
    caption("6/6 — MOVIMENTAÇÕES: histórico e filtro por tipo")
    page.locator('.nav-link[data-view="movements"]').click()
    page.locator("#movementTypeFilter").select_option("ENTRADA")
    page.wait_for_timeout(900)
    page.locator("#movementTypeFilter").select_option("TODAS")
    page.wait_for_timeout(1000)
    caption("ESTOQUEFÁCIL 1.1 — demonstração da aplicação em execução")
    page.wait_for_timeout(1800)
    video = page.video
    context.close()
    browser.close()
    tmp = Path(video.path())
    output = DOCS / "Demo_EstoqueFacil_Interativo.mp4"
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(tmp),"-c:v","libx264",
                    "-preset","veryfast","-crf","22","-pix_fmt","yuv420p","-movflags","+faststart","-an",str(output)], check=True)
    print("VIDEO_OK", output, output.stat().st_size)
