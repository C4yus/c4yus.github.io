---
name: prompts-redes-cayus
description: "Escrever pedidos (prompts) prontos a colar à mão no Gemini do João para miniaturas de YouTube, carrosséis e posts do Instagram, frases sobre imagem e gráficos da marca Cayus, com aprovação antes de gerar. Usar quando o João disser 'miniatura', 'thumbnail', 'carrossel', 'post para o Instagram', 'gráfico', 'frase com imagem' ou 'prompt para o Gemini'."
---

# Prompts para redes (Gemini à mão)

Responder ao João em PT-PT, curto; prompts em inglês.
Esta skill só ESCREVE os pedidos. Quem gera é o João no Gemini da conta dele (ou a skill `gemini-pedidos-precisos`, no Chrome dele). Sem APIs, sem chaves, sem ligar serviços, sem publicar.

## Antes de escrever
1. Ler `MARCA.md` (ou a skill `kit-de-marca-cayus`): colar a folha de estilo tal e qual no prompt, com os hex.
2. Saber para onde vai: canal (Relaxing with Cayus, Waddle Hop Pals), Instagram @c4yus3d (modelos 3D) ou livros Cayus Books.
3. Nunca pôr no prompt dados pessoais, caras de pessoas reais sem foto dada pelo João, marcas de outros ou arte de outros livros.

## Estrutura de cada prompt (por esta ordem)
1. `Generate an image:` + assunto e função ("YouTube thumbnail for a 1-hour campfire video").
2. Estilo e ambiente.
3. Elementos obrigatórios, contáveis e com posição ("one campfire centred low, pine trees left and right").
4. Paleta com hex e materiais.
5. Texto na imagem: as palavras exatas entre aspas, tipo de letra (bold sans-serif), posição, cor. Máximo 3–5 palavras. Se o texto sair torto, gerar sem texto e pôr o texto depois por código (Pillow/HTML).
6. Proibido: "no extra text, no watermark, no logos, no frame, no signature".
7. Formato: proporção e tamanho.

Correções: "Keep everything the same. Changes: (1)… (2)…", no máximo 3 mudanças por volta e 3 voltas; depois mostrar ao João.

## Formatos
| Peça | Proporção / tamanho | Regras |
|---|---|---|
| Miniatura YouTube | 16:9, 1280x720 | um foco, duas cores dominantes, legível a 320px, nada no canto inferior direito, texto ≠ título |
| Short / Reel / Story | 9:16, 1080x1920 | texto longe das margens de cima e de baixo (interface) |
| Post Instagram | 4:5, 1080x1350 | uma ideia por imagem |
| Carrossel | 4:5, 1080x1350, 5–8 slides | slide 1 = gancho; 1 ideia por slide; último = chamada à ação; mesmo fundo/estilo em todos |
| Frase sobre imagem | 4:5 ou 1:1 | frase original (nunca citar sem autor certo), curta, tipo grande |
| Pin Pinterest (livros) | 2:3, 1000x1500 | capa + 2–3 páginas de amostra + título |

## Fluxo
1. **Brief** (aprovação primeiro): objetivo, texto exato, cena, paleta, formato. Para carrosséis, o texto de cada slide. Esperar o "sim" do João.
2. **Prompts:** um por imagem (um por slide), em blocos de código prontos a colar, com o nome de ficheiro sugerido (ex.: `mini_campfire_v1.png`).
3. **Verificar o que voltar:** ver em tamanho real e em tamanho de feed (≈360px; miniaturas ≈320px): texto exato e sem erros, nada cortado, legível, cores da marca, sem marcas de água. Corrigir e voltar a ver.
4. Uma imagem gerada não é ficheiro editável: se for para reutilizar, refazer o texto por código.

## Exemplos de arranque
- Relaxing with Cayus: "warm firelight, deep blue night, calm, cinematic, photographic, no people".
- Waddle Hop Pals: "cute rounded cartoon animal characters, bright friendly colours, simple clean shapes, child-safe".
- Livros Cayus: mostrar a capa real e páginas reais (nunca inventar páginas que o livro não tem).

Baseada nas skills youtube-thumbnail, gemini-carousel, quote-post e graphic-designer de Charlie Hills (MIT), reescrita para o Gemini usado à mão e para a marca Cayus, sem ligações a serviços.
