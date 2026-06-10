"""Capture a real FocusDeck window screenshot for website assets."""
import ctypes
import os
import sys
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
FOCUS_DECK_ROOT = os.path.join(os.path.dirname(ROOT), "focus_deck")
OUTPUT = os.path.join(ROOT, "focusdeck", "assets", "screenshot.png")

if FOCUS_DECK_ROOT not in sys.path:
    sys.path.insert(0, FOCUS_DECK_ROOT)

from PIL import ImageGrab  # noqa: E402
from focusdeck.ui.app import FocusDeckApp  # noqa: E402


def _bring_to_front(app) -> None:
    hwnd = ctypes.windll.user32.GetParent(app.winfo_id()) or app.winfo_id()
    ctypes.windll.user32.ShowWindow(hwnd, 9)
    ctypes.windll.user32.SetForegroundWindow(hwnd)
    app.state("normal")
    app.attributes("-topmost", True)
    app.update_idletasks()
    app.update()
    time.sleep(0.3)
    app.attributes("-topmost", False)
    app.focus_force()
    app.update()


def capture(path: str = OUTPUT) -> str:
    app = FocusDeckApp()
    app.geometry("820x780+120+40")
    app.update_idletasks()
    app.update()
    _bring_to_front(app)
    time.sleep(0.5)

    x = app.winfo_rootx()
    y = app.winfo_rooty()
    w = app.winfo_width()
    h = app.winfo_height()
    shot = ImageGrab.grab(bbox=(x, y, x + w, y + h))

    # Trim accidental desktop/taskbar bleed at the bottom edge.
    pixels = shot.load()
    bottom = h - 1
    for row in range(h - 1, max(h - 80, 0), -1):
        sample = [pixels[col, row] for col in range(0, w, max(1, w // 12))]
        if all(sum(px) > 120 for px in sample):
            bottom = row - 1
            break
    if bottom < h - 4:
        shot = shot.crop((0, 0, w, bottom))

    os.makedirs(os.path.dirname(path), exist_ok=True)
    shot.save(path, "PNG", optimize=True)
    print(f"[OK] Screenshot: {path} ({shot.width}x{shot.height})")

    app.destroy()
    return path


if __name__ == "__main__":
    capture()
