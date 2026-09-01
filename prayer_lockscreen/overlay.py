"""Draw prayer times overlay on a wallpaper image."""

import os
from datetime import datetime
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .prayer import PRAYER_NAMES, PRAYER_ORDER, format_time, next_prayer


_FONT_CACHE: dict[tuple[int, bool], ImageFont.FreeTypeFont] = {}

_FONT_PATHS = [
    "/usr/share/fonts/noto-sans/NotoSans-{variant}.ttf",
    "/usr/share/fonts/noto/NotoSans-{variant}.ttf",
    "/usr/share/fonts/TTF/DejaVuSans{variant}.ttf",
    "/usr/share/fonts/dejavu-sans-fonts/DejaVuSans{variant}.ttf",
]


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

    font_size = config.get("font_size", 24)
    title_font = _get_font(font_size + 8, bold=True)
    prayer_font = _get_font(font_size, bold=False)
    bold_font = _get_font(font_size, bold=True)
    small_font = _get_font(font_size - 4, bold=False)

    now = datetime.now()
    now_minutes = now.hour * 60 + now.minute
    upcoming = next_prayer(prayer_times, now_minutes)

    style = config.get("overlay_style", "modern")
    padding = 30
    line_height = font_size + 12

    use_24h = config.get("use_24h", False)
    city = config.get("city", "")
    date_str = now.strftime("%A, %B %d")

    # Measure text widths to determine box size
    title_text = "\u262a Prayer Times"
    subtitle_text = f"{date_str} \u2022 {city}"

    title_w = draw.textlength(title_text, font=title_font)
    subtitle_w = draw.textlength(subtitle_text, font=small_font)

    # Measure prayer row widths (name + time)
    max_prayer_row_w = 0
    for name in PRAYER_ORDER:
        if name not in prayer_times:
            continue
        time_str = format_time(prayer_times[name], use_24h)
        name_w = draw.textlength(PRAYER_NAMES[name], font=prayer_font)
        time_w = draw.textlength(time_str, font=prayer_font)
        # Account for bold font on next prayer
        if name == upcoming and config.get("highlight_next_prayer", True):
            name_w = draw.textlength(PRAYER_NAMES[name], font=bold_font)
        row_w = name_w + 24 + time_w  # 24 for indicator gap
        max_prayer_row_w = max(max_prayer_row_w, row_w)

    countdown_text = ""
    if upcoming in prayer_times:
        remaining = prayer_times[upcoming] - now_minutes
        if remaining < 0:
            remaining += 1440
        hrs, mins = int(remaining // 60), int(remaining % 60)
        countdown_text = f"Next: {PRAYER_NAMES[upcoming]} in {hrs}h {mins}m"
    countdown_w = draw.textlength(countdown_text, font=small_font) if countdown_text else 0

    content_w = max(title_w, subtitle_w, max_prayer_row_w, countdown_w)
    box_width = int(content_w + padding * 2 + 16)  # extra margin
    box_width = max(box_width, 300)  # minimum width
    box_width = min(box_width, w - padding * 2)  # don't exceed screen

    num_prayers = sum(1 for name in PRAYER_ORDER if name in prayer_times)
    box_height = padding * 2 + line_height * (num_prayers + 2)  # title + subtitle + prayers

    position = config.get("overlay_position", "bottom-right")
    if position == "bottom-right":
        x, y = w - box_width - padding, h - box_height - padding
    elif position == "bottom-left":
        x, y = padding, h - box_height - padding
    elif position == "top-right":
        x, y = w - box_width - padding, padding
    elif position == "top-left":
        x, y = padding, padding
    else:
        x, y = (w - box_width) // 2, (h - box_height) // 2

    # Clamp to screen bounds
    x = max(0, min(x, w - box_width))
    y = max(0, min(y, h - box_height))

    if style == "modern":
        draw.rounded_rectangle([x, y, x + box_width, y + box_height], radius=20, fill=(0, 0, 0, 160))
    elif style == "minimal":
        draw.rectangle([x, y, x + box_width, y + box_height], fill=(0, 0, 0, 120))
    else:
        draw.rectangle([x, y, x + box_width, y + box_height], fill=(0, 0, 0, 200))

    # Clip region for text
    clip = (x + padding, y, x + box_width - padding, y + box_height)

    draw.text((x + padding, y + padding), title_text, fill=(255, 255, 255, 255), font=title_font)
    draw.text(
        (x + padding, y + padding + line_height + 8),
        subtitle_text,
        fill=(200, 200, 200, 255),
        font=small_font,
    )

    start_y = y + padding + line_height + 30

    for i, name in enumerate(PRAYER_ORDER):
        if name not in prayer_times:
            continue

        py = start_y + i * line_height
        time_str = format_time(prayer_times[name], use_24h)
        is_next = (name == upcoming) and config.get("highlight_next_prayer", True)

        if is_next:
            accent = (100, 200, 255, 255)
            draw.text((x + padding, py), "\u25b6", fill=accent, font=prayer_font, clip=clip)
            draw.text(
                (x + padding + 24, py),
                PRAYER_NAMES[name],
                fill=(255, 255, 255, 255),
                font=bold_font,
                clip=clip,
            )
            time_x = x + box_width - padding - draw.textlength(time_str, font=prayer_font)
            draw.text((time_x, py), time_str, fill=accent, font=prayer_font, clip=clip)
        else:
            draw.text((x + padding, py), PRAYER_NAMES[name], fill=(200, 200, 200, 255), font=prayer_font, clip=clip)
            time_x = x + box_width - padding - draw.textlength(time_str, font=prayer_font)
            draw.text((time_x, py), time_str, fill=(255, 255, 255, 255), font=prayer_font, clip=clip)

    if countdown_text:
        draw.text(
            (x + padding, start_y + num_prayers * line_height + 8),
            countdown_text,
            fill=(100, 200, 255, 255),
            font=small_font,
            clip=clip,
        )

    result = Image.alpha_composite(img, overlay)
    if output_path.endswith((".jpg", ".jpeg")):
        result = result.convert("RGB")
    result.save(output_path, quality=95)
    return output_path
