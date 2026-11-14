# EstoqueFácil — Controle de Estoque

**Disciplina:** Análise e Projeto de Sistemas  
**Responsável pelo trabalho:** José Carlos de Moraes Sousa  
**Modalidade:** individual  
**Data:** novembro de 2026

Protótipo funcional de controle de estoque para uma pequena loja de panelas e utensílios, desenvolvido para aplicar requisitos, casos de uso, classes de projeto, implementação inicial, testes e versionamento Git.

## Funcionalidades implementadas

- **Cadastrar e editar** produtos, com nome, SKU, categoria, preço, estoque inicial e mínimo;
- **Registrar entradas e saídas** de mercadorias, com validação do saldo disponível;
- **Buscar** itens por nome, SKU ou categoria;
- **Filtrar estoque baixo**, quando o saldo está no mínimo ou abaixo;
- **Consultar painel** com produtos, unidades, valor estimado e alertas;
- **Visualizar histórico** das últimas cinco movimentações;
- **Exportar** a listagem em CSV.

## Executar localmente

Requisitos: navegador moderno e **Python 3** (ou servidor HTTP estático equivalente).

```bash
python -m http.server 8000
```

Abra <http://localhost:8000> no navegador. Não execute `index.html` diretamente pelo explorador de arquivos: o aplicativo usa módulos JavaScript e deve ser servido por HTTP local.

## Executar os testes

Requisito: Node.js 20+.

```bash
node --test
```

A revisão de 14/11/2026 contabilizou **21 testes automatizados aprovados** sobre cadastro, edição, movimentação, bloqueios de entradas inválidas, busca, indicadores e exportação.

## Organização do projeto

| Arquivo | Responsabilidade |
| --- | --- |
| `index.html` | Elementos visuais da aplicação |
| `src/style.css` | Estilos e adaptação à tela |
| `src/app.js` | Eventos, manipulação da interface e armazenamento local |
| `src/stock.js` | Regras de negócio puras |
| `test/stock.test.js` | Testes automáticos de regras de negócio |
| `docs/classes.png` | Diagrama de classes de projeto |
| `docs/casos_de_uso.png` | Diagrama de casos de uso |
| `docs/Documentacao_EstoqueFacil.pdf` | Documentação acadêmica |
| `docs/Demo_EstoqueFacil_Interativo.mp4` | Demonstração em navegador (menos de 1 minuto) |

**Tecnologias:** HTML, CSS, JavaScript com módulos ES, `localStorage` e executor nativo de testes do Node.js. O diagrama de classes documenta o projeto lógico, enquanto a versão inicial usa funções e objetos JavaScript; os conceitos correspondem às responsabilidades dos módulos.

## Regras centrais

SKU único, preço e estoques não negativos, campos numéricos obrigatórios, quantidades inteiras, saída limitada ao saldo disponível e alerta quando `saldo <= mínimo`.

## Limitações desta versão

Os dados são **de demonstração** e ficam no `localStorage`; limpar os dados do navegador pode apagá-los. Não há banco de dados remoto, autenticação, multiusuário, backup automático nem integração com plataformas de vendas. O valor de estoque é estimado pelo preço cadastrado, não pelo custo das mercadorias.

## Repositório e entrega acadêmica

**Repositório público:** [github.com/Josecarlos3052/Estoque-facil](https://github.com/Josecarlos3052/Estoque-facil)  
**Documentação acadêmica:** [`docs/Documentacao_EstoqueFacil.pdf`](docs/Documentacao_EstoqueFacil.pdf)  
**Vídeo de demonstração:** [`docs/Demo_EstoqueFacil_Interativo.mp4`](docs/Demo_EstoqueFacil_Interativo.mp4)

O trabalho exige PDF com o endereço do repositório, vídeo MP4 de até um minuto e código público ou acesso ao professor. O documento final inclui o URL acima.

O histórico inicial contém oito commits incrementais realizados em 14/11/2026. Seus autores estão registrados como `Autor do projeto` (identidade genérica de preparação do pacote). O histórico não deve ser retrodatado ou reescrito para aparentar uma cronologia diferente. Para registrar suas contribuições futuras, configure nome e e-mail próprios no GitHub Desktop e realize alterações efetivas, com commits semânticos nas datas em que ocorrerem.

Consulte [`docs/CHECKLIST_ENUNCIADO.md`](docs/CHECKLIST_ENUNCIADO.md) para os requisitos e [`docs/PUBLICAR_NO_GITHUB.md`](docs/PUBLICAR_NO_GITHUB.md) para atualizar os arquivos por meio do GitHub Desktop. A revisão, a autoria e a coerência entre código, documentação e demonstração são essenciais para a avaliação.
