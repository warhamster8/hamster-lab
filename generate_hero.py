"""Generate FocusDeck website assets — grid background + real app screenshot."""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = os.path.dirname(os.path.abspath(__file__))
ICON_SRC = os.path.join(
    os.path.dirname(ROOT), "focus_deck", "focusdeck", "ui", "theme", "icon.png"
)
ICON_LOCAL = os.path.join(ROOT, "focusdeck", "assets", "logo.png")
SCREENSHOT_PATH = os.path.join(ROOT, "focusdeck", "assets", "screenshot.png")
HERO_PATH = os.path.join(ROOT, "focusdeck", "assets", "hero.png")
CARD_PATH = os.path.join(ROOT, "assets", "FocusDeck_Logo.png")
COVER_PATH = os.path.join(ROOT, "focusdeck", "assets", "github-cover.png")

PURPLE = (138, 43, 226)
ORANGE = (255, 140, 0)
AMBER = (232, 168, 73)
WARM_WHITE = (245, 240, 232)
WARM_GREY = (168, 159, 146)
MUTED = (107, 99, 88)


def _font(size, bold=False, mono=False):
    if mono:
        candidates = [
            "C:/Windows/Fonts/consola.ttf",
            "C:/Windows/Fonts/Consolas.ttf",
        ]
    elif bold:
        candidates = [
            "C:/Windows/Fonts/segoeuib.ttf",
            "C:/Windows/Fonts/Segoe UI Bold.ttf",
        ]
    else:
        candidates = [
            "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/Segoe UI.ttf",
        ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _grid_background(width: int, height: int) -> Image.Image:
    """Purple-orange gradient panel with white grid lines."""
    img = Image.new("RGBA", (width, height), (13, 10, 20, 255))
    draw = ImageDraw.Draw(img)

    for y in range(height):
        alpha = int(55 * (y / max(height - 1, 1)))
        draw.line([(0, y), (width, y)], fill=PURPLE + (alpha,))

    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([-int(width * 0.15), -int(height * 0.2), int(width * 0.55), int(height * 0.65)], fill=ORANGE + (55,))
    gd.ellipse([int(width * 0.45), int(height * 0.35), int(width * 1.15), int(height * 1.05)], fill=PURPLE + (45,))
    gd.ellipse([int(width * 0.2), int(height * 0.1), int(width * 0.85), int(height * 0.75)], fill=AMBER + (18,))
    img = Image.alpha_composite(img, glow.filter(ImageFilter.GaussianBlur(28)))

    draw = ImageDraw.Draw(img)
    step = 24
    for x in range(0, width, step):
        draw.line([(x, 0), (x, height)], fill=(255, 255, 255, 38), width=1)
    for y in range(0, height, step):
        draw.line([(0, y), (width, y)], fill=(255, 255, 255, 38), width=1)

    draw.rectangle([0, 0, width - 1, height - 1], outline=(255, 255, 255, 28), width=1)
    draw.rectangle([0, 0, width - 1, 2], fill=PURPLE + (210,))
    return img


def _rounded(img: Image.Image, radius: int) -> Image.Image:
    img = img.convert("RGBA")
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, img.width, img.height], radius=radius, fill=255)
    img.putalpha(mask)
    return img


def _load_screenshot() -> Image.Image | None:
    if not os.path.exists(SCREENSHOT_PATH):
        return None
    return Image.open(SCREENSHOT_PATH).convert("RGB")


def _composite_screenshot(
    canvas: Image.Image,
    screenshot: Image.Image,
    padding: int = 28,
    corner_radius: int = 14,
    shadow_offset: tuple[int, int] = (6, 10),
) -> Image.Image:
    """Place a real app screenshot centered on the grid canvas."""
    avail_w = canvas.width - padding * 2
    avail_h = canvas.height - padding * 2
    scale = min(avail_w / screenshot.width, avail_h / screenshot.height)
    sw = max(1, int(screenshot.width * scale))
    sh = max(1, int(screenshot.height * scale))
    shot = screenshot.resize((sw, sh), Image.Resampling.LANCZOS)
    shot = _rounded(shot, corner_radius)

    x = (canvas.width - sw) // 2
    y = (canvas.height - sh) // 2

    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(shadow)
    sd.rounded_rectangle(
        [x + shadow_offset[0], y + shadow_offset[1], x + sw + shadow_offset[0], y + sh + shadow_offset[1]],
        radius=corner_radius,
        fill=(0, 0, 0, 110),
    )
    canvas = Image.alpha_composite(canvas, shadow.filter(ImageFilter.GaussianBlur(10)))

    canvas.paste(shot, (x, y), shot)
    return canvas


def generate_hero():
    """FocusDeck landing page hero — grid + real screenshot."""
    W, H = 620, 500
    img = _grid_background(W, H)
    shot = _load_screenshot()
    if shot:
        img = _composite_screenshot(img, shot, padding=32, corner_radius=16)
    img.convert("RGB").save(HERO_PATH, "PNG", optimize=True)
    print(f"[OK] Hero: {HERO_PATH}")


def generate_card():
    """Hamster Lab software card visual — grid + real screenshot."""
    W, H = 380, 260
    img = _grid_background(W, H)
    shot = _load_screenshot()
    if shot:
        img = _composite_screenshot(img, shot, padding=18, corner_radius=12, shadow_offset=(4, 7))
    img.convert("RGB").save(CARD_PATH, "PNG", optimize=True)
    print(f"[OK] Card: {CARD_PATH}")


def generate_github_cover():
    """Wide cover for GitHub social preview / README banner."""
    W, H = 1280, 640
    img = _grid_background(W, H)
    draw = ImageDraw.Draw(img)

    draw.text((72, 100), "FocusDeck", font=_font(72, bold=True), fill=WARM_WHITE + (255,))
    draw.text((72, 188), "Batch convert. Zero cloud.", font=_font(28), fill=AMBER + (255,))

    features = [
        "Native Drag & Drop — RAW, JPEG, PNG",
        "WebP / JPEG export with EXIF preserved",
        "Smart rename · Social presets · Offline",
    ]
    y = 270
    for text in features:
        draw.text((72, y), "◇", font=_font(20), fill=AMBER + (255,))
        draw.text((100, y), text, font=_font(20), fill=WARM_GREY + (255,))
        y += 44

    draw.text(
        (72, H - 60),
        "Windows portable  ·  Fully offline  ·  Free",
        font=_font(16),
        fill=MUTED + (255,),
    )

    shot = _load_screenshot()
    if shot:
        panel = Image.new("RGBA", (520, 560), (0, 0, 0, 0))
        panel = _composite_screenshot(panel, shot, padding=24, corner_radius=16)
        img.paste(panel, (W - 560, (H - 560) // 2), panel)

    img.convert("RGB").save(COVER_PATH, "PNG", optimize=True)
    print(f"[OK] GitHub cover: {COVER_PATH}")


def sync_logo():
    src = ICON_SRC if os.path.exists(ICON_SRC) else ICON_LOCAL
    if os.path.exists(src):
        icon = Image.open(src).convert("RGBA")
        icon.save(ICON_LOCAL, "PNG", optimize=True)
        print(f"[OK] Logo synced: {ICON_LOCAL}")


if __name__ == "__main__":
    if not os.path.exists(SCREENSHOT_PATH):
        print("[WARN] No screenshot found — run capture_screenshot.py first")
    sync_logo()
    generate_hero()
    generate_card()
    generate_github_cover()
