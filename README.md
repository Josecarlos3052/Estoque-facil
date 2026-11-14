# EstoqueFácil — Controle de Estoque

**Disciplina:** Análise e Projeto de Sistemas  
**Responsável pelo trabalho:** José Carlos de Moraes Sousa  
**Modalidade:** individual  
**Versão documentada:** 1.1  
**Data:** novembro de 2026

Protótipo web de controle de estoque para uma pequena loja de panelas e utensílios. O projeto demonstra levantamento de requisitos, modelagem UML, implementação inicial, testes automatizados e versionamento com Git.

## Funcionalidades implementadas

- Cadastro de produtos com nome, SKU, categoria, preço, estoque inicial e estoque mínimo;
- Edição e exclusão de produtos, com confirmação antes de excluir;
- Registro de entradas e saídas, com validação de quantidade e saldo disponível;
- Pesquisa de produtos por nome, SKU ou categoria;
- Filtro de produtos com estoque baixo (saldo menor ou igual ao mínimo);
- Painel com quantidade de produtos, unidades disponíveis, alertas e valor estimado em estoque;
- Histórico de movimentações com pesquisa por produto/SKU e filtro por tipo;
- Exportação da listagem de produtos em CSV.

## Executar localmente

Requisitos: Python 3 e navegador moderno.

```bash
python -m http.server 8000
```

Abra http://localhost:8000 no navegador. A aplicação utiliza módulos JavaScript e deve ser executada por HTTP local; não abra o arquivo HTML diretamente pelo explorador.

## Executar os testes de regras de negócio

Requisito: Node.js 20 ou superior.

```bash
npm test
```

O comando executa os testes nativos do Node.js em `test/stock.test.js`.

## Verificação da interface e geração das evidências

O repositório inclui scripts de verificação automatizada da interface e de geração dos artefatos acadêmicos. O fluxo do GitHub Actions executa os testes, verifica a interface em Chromium, atualiza os diagramas, grava o vídeo demonstrativo e gera o PDF.

Para executar localmente, instale Python com `reportlab`, `pillow` e `playwright`, instale o Chromium do Playwright e tenha Graphviz e FFmpeg disponíveis. Depois execute:

```bash
python docs/verify_ui.py
python docs/render_use_cases.py
dot -Tpng docs/classes.dot -o docs/classes.png
dot -Tsvg docs/classes.dot -o docs/classes.svg
dot -Tpng docs/arquitetura.dot -o docs/arquitetura.png
python docs/record_real_demo.py
python docs/build_pdf.py
```

## Organização do projeto

| Arquivo | Responsabilidade |
| --- | --- |
| `index.html` | Estrutura das telas da aplicação |
| `src/style.css` | Layout e responsividade |
| `src/app.js` | Eventos, navegação, estado, persistência e apresentação |
| `src/stock.js` | Regras de negócio puras |
| `test/stock.test.js` | Testes automatizados das regras |
| `docs/casos_de_uso.dot` | Fonte editável do diagrama de casos de uso |
| `docs/render_use_cases.py` | Desenha a fronteira do sistema na imagem do diagrama |
| `docs/classes.dot` | Fonte editável do diagrama de classes |
| `docs/arquitetura.dot` | Fonte editável do diagrama de arquitetura |
| `docs/Documentacao_EstoqueFacil.pdf` | Documentação acadêmica |
| `docs/Demo_EstoqueFacil_Interativo.mp4` | Vídeo demonstrativo da aplicação |

## Tecnologias e arquitetura

HTML, CSS e JavaScript com módulos ES, armazenamento local por `localStorage`, Node.js para testes, Playwright/Chromium para verificação da interface e ReportLab para gerar o PDF.

O diagrama de classes representa o projeto lógico. A implementação inicial em JavaScript utiliza funções e objetos, com regras de negócio separadas da interface.

## Regras centrais

SKU único; preço e estoques não negativos; campos numéricos obrigatórios; quantidades inteiras; saída limitada ao saldo disponível; alerta quando `saldo <= mínimo`; exclusão de produto mediante confirmação; preservação do histórico de movimentações já registradas.

## Limitações desta versão

Os dados ficam no `localStorage` do navegador e podem ser apagados pelo usuário. Não há backend, banco de dados remoto, autenticação, multiusuário, sincronização entre dispositivos, backup automático ou integração com marketplaces. O valor em estoque é uma estimativa calculada pelo preço cadastrado, não pelo custo de aquisição.

## Repositório e entrega

**Repositório público:** https://github.com/Josecarlos3052/Estoque-facil  
**Documentação:** [docs/Documentacao_EstoqueFacil.pdf](docs/Documentacao_EstoqueFacil.pdf)  
**Vídeo:** [docs/Demo_EstoqueFacil_Interativo.mp4](docs/Demo_EstoqueFacil_Interativo.mp4)  
**Histórico Git:** https://github.com/Josecarlos3052/Estoque-facil/commits/main

A documentação e o vídeo devem ser conferidos e enviados na plataforma acadêmica pelo estudante. A existência dos arquivos no GitHub não substitui o envio na atividade.
