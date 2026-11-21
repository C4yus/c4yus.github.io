# kindle-cover-skill

Claude skill that generates full-wrap paperback cover PDFs for Amazon KDP.

Takes a front cover image and produces a print-ready PDF with front, spine, and back cover — correctly sized for KDP upload.

> Part of the **KDP Publishing Toolkit** — use with [kindle-book-skill](https://github.com/nikmcfly/kindle-book-skill) to go from manuscript to published book entirely inside Claude.

## What it does

- Calculates spine width from page count and paper type
- Places your front cover image with configurable fit (cover/contain)
- Generates back cover with headline, bullet points, tagline
- Applies KDP-compliant bleed (0.125") and safe zones (0.375")
- Outputs a single PDF ready for KDP Paperback upload
- No barcode — Amazon places its own at print time

## Install

```bash
claude install nikmcfly/kindle-cover-skill
```

## Quick start

Just tell Claude:

```
Make a paperback cover for my book. Front image is cover.jpg,
title "Digital Dolls, Real Dollars" by Nik McFly, 333 pages.
Back cover should say it's a 333-page playbook with 28 chapters.
```

Or invoke directly:

```bash
python3 scripts/generate_cover.py \
  --front-image cover.jpg \
  --title "My Book Title" \
  --author "Author Name" \
  --pages 333 \
  --output fullwrap_cover.pdf \
  --back-headline "The book they don't want you to read" \
  --back-bullets "200+ pages of real tactics" "Step-by-step guides" "Case studies" \
  --back-tagline "Based on documented results, not theory."
```

## Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--front-image` | Yes | — | Front cover image (JPG/PNG) |
| `--title` | Yes | — | Book title (appears on spine) |
| `--author` | Yes | — | Author name (appears on spine) |
| `--pages` | Yes | — | Page count (determines spine width) |
| `--output` | Yes | — | Output PDF path |
| `--trim` | No | `6x9` | Trim size: `5x8`, `5.5x8.5`, `6x9`, `8.5x11` |
| `--paper` | No | `white` | Paper type: `white` or `cream` |
| `--front-fit` | No | `cover` | `cover` (crop to fill) or `contain` (fit inside) |
| `--front-padding` | No | `0` | Inches of padding around front image |
| `--back-headline` | No | — | Main headline text (use `\n` for line breaks) |
| `--back-subtitle` | No | — | Subtitle below headline |
| `--back-bullets` | No | — | Bullet point items |
| `--back-cta` | No | — | Bold call-to-action line |
| `--back-tagline` | No | — | Italic closing line |
| `--accent-color` | No | `#e040a0` | Color for accent line and bullets |
| `--bg-color` | No | `#0a0a0a` | Back cover background |
| `--spine-bg` | No | `#111111` | Spine background |

## Example output

![Cover example](example_cover.png)

*Full wrap: back cover + spine + front cover in one PDF*

## KDP specs

| Spec | Value |
|------|-------|
| Bleed | 0.125" all sides |
| Safe zone | 0.375" from trim (text only) |
| Spine | Auto-calculated per page count |
| White paper | 0.002252" per page |
| Cream paper | 0.0025" per page |

## Workflow with kindle-book-skill

These two skills cover the complete KDP publishing pipeline:

```
                    ┌─────────────────────┐
   manuscript.md ──▶│  kindle-book-skill  │──▶ book.epub (Kindle eBook)
                    │                     │──▶ book.pdf  (print interior)
                    └─────────────────────┘
                              │
                         page count
                              │
                              ▼
                    ┌─────────────────────┐
    cover.jpg ────▶│ kindle-cover-skill  │──▶ fullwrap.pdf (KDP cover)
                    └─────────────────────┘
```

1. Use **kindle-book-skill** to convert your markdown manuscript into EPUB + print PDF
2. Note the page count from the PDF output
3. Use **kindle-cover-skill** to generate the full-wrap cover with that page count
4. Upload all three files to KDP

## Dependencies

```bash
pip install reportlab Pillow
```

## License

MIT

## Author

[Nik McFly](https://nikmcfly.com)
