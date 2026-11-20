#!/usr/bin/env python3
"""Verifica o site Cayus antes de publicar. Só biblioteca padrão.

Uso (na raiz do repo):  python3 tools/verificar_site.py
Sai com código 1 se houver ERROS; AVISOS não bloqueiam.
Checks: estrutura HTML, SEO, acessibilidade, links internos e de ficheiros,
links Amazon, sitemap, JSON-LD, contraste da paleta, CSS (foco, movimento
reduzido), páginas de livros iguais ao que build_books.py gera.
"""
import json, os, re, subprocess, sys, tempfile, shutil
from html.parser import HTMLParser
from urllib.parse import urlparse, unquote

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SITE = "https://c4yus.github.io"
errors, warns = [], []
def err(p, m): errors.append(f"{p}: {m}")
def warn(p, m): warns.append(f"{p}: {m}")

# --- contraste (WCAG) ---
def lum(h):
    h = h.lstrip("#"); r, g, b = (int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)
def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True); return (la + 0.05) / (lb + 0.05)

# pares (texto, fundo, mínimo) que a MARCA.md garante
PARES = [("#fbfcf9", "#4f7f35", 4.5, "texto claro sobre leaf (Livros)"),
         ("#14261f", "#e2701f", 4.5, "texto escuro sobre ember (Modelos)"),
         ("#fbfcf9", "#2a2d66", 4.5, "texto claro sobre dusk (Vídeos)"),
         ("#14261f", "#eef3ea", 4.5, "forest sobre sage (texto base)"),
         ("#3d6429", "#eef3ea", 4.5, "leaf-escuro sobre sage ('em breve')"),
         ("#51604f", "#eef3ea", 4.5, "mute sobre sage")]
for fg, bg, mn, nome in PARES:
    r = ratio(fg, bg)
    if r < mn: err("contraste", f"{nome}: {r:.2f}:1 (< {mn})")

class P(HTMLParser):
    def __init__(s): super().__init__(); s.t = []; s.in_title = False; s.title = ""; s.ld = None; s.ldtxt = []; s.h1 = 0; s.imgs = []; s.links = []; s.meta = {}; s.lang = None; s.scripts = []
    def handle_starttag(s, tag, a):
        a = dict(a); s.t.append(tag)
        if tag == "html": s.lang = a.get("lang")
        if tag == "title": s.in_title = True
        if tag == "h1": s.h1 += 1
        if tag == "meta":
            k = a.get("name") or a.get("property")
            if k: s.meta[k] = a.get("content", "")
        if tag == "img": s.imgs.append(a)
        if tag in ("a", "link") and a.get("href"): s.links.append((tag, a))
        if tag in ("script", "img", "source") and a.get("src"): s.links.append((tag, a))
        if tag == "script" and a.get("type") == "application/ld+json": s.ld = True
    def handle_endtag(s, tag):
        if tag == "title": s.in_title = False
        if tag == "script": s.ld = None
    def handle_data(s, d):
        if s.in_title: s.title += d
        if s.ld: s.ldtxt.append(d)

def pages():
    out = []
    for d, ds, fs in os.walk(ROOT):
        ds[:] = [x for x in ds if x not in (".git", "node_modules", "tools")]
        for f in fs:
            if f.endswith(".html"): out.append(os.path.join(d, f))
    return sorted(out)

def url_of(path):
    rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
    rel = rel[:-len("index.html")] if rel.endswith("index.html") else rel
    return f"{SITE}/{rel}"

