from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
OUT = DOCS / "Documentacao_EstoqueFacil.pdf"
NAVY = colors.HexColor("#142b3e")
TEAL = colors.HexColor("#0f9b84")
GREY = colors.HexColor("#5e7180")
PALE = colors.HexColor("#f1f8f6")
BORDER = colors.HexColor("#dce7e7")
WHITE = colors.white

styles = {
    "cover_kicker": ParagraphStyle("cover_kicker", fontName="Helvetica-Bold", fontSize=10, leading=15, alignment=TA_CENTER, textColor=TEAL, spaceAfter=12),
    "cover_title": ParagraphStyle("cover_title", fontName="Helvetica-Bold", fontSize=31, leading=38, alignment=TA_CENTER, textColor=NAVY),
    "cover_sub": ParagraphStyle("cover_sub", fontName="Helvetica", fontSize=13, leading=20, alignment=TA_CENTER, textColor=GREY),
    "h1": ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=15, leading=20, textColor=NAVY, spaceBefore=10, spaceAfter=8, keepWithNext=True),
    "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=TEAL, spaceBefore=8, spaceAfter=5, keepWithNext=True),
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=9, leading=13.5, textColor=NAVY, spaceAfter=6),
    "small": ParagraphStyle("small", fontName="Helvetica", fontSize=7.5, leading=10, textColor=GREY, spaceAfter=4),
    "table_head": ParagraphStyle("table_head", fontName="Helvetica-Bold", fontSize=7.5, leading=10, textColor=WHITE),
    "table_body": ParagraphStyle("table_body", fontName="Helvetica", fontSize=7.3, leading=10.5, textColor=NAVY),
    "caption": ParagraphStyle("caption", fontName="Helvetica", fontSize=7.5, leading=10, alignment=TA_CENTER, textColor=GREY, spaceBefore=4, spaceAfter=8),
    "note": ParagraphStyle("note", fontName="Helvetica", fontSize=8.5, leading=12, textColor=NAVY, backColor=PALE, borderColor=BORDER, borderWidth=.5, borderPadding=8, spaceAfter=8),
}

def P(value, style="body"):
    return Paragraph(value, styles[style])

story = []
def add(*items):
    story.extend(items)
def h1(number, title):
    add(P(f"{number}. {title}", "h1"))
def h2(title):
    add(P(title, "h2"))
def para(value):
    add(P(value))
def bullet(value):
    add(P("• " + value))
def caption(value):
    add(P(value, "caption"))
def image(name, max_width=500, max_height=360):
    path = DOCS / name
    if not path.exists():
        add(P(f"[Imagem não gerada nesta execução: {escape(name)}]", "small"))
        return
    from PIL import Image as PILImage
    with PILImage.open(path) as im:
        iw, ih = im.size
    scale = min(max_width / iw, max_height / ih, 1)
    add(Image(str(path), width=iw * scale, height=ih * scale, hAlign="CENTER"))
def table(rows, widths, header=True):
    converted = []
    for idx, row in enumerate(rows):
        style = "table_head" if header and idx == 0 else "table_body"
        converted.append([P(escape(str(cell)), style) for cell in row])
    t = Table(converted, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("VALIGN", (0,0), (-1,-1), "TOP"),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LINEBELOW", (0,-1), (-1,-1), .5, BORDER),
    ]
    if header:
        commands += [("BACKGROUND", (0,0), (-1,0), NAVY), ("ROWBACKGROUNDS", (0,1), (-1,-1), [WHITE, colors.HexColor("#f8fafb")])]
    else:
        commands += [("ROWBACKGROUNDS", (0,0), (-1,-1), [WHITE, colors.HexColor("#f8fafb")])]
    t.setStyle(TableStyle(commands))
    add(t, Spacer(1, 8))

def use_case(title, goal, pre, main, alt, exceptions, post):
    h2(title)
    table([
        ["Campo", "Descrição"],
        ["Ator", "Operador da loja"],
        ["Objetivo", goal],
        ["Pré-condições", pre],
        ["Fluxo principal", main],
        ["Fluxos alternativos", alt],
        ["Exceções", exceptions],
        ["Pós-condições", post],
    ], [105, 398])

# CAPA
add(Spacer(1, 100), P("CIÊNCIA DA COMPUTAÇÃO  •  ANÁLISE E PROJETO DE SISTEMAS", "cover_kicker"),
    Spacer(1, 15), P("ESTOQUEFÁCIL", "cover_title"), Spacer(1, 14),
    P("Documentação de análise, projeto e implementação inicial de um sistema de controle de estoque", "cover_sub"),
    Spacer(1, 55), P("<b>Acadêmico:</b> José Carlos de Moraes Sousa", "cover_sub"),
    Spacer(1, 12), P("Trabalho individual", "cover_sub"), Spacer(1, 85),
    P("Franca - SP<br/>Novembro de 2026<br/>Versão documentada: 1.1", "cover_sub"),
    PageBreak())

