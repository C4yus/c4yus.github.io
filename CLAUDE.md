# Site Cayus (C4yus/c4yus.github.io, GitHub Pages)

Site estático, sem build de JS. Publicado em https://c4yus.github.io/ (repositório renomeado de cayus-livros a 20 nov 2026)
Secções: Livros, Vídeos, Modelos 3D. O João responde em português de Portugal; o texto do site é em inglês.

## Antes de mexer
1. Ler `MARCA.md` (cores, tipos, regras). O site tem de ficar com um toque de steampunk (pedido do João, 20 nov 2026), sem perder o contraste 4,5:1 nem as regras da marca.
2. As páginas `livros/<slug>/index.html` são GERADAS por `python3 tools/build_books.py`. Nunca editar à mão: alterar a lista `BOOKS` no script e correr o build.
3. As restantes páginas (`index.html`, `livros/index.html`, `videos/`, `modelos/`) são editadas à mão.

## Ferramentas
| Ficheiro | Para que serve | Como se corre |
|---|---|---|
| `tools/build_books.py` | gera as 4 páginas de livro a partir de `BOOKS` | `python3 tools/build_books.py` (raiz do repo) |
| `tools/verificar_site.py` | verifica estrutura, SEO, acessibilidade, links, Amazon, sitemap, contraste, CSS, livros == build | `python3 -I tools/verificar_site.py` (sai com 1 se houver ERRO) |

## Novo livro
1. Acrescentar o dict em `BOOKS` (slug, ASIN, textos, capa).
2. Capa em `img/<slug>.jpg` e 4 amostras `img/samples/<slug>-1..4.jpg`.
3. Correr o build; acrescentar o livro em `livros/index.html` e a URL em `sitemap.xml`.
4. Correr o verificador.

## Quando está pronto (passar item a item, dizer no relatório o que foi verificado)
- [ ] `python3 -I tools/verificar_site.py` termina com 0 erros (ler a saída, não só o código de saída)
- [ ] Se mexi no CSS ou em cores: contraste dos pares novos calculado (>= 4,5:1) e cores dentro da paleta
- [ ] Vi a página em telemóvel, tablet e PC (skill `revisao-visual-site`) e li a consola sem erros
- [ ] Auditoria SEO/acessibilidade/conversão feita (skill `auditoria-site`) quando a mudança é grande
- [ ] Links "Buy on Amazon" abrem o ASIN certo
- [ ] Só depois de o João dizer sim: publicar (skill `publicar-site`) e abrir o URL público para provar que está no ar

## Regras
- Publicar só com o sim do João. Mostrar primeiro o que muda.
- Sem gradientes decorativos (exceto o wordmark listrado), sem cartões todos iguais, movimento reduzido respeitado, foco visível.
- Arte e nome StarNet não se reutilizam. Imagens pesadas e chaves nunca vão para o repositório.
- Não editar o repositório privado `cayus-projetos` a partir daqui.
- Skills e plugins: nenhum pode enviar dados para fora (regra do João, 22 nov 2026). Se for bom mas enviar, escrever uma versão nossa só local; na dúvida, escrever sempre a nossa. Ver skill `regras-skills-cayus` e `.claude/LISTA-SKILLS.md`.
