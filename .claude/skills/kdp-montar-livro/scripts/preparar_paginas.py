#!/usr/bin/env python3
"""Prepara desenhos (PNG/JPG do Gemini) para o interior KDP: preto e branco puro, 300 ppi, centrados na página.

Uso:
  python3 preparar_paginas.py ENTRADA SAIDA [--trim 8.5x11] [--margem 0.5] [--limiar 160]

ENTRADA: pasta com as imagens, pela ordem do nome (pagina_01.png, pagina_02.png...).
SAIDA:   pasta onde ficam paginas 1 bit (ex.: 2550x3300 px para 8,5x11) + relatorio.txt.
Sem sangria: o desenho fica dentro da margem (por defeito 0,5", acima do mínimo da KDP).
Só local (Pillow + NumPy). Sai com 1 se alguma página falhar.
"""
import argparse, os, sys
import numpy as np
from PIL import Image, ImageFilter

PPI = 300


def preparar(caminho, w_px, h_px, margem_px, limiar):
    im = Image.open(caminho).convert("L")
    arr = np.asarray(im)
    avisos, erros = [], []
    cinzento = np.mean((arr > 40) & (arr < 215))
    if cinzento > 0.08:
        avisos.append(f"{cinzento:.0%} de píxeis cinzentos no original (sombreado?)")
    # recortar o branco à volta do desenho
    tinta = arr < limiar
    if not tinta.any():
        return None, ["página em branco"], avisos
    ys, xs = np.where(tinta)
    im = im.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))
    caixa_w, caixa_h = w_px - 2 * margem_px, h_px - 2 * margem_px
    esc = min(caixa_w / im.width, caixa_h / im.height)
    if esc > 3:
        avisos.append(f"ampliado {esc:.1f}x (original pequeno: {im.width}x{im.height} px); ver se as linhas ficaram limpas")
    novo = im.resize((max(1, round(im.width * esc)), max(1, round(im.height * esc))), Image.LANCZOS)
    novo = novo.filter(ImageFilter.MedianFilter(3))
    bw = novo.point(lambda v: 255 if v >= limiar else 0, mode="1")
    pag = Image.new("1", (w_px, h_px), 1)
    pag.paste(bw, ((w_px - bw.width) // 2, (h_px - bw.height) // 2))
    # espessura do traço: erodir 3x3 (0,01" = 3 px a 300 ppi); se o traço desaparece, é fino demais
    preto = ~np.asarray(pag.convert("L")).astype(bool)
    er = np.asarray(Image.fromarray((preto * 255).astype("uint8")).filter(ImageFilter.MinFilter(3))) > 0
    sobra = er.sum() / max(1, preto.sum())
    if sobra < 0.35:
        erros.append(f"traço demasiado fino: só {sobra:.0%} resiste a 0,01\" (mínimo KDP 0,75 pt)")
    elif sobra < 0.55:
        avisos.append(f"traço fino: {sobra:.0%} resiste a 0,01\"")
    tinta_pct = preto.mean()
    if tinta_pct > 0.35:
        avisos.append(f"{tinta_pct:.0%} de tinta (muito preto para colorir?)")
    return pag, erros, avisos


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entrada"); ap.add_argument("saida")
    ap.add_argument("--trim", default="8.5x11"); ap.add_argument("--margem", type=float, default=0.5)
    ap.add_argument("--limiar", type=int, default=160, help="0-255; abaixo disto é tinta")
    a = ap.parse_args()
    tw, th = (float(x) for x in a.trim.lower().split("x"))
    w_px, h_px, m_px = round(tw * PPI), round(th * PPI), round(a.margem * PPI)
    if a.margem < 0.25:
        sys.exit("Margem abaixo do mínimo da KDP sem sangria (0,25\").")
    os.makedirs(a.saida, exist_ok=True)
    fich = sorted(f for f in os.listdir(a.entrada) if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")))
    if not fich:
        sys.exit("Nenhuma imagem na pasta de entrada.")
    linhas, falhas = [], 0
    for i, f in enumerate(fich, 1):
        pag, erros, avisos = preparar(os.path.join(a.entrada, f), w_px, h_px, m_px, a.limiar)
        nome = f"pagina_{i:03d}.png"
        if pag is not None:
            pag.save(os.path.join(a.saida, nome), dpi=(PPI, PPI))
        estado = "FALHA" if erros else ("AVISO" if avisos else "OK")
        falhas += bool(erros)
        linhas.append(f"{estado:5} {f} -> {nome} " + "; ".join(erros + avisos))
    rel = "\n".join(linhas) + f"\n\n{len(fich)} páginas, {falhas} com falha. Tamanho {w_px}x{h_px} px a {PPI} ppi, margem {a.margem}\".\n"
    open(os.path.join(a.saida, "relatorio.txt"), "w").write(rel)
    print(rel)
    sys.exit(1 if falhas else 0)


if __name__ == "__main__":
    main()
