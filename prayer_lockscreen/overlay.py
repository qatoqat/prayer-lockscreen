"""Draw prayer times overlay on a wallpaper image."""

import os
from datetime import datetime

from PIL import Image, ImageDraw, ImageFont

from .prayer import PRAYER_NAMES, PRAYER_ORDER, format_time, next_prayer


_FONT_CACHE: dict[tuple[int, bool], ImageFont.FreeTypeFont] = {}

_FONT_PATHS = [
    "/usr/share/fonts/noto-sans/NotoSans-{variant}.ttf",
    "/usr/share/fonts/noto/NotoSans-{variant}.ttf",
    "/usr/share/fonts/TTF/DejaVuSans{variant}.ttf",
    "/usr/share/fonts/dejavu-sans-fonts/DejaVuSans{variant}.ttf",
]

# Colors
WHITE = (255, 255, 255, 255)
GRAY = (180, 180, 180, 255)
ACCENT = (100, 200, 255, 255)
BG = (0, 0, 0, 180)


def _get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    key = (size, bold)
    if key in _FONT_CACHE:
        return _FONT_CACHE[key]

    variant = "Bold" if bold else "Regular"
    for template in _FONT_PATHS:
        path = template.format(variant=variant)
        if os.path.exists(path):
            font = ImageFont.truetype(path, size)
            _FONT_CACHE[key] = font
            return font

    font = ImageFont.load_default()
    _FONT_CACHE[key] = font
    return font


def draw_overlay(
    source_path: str,
    prayer_times: dict[str, float],
    config: dict,
    output_path: str,
) -> str:
    """Render prayer times onto source_path and save to output_path."""
    img = Image.open(source_path).convert("RGBA")
    w, h = img.size

    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    font_size = config.get("font_size", 32)
    name_font = _get_font(font_size - 4, bold=False)
    time_font = _get_font(font_size + 4, bold=True)
    small_font = _get_font(font_size - 8, bold=False)

    now = datetime.now()
    now_minutes = now.hour * 60 + now.minute
    upcoming = next_prayer(prayer_times, now_minutes)
    use_24h = config.get("use_24h", False)

    # Collect active prayers
    active = [name for name in PRAYER_ORDER if name in prayer_times]
    num = len(active)

    # Measure column widths
    col_gap = 40
    col_widths = []
    for name in active:
        time_str = format_time(prayer_times[name], use_24h)
        nw = draw.textlength(PRAYER_NAMES[name], font=name_font)
        tw = draw.textlength(time_str, font=time_font)
        col_widths.append(max(nw, tw))

    total_w = sum(col_widths) + col_gap * (num - 1)
    padding_x = 40
    padding_y = 24
    box_w = int(total_w + padding_x * 2)
    row_gap = 8
    box_h = int(font_size + 4 + font_size + 8 + padding_y * 2)

    # Center on screen
    x = (w - box_w) // 2
    y = h - box_h - 40  # near bottom

    # Clamp to screen
    x = max(0, min(x, w - box_w))
    y = max(0, min(y, h - box_h))

    # Background
    draw.rounded_rectangle([x, y, x + box_w, y + box_h], radius=16, fill=BG)

    # Draw columns
    cx = x + padding_x
    name_y = y + padding_y
    time_y = name_y + font_size + 4

    for i, name in enumerate(active):
        time_str = format_time(prayer_times[name], use_24h)
        is_next = (name == upcoming) and config.get("highlight_next_prayer", True)

        name_color = ACCENT if is_next else GRAY
        time_color = ACCENT if is_next else WHITE

        # Center text in column
        nw = draw.textlength(PRAYER_NAMES[name], font=name_font)
        tw = draw.textlength(time_str, font=time_font)
        col_w = col_widths[i]

        name_x = cx + (col_w - nw) // 2
        time_x = cx + (col_w - tw) // 2

        draw.text((name_x, name_y), PRAYER_NAMES[name], fill=name_color, font=name_font)
        draw.text((time_x, time_y), time_str, fill=time_color, font=time_font)

        cx += col_w + col_gap

    result = Image.alpha_composite(img, overlay)
    if output_path.endswith((".jpg", ".jpeg")):
        result = result.convert("RGB")
    result.save(output_path, quality=95)
    return output_path
