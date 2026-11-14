# Publicação e atualização do EstoqueFácil

**Repositório público:** https://github.com/Josecarlos3052/Estoque-facil  
**Ramificação:** main

O repositório já está publicado. Não crie outro repositório, não reinicialize a pasta .git e não altere datas/autores de commits antigos.

## Atualizar pelo GitHub Desktop

1. No GitHub Desktop, selecione `Estoque-facil`.
2. Use **Repository > Show in Explorer** para abrir a pasta local.
3. Faça ou copie apenas alterações que você realmente desenvolveu.
4. Na guia **Changes**, revise cada arquivo.
5. Em **File > Options > Git**, confirme nome e e-mail verificados da sua conta.
6. Registre um commit com mensagem semântica, por exemplo `docs: atualiza requisitos e documentação da versão 1.1`.
7. Clique em **Push origin**.
8. Confira o resultado no GitHub e, se houver workflow em execução, aguarde a validação terminar.

## Geração de documentação e evidências

O fluxo `.github/workflows/validar-evidencias.yml` executa os testes, verifica a interface com Chromium/Playwright, atualiza diagramas e capturas, grava o vídeo MP4 e gera o PDF. Os arquivos gerados são publicados no repositório quando o workflow termina com sucesso na ramificação main.

Se executar localmente, consulte as instruções do README e instale as dependências indicadas.

## Cuidados com o histórico

A conferência de 14/11/2026 encontrou commits anteriores com a identidade genérica `Autor do projeto` e commits posteriores associados a `Josecarlos3052`. Preserve esse histórico; não altere datas ou autores para simular evolução anterior. A maneira correta de fortalecer o histórico é realizar novas melhorias verdadeiras, em etapas pequenas, e registrá-las com sua própria identidade verificada.

## Antes de entregar

- Abra o PDF atualizado e confira capa, diagramas, capturas e link do repositório.
- Reproduza o MP4 e confirme que a duração é inferior a 60 segundos.
- Abra o repositório em uma janela anônima para confirmar que está público.
- Leia o código e esteja preparado para explicar as regras, os diagramas e as limitações.
- Anexe o PDF e o MP4 na atividade da plataforma acadêmica antes do prazo indicado pelo professor.
