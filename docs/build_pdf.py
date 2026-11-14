from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, KeepTogether, HRFlowable
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pathlib import Path
from xml.sax.saxutils import escape
root=Path(__file__).resolve().parents[1]; docs=root/'docs'; outfile=docs/'Documentacao_EstoqueFacil.pdf'
pdfmetrics.registerFont(TTFont('DejaVu','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'))
pdfmetrics.registerFont(TTFont('DejaVu-Bold','/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'))
NAVY=colors.HexColor('#142b3e'); TEAL=colors.HexColor('#0f9b84'); GREY=colors.HexColor('#5e7180'); LIGHT=colors.HexColor('#f1f8f6'); BORD=colors.HexColor('#dce7e7')
styles={
 'cover_label':ParagraphStyle('cover_label',fontName='DejaVu-Bold',fontSize=11,leading=18,alignment=TA_CENTER,textColor=TEAL,spaceAfter=13),
 'cover_title':ParagraphStyle('cover_title',fontName='DejaVu-Bold',fontSize=34,leading=42,alignment=TA_CENTER,textColor=NAVY),
 'cover_sub':ParagraphStyle('cover_sub',fontName='DejaVu',fontSize=14,leading=22,alignment=TA_CENTER,textColor=GREY),
 'h1':ParagraphStyle('h1',fontName='DejaVu-Bold',fontSize=16,leading=23,spaceBefore=14,spaceAfter=10,textColor=NAVY),
 'h2':ParagraphStyle('h2',fontName='DejaVu-Bold',fontSize=12,leading=18,spaceBefore=13,spaceAfter=6,textColor=TEAL),
 'body':ParagraphStyle('body',fontName='DejaVu',fontSize=9.55,leading=15.6,spaceAfter=8,textColor=NAVY),
 'small':ParagraphStyle('small',fontName='DejaVu',fontSize=8.2,leading=12.7,spaceAfter=7,textColor=GREY),
 'note':ParagraphStyle('note',fontName='DejaVu',fontSize=9.1,leading=14.8,spaceAfter=9,textColor=NAVY,backColor=LIGHT,borderPadding=10,borderColor=BORD,borderWidth=.5),
 'tablehead':ParagraphStyle('tablehead',fontName='DejaVu-Bold',fontSize=8,leading=11,textColor=colors.white),
 'tablebody':ParagraphStyle('tablebody',fontName='DejaVu',fontSize=7.8,leading=12.5,textColor=NAVY),
 'caption':ParagraphStyle('caption',fontName='DejaVu',fontSize=8.2,leading=12.8,alignment=TA_CENTER,textColor=GREY,spaceBefore=5,spaceAfter=15),
}
def P(text,style='body'):return Paragraph(text,styles[style])
width=A4[0]-92
story=[]
def add(*items):story.extend(items)
def section(n,title):add(P(f'{n}. {title}','h1'))
def sub(title):add(P(title,'h2'))
def para(text):add(P(text))
def bullet(text):add(P('• '+text))
def img(p,w=None,maxh=415):
 from PIL import Image as PILImage
 a=PILImage.open(p); iw,ih=a.size
 w=w or width; h=w*ih/iw
 if h>maxh: h=maxh;w=h*iw/ih
 add(Image(str(p),width=w,height=h,hAlign='CENTER'))
