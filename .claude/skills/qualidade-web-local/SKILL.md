---
name: qualidade-web-local
description: "Auditar a velocidade, Core Web Vitals (LCP, CLS, INP), peso das imagens, acessibilidade técnica, SEO técnico e boas práticas do site Cayus num browser local, sem PageSpeed, CrUX nem outros serviços externos. Usar quando o João pedir 'o site está lento?', 'auditoria', 'Lighthouse', 'otimizar imagens', 'melhorar o SEO técnico' ou antes de uma mudança grande ir para o ar."
---

# Qualidade web (só local)

Responder ao João em PT-PT, curto. Complementa `auditoria-site` (SEO de conteúdo, acessibilidade, conversão) e `revisao-visual-site` (capturas). Esta skill trata do que se mede.
Nunca enviar URLs para PageSpeed Insights, CrUX, WebPageTest ou outros serviços. Medir aqui.

## 1. Medir
1. Servir o repo na raiz: `python3 -m http.server 8765`.
2. Correr: `python3 .claude/skills/qualidade-web-local/scripts/medir_pagina.py --telemovel http://localhost:8765/ http://localhost:8765/livros/ http://localhost:8765/livros/<slug>/`
   - Precisa de `pip install playwright` e `python -m playwright install chromium` (ou `--chromium <caminho>` para um Chromium já instalado).
   - Sai com 1 se houver ERRO. Ler a saída toda, não só o código de saída.
3. Correr também `python3 -I tools/verificar_site.py`.

Os tempos em localhost são otimistas (sem rede). Contam as diferenças entre versões e os problemas de estrutura (CLS, peso, imagens), não o número absoluto.

## 2. Limites
| Métrica | Bom | O que costuma resolver |
|---|---|---|
| LCP (maior elemento visível) | ≤ 2,5 s | imagem principal leve (WebP, ≤ 200 KB), `fetchpriority="high"` nela, sem `loading=lazy` na primeira imagem, CSS pequeno, `font-display: swap` |
| CLS (saltos) | ≤ 0,1 | `width`/`height` ou `aspect-ratio` em todas as imagens e canvas; reservar espaço para o que carrega depois |
| INP (resposta a cliques) | ≤ 200 ms | pouco JS; trabalho pesado (ex.: animação da cor) fora do clique, em `requestAnimationFrame` |
| Peso da página | ≤ 1,6 MB | imagens à medida em que aparecem (máx. 2× a largura mostrada), WebP/AVIF com `<picture>` |
| Imagem individual | ≤ 300 KB | reduzir, WebP qualidade ~80 |

## 3. Lista técnica
**Desempenho:** imagens fora do ecrã com `loading="lazy"` e `decoding="async"`; `srcset`/`sizes` quando a mesma imagem aparece em tamanhos muito diferentes; pré-ligar só o necessário; sem scripts bloqueantes no `<head>`.
**Fontes:** o site carrega Bricolage Grotesque e Literata do Google Fonts — é um pedido a outro domínio em cada visita. Alternativa local: guardar os .woff2 em `fonts/` e declarar `@font-face` com `font-display: swap` (mais rápido e sem enviar visitas ao Google). Só mudar com o sim do João.
**Acessibilidade técnica:** `lang` no `<html>`, um `<h1>`, `alt` em todas as imagens (vazio só se decorativa), foco visível, alvos de toque ≥ 24px (ideal 44px), contraste ≥ 4,5:1, `prefers-reduced-motion` respeitado, nada de scroll horizontal.
**SEO técnico:** `<title>` e `meta description` únicos, `link rel="canonical"`, `og:title`/`og:image`, `sitemap.xml` e `robots.txt` certos, dados estruturados JSON-LD (`Book` com `isbn`/`offers` quando houver, `BreadcrumbList`), URLs limpas, links internos com texto descritivo.
**Boas práticas:** HTTPS em todos os recursos, `rel="noopener"` em links externos, sem erros na consola, sem bibliotecas desnecessárias, `<meta name="viewport">`.

## 4. Relatório ao João
Por página: números (LCP, CLS, peso), os ERROS, e no máximo 5 melhorias ordenadas por ganho/esforço. Dizer o que foi medido e o que não foi (INP só se mede com cliques reais; na dúvida dizer "não medido").

Baseada nas listas das web-quality-skills de Addy Osmani (MIT), reescrita para funcionar só localmente (a original recomenda CrUX e PageSpeed, que enviam o endereço para a Google).
