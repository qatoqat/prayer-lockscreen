"""KDE settings dialog for prayer-lockscreen."""

import json
import subprocess
import sys
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "prayer-lockscreen"

# Malaysia timezones
MALAYSIA_TIMEZONES = [
    ("Asia/Kuala_Lumpur", "Peninsular Malaysia (UTC+8)"),
    ("Asia/Kuching", "Sabah & Sarawak (UTC+8)"),
]

# All available timezones grouped by region
TIMEZONE_GROUPS = {
    "Malaysia": MALAYSIA_TIMEZONES,
    "Other": [
        ("Asia/Jakarta", "Western Indonesia (UTC+7)"),
        ("Asia/Makassar", "Central Indonesia (UTC+8)"),
        ("Asia/Jayapura", "Eastern Indonesia (UTC+9)"),
        ("Asia/Brunei", "Brunei (UTC+8)"),
        ("Asia/Singapore", "Singapore (UTC+8)"),
        ("Asia/Kolkata", "India (UTC+5:30)"),
        ("Asia/Dubai", "UAE (UTC+4)"),
        ("Asia/Riyadh", "Saudi Arabia (UTC+3)"),
        ("Europe/London", "UK (UTC+0/+1)"),
        ("Europe/Paris", "Central Europe (UTC+1/+2)"),
        ("America/New_York", "US Eastern (UTC-5/-4)"),
        ("America/Los_Angeles", "US Pacific (UTC-8/-7)"),
    ],
}


def _kdialog(*args: str) -> str | None:
    """Run kdialog and return stdout, or None on cancel/error."""
    try:
        result = subprocess.run(
            ["kdialog", *args],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return None
        return result.stdout.strip()
    except FileNotFoundError:
        print("Error: kdialog not found. Install plasma-desktop.", file=sys.stderr)
        return None


def _load_config() -> dict:
    config_path = CONFIG_DIR / "config.json"
    if not config_path.exists():
        return {}
    with open(config_path) as f:
        return json.load(f)


def _save_config(config: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_DIR / "config.json", "w") as f:
        json.dump(config, f, indent=4)


def _is_malaysia(lat: float | None, lon: float | None) -> bool:
    if lat is None or lon is None:
        return False
    return 0.8 <= lat <= 7.4 and 99.6 <= lon <= 119.3


def cmd_settings() -> None:
    """Open KDE settings dialog for prayer-lockscreen."""
    config = _load_config()
    if not config:
        print("No config found. Run: prayer-lockscreen init", file=sys.stderr)
        sys.exit(1)

    # ── Step 1: Location settings ──
    current_method = config.get("method", "ISNA")
    methods = ["ISNA", "MWL", "Egypt", "Karachi", "Gulf", "JAKIM"]
    method_labels = " ".join(f"{m}{'*' if m == current_method else ''}" for m in methods)

    method = _kdialog(
        "--combobox",
        "--title", "Prayer Calculation Method",
        "--geometry", "400x300",
        method_labels,
    )
    if method is None:
        return
    config["method"] = method.strip().rstrip("*").strip()

    # ── Step 2: Timezone (if Malaysia) ──
    lat = config.get("latitude")
    lng = config.get("longitude")
    current_tz = config.get("timezone", "Asia/Kuala_Lumpur")

    if _is_malaysia(lat, lng):
        # Find current tz in list for default selection
        tz_items = []
        default_idx = 0
        for i, (tz_val, tz_label) in enumerate(MALAYSIA_TIMEZONES):
            tz_items.append(f"{tz_label}")
            if tz_val == current_tz:
                default_idx = i

        tz_idx = _kdialog(
            "--menu",
            "--title", "Malaysia Timezone",
            "--geometry", "400x200",
            "Select timezone for prayer times:",
            *sum(([str(i), label] for i, label in enumerate(tz_items)), []),
        )
        if tz_idx is not None:
            idx = int(tz_idx)
            config["timezone"] = MALAYSIA_TIMEZONES[idx][0]

    # ── Step 3: Display settings ──
    use_24h = config.get("use_24h", False)
    result = _kdialog(
        "--checklist",
        "--title", "Display Settings",
        "--geometry", "400x200",
        "Select display options:",
        "use_24h", "Use 24-hour format", "on" if use_24h else "off",
    )
    if result is not None:
        config["use_24h"] = "use_24h" in result

    # ── Step 4: Font size ──
    current_size = str(config.get("font_size", 24))
    size = _kdialog(
        "--inputbox",
        "--title", "Font Size",
        "--geometry", "400x100",
        "Overlay font size (px):",
        current_size,
    )
    if size is not None:
        try:
            config["font_size"] = int(size)
        except ValueError:
            pass

    # ── Step 5: Wallpaper ──
    current_wp = config.get("source_wallpaper", "")
    wp = _kdialog(
        "--inputbox",
        "--title", "Source Wallpaper",
        "--geometry", "500x100",
        "Path to your wallpaper image:",
        current_wp,
    )
    if wp is not None:
        config["source_wallpaper"] = wp

    # ── Save ──
    _save_config(config)
    _kdialog("--msgbox", "--title", "Settings Saved",
             "Prayer lockscreen settings saved successfully.")


def register_settings_module() -> None:
    """Register as a KDE System Settings module (optional)."""
    kde_dir = Path.home() / ".local" / "share" / "kservices5" / "kcm_prayerlockscreen.desktop"
    kde_dir.parent.mkdir(parents=True, exist_ok=True)

    desktop = f"""[Desktop Entry]
Type=Service
ServiceTypes=KCModule
X-KDE-Library=kcm_prayerlockscreen
Icon=prayer-lockscreen
Name=Prayer Lock Screen
Comment=Configure prayer times overlay for lock screen
"""
    kde_dir.write_text(desktop)
