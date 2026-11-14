# Como publicar o EstoqueFácil no GitHub

1. Entre em https://github.com e clique em **New repository**.
2. Crie um repositório chamado `estoque-facil`, escolha **Public** (ou conceda acesso ao professor `EulerF`) e deixe desmarcadas as opções automáticas de README / .gitignore / license, porque os arquivos já existem.
3. Abra um terminal na pasta `EstoqueFacil` e execute:

```bash
git init
git add .
git commit -m "feat: implementar controle inicial de estoque"
git branch -M main
git remote add origin https://github.com/SEU-USUARIO/estoque-facil.git
git push -u origin main
```

> Substitua **SEU-USUARIO** pelo seu usuário do GitHub. Se esta pasta já veio com um repositório Git inicializado e commitado, pule `git init`, `git add` e `git commit`.

4. Abra `https://github.com/SEU-USUARIO/estoque-facil`, confirme que os arquivos estão visíveis e copie a URL.
5. Insira **a URL verdadeira** no campo `Link do repositório` da documentação PDF antes da entrega.
6. Caso o repositório seja privado, conceda explicitamente acesso ao usuário GitHub **EulerF** e confirme que o convite foi aceito.

**Antes de enviar:** rode `node --test`; confirme que a página abre em `http://localhost:8000`; verifique que o vídeo MP4 tem até 1 minuto e que o PDF contém o link real.
