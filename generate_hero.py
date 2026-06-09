"""Generate clean, modern hero and card images for FocusDeck website."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.abspath(__file__))
ICON_PATH = os.path.join(ROOT, "focusdeck", "assets", "logo.png")
HERO_PATH = os.path.join(ROOT, "focusdeck", "assets", "hero.png")
CARD_PATH = os.path.join(ROOT, "assets", "FocusDeck_Logo.png")

HERO_W, HERO_H = 580, 460


def _font(size, bold=False, mono=False):
    candidates = []
    if mono:
        candidates = [
            "C:/Windows/Fonts/consola.ttf",
            "C:/Windows/Fonts/Consolas.ttf",
            "/System/Library/Fonts/Menlo.ttc",
            "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
        ]
    elif bold:
        candidates = [
            "C:/Windows/Fonts/segoeuib.ttf",
            "C:/Windows/Fonts/Segoe UI Bold.ttf",
            "/System/Library/Fonts/SFNSDisplay-Bold.otf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        ]
    else:
        candidates = [
            "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/Segoe UI.ttf",
            "/System/Library/Fonts/SFNSDisplay-Regular.otf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _rrect(draw, xy, r, fill=None, outline=None, width=1):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=outline, width=width)


def generate_hero():
    """Clean hero: large app icon centered, brand name, tagline, feature rows."""
    img = Image.new("RGBA", (HERO_W, HERO_H), (11, 15, 25, 255))
    draw = ImageDraw.Draw(img)

    # Background glow
    g = Image.new("RGBA", (HERO_W, HERO_H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    gd.ellipse([100, -50, 500, 250], fill=(138, 43, 226, 30))
    gd.ellipse([-20, 200, 250, 500], fill=(0, 240, 255, 12))
    gd.ellipse([350, 250, 650, 550], fill=(232, 168, 73, 10))
    img = Image.alpha_composite(img, g.filter(ImageFilter.GaussianBlur(50)))

    # Subtle grid
    for x in range(0, HERO_W, 30):
        draw.line([(x, 0), (x, HERO_H)], fill=(255, 255, 255, 5), width=1)
    for y in range(0, HERO_H, 30):
        draw.line([(0, y), (HERO_W, y)], fill=(255, 255, 255, 5), width=1)

    # Top accent
    draw.rectangle([0, 0, HERO_W, 2], fill=(138, 43, 226, 255))

    # Large app icon
    if os.path.exists(ICON_PATH):
        icon = Image.open(ICON_PATH).convert("RGBA").resize((140, 140), Image.Resampling.LANCZOS)

        # Glow behind icon
        ig = Image.new("RGBA", (HERO_W, HERO_H), (0, 0, 0, 0))
        igd = ImageDraw.Draw(ig)
        igd.ellipse([185, 40, 395, 250], fill=(138, 43, 226, 35))
        igd.ellipse([210, 65, 370, 225], fill=(0, 240, 255, 12))
        img = Image.alpha_composite(img, ig.filter(ImageFilter.GaussianBlur(30)))

        img.paste(icon, (220, 40), icon)

    # Brand name
    draw.text((HERO_W // 2, 220), "FocusDeck", font=_font(38, bold=True), fill=(255, 255, 255, 255), anchor="mm")

    # Tagline
    draw.text((HERO_W // 2, 268), "Batch Convert. Zero Cloud.", font=_font(18), fill=(0, 240, 255, 255), anchor="mm")

    # Feature badges
    features = [
        ("RAW Support", "RAF · CR2 · NEF · ARW · DNG"),
        ("Web Output", "WebP · JPEG · EXIF Safe"),
        ("Smart Tools", "Batch Rename · Resize Presets"),
    ]
    badge_w = 180
    badge_h = 70
    gap = 12
    total_w = 3 * badge_w + 2 * gap
    sx = (HERO_W - total_w) // 2

    for i, (title, desc) in enumerate(features):
        bx = sx + i * (badge_w + gap)
        by = 310
        _rrect(draw, [bx, by, bx + badge_w, by + badge_h], 12, fill=(18, 24, 38, 255), outline=(36, 49, 76, 180), width=1)

        # Small dot
        draw.ellipse([bx + 12, by + 14, bx + 20, by + 22], fill=(0, 240, 255, 220))

        draw.text((bx + badge_w // 2, by + 28), title, font=_font(12, bold=True), fill=(255, 255, 255, 230), anchor="mm")
        draw.text((bx + badge_w // 2, by + 50), desc, font=_font(8, mono=True), fill=(143, 160, 196, 200), anchor="mm")

    # Bottom accent line
    draw.rectangle([150, HERO_H - 3, HERO_W - 150, HERO_H - 2], fill=(138, 43, 226, 80))

    img = img.convert("RGB")
    img.save(HERO_PATH, "PNG", optimize=True)
    print(f"[OK] Hero: {HERO_PATH}")


def generate_card():
    """Product card for main site: icon + name + tagline on dark gradient."""
    W, H = 380, 260
    img = Image.new("RGBA", (W, H), (13, 10, 20, 255))
    draw = ImageDraw.Draw(img)

    # Dark gradient overlay
    for y in range(H):
        alpha = int(50 * (y / H))
        draw.line([(0, y), (W, y)], fill=(138, 43, 226, alpha))

    # Subtle grid
    for x in range(0, W, 20):
        draw.line([(x, 0), (x, H)], fill=(255, 255, 255, 4), width=1)
    for y in range(0, H, 20):
        draw.line([(0, y), (W, y)], fill=(255, 255, 255, 4), width=1)

    # Glow
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    gd.ellipse([-30, -20, 170, 170], fill=(232, 168, 73, 18))
    gd.ellipse([200, 80, 420, 300], fill=(138, 43, 226, 15))
    img = Image.alpha_composite(img, g.filter(ImageFilter.GaussianBlur(35)))

    # Border
    draw.rectangle([0, 0, W - 1, H - 1], outline=(180, 120, 40, 60), width=1)
    draw.rectangle([0, 0, W - 1, 2], fill=(138, 43, 226, 200))

    # Icon
    if os.path.exists(ICON_PATH):
        icon = Image.open(ICON_PATH).convert("RGBA").resize((130, 130), Image.Resampling.LANCZOS)
        ig = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        igd = ImageDraw.Draw(ig)
        igd.ellipse([95, 5, 285, 195], fill=(138, 43, 226, 18))
        img = Image.alpha_composite(img, ig.filter(ImageFilter.GaussianBlur(20)))
        img.paste(icon, (125, 22), icon)

    # Text
    draw.text((W // 2, 175), "FocusDeck", font=_font(26, bold=True), fill=(245, 240, 232, 240), anchor="mm")
    draw.text((W // 2, 210), "Batch Convert. Zero Cloud.", font=_font(13), fill=(232, 168, 73, 220), anchor="mm")

    # Small chips
    chips = ["RAW", "WebP", "EXIF"]
    cw, ch = 42, 20
    gap = 6
    total = len(chips) * cw + (len(chips) - 1) * gap
    sx = (W - total) // 2
    for i, chip in enumerate(chips):
        cx = sx + i * (cw + gap)
        _rrect(draw, [cx, 224, cx + cw, 224 + ch], 10, fill=(18, 24, 38, 200), outline=(36, 49, 76, 150), width=1)
        draw.text((cx + cw // 2, 224 + ch // 2), chip, font=_font(9, mono=True), fill=(143, 160, 196, 200), anchor="mm")

    img = img.convert("RGB")
    img.save(CARD_PATH, "PNG", optimize=True)
    print(f"[OK] Card: {CARD_PATH}")


if __name__ == "__main__":
    generate_hero()
    generate_card()