ALL = pages()
urls = set()
for path in ALL:
    rel = os.path.relpath(path, ROOT); urls.add(url_of(path))
    p = P(); p.feed(open(path, encoding="utf-8").read())
    if p.lang != "en": err(rel, f"<html lang> = {p.lang!r} (esperado 'en')")
    if not p.title.strip(): err(rel, "sem <title>")
    elif len(p.title) > 70: warn(rel, f"<title> com {len(p.title)} caracteres (>70)")
    d = p.meta.get("description", "")
    if not d: err(rel, "sem meta description")
    elif len(d) > 175: warn(rel, f"meta description com {len(d)} caracteres (>175)")
    if "viewport" not in p.meta: err(rel, "sem meta viewport")
    if p.h1 != 1: err(rel, f"{p.h1} <h1> (esperado 1)")
    if "main" not in p.t: err(rel, "sem <main>")
    if not p.meta.get("og:title"): warn(rel, "sem og:title")
    for im in p.imgs:
        if "alt" not in im: err(rel, f"imagem sem alt: {im.get('src')}")
        if not im.get("width") or not im.get("height"): warn(rel, f"imagem sem width/height: {im.get('src')}")
    if p.ldtxt:
        try: json.loads("".join(p.ldtxt))
        except Exception as e: err(rel, f"JSON-LD inválido: {e}")
    base = os.path.dirname(path)
    for tag, a in p.links:
        u = a.get("href") or a.get("src")
        if not u or u.startswith(("#", "mailto:", "data:")): continue
        pu = urlparse(u)
        if pu.scheme in ("http", "https"):
            if "amazon." in pu.netloc:
                if not re.fullmatch(r"/dp/B[0-9A-Z]{9}", pu.path): err(rel, f"link Amazon fora do formato /dp/ASIN: {u}")
                if "noopener" not in a.get("rel", ""): warn(rel, f"link Amazon sem rel=noopener: {u}")
            continue
        tgt = os.path.normpath(os.path.join(base, unquote(pu.path)))
        if os.path.isdir(tgt): tgt = os.path.join(tgt, "index.html")
        if not os.path.exists(tgt): err(rel, f"link/ficheiro em falta: {u}")
    # cada página com Amazon deve ter pelo menos um botão de compra (só livros)
    if "/livros/" in path.replace(os.sep, "/") and path.count(os.sep) > ROOT.count(os.sep) + 2:
        if not any("amazon." in (a.get("href") or "") for _, a in p.links): err(rel, "página de livro sem link para a Amazon")

# --- sitemap / robots ---
sm = os.path.join(ROOT, "sitemap.xml")
if os.path.exists(sm):
    locs = set(re.findall(r"<loc>([^<]+)</loc>", open(sm).read()))
    for u in sorted(urls - locs): err("sitemap.xml", f"falta a página {u}")
    for u in sorted(locs - urls): err("sitemap.xml", f"aponta para página que não existe: {u}")
else: err("sitemap.xml", "não existe")
if not os.path.exists(os.path.join(ROOT, "robots.txt")): err("robots.txt", "não existe")

# --- CSS e JS ---
css = open(os.path.join(ROOT, "css/site.css")).read()
if ":focus-visible" not in css: err("css/site.css", "sem estilo :focus-visible")
if "prefers-reduced-motion" not in css: err("css/site.css", "sem prefers-reduced-motion")
pal = {"#14261f", "#4f7f35", "#e2701f", "#2a2d66", "#eef3ea", "#fbfcf9", "#c8372d", "#3d6429", "#51604f", "#c5d1bf"}
for h in set(re.findall(r"#[0-9a-fA-F]{6}\b", css)):
    if h.lower() not in pal: warn("css/site.css", f"cor fora da paleta: {h}")
for g in re.findall(r"[a-z-]*gradient", css):
    if g != "repeating-linear-gradient":  # o wordmark listrado é a "coisa memorável" permitida
        warn("css/site.css", f"usa {g} (a MARCA diz sem gradientes decorativos)")
js = os.path.join(ROOT, "js/colorfill.js")
if os.path.exists(js) and "prefers-reduced-motion" not in open(js).read(): err("js/colorfill.js", "não respeita prefers-reduced-motion")

# --- livros gerados == build_books.py ---
bb = os.path.join(ROOT, "tools/build_books.py")
if os.path.exists(bb):
    tmp = tempfile.mkdtemp()
    try:
        shutil.copytree(ROOT, tmp + "/r", ignore=shutil.ignore_patterns(".git"))
        r = subprocess.run([sys.executable, "tools/build_books.py"], cwd=tmp + "/r", capture_output=True, text=True)
        if r.returncode: err("tools/build_books.py", f"falhou: {r.stderr[-300:]}")
        else:
            for d in sorted(os.listdir(os.path.join(ROOT, "livros"))):
                a = os.path.join(ROOT, "livros", d, "index.html"); b = os.path.join(tmp, "r/livros", d, "index.html")
                if os.path.isfile(a) and os.path.exists(b) and open(a).read() != open(b).read():
                    err(f"livros/{d}/index.html", "difere do que build_books.py gera (alterado à mão? corre o build e edita o BOOKS)")
    finally: shutil.rmtree(tmp, ignore_errors=True)

print(f"Páginas verificadas: {len(ALL)}")
for w in warns: print("AVISO ", w)
for e in errors: print("ERRO  ", e)
print(f"\n{len(errors)} erro(s), {len(warns)} aviso(s)")
sys.exit(1 if errors else 0)
