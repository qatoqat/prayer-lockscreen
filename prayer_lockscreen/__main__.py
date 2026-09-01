#!/usr/bin/env python3
"""CLI entry point for prayer-lockscreen."""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

from .geolocate import detect_location
from .kde import set_lockscreen_wallpaper
from .overlay import draw_overlay
from .prayer import PRAYER_NAMES, PRAYER_ORDER, calc_prayer_times, format_time

CONFIG_DIR = Path.home() / ".config" / "prayer-lockscreen"
CACHE_DIR = Path.home() / ".cache" / "prayer-lockscreen"


def load_config() -> dict:
    config_path = CONFIG_DIR / "config.json"
    if not config_path.exists():
        print(f"Error: Config not found at {config_path}", file=sys.stderr)
        print("Run with --init to create a default config.", file=sys.stderr)
        sys.exit(1)
    with open(config_path) as f:
        return json.load(f)


def save_config(config: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_DIR / "config.json", "w") as f:
        json.dump(config, f, indent=4)
    print(f"Config saved to {CONFIG_DIR / 'config.json'}")


def cmd_init(args: argparse.Namespace) -> None:
    """Create a default config file."""
    default = {
        "detect_location": True,
        "latitude": None,
        "longitude": None,
        "timezone": None,
        "city": "Your Location",
        "method": "ISNA",
        "source_wallpaper": "",
        "overlay_position": "bottom-right",
        "overlay_style": "modern",
        "font_size": 24,
        "use_24h": False,
        "highlight_next_prayer": True,
    }
    save_config(default)
    print("\nEdit the config to set source_wallpaper, then run: prayer-lockscreen")


def cmd_run(args: argparse.Namespace) -> None:
    """Calculate prayer times, overlay on wallpaper, set as lock screen."""
    config = load_config()

    detect = config.get("detect_location", False)
    lat = config.get("latitude")
    lng = config.get("longitude")
    method = config.get("method", "ISNA")
    timezone_str = config.get("timezone")
    source_wallpaper = config.get("source_wallpaper", "")
    city = config.get("city", "")

    geo = None
    if detect or lat is None or lng is None:
        print("Detecting location from IP...")
        geo = detect_location()
        if geo:
            lat = lat or geo.lat
            lng = lng or geo.lon
            timezone_str = timezone_str or geo.timezone
            if not city or city == "Your Location":
                parts = [p for p in [geo.city, geo.region, geo.country] if p]
                city = ", ".join(parts) if parts else "Your Location"
            print(f"  Detected: {city} ({lat:.4f}, {lng:.4f})")
        elif lat is None or lng is None:
            print("Error: Could not detect location and no coordinates in config.", file=sys.stderr)
            sys.exit(1)

    if not source_wallpaper:
        print("Error: source_wallpaper not set in config.", file=sys.stderr)
        sys.exit(1)

    source_wallpaper = os.path.expanduser(source_wallpaper)
    if not os.path.exists(source_wallpaper):
        print(f"Error: Wallpaper not found: {source_wallpaper}", file=sys.stderr)
        sys.exit(1)

    today = datetime.now()
    prayer_times = calc_prayer_times(today, lat, lng, method, timezone_str or "UTC")

    config["city"] = city
    print(f"Prayer times for {today.strftime('%Y-%m-%d')} ({city}):")
    for name in PRAYER_ORDER:
        if name in prayer_times:
            print(f"  {PRAYER_NAMES[name]:>10}: {format_time(prayer_times[name], config.get('use_24h', False))}")

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    output_path = str(CACHE_DIR / "prayer-wallpaper.png")

    print("\nGenerating overlay...")
    draw_overlay(source_wallpaper, prayer_times, config, output_path)
    print(f"  Saved: {output_path}")

    print("Setting lock screen wallpaper...")
    set_lockscreen_wallpaper(output_path)

    print("\nDone!")


def cmd_show(args: argparse.Namespace) -> None:
    """Print today's prayer times without modifying the wallpaper."""
    config = load_config()

    lat = config.get("latitude")
    lng = config.get("longitude")
    method = config.get("method", "ISNA")
    timezone_str = config.get("timezone")
    city = config.get("city", "")

    if config.get("detect_location", False) or lat is None:
        geo = detect_location()
        if geo:
            lat = lat or geo.lat
            lng = lng or geo.lon
            timezone_str = timezone_str or geo.timezone
            if not city or city == "Your Location":
                parts = [p for p in [geo.city, geo.region, geo.country] if p]
                city = ", ".join(parts) if parts else "Your Location"

    today = datetime.now()
    prayer_times = calc_prayer_times(today, lat, lng, method, timezone_str or "UTC")

    print(f"Prayer times for {today.strftime('%Y-%m-%d')} ({city}):")
    for name in PRAYER_ORDER:
        if name in prayer_times:
            print(f"  {PRAYER_NAMES[name]:>10}: {format_time(prayer_times[name], config.get('use_24h', False))}")


def cmd_timer(args: argparse.Namespace) -> None:
    """Enable or disable the systemd user timer."""
    from .kde import disable_systemd_timer, enable_systemd_timer

    if args.disable:
        if disable_systemd_timer():
            print("Timer disabled.")
        else:
            print("Failed to disable timer.", file=sys.stderr)
    else:
        if enable_systemd_timer():
            print("Timer enabled (runs daily).")
        else:
            print("Failed to enable timer.", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="prayer-lockscreen",
        description="Overlay prayer times on your KDE Plasma lock screen wallpaper.",
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("init", help="Create default config file")
    sub.add_parser("run", help="Generate overlay and set lock screen wallpaper")
    sub.add_parser("show", help="Print prayer times (no wallpaper change)")

    p_timer = sub.add_parser("timer", help="Manage systemd user timer")
    p_timer.add_argument("--disable", action="store_true", help="Disable the timer")

    args = parser.parse_args()

    commands = {
        "init": cmd_init,
        "run": cmd_run,
        "show": cmd_show,
        "timer": cmd_timer,
    }

    if args.command in commands:
        commands[args.command](args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