h1("1", "Apresentação do projeto")
para("<b>Disciplina:</b> Análise e Projeto de Sistemas. <b>Modalidade:</b> individual. <b>Data da revisão:</b> 14 de novembro de 2026.")
para("O <b>EstoqueFácil</b> é um protótipo web para gerenciamento de estoque de uma pequena loja de panelas e utensílios domésticos. Permite cadastrar, editar e excluir produtos, registrar entradas e saídas, consultar indicadores, pesquisar itens, identificar estoque baixo, consultar o histórico e exportar a listagem em CSV.")
h2("1.1 Problema e justificativa")
para("O controle manual de quantidades por anotações ou planilhas isoladas pode dificultar a identificação do saldo disponível e dos itens que precisam de reposição. O protótipo concentra as operações essenciais em uma interface web simples e oferece retorno imediato após cada alteração.")
h2("1.2 Objetivos")
bullet("<b>Geral:</b> desenvolver e documentar um protótipo funcional de controle de estoque com regras explícitas de cadastro e movimentação.")
bullet("<b>Específicos:</b> levantar requisitos; definir regras de negócio; representar casos de uso e classes; implementar funcionalidades; testar regras; organizar e versionar o código.")
h2("1.3 Escopo e limitações")
para("A versão 1.1 é executada no navegador por meio de um servidor HTTP estático local. A interface possui três áreas: Visão geral, Produtos e Movimentações. Os dados são persistidos em <b>localStorage</b> no navegador utilizado. Não há backend, autenticação, sincronização entre dispositivos, banco de dados remoto ou integração com marketplaces.")
add(P("<b>Repositório público:</b> https://github.com/Josecarlos3052/Estoque-facil — ramificação main.", "note"))

h1("2", "Requisitos funcionais")
table([
    ["ID", "Requisito", "Evidência na aplicação"],
    ["RF01", "Cadastrar produto com nome, SKU, categoria, preço, estoque inicial e mínimo.", "Formulário de cadastro"],
    ["RF02", "Alterar os dados cadastrais de um produto.", "Formulário de edição"],
    ["RF03", "Registrar entrada de unidades em produto existente.", "Movimentação de entrada"],
    ["RF04", "Registrar saída de unidades em produto existente.", "Movimentação de saída"],
    ["RF05", "Buscar produtos por nome, SKU ou categoria.", "Campo de pesquisa"],
    ["RF06", "Filtrar produtos com saldo menor ou igual ao mínimo.", "Filtro de estoque baixo"],
    ["RF07", "Exibir indicadores consolidados e movimentações recentes.", "Tela Visão geral"],
    ["RF08", "Exportar a listagem de produtos em formato CSV.", "Botão Exportar CSV"],
    ["RF09", "Excluir um produto cadastrado após confirmação do operador.", "Ação Excluir"],
    ["RF10", "Consultar o histórico com pesquisa e filtro por tipo.", "Tela Movimentações"],
], [42, 300, 161])

h1("3", "Requisitos não funcionais")
table([
    ["ID", "Descrição", "Critério de observação"],
    ["RNF01", "Executar em navegador moderno com suporte a módulos JavaScript e localStorage.", "Servidor HTTP local"],
    ["RNF02", "Apresentar interface em português e adaptar-se a telas menores.", "Layout responsivo"],
    ["RNF03", "Salvar alterações localmente após cadastro e movimentação.", "Persistência no mesmo navegador"],
    ["RNF04", "Separar interface e regras de negócio em módulos.", "src/app.js e src/stock.js"],
    ["RNF05", "Permitir execução e testes sem serviço pago ou dependências externas de runtime.", "Servidor local e Node.js para testes"],
], [48, 305, 150])

h1("4", "Regras de negócio")
for item in [
    "<b>RN01:</b> o SKU é obrigatório e único entre os produtos cadastrados.",
    "<b>RN02:</b> preço e estoques não podem ser negativos.",
    "<b>RN03:</b> estoque e estoque mínimo devem ser quantidades inteiras.",
    "<b>RN04:</b> uma saída não pode superar a quantidade disponível.",
    "<b>RN05:</b> cada movimentação exige quantidade inteira maior que zero.",
    "<b>RN06:</b> o alerta de estoque baixo é acionado quando saldo ≤ mínimo.",
    "<b>RN07:</b> editar dados cadastrais não altera o saldo; o saldo muda por movimentações.",
]:
    bullet(item)

