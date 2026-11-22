#!/usr/bin/env python3
"""Monta a capa KDP completa (verso + lombada + frente) com as medidas oficiais, num único PDF.

Uso:
  python3 montar_capa.py --frente frente.png --paginas 102 --saida capa.pdf \
      [--verso verso.png | --cor-verso "#eef3ea"] [--trim 8.5x11] [--papel branco] \
      [--lombada-titulo "GARDEN BIRDS"] [--lombada-autor "CAYUS"] [--cor-lombada "#14261f"] \
      [--cor-texto-lombada "#fbfcf9"] [--fonte caminho.ttf]

- Largura = 0,125 + verso + lombada + frente + 0,125 (pol.); altura = trim + 0,25.
- Lombada = páginas x 0,002252" (branco), 0,0025" (creme), 0,002347" (cor).
- Texto na lombada só com mais de 79 páginas, a 0,0625" das dobras.
- Zona do código de barras (2" x 1,2") em branco no canto inferior direito do verso,
  a 0,25" da lombada e do corte de baixo.
- A frente e o verso são esticados para cobrir o painel com a sangria (cortar ao centro):
  manter texto importante a 0,25" do corte.
Grava também <saida>_guias.png com as linhas de corte, dobra e zona segura para ver.
Só local (Pillow). Confirmar depois com verificar_capa_kdp.py e no pré-visualizador da KDP.
"""
import argparse, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageOps

PPI, SANGRIA = 300, 0.125
POR_PAGINA = {"branco": 0.002252, "creme": 0.0025, "cor": 0.002347}


def px(pol):
    return round(pol * PPI)


def fonte(caminho, tam):
    for c in ([caminho] if caminho else []) + ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
              "C:/Windows/Fonts/arialbd.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"]:
        if c and os.path.exists(c):
            return ImageFont.truetype(c, tam)
    sys.exit("Não encontrei um tipo de letra .ttf: indicar com --fonte")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--frente", required=True); ap.add_argument("--verso"); ap.add_argument("--cor-verso", default="#fbfcf9")
    ap.add_argument("--paginas", type=int, required=True); ap.add_argument("--saida", required=True)
    ap.add_argument("--trim", default="8.5x11"); ap.add_argument("--papel", default="branco", choices=POR_PAGINA)
    ap.add_argument("--lombada-titulo", default=""); ap.add_argument("--lombada-autor", default="CAYUS")
    ap.add_argument("--cor-lombada", default="#14261f"); ap.add_argument("--cor-texto-lombada", default="#fbfcf9")
    ap.add_argument("--fonte")
    a = ap.parse_args()
    if a.paginas < 24 or a.paginas % 2:
        sys.exit("O nº de páginas do interior tem de ser par e >= 24 (usar o número que montar_interior.py deu).")
    tw, th = (float(x) for x in a.trim.lower().split("x"))
    lomb = a.paginas * POR_PAGINA[a.papel]
    W_pol, H_pol = SANGRIA * 2 + tw * 2 + lomb, th + SANGRIA * 2
    W, H = px(W_pol), px(H_pol)
    x_lomb0, x_lomb1 = px(SANGRIA + tw), px(SANGRIA + tw + lomb)
    capa = Image.new("RGB", (W, H), a.cor_verso)

    def painel(caminho, x0, x1):
        im = Image.open(caminho).convert("RGB")
        alvo = (x1 - x0, H)
        if im.width < alvo[0] * 0.66:
            print(f"AVISO {os.path.basename(caminho)}: {im.width}px para {alvo[0]}px ({im.width / (alvo[0] / PPI):.0f} ppi): ampliar para 300 ppi antes de imprimir")
        capa.paste(ImageOps.fit(im, alvo, Image.LANCZOS), (x0, 0))

    if a.verso:
        painel(a.verso, 0, x_lomb0)
    painel(a.frente, x_lomb1, W)
    d = ImageDraw.Draw(capa)
    d.rectangle([x_lomb0, 0, x_lomb1 - 1, H], fill=a.cor_lombada)
    # código de barras: canto inferior direito do verso
    bx1 = x_lomb0 - px(0.25); by1 = H - px(SANGRIA) - px(0.25)
    d.rectangle([bx1 - px(2.0), by1 - px(1.2), bx1, by1], fill="white")
    if a.paginas > 79 and (a.lombada_titulo or a.lombada_autor):
        larg_util = x_lomb1 - x_lomb0 - 2 * px(0.0625)
        tam = max(10, int(larg_util * 0.62))
        f = fonte(a.fonte, tam)
        txt = "   ".join(t for t in (a.lombada_titulo, a.lombada_autor) if t)
        comp = d.textlength(txt, font=f)
        limite = H - 2 * px(SANGRIA) - 2 * px(0.375)
        if comp > limite:
            f = fonte(a.fonte, int(tam * limite / comp)); comp = d.textlength(txt, font=f)
        tira = Image.new("RGBA", (int(comp) + 4, int(tam * 1.4)), (0, 0, 0, 0))
        ImageDraw.Draw(tira).text((2, 0), txt, font=f, fill=a.cor_texto_lombada)
        tira = tira.rotate(-90, expand=True)  # lê-se de cima para baixo (padrão EUA)
        capa.paste(tira, (x_lomb0 + (x_lomb1 - x_lomb0 - tira.width) // 2, (H - tira.height) // 2), tira)
    elif a.lombada_titulo and a.paginas <= 79:
        print("AVISO: com 79 páginas ou menos a lombada fica sem texto (regra da KDP).")
    capa.save(a.saida, resolution=PPI)
    g = capa.copy(); dg = ImageDraw.Draw(g)
    for x in (px(SANGRIA), W - px(SANGRIA)):
        dg.line([x, 0, x, H], fill="red", width=3)
    for y in (px(SANGRIA), H - px(SANGRIA)):
        dg.line([0, y, W, y], fill="red", width=3)
    for x in (x_lomb0, x_lomb1):
        dg.line([x, 0, x, H], fill="blue", width=3)
    s = px(SANGRIA + 0.25)
    dg.rectangle([s, s, x_lomb0 - px(0.25), H - s], outline="orange", width=3)
    dg.rectangle([x_lomb1 + px(0.25), s, W - s, H - s], outline="orange", width=3)
    g.thumbnail((2000, 2000)); g.save(os.path.splitext(a.saida)[0] + "_guias.png")
    print(f"OK {a.saida}: {W_pol:.3f}\" x {H_pol:.3f}\" ({W}x{H} px a {PPI} ppi), lombada {lomb:.3f}\" "
          f"({a.paginas} páginas, papel {a.papel}). Guias: vermelho=corte, azul=dobras, laranja=zona segura.")


if __name__ == "__main__":
    main()
