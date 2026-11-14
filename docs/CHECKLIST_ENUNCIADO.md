# Conferência da entrega — Análise e Projeto de Sistemas

**Projeto:** EstoqueFácil  
**Disciplina:** Análise e Projeto de Sistemas  
**Modalidade:** individual  
**Repositório:** https://github.com/Josecarlos3052/Estoque-facil  
**Versão do sistema:** 1.1  
**Data desta conferência:** 14/11/2026

A tabela abaixo consolida os requisitos que foi possível ler no enunciado do Notion e confronta-os com os arquivos e a implementação do repositório. A conferência não substitui a avaliação do professor.

| Requisito | Situação | Evidência / observação |
| --- | --- | --- |
| Tema livre e escopo realista | Atendido | Controle de estoque de uma loja de panelas |
| Identificação, disciplina, modalidade e data | Atendido | Capa e seção 1 do PDF |
| Contexto, problema, objetivo, escopo e exclusões | Atendido | Seção 1 do PDF |
| Requisitos funcionais | Atendido | RF01 a RF10, incluindo exclusão e consulta do histórico |
| Requisitos não funcionais | Atendido | RNF01 a RNF05 |
| Regras de negócio | Atendido | RN01 a RN07 |
| Diagrama de casos de uso | Atendido | Ator, fronteira, associações e casos de uso da versão atual |
| Include/extend/generalização quando fizer sentido | Não aplicável | O escopo não exige esses vínculos; não foram forçados |
| No mínimo três casos de uso textuais | Atendido | UC01 a UC06, com ator, pré-condições, fluxo principal, alternativos, exceções e pós-condições |
| Diagrama de classes de projeto | Atendido | Atributos, visibilidade, tipos, métodos, parâmetros, retornos e multiplicidades |
| Classificação e multiplicidade dos relacionamentos | Atendido | Associações explicitadas; sem herança/agregação/composição artificiais |
| Diagrama de sequência | Atendido | Fluxo de registro de saída e alternativa de saldo insuficiente |
| Arquitetura e armazenamento | Atendido | HTML/CSS, app.js, stock.js e localStorage |
| Implementação real | Atendido no escopo do protótipo | Cadastro, edição, exclusão, movimentação, filtros, histórico e CSV |
| Testes automatizados de regras | Atendido | 21 cenários em test/stock.test.js; execução pelo npm test |
| Verificação da interface | Configurada | Playwright/Chromium verifica os fluxos principais e gera capturas |
| Vídeo MP4 até 1 minuto | A conferir após a execução do fluxo | docs/Demo_EstoqueFacil_Interativo.mp4; o workflow valida a duração |
| Repositório Git público | Atendido | Repositório público na ramificação main |
| README com descrição e execução | Atendido | README.md |
| Commits semânticos | Parcialmente atendido | Há mensagens semânticas, mas o histórico anterior contém identidades genéricas |
| Commits frequentes ao longo do tempo | Pendente / limitação histórica | Os commits consultados estão concentrados em 14/11/2026; não é correto apresentá-los como evolução distribuída por vários dias |
| Autoria Git vinculada ao estudante | Parcial / conferir | Parte dos commits antigos usa “Autor do projeto”; commits posteriores aparecem associados a Josecarlos3052. Não reescrever autorias ou datas antigas |
| PDF e vídeo enviados na plataforma acadêmica | Pendente do estudante | O estudante deve anexar os dois arquivos na atividade |
| Prazo | Conforme enunciado consultado | 18/11/2026 às 21h00 |

## Verificações que não podem ser resolvidas automaticamente

1. O histórico antigo não pode ser transformado em uma sequência de commits de vários dias sem falsificar a cronologia. O estudante deve continuar o desenvolvimento real e registrar novas etapas quando ocorrerem.
2. Confirme que os commits feitos pelo estudante usam nome e e-mail verificados na conta GitHub.
3. A extração acessível da página do Notion não exibiu integralmente a distribuição de pontos da seção 8. Confira essa tabela diretamente na plataforma da disciplina.
4. O envio do PDF e do MP4 na plataforma acadêmica é uma ação que precisa ser realizada pelo estudante.

## Comandos de conferência

```bash
npm test
python docs/verify_ui.py
python docs/record_real_demo.py
python docs/build_pdf.py
```

O GitHub Actions também executa as verificações e atualiza as evidências geradas, quando o fluxo termina com sucesso.