h1("5", "Casos de uso")
para("O ator principal é o <b>operador da loja</b>. O diagrama apresenta a fronteira do sistema e as operações disponíveis. Não foram incluídos relacionamentos include, extend ou generalização artificiais, pois o escopo implementado não exige esses vínculos.")
image("casos_de_uso.png", max_width=495, max_height=285)
caption("Figura 1 — Diagrama de casos de uso do EstoqueFácil 1.1. Fonte: elaboração do projeto.")
h2("5.1 Especificações textuais")
use_case("UC01 — Cadastrar produto", "Registrar um novo produto no catálogo.",
         "Aplicação aberta; acesso à tela Produtos.",
         "1. Selecionar Novo produto; 2. Preencher nome, SKU, categoria, preço, estoque inicial e mínimo; 3. Confirmar; 4. Sistema valida os dados e a unicidade do SKU; 5. Produto é incluído e salvo.",
         "O operador pode cancelar o formulário antes de confirmar.",
         "Nome curto, SKU inválido ou duplicado, categoria inválida, campo numérico vazio/negativo ou estoque fracionário: exibir erro e não cadastrar.",
         "Produto disponível na listagem e nos indicadores; armazenamento local atualizado.")
use_case("UC02 — Editar produto", "Alterar dados cadastrais de um produto existente.",
         "Produto cadastrado e disponível na tela Produtos.",
         "1. Selecionar Editar; 2. Alterar os campos permitidos; 3. Confirmar; 4. Sistema valida os dados e salva as alterações sem alterar o saldo.",
         "O operador pode cancelar a edição.",
         "Produto inexistente, SKU duplicado ou dados inválidos: manter os dados anteriores e apresentar erro.",
         "Dados cadastrais atualizados; saldo preservado.")
use_case("UC03 — Registrar entrada", "Acrescentar unidades ao saldo de um produto.",
         "Produto cadastrado e disponível para movimentação.",
         "1. Selecionar Movimentar; 2. Escolher Entrada; 3. Informar quantidade inteira positiva; 4. Confirmar; 5. Sistema soma as unidades e registra o evento.",
         "O operador pode cancelar antes de confirmar.",
         "Quantidade zero, negativa ou fracionária: nenhuma entrada é registrada.",
         "Saldo acrescido; evento incluído no histórico; dados salvos localmente.")
use_case("UC04 — Registrar saída", "Retirar unidades do saldo de um produto.",
         "Produto cadastrado; saldo disponível.",
         "1. Selecionar Movimentar; 2. Escolher Saída; 3. Informar quantidade; 4. Confirmar; 5. Sistema valida o saldo e registra a saída.",
         "O operador pode cancelar antes da confirmação.",
         "Quantidade inválida ou superior ao saldo: exibir erro, não alterar o saldo e não registrar evento.",
         "Saldo atualizado; movimentação adicionada ao histórico.")
story.append(PageBreak())
use_case("UC05 — Excluir produto", "Remover um produto do catálogo após confirmação.",
         "Produto cadastrado e visível na tela Produtos.",
         "1. Localizar o produto; 2. Selecionar Excluir; 3. Ler a confirmação; 4. Confirmar; 5. Sistema remove o produto do catálogo e atualiza os indicadores.",
         "Se o operador cancelar a confirmação, o produto permanece cadastrado.",
         "Se o produto não existir mais no estado atual, nenhuma alteração é realizada.",
         "Produto removido do catálogo; movimentações anteriores permanecem no histórico.")
use_case("UC06 — Consultar histórico", "Consultar entradas e saídas já registradas.",
         "Aplicação aberta; registros de movimentação disponíveis.",
         "1. Abrir Movimentações; 2. Consultar a lista; 3. Pesquisar por nome ou SKU; 4. Selecionar Todas, Entradas ou Saídas; 5. Sistema apresenta os registros correspondentes.",
         "Limpar a pesquisa ou selecionar Todas restaura os registros compatíveis com os demais filtros.",
         "Quando nenhum registro corresponde aos filtros, o sistema apresenta estado vazio sem alterar dados.",
         "Histórico consultado; registros preservados.")
h2("5.2 Rastreabilidade")
para("RF01 → UC01; RF02 → UC02; RF03 → UC03; RF04 → UC04; RF05/RF06 → pesquisa e filtros; RF07 → indicadores; RF08 → exportação CSV; RF09 → UC05; RF10 → UC06.")

