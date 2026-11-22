---
name: design-cayus
description: "Desenhar, redesenhar, criticar ou polir páginas do site Cayus (HTML/CSS estático) com nível de diretor de arte, sem ferramentas externas. Usar ao criar uma página nova, mudar o aspeto do site, pedir 'mais bonito', 'mais ousado', 'mais calmo', rever tipografia, espaçamento, cores, animação ou o site no telemóvel."
---

# Design Cayus

Responder ao João em PT-PT, curto. O texto do site é em inglês.
Tudo local: ler ficheiros, editar CSS/HTML, ver o resultado com Playwright em `localhost`. Nada de serviços externos, telemetria ou programas descarregados.

## Antes de mexer
1. Ler `MARCA.md` e `CLAUDE.md` do repo (cores, tipos, regras, toque steampunk).
2. **A marca ganha.** O que o João decidiu (paleta, Bricolage Grotesque + Literata, sombra dura 6px forest nas capas, wordmark listrado, steampunk) manda sobre qualquer regra geral abaixo.
3. **Refinar preserva; redesenhar substitui.** Num refinamento mantém-se identidade, textos e tudo o que está fora do pedido. Perguntar antes de mudar textos factuais ou acrescentar promessas.

## Modo da página (decide a ambição)
- **Persuadir** (página inicial, lista de livros, página de livro): o visitante decide e clica em "Buy on Amazon". Compromisso total: imagem real, uma ideia forte, botão óbvio.
- **Ler** (textos, ajuda): estrutura para compreender; medida de linha confortável.
- **Mostrar** (amostras, galeria): a arte manda, a interface recua.

## Comandos (o João pode pedir por nome ou por ideia)
| Pedido | O que fazer |
|---|---|
| criticar | Rever como visitante: hierarquia, clareza do botão, confiança, ritmo. Nota 1–5 em cada e os 3 problemas que mais custam vendas. |
| polir | Passagem final: estados (hover, foco, desativado), espaçamentos, alinhamentos ópticos, superfícies do browser, textos dos botões. |
| mais ousado | Aumentar contraste de escala, uma cor de destaque com intenção, imagem maior, menos elementos a competir. |
| mais calmo | Tirar efeitos, reduzir pesos, mais espaço, uma só animação. |
| tipografia | Escala com passos óbvios, medida 65–75 caracteres, títulos equilibrados (`text-wrap: balance`), tracking ≥ -0.04em. |
| espaçamento | Grupos apertados, separação generosa, mais espaço acima de um título do que abaixo. |
| adaptar | Telemóvel (390px), tablet (820px) e PC (1280px): nada sai do ecrã, toques ≥ 44px, menu cabe. |
| animar | UM momento memorável (o wordmark a imprimir); o resto quieto. Ease-out, a partir de um estado já visível; respeitar `prefers-reduced-motion`. |
| cor | Cor com função (sala, ação, destaque), nunca decorativa. Sempre dentro da paleta. |

## Chão de qualidade (verificar no resultado, não na intenção)
- **Contraste:** texto ≥ 4,5:1, texto grande ≥ 3:1. Calcular (fórmula WCAG), não adivinhar.
- **Profundidade:** sombras com intenção. No Cayus a sombra dura forest é marca (capas, amostras); não a espalhar por tudo.
- **Tipo:** medida 65–75ch no corpo, display até ~6rem, hierarquia por peso e tamanho.
- **Estados:** hover, foco visível (contorno ember), desativado, carregamento, erro, vazio.
- **Superfícies do browser:** seleção de texto, caret, foco, sublinhado (`text-underline-offset`), barras de scroll — tematizar com a paleta. É o sinal mais barato de página "construída".
- **Textos:** a língua do produto. Botões dizem a ação ("Buy on Amazon", "Look inside").
- **Cobertura:** tudo o que o pedido pede, encontrável em segundos.

## Recusar (vícios de página feita por IA)
- Cartões todos iguais de ícone + título + texto como estrutura da página; cartões dentro de cartões.
- Etiqueta pequena em maiúsculas por cima de um título (proibido).
- Números de secção 01/02/03 sem função.
- Texto em gradiente; vidro/blur decorativo; gradientes decorativos (só o wordmark listrado é exceção).
- Barra colorida num só lado de uma caixa arredondada.
- Emoji ou símbolos Unicode em vez de ícones desenhados (usar SVG próprio, um só traço).
- Fonte do sistema como voz de título.
- Animações iguais em todas as secções.

## Steampunk Cayus (pedido do João, 20 nov 2026)
Engrenagens em SVG (máscara com `currentColor`/ember), rebites em fila, placas de "latão" com rebites nos cantos, fio de cobre nos botões. Formas e cores da paleta, sem gradientes, com contraste intacto e engrenagens paradas em movimento reduzido.

## Ver o resultado (obrigatório)
1. Servir o repo: `python3 -m http.server 8765` na raiz.
2. Capturas com Playwright em 390x844, 820x1180 e 1280x900 (página inteira), ler a consola e verificar se há scroll horizontal (`scrollWidth > innerWidth`).
3. Olhar para as capturas, corrigir o que uma volta mostra, só depois voltar a olhar.
4. Correr `python3 -I tools/verificar_site.py` (0 erros) e seguir a skill `revisao-visual-site`.
5. Mostrar ao João antes de publicar.

Baseada nas ideias da skill Impeccable de Paul Bakaus (Apache-2.0), reescrita sem o programa, o catálogo online nem a telemetria da original.
