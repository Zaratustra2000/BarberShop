# 03: Adicionando a foto principal da Barbearia

**What to build:** O Dono adiciona ou substitui uma foto principal opcional, que aparece no perfil da Barbearia.

**Blocked by:** 02: Editando o perfil da Barbearia e suas Cadeiras.

**Status:** done

- [x] O Dono responsável pode enviar uma foto JPG, PNG ou WebP de até 5 MB.
- [x] O arquivo é validado, recebe um nome gerado pela aplicação e fica em armazenamento local configurável.
- [x] Uma imagem inválida ou acima do limite é recusada com mensagem clara e sem alterar a foto existente.
- [x] Substituir a foto atualiza o perfil e não deixa a aplicação exposta a nomes de arquivo controlados pelo usuário.
- [x] O perfil autenticado da Barbearia mostra a foto atual quando houver uma.
- [x] Testes usam imagens sintéticas e não dependem de serviço externo de armazenamento.
