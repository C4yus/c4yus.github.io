"""Gera livros/<slug>/index.html para cada livro. Correr na raiz do repo: python3 tools/build_books.py"""
import os, json
SITE = "https://c4yus.github.io/cayus-livros"
BOOKS = [
 dict(slug="garden-birds", asin="B0HSCBDB7D", title="Bold & Easy Garden Birds", sub="50 Large-Print Designs of Cardinals, Blue Jays and Songbirds",
  line="Large birds, simple flowers and plenty of room for your markers.",
  d1="Fifty large-print designs of cardinals, blue jays and songbirds sit among simple flowers. The shapes are bold and open, so they are easy to color.",
  d2="Each design is printed on one side of the page, with a blank page behind it.",
  n=50, extra=None, cover="garden-birds.jpg", alt="Cover of Bold and Easy Garden Birds coloring book",
  meta="Bold and easy coloring book for adults: 50 large-print designs of cardinals, blue jays and songbirds among simple flowers."),
 dict(slug="garden-friends", asin="B0HSCH25HN", title="Bold & Easy Garden Friends", sub="50 Large-Print Designs of Bunnies, Hedgehogs, Butterflies and Flowers",
  line="Garden animals and flowers drawn with thick, easy lines.",
  d1="Fifty large-print designs of bunnies, hedgehogs, butterflies and flowers. The lines are thick and the spaces are open.",
  d2="Each design is printed on one side of the page, with a blank page behind it.",
  n=50, extra=None, cover="garden-friends.jpg", alt="Cover of Bold and Easy Garden Friends coloring book",
  meta="Bold and easy coloring book for adults: 50 large-print designs of bunnies, hedgehogs, butterflies and flowers."),
 dict(slug="botanical-garden", asin="B0HS565MBD", title="Botanical Garden", sub="60 Calming Flower, Herb and Pollinator Designs",
  line="Flowers, herbs and pollinators, drawn in fine line, one design per page.",
  d1="Sixty botanical designs: poppies, lavender, sunflowers, herbs and the bees and butterflies that visit them. Each page holds one design.",
  d2="Each design is printed on one side of the page, with a blank page behind it.",
  n=60, extra=None, cover="botanical-garden.jpg", alt="Cover of Botanical Garden coloring book",
  meta="Botanical Garden coloring book for adults: 60 flower, herb and pollinator designs, one design per page."),
 dict(slug="mindful-nature", asin="B0HS37XJ1P", title="Mindful Nature", sub="An Adult Coloring Book of Animals, Flowers and Mandalas",
  line="Detailed animals, flowers and mandalas for slow, careful coloring.",
  d1="Fifty detailed designs of animals, flowers and mandalas, from a lion and an owl to a stained-glass lotus. The patterns reward time and sharp pencils.",
  d2="The book includes a belongs-to page and a color test page. Each design is printed on one side of the page, with a blank page behind it.",
  n=50, extra="Belongs-to page and color test page", cover="mindful-nature.jpg", alt="Cover of Mindful Nature coloring book",
  meta="Mindful Nature coloring book for adults: 50 detailed designs of animals, flowers and mandalas, with a color test page."),
]
HEAD = '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,600;12..96,700;12..96,800&family=Literata:opsz,wght@7..72,400;7..72,600&display=swap" rel="stylesheet">'
for b in BOOKS:
    url = f"https://www.amazon.com/dp/{b['asin']}"
    ld = {"@context":"https://schema.org","@type":"Book","name":b["title"],"alternateName":b["sub"],"author":{"@type":"Person","name":"Cayus"},
          "bookFormat":"https://schema.org/Paperback","numberOfPages":None,"image":f"{SITE}/img/{b['cover']}","url":f"{SITE}/livros/{b['slug']}/"}
    ld.pop("numberOfPages")
    samples = "".join(f'<li><img src="../../img/samples/{b["slug"]}-{i}.jpg" alt="Sample coloring page {i} from {b["title"]}" width="680" height="880" loading="lazy"></li>' for i in range(1,5))
    anim = ('<section aria-labelledby="fill"><h2 id="fill">From line art to color</h2><div class="fill" data-colorfill="../../img/anim/cardinal"><canvas width="640" height="876" role="img" aria-label="A cardinal on a flowering branch, shown as line art that fills with colored-pencil color."></canvas><div><p>One page from the book, colored in. Yours starts as plain lines like this.</p><button type="button" class="btn">Loading…</button></div></div></section><script src="../../js/colorfill.js" defer></script>' if b["slug"]=="garden-birds" else "")
    extra = f'<div><dt>Also inside</dt><dd>{b["extra"]}</dd></div>' if b["extra"] else ""
    html = f'''{HEAD}<title>{b["title"]} coloring book | Cayus</title>
<meta name="description" content="{b["meta"]}"><link rel="stylesheet" href="../../css/site.css"><link rel="icon" href="../../favicon.svg" type="image/svg+xml">
<meta property="og:title" content="{b["title"]} | Cayus Books"><meta property="og:type" content="book"><meta property="og:image" content="{SITE}/img/{b["cover"]}"><meta name="theme-color" content="#14261f">
<script type="application/ld+json">{json.dumps(ld)}</script>
</head><body>
<div class="wrap"><div class="bar"><a class="mark" href="../../index.html">Cayus</a><nav aria-label="Main">
<a href="../index.html" aria-current="page">Books</a><a href="../../videos/index.html">Videos</a><a href="../../modelos/index.html">3D models</a></nav></div></div>
<main class="wrap">
<p class="crumb"><a href="../index.html">All books</a></p>
<section class="bookhead"><img class="cover" src="../../img/{b["cover"]}" alt="{b["alt"]}" width="765" height="990">
<div><h1>{b["title"]}</h1><p class="sub">{b["sub"]}</p><p class="lede">{b["line"]}</p>
<p><a class="btn" href="{url}" rel="noopener sponsored">Buy on Amazon</a></p></div></section>
<section class="about"><p>{b["d1"]}</p><p>{b["d2"]}</p></section>
{anim}<section aria-labelledby="inside"><h2 id="inside">A look inside</h2>
<ul class="strip">{samples}</ul></section>
<section aria-labelledby="facts"><h2 id="facts">Details</h2>
<dl class="facts spec"><div><dt>Designs</dt><dd>{b["n"]}</dd></div><div><dt>Page size</dt><dd>8.5 &times; 11 in</dd></div><div><dt>Print</dt><dd>One side only</dd></div><div><dt>Paper</dt><dd>Blank page behind each design</dd></div>{extra}</dl></section>
<p class="endcta"><a class="btn" href="{url}" rel="noopener sponsored">Buy on Amazon</a></p>
</main>
<div class="wrap"><footer>&copy; 2026 Cayus Books. All rights reserved. Illustrations are created with the help of AI tools and reviewed by the author.</footer></div></body></html>'''
    os.makedirs(f"livros/{b['slug']}", exist_ok=True)
    open(f"livros/{b['slug']}/index.html","w").write(html)
    print("ok", b["slug"])
