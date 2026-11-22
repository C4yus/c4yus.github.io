#!/usr/bin/env python3
"""Mede a qualidade de páginas do site num browser local (Playwright), sem serviços externos.

Uso (com o site servido em localhost, ex.: python3 -m http.server 8765):
  python3 medir_pagina.py http://localhost:8765/ http://localhost:8765/livros/
  python3 medir_pagina.py --telemovel --json relatorio.json http://localhost:8765/

Mede: LCP, CLS, peso total e por tipo, nº de pedidos, pedidos a outros domínios,
imagens grandes / sem width+height / sem alt / sem lazy fora do ecrã, erros da consola,
scroll horizontal, alvos de toque pequenos. Sai com 1 se alguma página tiver ERRO.
Opção --chromium CAMINHO para usar um Chromium já instalado.
"""
import argparse, json, sys
from urllib.parse import urlparse

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit("Falta o Playwright: pip install playwright && python -m playwright install chromium")

LIMITES = {"lcp_ms": 2500, "cls": 0.1, "peso_kb": 1600, "img_kb": 300, "pedidos": 50}

OBS = """
window.__cls = 0; window.__lcp = 0;
new PerformanceObserver(l => { for (const e of l.getEntries()) if (!e.hadRecentInput) window.__cls += e.value; })
  .observe({type: 'layout-shift', buffered: true});
new PerformanceObserver(l => { const e = l.getEntries(); if (e.length) window.__lcp = e[e.length-1].startTime; })
  .observe({type: 'largest-contentful-paint', buffered: true});
"""

INSPECAO = """() => {
  const vh = innerHeight, out = {imgs: [], toques: 0};
  for (const im of document.images) {
    const r = im.getBoundingClientRect();
    out.imgs.push({src: im.currentSrc || im.src, alt: im.getAttribute('alt'),
      wh: im.hasAttribute('width') && im.hasAttribute('height') || !!getComputedStyle(im).aspectRatio && getComputedStyle(im).aspectRatio !== 'auto',
      lazy: im.loading === 'lazy', abaixo: r.top > vh, natural: im.naturalWidth, mostrada: Math.round(r.width * devicePixelRatio)});
  }
  for (const a of document.querySelectorAll('a,button,input,select,textarea')) {
    const r = a.getBoundingClientRect();
    if (r.width && r.height && (r.width < 24 || r.height < 24)) out.toques++;
  }
  out.scrollH = document.documentElement.scrollWidth > innerWidth;
  out.lcp = window.__lcp; out.cls = window.__cls;
  return out;
}"""


def medir(browser, url, telemovel):
    vp = {"width": 390, "height": 844} if telemovel else {"width": 1280, "height": 900}
    ctx = browser.new_context(viewport=vp, device_scale_factor=2 if telemovel else 1)
    pg = ctx.new_page()
    pg.add_init_script(OBS)
    pedidos, consola = [], []
    pg.on("console", lambda m: consola.append(m.text) if m.type == "error" else None)
    pg.on("pageerror", lambda e: consola.append(str(e)))

    def resp(r):
        try:
            tam = len(r.body())
        except Exception:
            tam = int(r.headers.get("content-length", 0) or 0)
        pedidos.append({"url": r.url, "tipo": r.request.resource_type, "bytes": tam, "estado": r.status})
    pg.on("response", resp)
    pg.goto(url, wait_until="networkidle")
    pg.wait_for_timeout(1500)
    d = pg.evaluate(INSPECAO)
    ctx.close()

    host = urlparse(url).hostname
    peso = sum(p["bytes"] for p in pedidos)
    por_tipo = {}
    for p in pedidos:
        por_tipo[p["tipo"]] = por_tipo.get(p["tipo"], 0) + p["bytes"]
    fora = sorted({urlparse(p["url"]).hostname for p in pedidos if urlparse(p["url"]).hostname not in (host, None)})
    erros, avisos = [], []
    if d["lcp"] > LIMITES["lcp_ms"]: avisos.append(f"LCP {d['lcp']:.0f} ms (> {LIMITES['lcp_ms']}; medido em localhost, na net é pior)")
    if d["cls"] > LIMITES["cls"]: erros.append(f"CLS {d['cls']:.3f} (> {LIMITES['cls']}): coisas a saltar ao carregar")
    if peso / 1024 > LIMITES["peso_kb"]: avisos.append(f"página pesa {peso/1024:.0f} KB (> {LIMITES['peso_kb']})")
    if len(pedidos) > LIMITES["pedidos"]: avisos.append(f"{len(pedidos)} pedidos (> {LIMITES['pedidos']})")
    for p in pedidos:
        if p["estado"] >= 400: erros.append(f"{p['estado']} em {p['url']}")
        if p["tipo"] == "image" and p["bytes"] / 1024 > LIMITES["img_kb"]:
            avisos.append(f"imagem de {p['bytes']/1024:.0f} KB: {p['url'].split('/')[-1]} (passar a WebP ou reduzir)")
    for im in d["imgs"]:
        nome = im["src"].split("/")[-1]
        if im["alt"] is None: erros.append(f"imagem sem alt: {nome}")
        if not im["wh"]: avisos.append(f"imagem sem width/height nem aspect-ratio (pode saltar): {nome}")
        if im["abaixo"] and not im["lazy"]: avisos.append(f"imagem fora do ecrã sem loading=lazy: {nome}")
        if im["mostrada"] and im["natural"] > im["mostrada"] * 2: avisos.append(f"imagem com {im['natural']}px de largura para {im['mostrada']}px no ecrã (já com a densidade do ecrã): {nome}")
    if d["scrollH"]: erros.append("scroll horizontal (algo sai do ecrã)")
    if d["toques"]: avisos.append(f"{d['toques']} alvos de toque com menos de 24px")
    erros += [f"consola: {c}" for c in consola]
    return {"url": url, "vista": "telemovel" if telemovel else "pc", "lcp_ms": round(d["lcp"]), "cls": round(d["cls"], 3),
            "peso_kb": round(peso / 1024), "pedidos": len(pedidos),
            "por_tipo_kb": {k: round(v / 1024) for k, v in por_tipo.items()},
            "outros_dominios": fora, "erros": erros, "avisos": avisos}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("urls", nargs="+")
    ap.add_argument("--telemovel", action="store_true", help="medir também em 390x844")
    ap.add_argument("--json", help="gravar o relatório neste ficheiro")
    ap.add_argument("--chromium", help="caminho de um Chromium já instalado")
    a = ap.parse_args()
    for u in a.urls:
        if urlparse(u).hostname not in ("localhost", "127.0.0.1"):
            print(f"AVISO: {u} não é localhost; a medição abre esse site (só leitura).")
    res = []
    with sync_playwright() as p:
        b = p.chromium.launch(**({"executable_path": a.chromium} if a.chromium else {}))
        for u in a.urls:
            res.append(medir(b, u, False))
            if a.telemovel:
                res.append(medir(b, u, True))
        b.close()
    total = 0
    for r in res:
        print(f"\n== {r['url']} ({r['vista']})")
        print(f"   LCP {r['lcp_ms']} ms | CLS {r['cls']} | {r['peso_kb']} KB em {r['pedidos']} pedidos | {r['por_tipo_kb']}")
        if r["outros_dominios"]: print(f"   outros domínios: {', '.join(r['outros_dominios'])}")
        for e in r["erros"]: print(f"   ERRO  {e}")
        for w in r["avisos"]: print(f"   AVISO {w}")
        total += len(r["erros"])
    print(f"\n{total} erro(s)")
    if a.json:
        json.dump(res, open(a.json, "w"), indent=2, ensure_ascii=False)
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