h1("6", "Projeto de classes")
para("O diagrama representa classes de projeto com atributos privados (−), operações públicas (+), tipos, parâmetros, retornos e multiplicidades. A implementação inicial em JavaScript utiliza funções e objetos; não há tradução literal de cada elemento para a sintaxe class.")
image("classes.png", max_width=500, max_height=340)
caption("Figura 2 — Diagrama de classes de projeto. Fonte: elaboração do projeto.")
h2("6.1 Classes e responsabilidades")
table([
    ["Classe", "Responsabilidade"],
    ["Produto", "Identificação, SKU, nome, categoria, preço, saldo, mínimo e data de criação."],
    ["Movimentacao", "Registra produto relacionado, tipo, quantidade e data/hora."],
    ["ServicoEstoque", "Coordena cadastro, edição, movimentação, consulta, indicadores, exclusão e exportação."],
    ["RepositorioLocal", "Representa a responsabilidade de carregar e salvar o estado em localStorage."],
], [120, 383])
h2("6.2 Tipos, associações e multiplicidades")
para("<b>String</b> representa texto; <b>Decimal</b>, preço monetário; <b>Integer</b>, quantidades; <b>DateTime</b>, instante de registro. TipoMovimentacao admite Entrada e Saída. As associações indicam que um ServiçoEstoque gerencia zero ou muitos Produtos, consulta zero ou muitas Movimentações e utiliza um RepositorioLocal. Cada Movimentação refere-se a um Produto, que pode ter nenhuma ou muitas movimentações.")
para("Não foram criadas relações de herança, agregação ou composição artificiais. A exclusão do produto do catálogo não apaga os registros históricos associados.")
h2("6.3 Mapeamento para a implementação")
para("As regras puras estão em <b>src/stock.js</b> (validação, cadastro, edição, movimentação, pesquisa, indicadores e CSV). A navegação, os eventos, a exclusão e a persistência ficam em <b>src/app.js</b>. A interface é definida em <b>index.html</b> e <b>src/style.css</b>.")

h1("7", "Diagrama de sequência e arquitetura")
para("A sequência abaixo descreve o registro de uma saída: ação do operador, validação das regras, atualização do estado e persistência local.")
image("sequencia_saida.png", max_width=500, max_height=255)
caption("Figura 3 — Sequência de registro de saída. Fonte: elaboração do projeto.")
h2("7.1 Arquitetura")
image("arquitetura.png", max_width=500, max_height=210)
caption("Figura 4 — Organização dos componentes. Fonte: elaboração do projeto.")
para("O navegador apresenta a interface; app.js coordena eventos e estado; stock.js concentra regras de negócio; localStorage persiste os dados no navegador utilizado. O sistema não depende de backend ou serviço externo para as funções descritas.")

h1("8", "Modelo de dados e armazenamento")
table([
    ["Conjunto", "Principais campos"],
    ["products[]", "id, sku, name, category, price, stock, minimum, createdAt"],
    ["history[]", "id, productId, productName, sku, type, quantity, date"],
], [105, 398])
para("A chave de armazenamento é <b>estoquefacil-v1</b>. Na primeira inicialização, a aplicação carrega quatro produtos demonstrativos se não houver dados existentes. Cadastros e movimentações atualizam o estado completo no localStorage.")
para("O armazenamento local não sincroniza dispositivos e pode ser apagado pelo usuário. Não substitui um banco de dados corporativo nem oferece backup automático, autenticação ou controle de acesso.")

h1("9", "Interface implementada")
para("A versão 1.1 possui três telas: Visão geral, Produtos e Movimentações. A primeira apresenta quatro indicadores e resumos de estoque baixo e movimentações recentes. Produtos reúne cadastro, edição, exclusão, pesquisa, filtro de estoque baixo e exportação CSV. Movimentações permite registrar entradas e saídas e consultar o histórico por produto/SKU e tipo.")
image("tela_01_painel.png", max_width=500, max_height=275)
caption("Figura 5 — Visão geral da aplicação em execução.")
image("tela_02_cadastro.png", max_width=500, max_height=250)
caption("Figura 6 — Formulário de cadastro.")
image("tela_04_movimentacao.png", max_width=500, max_height=250)
caption("Figura 7 — Formulário de movimentação.")
image("tela_06_estoque_baixo.png", max_width=500, max_height=270)
caption("Figura 8 — Filtro de estoque baixo.")
image("tela_08_historico.png", max_width=500, max_height=270)
caption("Figura 9 — Histórico com filtros.")

