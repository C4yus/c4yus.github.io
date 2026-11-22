#!/usr/bin/env python3
"""Monta o PDF do interior KDP: um desenho por folha, só de um lado.

Uso:
  python3 montar_interior.py PASTA_PAGINAS interior.pdf --titulo "Bold & Easy Garden Birds" \
      [--autor "Cayus Books"] [--ano 2026] [--trim 8.5x11] [--fonte caminho.ttf]

Ordem: página de título, página de direitos (verso), depois cada desenho seguido de um verso
com uma linha discreta ("This page is intentionally left blank..."), para a KDP não ver
páginas em branco a mais. Total sempre par e >= 24. O texto é desenhado em imagem
(não há fontes por embutir). Só local (Pillow).
"""
import argparse, os, sys
from PIL import Image, ImageDraw, ImageFont

PPI = 300
VERSO = "This page is intentionally left blank so markers don't bleed through."


def fonte(caminho, tam):
    candidatos = [caminho] if caminho else []
    candidatos += ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "C:/Windows/Fonts/arial.ttf",
                   "/System/Library/Fonts/Supplemental/Arial.ttf", "/Library/Fonts/Arial.ttf"]
    for c in candidatos:
        if c and os.path.exists(c):
            return ImageFont.truetype(c, tam)
    sys.exit("Não encontrei um tipo de letra .ttf: indicar com --fonte")


def texto_centrado(d, y, txt, f, w):
    larg = d.textlength(txt, font=f)
    d.text(((w - larg) / 2, y), txt, font=f, fill=0)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("paginas"); ap.add_argument("saida")
    ap.add_argument("--titulo", required=True); ap.add_argument("--autor", default="Cayus Books")
    ap.add_argument("--ano", default="2026"); ap.add_argument("--trim", default="8.5x11")
    ap.add_argument("--fonte"); ap.add_argument("--sem-verso-texto", action="store_true", help="versos totalmente brancos")
    a = ap.parse_args()
    tw, th = (float(x) for x in a.trim.lower().split("x"))
    W, H = round(tw * PPI), round(th * PPI)
    fich = sorted(f for f in os.listdir(a.paginas) if f.lower().endswith(".png") and f.startswith("pagina_"))
    if not fich:
        sys.exit("Sem ficheiros pagina_*.png (correr primeiro preparar_paginas.py).")

    def branca():
        return Image.new("L", (W, H), 255)

    paginas = []
    t = branca(); d = ImageDraw.Draw(t)
    ft = fonte(a.fonte, 150)
    linhas, atual = [], ""
    for p in a.titulo.split():  # quebra o título em linhas
        teste = (atual + " " + p).strip()
        if d.textlength(teste, font=ft) > W - 2 * PPI and atual:
            linhas.append(atual); atual = p
        else:
            atual = teste
    linhas.append(atual)
    y = H * 0.32
    for l in linhas:
        texto_centrado(d, y, l, ft, W); y += 190
    texto_centrado(d, y + 120, a.autor, fonte(a.fonte, 70), W)
    paginas.append(t)
    c = branca(); d = ImageDraw.Draw(c); fp = fonte(a.fonte, 38)
    texto_centrado(d, H * 0.80, f"Copyright © {a.ano} {a.autor}. All rights reserved.", fp, W)
    texto_centrado(d, H * 0.80 + 60, "No part of this book may be reproduced without written permission.", fp, W)
    paginas.append(c)
    for f in fich:
        im = Image.open(os.path.join(a.paginas, f)).convert("L")
        if im.size != (W, H):
            sys.exit(f"{f} tem {im.size}, esperado {(W, H)}: preparar com o mesmo --trim.")
        paginas.append(im)
        v = branca()
        if not a.sem_verso_texto:
            texto_centrado(ImageDraw.Draw(v), H - 1.0 * PPI, VERSO, fonte(a.fonte, 34), W)
        paginas.append(v)
    if len(paginas) % 2:
        paginas.append(branca())
    if len(paginas) < 24:
        sys.exit(f"Só {len(paginas)} páginas: a KDP exige pelo menos 24.")
    paginas = [p.convert("1") for p in paginas]
    paginas[0].save(a.saida, save_all=True, append_images=paginas[1:], resolution=PPI)
    print(f"OK {a.saida}: {len(paginas)} páginas ({len(fich)} desenhos), {tw}x{th}\" sem sangria, {PPI} ppi.")
    print(f"Para a capa: --paginas {len(paginas)}")


if __name__ == "__main__":
    main()