def caption(text):add(P(text,'caption'))
def table(rows,widths,header=True):
 converted=[]
 for r,row in enumerate(rows):converted.append([P(escape(str(x)), 'tablehead' if r==0 and header else 'tablebody') for x in row])
 t=Table(converted,colWidths=widths,repeatRows=1 if header else 0,hAlign='LEFT')
 cmds=[('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),6.4),('BOTTOMPADDING',(0,0),(-1,-1),6.4),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('LINEBELOW',(0,-1),(-1,-1),.6,BORD)]
 if header:cmds.extend([('BACKGROUND',(0,0),(-1,0),NAVY),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#f8fafb')])])
 else:cmds.append(('ROWBACKGROUNDS',(0,0),(-1,-1),[colors.white,colors.HexColor('#f8fafb')]))
 t.setStyle(TableStyle(cmds)); add(t,Spacer(1,10))
def page():add(PageBreak())
# COVER
add(Spacer(1,113),P('CIÊNCIA DA COMPUTAÇÃO  •  ANÁLISE E PROJETO DE SISTEMAS','cover_label'),Spacer(1,19),P('ESTOQUEFÁCIL','cover_title'),Spacer(1,18),P('Documentação de análise, projeto e implementação inicial de um sistema de controle de estoque','cover_sub'),Spacer(1,64))
add(HRFlowable(width='42%',thickness=4,color=TEAL,hAlign='CENTER'),Spacer(1,50))
add(P('<b>Acadêmico:</b> José Carlos de Moraes Sousa','cover_sub'),Spacer(1,17),P('<b>Trabalho individual</b>','cover_sub'),Spacer(1,110),P('Franca - SP<br/>Novembro de 2026<br/>Entrega: 18/11/2026, até 21h','cover_sub'))
page()
section('1','Apresentação do projeto')
para('<b>Disciplina:</b> Análise e Projeto de Sistemas. <b>Modalidade:</b> individual. <b>Data da documentação:</b> 14 de novembro de 2026.')
para('O <b>EstoqueFácil</b> é um protótipo web para gerenciamento de estoque de uma pequena loja de panelas e utensílios domésticos. Ele permite consultar produtos, cadastrar itens, registrar entrada e saída de mercadorias e identificar produtos que necessitam reposição. O objetivo é aplicar análise de requisitos, modelagem de software, implementação inicial, testes e controle de versão com Git em um escopo possível de demonstrar.')
sub('1.1 Problema e justificativa')
para('Pequenos negócios podem controlar quantidades por anotações ou planilhas isoladas. Essa prática dificulta identificar o saldo disponível e perceber quando um item está abaixo do mínimo desejado. O sistema concentra dados e operações essenciais em uma interface web simples, com retorno imediato ao usuário.')
sub('1.2 Objetivos')
bullet('<b>Geral:</b> desenvolver e documentar um protótipo funcional de controle de estoque com regras explícitas de cadastro e movimentação.')
bullet('<b>Específicos:</b> levantar requisitos; descrever regras de negócio; representar casos de uso e estruturas; implementar funcionalidades; testar regras; organizar e versionar o código.')
sub('1.3 Público e envolvidos')
para('O ator principal é o <b>operador da loja</b>, responsável por acompanhar o estoque e registrar as movimentações. Os produtos representam mercadorias de demonstração de uma loja de panelas e utensílios; os dados não correspondem a uma operação comercial real.')
sub('1.4 Delimitação da entrega')
para('A versão 1.0 é executada no navegador, sem servidor e sem autenticação. Utiliza HTML, CSS, JavaScript e armazenamento local. Os dados persistem apenas no navegador utilizado. O foco está em uma implementação inicial verificável, não em um sistema comercial multiusuário.')
add(P('<b>Situação do repositório GitHub:</b> o código está preparado e contém commit local; <b>inserir aqui o link real após publicar o repositório.</b> A publicação remota ainda precisa ser concluída.','note'))
section('2','Metodologia e visão das etapas')
para('O trabalho foi organizado por levantamento do problema, definição de requisitos, modelagem, programação e testes. As funcionalidades foram priorizadas por valor de uso e baixa dependência externa. As regras de estoque foram isoladas em um módulo próprio, favorecendo validação por testes automatizados.')
page()
section('3','Requisitos funcionais')
table([
 ['ID','Requisito','Implementação'],
 ['RF01','Cadastrar produto com nome, SKU, categoria, preço, saldo inicial e mínimo.','Formulário de cadastro'],
 ['RF02','Alterar os dados cadastrais de um produto.','Formulário de edição'],
 ['RF03','Registrar entrada de unidades em produto existente.','Movimentação de entrada'],
 ['RF04','Registrar saída de unidades em produto existente.','Movimentação de saída'],
 ['RF05','Buscar produtos por nome, SKU ou categoria.','Campo de busca'],
 ['RF06','Listar apenas produtos com saldo no limite mínimo ou abaixo.','Filtro de estoque baixo'],
 ['RF07','Exibir indicadores consolidados e últimas movimentações.','Painel e histórico'],
 ['RF08','Exportar produtos em formato CSV.','Botão de exportação'],
], [43,320,140])
section('4','Requisitos não funcionais')
table([
 ['ID','Descrição','Critério de observação'],
 ['RNF01','Executar em navegador moderno com suporte a módulos JS e localStorage.','Abertura por servidor HTTP local'],
 ['RNF02','Interface em português e adaptável a telas menores.','Layout responsivo'],
 ['RNF03','Salvar alterações localmente após cadastro ou movimentação.','Persistência no mesmo navegador'],
 ['RNF04','Usar módulos de código separados para interface e regras.','Organização dos arquivos em src/'],
 ['RNF05','Permitir execução e testes sem serviço pago ou instalação de dependências.','Servidor local e node --test'],
], [55,295,153])
section('5','Regras de negócio')
bullet('<b>RN01:</b> o SKU é obrigatório e único entre os produtos cadastrados.')
bullet('<b>RN02:</b> preço e estoques não podem ser negativos.')
bullet('<b>RN03:</b> estoque e estoque mínimo devem ser quantidades inteiras.')
bullet('<b>RN04:</b> uma saída não pode superar a quantidade disponível.')
bullet('<b>RN05:</b> cada movimentação precisa ter quantidade inteira maior que zero.')
bullet('<b>RN06:</b> o alerta é acionado quando o saldo é menor ou igual ao mínimo cadastrado.')
bullet('<b>RN07:</b> a edição de cadastro não altera o saldo; este é atualizado por movimentações.')
section('6','Casos de uso')
para('O operador realiza operações diretamente pela interface do sistema. O diagrama resume as ações disponibilizadas na versão implementada.')
img(docs/'casos_de_uso.png',maxh=345);caption('Figura 1 - Casos de uso da versão 1.0. Fonte: elaboração do projeto.')
sub('6.1 Especificações textuais dos casos de uso')
para('Os casos de uso a seguir registram o comportamento observado na versão implementada e foram selecionados por serem funcionalidades centrais e demonstráveis.')
sub('UC01 - Cadastrar produto')
table([
 ['Campo','Descrição'],
 ['Ator','Operador da loja'],
 ['Objetivo','Registrar um novo produto para acompanhamento de estoque.'],
 ['Pré-condições','Aplicação aberta; acesso à tela de produtos.'],
 ['Fluxo principal','1. Selecionar Novo produto; 2. Preencher nome, SKU, categoria, preço, estoque inicial e mínimo; 3. Confirmar; 4. Sistema valida os dados e verifica unicidade do SKU; 5. Produto é cadastrado, exibido e salvo localmente.'],
 ['Fluxo alternativo','O operador pode cancelar o formulário antes de confirmar, sem alteração no estoque.'],
 ['Exceções','Nome curto, SKU fora do padrão ou duplicado, categoria inválida, valor numérico vazio/negativo ou estoque fracionário: informar erro e não cadastrar.'],
 ['Pós-condições','Novo produto disponível na listagem e nos indicadores; persistência local atualizada.'],
], [117,386])
sub('UC02 - Registrar entrada de mercadoria')
table([
 ['Campo','Descrição'],
 ['Ator','Operador da loja'],
 ['Objetivo','Acrescentar unidades ao saldo de um produto existente.'],
 ['Pré-condições','Produto cadastrado e localizado na listagem.'],
 ['Fluxo principal','1. Escolher Movimentar no produto; 2. Manter o tipo Entrada; 3. Informar quantidade inteira positiva; 4. Confirmar; 5. Sistema soma quantidade ao saldo, salva a movimentação e atualiza indicadores.'],
 ['Fluxo alternativo','Operador pode cancelar antes da confirmação, sem movimentar o estoque.'],
 ['Exceções','Quantidade zero, negativa ou fracionária: exibir mensagem de validação; nenhuma entrada é registrada.'],
 ['Pós-condições','Saldo acrescido; evento registrado no histórico; estado salvo no navegador.'],
], [117,386])
sub('UC03 - Registrar saída de mercadoria')
table([
 ['Campo','Descrição'],
 ['Identificação','UC03 - Registrar saída de mercadoria'],
 ['Ator','Operador da loja'],
 ['Pré-condições','Produto cadastrado; aplicação aberta no navegador.'],
 ['Fluxo principal','1. Selecionar Movimentar; 2. Escolher Saída; 3. Digitar quantidade; 4. Confirmar; 5. Sistema valida saldo e registra a movimentação.'],
 ['Fluxo alternativo','O operador pode cancelar a operação antes de confirmar, sem alterar o saldo.'],
 ['Exceções','Quantidade inválida (zero, negativa ou fracionária) ou maior que saldo: exibir erro, não descontar unidades e não registrar evento.'],
 ['Pós-condição','Saldo atualizado, movimentação adicionada ao histórico e estado salvo no navegador.'],
], [115,388])
sub('UC04 - Pesquisar e filtrar produtos')
table([
 ['Campo','Descrição'],
 ['Ator','Operador da loja'],
 ['Objetivo','Encontrar itens e consultar rapidamente os que precisam de reposição.'],
 ['Pré-condições','Aplicação aberta; listagem disponível.'],
 ['Fluxo principal','1. Digitar nome, SKU ou categoria na busca; 2. Sistema filtra a lista enquanto o texto é digitado; 3. Opcionalmente marcar Somente estoque baixo; 4. Sistema mostra produtos com saldo menor ou igual ao mínimo cadastrado.'],
 ['Fluxo alternativo','Busca sem correspondência mostra estado vazio, sem modificar cadastros; remover filtro restaura a listagem.'],
 ['Exceções','Não há erro de negócio previsto para texto de pesquisa livre; a operação não altera dados.'],
 ['Pós-condições','Lista visível ajustada ao filtro solicitado.'],
], [117,386])
sub('6.2 Rastreabilidade básica')
para('RF01 corresponde a Cadastrar produto; RF02 a Editar produto; RF03 e RF04 a Registrar entrada/saída; RF05 e RF06 a Buscar/filtrar; RF07 a Consultar indicadores/histórico; RF08 a Exportar CSV.')
section('7','Projeto do domínio e modelagem de classes')
para('O diagrama representa <b>classes de projeto</b> e contratos de responsabilidade para o domínio. Exibe atributos privados (-), operações públicas (+), tipos, parâmetros, retornos e multiplicidades. A implementação inicial é funcional em JavaScript (objetos e funções, principalmente em stock.js e app.js), sem uma tradução literal de cada classe para a sintaxe class; essa distinção integra a documentação da evolução do sistema.')
img(docs/'classes.png',maxh=380);caption('Figura 2 - Diagrama de classes de projeto com tipos, operações e associações. Fonte: elaboração do projeto.')
sub('7.1 Entidades')
para('<b>Produto:</b> possui identificação, SKU, nome, categoria, preço, saldo, estoque mínimo e data de criação. <b>Movimentação:</b> contém identificador, referência do produto, tipo, quantidade e data. <b>Serviço de estoque:</b> concentra validação, movimentação, consulta e exportação. <b>Repositório local:</b> representa a responsabilidade de carregar e salvar o estado em localStorage.')
sub('7.2 Tipos de projeto e multiplicidades')
para('<b>String</b> representa texto; <b>Decimal</b>, preço monetário; <b>Integer</b>, quantidades inteiras; e <b>DateTime</b>, instante de registro. <b>TipoMovimentacao</b> admite Entrada e Saída. DadosProduto, EstadoEstoque, Indicadores e ResultadoMovimentacao são estruturas de dados de entrada ou retorno dos métodos, não classes com identidade própria.')
para('As associações são: um ServiçoEstoque gerencia zero ou muitos Produtos; consulta zero ou muitas Movimentações; usa um RepositorioLocal; e cada Movimentação refere-se a um Produto, que pode ter nenhuma ou muitas movimentações. As multiplicidades estão indicadas em ambas as extremidades. Não foram criadas relações de herança, agregação ou composição artificiais, porque o domínio desta versão não exige esses vínculos.')
sub('7.3 Mapeamento projeto para implementação')
table([
 ['Classe de projeto','Responsabilidade na implementação inicial'],
 ['Produto','Objetos de produtos em products[]; validação por validateProduct; alerta por saldo menor ou igual a mínimo.'],
 ['Movimentacao','Objeto gerado por moveStock e salvo no vetor history[].'],
 ['ServicoEstoque','Operações de stock.js: createProduct, updateProduct, moveStock, searchProducts, getMetrics, toCSV.'],
 ['RepositorioLocal','Funções de leitura e persistência via localStorage em app.js.'],
], [135,368])
sub('7.4 Regras de consistência')
para('A relação de movimentação com produto utiliza productId e registra também nome/SKU do produto no momento do evento. A validação de estoque ocorre antes da criação da movimentação. Não há transações de banco de dados, pois o estado está confinado ao armazenamento local do navegador.')
page()
section('8','Diagrama de sequência')
para('A sequência abaixo descreve o fluxo de registro de uma <b>saída</b>: acionamento pela interface, validação de saldo, atualização do estado e persistência local.')
img(docs/'sequencia_saida.png',maxh=315);caption('Figura 3 - Sequência simplificada do fluxo de saída. Fonte: elaboração do projeto.')
sub('8.1 Fluxo alternativo')
para('Quando o operador solicita uma quantidade maior que o saldo disponível, a função moveStock lança uma validação de erro. A interface exibe a mensagem e conserva o estoque anterior. A mesma função rejeita quantidades zero, negativas ou fracionárias.')
section('9','Arquitetura e tecnologia')
img(docs/'arquitetura.png',maxh=230);caption('Figura 4 - Organização dos componentes. Fonte: elaboração do projeto.')
para('O módulo <b>stock.js</b> define as regras e dados demonstrativos, <b>app.js</b> liga essas regras à interface, <b>index.html</b> contém a estrutura visual e <b>style.css</b> contém o estilo. O navegador executa a aplicação por um servidor estático local. Não há bibliotecas JavaScript externas obrigatórias para execução.')
page()
section('10','Modelo de dados e armazenamento')
sub('10.1 Estrutura')
table([
 ['Conjunto','Principais campos'],
 ['products[]','id, sku, name, category, price, stock, minimum, createdAt'],
 ['history[]','id, productId, productName, sku, type, quantity, date'],
], [105,398])
para('A chave de armazenamento utilizada é <b>estoquefacil-v1</b>. A aplicação carrega um conjunto demonstrativo de quatro produtos na primeira inicialização, somente quando não encontra dados existentes. Em cadastros e movimentações, salva o objeto completo com produtos e histórico no localStorage.')
sub('10.2 Limitações da persistência')
para('O localStorage não substitui banco de dados corporativo; ele pode ser apagado pelo usuário, não sincroniza máquinas e não implementa mecanismos de recuperação automática. O protótipo não solicita informações pessoais e não possui controle de acesso. Para uso comercial futuro, seria necessária análise de segurança e de proteção de dados apropriada ao contexto.')
section('11','Interface implementada')
para('A interface possui quatro indicadores principais, tabela de produtos, ações de edição/movimentação, campo de busca, filtro de alertas, histórico e botão de exportação CSV.')
img(docs/'tela_01_painel.png',maxh=300);caption('Figura 5 - Painel inicial com dados demonstrativos, capturado a partir da interface executada em navegador de teste.')
page()
section('11.1','Cadastro de produtos')
para('O usuário abre o formulário Novo produto, preenche os campos necessários e confirma. O sistema valida os dados, impede SKUs repetidos e atualiza a tabela e os indicadores.')
img(docs/'tela_02_cadastro.png',maxh=285);caption('Figura 6 - Formulário de cadastro de produto.')
section('11.2','Movimentação de estoque')
para('O botão Movimentar permite escolher entrada ou saída. O sistema valida a quantidade, recalcula o saldo e registra a ação no histórico.')
img(docs/'tela_04_movimentacao.png',maxh=265);caption('Figura 7 - Formulário de movimentação.')
section('11.3','Consulta e filtros')
para('É possível pesquisar por texto e filtrar produtos com saldo menor ou igual ao estoque mínimo, facilitando a identificação de itens para reposição.')
img(docs/'tela_06_estoque_baixo.png',maxh=300);caption('Figura 8 - Filtro de estoque baixo.')
section('12','Estratégia de testes e resultados')
para('A lógica de negócio foi exercitada por testes automatizados com o executor nativo do Node.js. Em 14/11/2026, a execução local do comando <b>node --test</b> resultou em <b>21 testes aprovados, zero falhas</b>. Também foram executadas interações de cadastro, movimentação, filtro e pesquisa em sessão de navegador isolada, sem erros JavaScript nesses percursos.')
table([
 ['Grupo','Cenários verificados','Resultado'],
 ['Cadastro','Cadastro válido, SKU duplicado, nome curto, preço vazio ou inválido e saldo fracionário.','Aprovado'],
 ['Edição','Alteração de dados cadastrais sem mexer no saldo.','Aprovado'],
 ['Movimentação','Entrada, saída, tipo inválido, bloqueio por saldo insuficiente e quantidade inválida.','Aprovado'],
 ['Consulta','Busca, filtro de reposição e indicadores.','Aprovado'],
 ['Exportação','Formato CSV com separador de ponto e vírgula.','Aprovado'],
], [100,313,90])
add(P('<b>Observação:</b> os testes automatizados não cobrem segurança, carga, navegadores diversos ou integrações externas. As validações de interface foram pontuais e não substituem uma campanha completa de testes manuais.','note'))
section('13','Versionamento com Git e organização do repositório')
para('O projeto contém código-fonte, testes, documentação, diagramas, instruções e <b>histórico local com vários commits reais de escopos distintos</b>, identificados por mensagens semânticas. Não são commits retrodatados nem apresentados como trabalho realizado em datas diferentes. Para a entrega, ainda é necessário <b>publicar o histórico completo em repositório remoto público ou compartilhado com EulerF</b> e incluir a URL neste PDF.')
table([
 ['Diretório/arquivo','Responsabilidade'],
 ['index.html','Estrutura visual do sistema'],
 ['src/app.js','Ações da interface, estado da aplicação e armazenamento'],
 ['src/stock.js','Regras de negócio e dados de demonstração'],
 ['src/style.css','Layout e responsividade'],
 ['test/stock.test.js','Testes automatizados'],
 ['docs/','Diagramas, documentação e instruções de entrega'],
 ['README.md','Instruções de uso e limitações'],
], [160,343])
sub('13.1 Convenção de commit e colaboração')
para('Os commits locais utilizam prefixes como <b>feat:</b>, <b>fix:</b>, <b>test:</b> e <b>docs:</b> para representar mudanças de implementação, correção, testes e documentação. O histórico registra mudanças genuínas, mas a orientação do professor pede evolução frequente ao longo do tempo: novos incrementos devem ser efetivamente implementados e versionados, sem criar datas ou autoria fictícias. A ramificação principal pode ser nomeada <b>main</b> antes da publicação.')
sub('13.2 Como reproduzir')
para('1. Baixar o repositório; 2. Abrir um terminal na pasta; 3. Executar <b>python -m http.server 8000</b>; 4. Acessar <b>http://localhost:8000</b> no navegador; 5. Para testes, executar <b>node --test</b> com Node.js 20 ou superior.')
sub('13.3 Evidência do funcionamento')
para('O vídeo MP4, com menos de 1 minuto, registra a interação real com a aplicação em navegador: visão geral, cadastro, entrada e saída, filtro de estoque baixo e busca. O vídeo mostra a execução da interface, não somente o código-fonte ou quadros estáticos.')
section('14','Resultados, limitações e melhorias futuras')
para('A versão entregue implementa as funções centrais planejadas para o protótipo e mantém separadas as regras de negócio da interface. O resultado serve para demonstrar análise, projeto, implementação inicial, validação e versionamento. Não contempla login, múltiplas lojas, emissão fiscal, operações concorrentes, banco de dados remoto nem integração com marketplaces.')
para('Como evolução, recomenda-se adicionar autenticação, API, banco de dados, controle de permissões, backups e integração com pedidos de venda, após novo levantamento de requisitos.')
section('15','Conclusão')
para('O EstoqueFácil evidencia a passagem do <b>que o sistema deve fazer</b> para <b>como o sistema é construído</b>, a partir de requisitos, regras, modelos, interface e testes. A escolha de um escopo reduzido permitiu implementar e demonstrar funcionalidades verificáveis. A publicação do histórico completo em um repositório acessível, a conferência da autoria e a inserção do link verdadeiro no PDF são etapas obrigatórias antes do envio final.')
add(Spacer(1,11),P('<b>Link do repositório Git:</b> [PENDENTE - substituir pelo endereço real antes do envio]. <b>Aviso:</b> esta versão do PDF ainda não pode ser considerada a entrega final sem o link.','note'))

def on_page(c,doc):
 c.saveState()
 if doc.page>1:
  w,h=A4
  c.setStrokeColor(BORD);c.setLineWidth(.6);c.line(46,h-45,w-46,h-45)
  c.setFont('DejaVu-Bold',7.7);c.setFillColor(TEAL);c.drawString(46,h-36,'ESTOQUEFÁCIL  /  DOCUMENTAÇÃO TÉCNICA')
  c.setFont('DejaVu',8);c.setFillColor(GREY)
  c.drawString(46,32,'Análise e Projeto de Sistemas  •  Versão 1.0')
  c.drawRightString(w-46,32,str(doc.page-1))
 c.restoreState()

doc=SimpleDocTemplate(str(outfile),pagesize=A4,rightMargin=46,leftMargin=46,topMargin=57,bottomMargin=52,title='EstoqueFácil - Documentação de Análise e Projeto',author='José Carlos de Moraes Sousa',subject='Trabalho acadêmico - Análise e Projeto de Sistemas')
doc.build(story,onFirstPage=on_page,onLaterPages=on_page)
print(outfile, outfile.stat().st_size)