h1("10", "Testes e validação")
para("A suíte de regras de negócio em <b>test/stock.test.js</b> contém 21 cenários automatizados executados pelo comando <b>npm test</b>. São cobertos cadastro, SKU duplicado, valores inválidos, edição sem alterar saldo, entradas, saídas, bloqueio por saldo insuficiente, pesquisa, alertas, indicadores e CSV.")
para("O script <b>docs/verify_ui.py</b> usa Playwright/Chromium para verificar os fluxos de cadastro, entrada, saída, filtro, pesquisa, edição, exclusão, histórico, persistência no armazenamento simulado e exportação CSV. O fluxo do GitHub Actions executa as verificações antes de gerar os arquivos finais.")
add(P("<b>Limite dos testes:</b> não foram avaliados testes de carga, segurança, sincronização, integração externa ou funcionamento em todos os navegadores e dispositivos.", "note"))

h1("11", "Versionamento e organização do repositório")
para("O repositório público está em <b>https://github.com/Josecarlos3052/Estoque-facil</b>, na ramificação main. O histórico consultado em 14/11/2026 contém mensagens semânticas de implementação, testes, correções e documentação. Parte dos commits iniciais aparece com a identidade genérica “Autor do projeto”; commits posteriores aparecem associados à conta Josecarlos3052.")
para("Os commits históricos estão concentrados em 14/11/2026, portanto não demonstram evolução distribuída por vários dias. Esta revisão preserva datas e autorias anteriores. Novas contribuições devem ser feitas pelo estudante, com sua identidade verificada, à medida que forem efetivamente desenvolvidas.")
h2("11.1 Como executar")
para("1. Baixar o repositório; 2. Abrir um terminal na pasta; 3. Executar <b>python -m http.server 8000</b>; 4. Acessar <b>http://localhost:8000</b>; 5. Para testes, executar <b>npm test</b> com Node.js 20 ou superior.")
h2("11.2 Evidência em vídeo")
para("O vídeo MP4 é gerado por execução da aplicação atual em Chromium automatizado. Ele demonstra as telas, cadastro, entrada, saída, alertas, pesquisa e histórico. O arquivo deve permanecer abaixo de 60 segundos.")

h1("12", "Resultados, limitações e melhorias futuras")
para("O EstoqueFácil demonstra a passagem dos requisitos e regras de negócio para uma implementação inicial executável. A versão atende ao escopo acadêmico de cadastro e movimentação de estoque, consulta e exportação, mantendo as regras separadas da interface.")
para("Não contempla login, múltiplas lojas, emissão fiscal, operações concorrentes, banco de dados remoto, backup automático ou integração com marketplaces. Como evolução, podem ser estudados backend, banco de dados, autenticação, permissões, backup e integração com pedidos, após novo levantamento de requisitos.")

h1("13", "Conclusão")
para("A documentação reúne problema, objetivos, requisitos, regras de negócio, casos de uso, classes, sequência, arquitetura, implementação, testes e versionamento do EstoqueFácil 1.1. O protótipo permite demonstrar funcionalidades reais dentro de um escopo reduzido e explicitar suas limitações.")
add(P("<b>Repositório:</b> https://github.com/Josecarlos3052/Estoque-facil<br/><b>Visibilidade:</b> pública • <b>Ramificação:</b> main<br/><b>Arquivos acadêmicos:</b> Documentacao_EstoqueFacil.pdf e Demo_EstoqueFacil_Interativo.mp4.", "note"))

def on_page(canvas, doc):
    canvas.saveState()
    if doc.page > 1:
        w, h = A4
        canvas.setStrokeColor(BORDER)
        canvas.setLineWidth(.5)
        canvas.line(46, h - 43, w - 46, h - 43)
        canvas.setFont("Helvetica-Bold", 7.5)
        canvas.setFillColor(TEAL)
        canvas.drawString(46, h - 34, "ESTOQUEFÁCIL  /  DOCUMENTAÇÃO DE PROJETO")
        canvas.setFont("Helvetica", 7.5)
        canvas.setFillColor(GREY)
        canvas.drawString(46, 28, "Análise e Projeto de Sistemas • Versão 1.1")
        canvas.drawRightString(w - 46, 28, str(doc.page - 1))
    canvas.restoreState()

doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=46, leftMargin=46, topMargin=55, bottomMargin=45,
                        title="EstoqueFácil — Documentação de Análise e Projeto",
                        author="José Carlos de Moraes Sousa",
                        subject="Trabalho acadêmico — Análise e Projeto de Sistemas")
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print("PDF_OK", OUT, OUT.stat().st_size)
