---
name: kdp-montar-livro
description: "Montar os ficheiros finais de um livro de colorir Cayus para a Amazon KDP a partir dos desenhos feitos à mão no Gemini: limpar as linhas para preto e branco puro a 300 ppi, montar o PDF do interior (desenhos só de um lado) e a capa completa (verso, lombada, frente) com as medidas oficiais. Usar quando o João disser 'montar o livro', 'PDF do interior', 'fazer a capa KDP', 'lombada', 'preparar para a KDP' ou depois de ter os desenhos aprovados."
---

# Montar livro KDP (só local)

Responder ao João em PT-PT, curto. Faz parte do fluxo da skill `livros-colorir-cayus` (passo 4, "Montar"): ler essa skill primeiro, porque tem as regras do livro, a checklist e o `verificar_capa_kdp.py`.
Tudo local (Python + Pillow + NumPy). Os desenhos vêm do Gemini usado à mão pelo João: esta skill nunca gera imagens nem chama APIs.

## Regra de ouro: só arte original
Nunca usar páginas, capturas ou digitalizações de outros livros como entrada ou "exemplo de estilo". O estilo descreve-se por palavras ("thick uniform outlines, large open areas").

## Formato Cayus (decidido)
8,5x11", interior preto e branco, papel branco, desenhos só de um lado, sem sangria (o desenho fica dentro da margem), capa mate a cores. 50 desenhos (60 no Botanical Garden).

## Passos
Scripts em `scripts/` desta skill. Instalar uma vez: `pip install pillow numpy`.

1. **Preparar as páginas** (preto e branco puro, 2550x3300 px, desenho centrado com margem de 0,5"):
   `python3 scripts/preparar_paginas.py pasta_do_gemini pasta_paginas`
   - Lê as imagens pela ordem do nome; grava `pagina_001.png`... e `relatorio.txt`.
   - FALHA = traço fino demais para a KDP (mínimo 0,75 pt = 0,01"): regerar no Gemini com "thicker lines".
   - AVISO "ampliado Nx": imagem do Gemini pequena; ver a página em tamanho real. Para imprimir bem, pedir ao Gemini a imagem maior ou vetorizar com `potrace` (local).
   - AVISO de cinzentos/tinta: provável sombreado ou fundo escuro → regerar.
   - Antes disto correr sempre o `verificar_paginas.py` da skill `livros-colorir-cayus` e ver as folhas de contactos.
2. **Interior**: `python3 scripts/montar_interior.py pasta_paginas interior.pdf --titulo "Bold & Easy Garden Birds" --fonte <Bricolage ou Literata .ttf>`
   - Ordem: título, direitos de autor, e cada desenho seguido de um verso com uma linha discreta (evita a rejeição por "demasiadas páginas em branco").
   - Total par e ≥ 24; o script diz o nº de páginas para a capa.
3. **Capa**: `python3 scripts/montar_capa.py --frente frente.png --verso verso.png --paginas <nº do passo 2> --saida capa.pdf --lombada-titulo "GARDEN BIRDS" --lombada-autor "CAYUS" --fonte <Bricolage .ttf>`
   - Frente e verso feitos como painéis separados no Gemini (nunca a capa inteira de uma vez). Título e autor da lombada desenhados pelo script.
   - Painéis precisam de ~2588x3375 px para 300 ppi: o script avisa se estiverem abaixo.
   - Abre `capa_guias.png`: vermelho = corte, azul = dobras da lombada, laranja = zona segura (texto importante lá dentro).
4. **Verificar**: `python verificar_capa_kdp.py --capa capa.pdf --paginas N --trim 8.5x11 --papel branco --interior interior.pdf` (skill `livros-colorir-cayus`) tem de dar PASSA. Converter o PDF em imagens (`pdftoppm -r 40 -png interior.pdf p`) e olhar para todas as páginas.

## Medidas KDP usadas (confirmar na ajuda oficial da KDP antes de cada lançamento)
| Regra | Valor |
|---|---|
| Páginas | mínimo 24, total par; 8,5x11 até 590 |
| Margens sem sangria | exterior ≥ 0,25"; interior 0,375" (24–150 págs), 0,5" (151–300) — usamos 0,5" em tudo |
| Resolução | ≥ 300 ppi (abaixo de 200 = "baixa resolução") |
| Traço | ≥ 0,75 pt (0,01") |
| Lombada | páginas × 0,002252" (branco), 0,0025" (creme), 0,002347" (cor) |
| Texto na lombada | só com mais de 79 páginas, a 0,0625" das dobras |
| Capa | 0,125 + verso + lombada + frente + 0,125 de largura; altura + 0,25. Ex.: 8,5x11, 102 págs, branco = 17,48" x 11,25" (5244x3375 px) |
| Código de barras | zona branca 2" x 1,2" no canto inferior direito do verso, a ≥ 0,25" da lombada e do corte |
| Conteúdo de IA | declarar na KDP (capa e interior). Livros de colorir não são "low-content": não marcar essa opção |

## Quando está pronto
- Relatório do passo 1 sem FALHA (e avisos vistos um a um).
- Interior aberto e todas as páginas vistas; nº de páginas par e ≥ 24.
- `verificar_capa_kdp.py` = PASSA; guias vistas; texto dentro da zona segura e sem erros.
- No relatório ao João: o que foi verificado, o que falhou e foi refeito, o que não foi possível verificar.

Baseada na skill kdp-coloring-book de CarlosCaPe (MIT) e na kindle-cover de nikmcfly (MIT), reescrita sem geração de imagens por API e adaptada ao formato Cayus.
