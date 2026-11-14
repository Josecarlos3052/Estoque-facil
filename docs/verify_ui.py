from playwright.sync_api import sync_playwright
from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]
docs=root/'docs'
html=(root/'index.html').read_text()
css=(root/'src/style.css').read_text()
css=re.sub(r'@import[^;]+;','',css,count=1)
html=re.sub(r'<link rel="stylesheet"[^>]+>', '<style>'+css+'</style>',html)
html=re.sub(r'<script type="module"[^>]+></script>', '', html)
stock=(root/'src/stock.js').read_text().replace('export ','')
app=(root/'src/app.js').read_text()
app=re.sub(r'^import .*?;\n','',app,count=1)
js=stock+'\n'+app
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage','--no-proxy-server'])
    page=browser.new_page(viewport={'width':1440,'height':810},device_scale_factor=1)
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.set_content(html,wait_until='domcontentloaded')
    page.evaluate("""() => {const memory={}; Object.defineProperty(window,'localStorage',{configurable:true,value:{getItem:k=>memory[k]??null,setItem:(k,v)=>memory[k]=v,removeItem:k=>delete memory[k]}})}""")
    page.add_script_tag(content=js)
    page.wait_for_selector('tr')
    page.screenshot(path=str(docs/'tela_01_painel.png'))
    assert page.locator('#metricProducts').inner_text()=='4'
    page.click('#addProduct')
    page.locator('#productForm [name=name]').fill('Caçarola antiaderente 22 cm')
    page.locator('#productForm [name=sku]').fill('CAC-022')
    page.locator('#productForm [name=price]').fill('79.90')
    page.locator('#productForm [name=stock]').fill('9')
    page.locator('#productForm [name=minimum]').fill('4')
    page.screenshot(path=str(docs/'tela_02_cadastro.png'))
    page.locator('#productForm button[type=submit]').click()
    assert page.locator('#metricProducts').inner_text()=='5'
    page.screenshot(path=str(docs/'tela_03_produto_cadastrado.png'))
    page.locator('button[data-action="move"]').first.click()
    page.locator('#moveForm [name=quantity]').fill('5')
    page.screenshot(path=str(docs/'tela_04_movimentacao.png'))
    page.locator('#moveForm button[type=submit]').click()
    assert page.locator('#metricUnits').inner_text()=='54'
    page.screenshot(path=str(docs/'tela_05_movimentado.png'))
    page.locator('#onlyLow').check()
    page.screenshot(path=str(docs/'tela_06_estoque_baixo.png'))
    assert page.locator('#productRows tr').count()==1
    page.locator('#onlyLow').uncheck()
    page.locator('#searchInput').fill('frigideira')
    page.screenshot(path=str(docs/'tela_07_busca.png'))
    assert page.locator('#productRows tr').count()==1
    assert not errors, errors
    print('UI OK: cadastro, movimentação, filtro e pesquisa; erros JS:',len(errors))
    browser.close()
