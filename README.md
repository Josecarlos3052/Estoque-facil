# EstoqueFácil

Protótipo funcional de controle de estoque para uma pequena loja de panelas, desenvolvido como trabalho acadêmico de **Análise e Projeto de Sistemas**.

## Funcionalidades implementadas
- Cadastrar produtos com nome, SKU, categoria, preço, saldo inicial e mínimo;
- Editar cadastro sem alterar o saldo por esse caminho;
- Registrar **entradas** e **saídas** com validação de saldo;
- Filtrar produtos por nome, SKU ou categoria;
- Mostrar apenas produtos com estoque baixo;
- Exibir indicadores de produtos, unidades, valor e alertas;
- Consultar cinco movimentações mais recentes;
- Exportar cadastro de produtos em CSV.

## Executar localmente

Requisitos: navegador moderno e **Python 3** ou outro servidor HTTP estático.

```bash
python -m http.server 8000
```

Abra `http://localhost:8000` no navegador. **Não abra o arquivo `index.html` diretamente**: por utilizar módulos JavaScript, é recomendado usar servidor local.

## Testar regras de negócio

Requisito: Node.js 20+.

```bash
node --test
```

## Tecnologias
HTML, CSS, JavaScript ES Modules, `localStorage` e teste nativo do Node.js. Não há API, login ou servidor de banco de dados. Os dados ficam armazenados no navegador do usuário e não são sincronizados entre dispositivos.

## Arquitetura
- `index.html`: estrutura da interface;
- `src/style.css`: estilos e responsividade;
- `src/app.js`: interface, eventos, persistência e renderização;
- `src/stock.js`: regras de negócio puras e dados demonstrativos;
- `test/stock.test.js`: testes automatizados;
- `docs/`: documentação acadêmica e diagramas.

## Regras importantes
SKU único, preço e estoque não negativos, quantidades inteiras, saída limitada pelo saldo disponível, estoque baixo quando `saldo <= mínimo`.

## Limitações deste protótipo
Os dados são **demonstrativos** e ficam no `localStorage`; a limpeza do navegador pode eliminá-los. Não há autenticação, multiusuário, sincronização, backup automático nem integração com plataformas de venda. O valor do estoque é estimado pelo preço cadastrado (não pelo custo).

## Git e autoria
O projeto pode ser versionado em um repositório do GitHub. Consulte `docs/PUBLICAR_NO_GITHUB.md` para publicar e incluir o endereço na documentação.
