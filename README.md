# Prayer Times Lock Screen

Overlay Islamic prayer times on your KDE Plasma lock screen wallpaper.

## Features

- Calculates prayer times using astronomical formulas (offline, no API)
- Auto-detects location via IP geolocation (or manual coordinates)
- Overlays times on your wallpaper with a semi-transparent panel
- Highlights the next upcoming prayer with countdown
- Supports multiple calculation methods (ISNA, MWL, Egypt, Karachi, etc.)
- Systemd timer for automatic daily updates

## Install

### Arch Linux (AUR)

```sh
paru -S prayer-lockscreen
```

### Manual

```sh
pip install .
```

### From source

```sh
git clone https://github.com/q4t/prayer-lockscreen.git
cd prayer-lockscreen
pip install -e .
```

## Usage

```sh
prayer-lockscreen init     # create default config
prayer-lockscreen run      # generate overlay + set lock screen
prayer-lockscreen show     # print times (no wallpaper change)
prayer-lockscreen timer    # enable systemd timer
prayer-lockscreen timer --disable
```

## Configuration

Edit `~/.config/prayer-lockscreen/config.json`:

```json
{
    "detect_location": true,
    "latitude": null,
    "longitude": null,
    "timezone": null,
    "city": "Your Location",
    "method": "ISNA",
    "source_wallpaper": "/path/to/wallpaper.jpg",
    "overlay_position": "bottom-right",
    "overlay_style": "modern",
    "font_size": 24,
    "use_24h": false,
    "highlight_next_prayer": true
}
```

### Options

| Option | Values | Description |
|--------|--------|-------------|
| `detect_location` | `true`/`false` | Auto-detect coordinates from IP |
| `latitude`, `longitude` | float | Manual coordinates |
| `timezone` | IANA tz | e.g. `Asia/Kuala_Lumpur` |
| `method` | `ISNA`, `MWL`, `Egypt`, `Karachi`, `Tehran`, `Jafari`, `Gulf`, `Kuwait`, `Qatar` | Calculation method |
| `source_wallpaper` | path | Base wallpaper image |
| `overlay_position` | `top-left`, `top-right`, `bottom-left`, `bottom-right`, `center` | Panel position |
| `overlay_style` | `modern`, `minimal`, `classic` | Panel style |
| `font_size` | int | Base font size |
| `use_24h` | `true`/`false` | 24-hour format |
| `highlight_next_prayer` | `true`/`false` | Highlight upcoming prayer |

## Requirements

- Python 3.10+
- python-pillow
- KDE Plasma 5 or 6 (for `kwriteconfig5`/`kwriteconfig6`)

## Project layout

| Path | Description |
|------|-------------|
| `prayer_lockscreen/` | Python package |
| `prayer.py` | Prayer time calculation |
| `geolocate.py` | IP geolocation |
| `overlay.py` | PIL wallpaper overlay |
| `kde.py` | KDE settings integration |
| `__main__.py` | CLI entry point |
| `arch/` | Arch Linux packaging (PKGBUILD, systemd) |
| `config/` | Default config |

## License

MIT
