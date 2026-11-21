#!/usr/bin/env python3
"""
KDP Full Wrap Paperback Cover Generator

Generates a single PDF containing back cover + spine + front cover,
sized to Amazon KDP specifications with proper bleed and safe zones.

Usage:
    python generate_cover.py \
        --front-image cover.jpg \
        --title "My Book Title" \
        --author "Author Name" \
        --pages 333 \
        --output cover_fullwrap.pdf
"""

import argparse
import sys
import os

try:
    from reportlab.lib.pagesizes import inch
    from reportlab.pdfgen import canvas
    from reportlab.lib.colors import HexColor, white
except ImportError:
    print("ERROR: reportlab is required. Install with: pip install reportlab --break-system-packages")
    sys.exit(1)

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow is required. Install with: pip install Pillow --break-system-packages")
    sys.exit(1)


# ── Trim sizes ───────────────────────────────────────────────────────────────
TRIM_SIZES = {
    "5x8":     {"w": 5.0,  "h": 8.0},
    "5.5x8.5": {"w": 5.5,  "h": 8.5},
    "6x9":     {"w": 6.0,  "h": 9.0},
    "8.5x11":  {"w": 8.5,  "h": 11.0},
}

# Spine thickness per page (inches)
PAPER_THICKNESS = {
    "white": 0.002252,
    "cream": 0.0025,
}

BLEED = 0.125       # inches, KDP standard
SAFE_ZONE = 0.375   # inches from trim edge, KDP requirement for text


def calculate_dimensions(pages: int, trim: str, paper: str):
    """Calculate all cover dimensions from page count and trim size."""
    t = TRIM_SIZES[trim]
    spine = pages * PAPER_THICKNESS[paper]

    total_w = BLEED + t["w"] + spine + t["w"] + BLEED
    total_h = BLEED + t["h"] + BLEED

    # Panel x-coordinates (from left edge of PDF)
    back_start = BLEED
    back_end = BLEED + t["w"]
    spine_start = back_end
    spine_end = back_end + spine
    front_start = spine_end
    front_end = spine_end + t["w"]

    # Safe zone boundaries for back cover
    safe_left = BLEED + SAFE_ZONE
    safe_right = BLEED + t["w"] - SAFE_ZONE
    safe_top = BLEED + SAFE_ZONE          # top of page in PDF coords (y increases upward)
    safe_bottom = BLEED + t["h"] - SAFE_ZONE

    return {
        "total_w": total_w,
        "total_h": total_h,
        "trim_w": t["w"],
        "trim_h": t["h"],
        "spine": spine,
        "back_start": back_start,
        "back_end": back_end,
        "spine_start": spine_start,
        "spine_end": spine_end,
        "front_start": front_start,
        "front_end": front_end,
        "safe_left": safe_left,
        "safe_right": safe_right,
        "safe_top": safe_top,
        "safe_bottom": safe_bottom,
    }


def draw_front_cover(c, dims, img_path, fit, padding):
    """Draw the front cover with the provided image."""
    img = Image.open(img_path)

    pad = padding * inch
    front_x = dims["front_start"] * inch + pad
    front_area_w = (dims["trim_w"] + BLEED) * inch - 2 * pad
    front_area_h = dims["total_h"] * inch - 2 * pad
    front_y = pad

    if fit == "contain":
        # Fit image inside area without cropping
        img_aspect = img.width / img.height
        area_aspect = front_area_w / front_area_h
        if img_aspect > area_aspect:
            draw_w = front_area_w
            draw_h = draw_w / img_aspect
            draw_x = front_x
            draw_y = front_y + (front_area_h - draw_h) / 2
        else:
            draw_h = front_area_h
            draw_w = draw_h * img_aspect
            draw_x = front_x + (front_area_w - draw_w) / 2
            draw_y = front_y
    else:
        # Cover mode: fill area, crop overflow
        img_aspect = img.width / img.height
        area_aspect = front_area_w / front_area_h
        if img_aspect > area_aspect:
            draw_h = front_area_h
            draw_w = draw_h * img_aspect
            draw_x = front_x - (draw_w - front_area_w) / 2
            draw_y = front_y
        else:
            draw_w = front_area_w
            draw_h = draw_w / img_aspect
            draw_x = front_x
            draw_y = front_y - (draw_h - front_area_h) / 2

    c.drawImage(img_path, draw_x, draw_y, draw_w, draw_h)


