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

## Publicação GitHub / entrega

A pasta já inclui **histórico Git com commits reais** e não deve ser iniciada do zero. Leia [`docs/PUBLICAR_NO_GITHUB.md`](docs/PUBLICAR_NO_GITHUB.md) e [`docs/CHECKLIST_ENUNCIADO.md`](docs/CHECKLIST_ENUNCIADO.md). O trabalho acadêmico requer repositório público ou acesso concedido ao usuário `EulerF` e o link verdadeiro precisa constar no PDF antes da entrega.

Revise os materiais e certifique-se de conseguir explicar as regras e os diagramas na demonstração. O histórico de commits deve refletir o trabalho real, sem autoria ou datas fictícias.
