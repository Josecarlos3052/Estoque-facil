# Como publicar o EstoqueFácil preservando o histórico Git

Este pacote **já contém a pasta `.git/` e vários commits semânticos**. Não envie somente os arquivos pelo botão **Upload files** do GitHub, pois isso não preserva o histórico já criado.

## 1. Criar repositório vazio

1. Abra <https://github.com/new> e entre na sua conta.
2. Nome sugerido: `estoque-facil`.
3. Marque **Public**. Se escolher privado, conceda acesso ao usuário GitHub **EulerF**.
4. **Não** selecione a criação de README, `.gitignore` ou licença automática.
5. Clique em **Create repository**. Copie a URL apresentada.

## 2. Publicar *todos* os commits existentes

Extraia o ZIP do projeto preservando a pasta `.git`. No terminal, entre na pasta `EstoqueFacil`:

```bash
# Confirme que há vários commits semânticos:
git log --oneline
# Padronize o nome da ramificação principal:
git branch -M main
# Troque SEU-USUARIO pela conta real:
git remote add origin https://github.com/SEU-USUARIO/estoque-facil.git
# Publique o histórico completo:
git push -u origin main
```

Se aparecer `remote origin already exists`, utilize:

```bash
git remote set-url origin https://github.com/SEU-USUARIO/estoque-facil.git
git push -u origin main
```

Se o GitHub pedir autenticação, siga o fluxo de login do Git Credential Manager no Windows. **Não envie sua senha ou token em conversas.**

## 3. Verificar antes de enviar

1. Abra o repositório na web e clique na aba **Commits**. Confirme que aparecem várias mensagens `feat:`, `fix:`, `test:` e `docs:`.
2. Copie o endereço real do repositório, de preferência no formato `https://github.com/SEU-USUARIO/estoque-facil`.
3. Inclua esse link no **PDF da documentação**, substituindo o campo `[PENDENTE]` e confira que o endereço abre sem erros para o professor.
4. Confirme que o MP4 mostra o sistema executado em vez de apenas código ou slides; a duração deve ser inferior a 1 minuto.
5. Revise a documentação e o código para conseguir explicar o desenvolvimento na apresentação.

**Atenção:** o enunciado também solicita commits frequentes ao longo do desenvolvimento. O histórico deste pacote contém commits incrementais reais, mas concentrados no mesmo período. Não invente datas/autores: desenvolva e publique correções ou melhorias reais ao longo dos próximos dias, se possível. A aceitação final depende da avaliação do professor.