def draw_spine(c, dims, title, author, spine_bg):
    """Draw the spine with title and author."""
    sx = dims["spine_start"] * inch
    sw = dims["spine"] * inch

    # Spine background
    c.setFillColor(HexColor(spine_bg))
    c.rect(sx, 0, sw, dims["total_h"] * inch, fill=1, stroke=0)

    # Only add text if spine is wide enough (> 0.5")
    if dims["spine"] < 0.5:
        return

    # Spine text — rotated 90 degrees
    c.saveState()
    c.translate(sx + sw / 2, dims["total_h"] * inch / 2)
    c.rotate(90)
    c.setFillColor(white)

    # Auto-size font based on spine width
    max_font = min(10, dims["spine"] * 72 * 0.6)  # 60% of spine width
    c.setFont("Helvetica-Bold", max_font)

    spine_text = f"{title.upper()}  \u2014  {author.upper()}"
    c.drawCentredString(0, -max_font * 0.35, spine_text)
    c.restoreState()


def draw_back_cover(c, dims, args):
    """Draw the back cover with text content."""
    bg = args.bg_color
    accent = args.accent_color

    # Back cover background
    c.setFillColor(HexColor(bg))
    c.rect(0, 0, dims["back_end"] * inch + 0.01 * inch,
           dims["total_h"] * inch, fill=1, stroke=0)

    # All text coordinates within safe zone
    sl = dims["safe_left"] * inch      # safe left
    sr = dims["safe_right"] * inch     # safe right
    st = dims["safe_bottom"] * inch    # safe top (reportlab y=0 at bottom)
    sb = dims["safe_top"] * inch       # safe bottom
    center_x = (sl + sr) / 2
    usable_w = sr - sl

    # Start from top of safe zone, work downward
    y = st - 0.15 * inch

    # Accent line
    c.setStrokeColor(HexColor(accent))
    c.setLineWidth(3)
    c.line(sl, y, sr, y)
    y -= 0.45 * inch

    # Headline
    if args.back_headline:
        lines = args.back_headline.split("\\n") if "\\n" in args.back_headline else [args.back_headline]
        # Auto-size: try to fit in available width
        font_size = 16
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", font_size)
        for line in lines[:3]:  # max 3 lines
            # Shrink font if line is too wide
            while c.stringWidth(line, "Helvetica-Bold", font_size) > usable_w and font_size > 10:
                font_size -= 0.5
                c.setFont("Helvetica-Bold", font_size)
            c.drawCentredString(center_x, y, line)
            y -= font_size * 1.4
        y -= 8

    # Subtitle
    if args.back_subtitle:
        c.setFont("Helvetica", 10)
        c.setFillColor(HexColor("#cccccc"))
        sub_lines = args.back_subtitle.split("\\n") if "\\n" in args.back_subtitle else [args.back_subtitle]
        for line in sub_lines[:3]:
            c.drawCentredString(center_x, y, line)
            y -= 14
        y -= 10

    # Bullet points
    if args.back_bullets:
        y -= 5
        for bullet in args.back_bullets:
            c.setFillColor(HexColor(accent))
            c.setFont("Helvetica-Bold", 10)
            c.drawString(sl, y, "\u25CF")
            c.setFillColor(white)
            c.setFont("Helvetica", 10)
            c.drawString(sl + 12, y, bullet)
            y -= 17
        y -= 15

    # CTA (bold centered line)
    if args.back_cta:
        cta_lines = args.back_cta.split("\\n") if "\\n" in args.back_cta else [args.back_cta]
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(white)
        for line in cta_lines[:2]:
            c.drawCentredString(center_x, y, line)
            y -= 17
        y -= 8

    # Tagline (italic, muted)
    if args.back_tagline:
        c.setFont("Helvetica-Oblique", 10)
        c.setFillColor(HexColor("#999999"))
        c.drawCentredString(center_x, y, args.back_tagline)

    # No barcode zone — Amazon places its own at print time


