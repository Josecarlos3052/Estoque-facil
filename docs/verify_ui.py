"""Verifica os fluxos principais da interface atual com Chromium/Playwright."""
from pathlib import Path
import re
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)
html = (ROOT / "index.html").read_text(encoding="utf-8")
css = re.sub(r"@import[^;]+;", "", (ROOT / "src/style.css").read_text(encoding="utf-8"), count=1)
html = re.sub(r'<link rel="stylesheet"[^>]+>', "<style>" + css + "</style>", html)
html = re.sub(r'<script type="module"[^>]+></script>', "", html)
stock = (ROOT / "src/stock.js").read_text(encoding="utf-8").replace("export ", "")
app = re.sub(r"^import .*?;\n", "", (ROOT / "src/app.js").read_text(encoding="utf-8"), count=1, flags=re.M)
javascript = stock + "\n" + app

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
    context = browser.new_context(viewport={"width": 1440, "height": 900}, accept_downloads=True)
    page = context.new_page()
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.set_content(html, wait_until="domcontentloaded")
    page.evaluate("""() => {
      const memory = {};
      Object.defineProperty(window, "localStorage", {configurable:true, value:{
        getItem:key => memory[key] ?? null,
        setItem:(key,value) => { memory[key] = String(value); },
        removeItem:key => { delete memory[key]; }
      }});
    }""")
    page.add_script_tag(content=javascript)
    page.wait_for_function("document.querySelector('#metricProducts')?.textContent === '4'")
    page.screenshot(path=str(DOCS / "tela_01_painel.png"), full_page=True)

    page.locator('.nav-link[data-view="products"]').click()
    page.locator("#addProduct").click()
    for field, value in [("name","Caçarola antiaderente 22 cm"),("sku","CAC-022"),("price","79.90"),("stock","9"),("minimum","4")]:
        page.locator(f'#productForm [name="{field}"]').fill(value)
    page.screenshot(path=str(DOCS / "tela_02_cadastro.png"), full_page=True)
    page.locator('#productForm button[type="submit"]').click()
    assert page.locator("#metricProducts").inner_text() == "5"
    assert page.locator("#productRows tr").count() == 5
    page.screenshot(path=str(DOCS / "tela_03_produto_cadastrado.png"), full_page=True)

    page.locator('#productRows button[data-action="move"]').first.click()
    page.locator('#moveForm [name="quantity"]').fill("5")
    page.screenshot(path=str(DOCS / "tela_04_movimentacao.png"), full_page=True)
    page.locator('#moveForm button[type="submit"]').click()
    assert page.locator("#movementRows tr").count() == 1
    page.screenshot(path=str(DOCS / "tela_05_movimentado.png"), full_page=True)

    page.locator('.nav-link[data-view="products"]').click()
    page.locator('#productRows button[data-action="move"]').first.click()
    page.locator('#moveForm [name="type"]').select_option("SAÍDA")
    page.locator('#moveForm [name="quantity"]').fill("2")
    page.locator('#moveForm button[type="submit"]').click()
    assert page.locator("#movementRows tr").count() == 2

    page.locator('.nav-link[data-view="products"]').click()
    page.locator("#onlyLow").check()
    assert page.locator("#productRows tr").count() == 1
    page.screenshot(path=str(DOCS / "tela_06_estoque_baixo.png"), full_page=True)
    page.locator("#onlyLow").uncheck()
    page.locator("#searchInput").fill("frigideira")
    assert page.locator("#productRows tr").count() == 1
    page.screenshot(path=str(DOCS / "tela_07_busca.png"), full_page=True)
    page.locator("#searchInput").fill("")

    page.locator('#productRows button[data-action="edit"]').first.click()
    page.locator('#productForm [name="name"]').fill("Caçarola premium 22 cm")
    page.locator('#productForm button[type="submit"]').click()
    assert "Caçarola premium 22 cm" in page.locator("#productRows").inner_text()
    page.once("dialog", lambda dialog: dialog.accept())
    page.locator('#productRows button[data-action="delete"]').first.click()
    assert page.locator("#metricProducts").inner_text() == "4"
    page.wait_for_timeout(1600)  # aguarda o aviso temporário desaparecer antes da captura

    page.locator('.nav-link[data-view="movements"]').click()
    assert page.locator("#movementRows tr").count() == 2
    page.screenshot(path=str(DOCS / "tela_08_historico.png"), full_page=True)
    page.locator("#movementTypeFilter").select_option("ENTRADA")
    assert page.locator("#movementRows tr").count() == 1
    page.locator("#movementTypeFilter").select_option("SAÍDA")
    assert page.locator("#movementRows tr").count() == 1
    page.locator("#movementTypeFilter").select_option("TODAS")
    page.locator("#movementSearch").fill("CAC-022")
    assert page.locator("#movementRows tr").count() == 2

    page.locator('.nav-link[data-view="products"]').click()
    with page.expect_download() as info:
        page.locator("#exportCSV").click()
    assert info.value.suggested_filename == "estoque-facil.csv"
    saved = page.evaluate("JSON.parse(localStorage.getItem('estoquefacil-v1'))")
    assert len(saved["history"]) == 2 and len(saved["products"]) == 4
    assert not errors, errors
    print("UI OK: cadastro, entrada, saída, filtro, busca, edição, exclusão, histórico, persistência e CSV.")
    browser.close()