def generate_cover(args):
    """Main cover generation function."""
    if args.trim not in TRIM_SIZES:
        print(f"ERROR: Unknown trim size '{args.trim}'. Options: {list(TRIM_SIZES.keys())}")
        sys.exit(1)

    if args.paper not in PAPER_THICKNESS:
        print(f"ERROR: Unknown paper type '{args.paper}'. Options: {list(PAPER_THICKNESS.keys())}")
        sys.exit(1)

    if not os.path.exists(args.front_image):
        print(f"ERROR: Front image not found: {args.front_image}")
        sys.exit(1)

    dims = calculate_dimensions(args.pages, args.trim, args.paper)

    print(f"Cover specs:")
    print(f"  Trim: {args.trim} | Pages: {args.pages} | Paper: {args.paper}")
    print(f"  Spine width: {dims['spine']:.3f}\"")
    print(f"  Total size: {dims['total_w']:.3f}\" x {dims['total_h']:.3f}\"")
    print(f"  Safe zone: {SAFE_ZONE}\" from all trim edges")

    total_w_pt = dims["total_w"] * inch
    total_h_pt = dims["total_h"] * inch

    c = canvas.Canvas(args.output, pagesize=(total_w_pt, total_h_pt))

    # 1. Full background
    c.setFillColor(HexColor(args.bg_color))
    c.rect(0, 0, total_w_pt, total_h_pt, fill=1, stroke=0)

    # 2. Front cover (image)
    draw_front_cover(c, dims, args.front_image, args.front_fit, args.front_padding)

    # 3. Spine
    draw_spine(c, dims, args.title, args.author, args.spine_bg)

    # 4. Back cover (text)
    draw_back_cover(c, dims, args)

    c.save()

    size_kb = os.path.getsize(args.output) / 1024
    print(f"\n  Saved: {args.output} ({size_kb:.0f} KB)")


def main():
    parser = argparse.ArgumentParser(
        description="Generate a KDP full-wrap paperback cover PDF"
    )

    # Required
    parser.add_argument("--front-image", required=True, help="Path to front cover image (JPG/PNG)")
    parser.add_argument("--title", required=True, help="Book title (used on spine)")
    parser.add_argument("--author", required=True, help="Author name (used on spine)")
    parser.add_argument("--pages", required=True, type=int, help="Total page count")
    parser.add_argument("--output", required=True, help="Output PDF path")

    # Optional — dimensions
    parser.add_argument("--trim", default="6x9", choices=list(TRIM_SIZES.keys()), help="Trim size")
    parser.add_argument("--paper", default="white", choices=list(PAPER_THICKNESS.keys()), help="Paper type")

    # Optional — front cover
    parser.add_argument("--front-fit", default="cover", choices=["cover", "contain"],
                        help="How front image fills area: cover (crop) or contain (fit)")
    parser.add_argument("--front-padding", type=float, default=0,
                        help="Padding around front image in inches")

    # Optional — back cover content
    parser.add_argument("--back-headline", help="Main headline (use \\\\n for line breaks)")
    parser.add_argument("--back-subtitle", help="Subtitle text below headline")
    parser.add_argument("--back-bullets", nargs="+", help="Bullet point items")
    parser.add_argument("--back-cta", help="Bold call-to-action line")
    parser.add_argument("--back-tagline", help="Italic tagline at bottom")

    # Optional — colors
    parser.add_argument("--accent-color", default="#e040a0", help="Accent color (hex)")
    parser.add_argument("--bg-color", default="#0a0a0a", help="Back cover background color (hex)")
    parser.add_argument("--spine-bg", default="#111111", help="Spine background color (hex)")

    args = parser.parse_args()
    generate_cover(args)


if __name__ == "__main__":
    main()
