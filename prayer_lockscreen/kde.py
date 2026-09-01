"""KDE Plasma lock screen and system settings integration."""

import subprocess
import sys


def find_kwriteconfig() -> str | None:
    """Find the correct kwriteconfig binary (Plasma 6优先, then 5)."""
    for cmd in ("kwriteconfig6", "kwriteconfig5"):
        try:
            subprocess.run([cmd, "--help"], capture_output=True, check=True)
            return cmd
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    return None


def set_lockscreen_wallpaper(image_path: str) -> bool:
    """Set the KDE lock screen wallpaper via kwriteconfig."""
    kwc = find_kwriteconfig()
    if kwc is None:
        print("  Warning: kwriteconfig not found, skipping lock screen update", file=sys.stderr)
        return False

    file_url = f"file://{image_path}"
    try:
        # Set the wallpaper image
        subprocess.run(
            [
                kwc,
                "--file", "kscreenlockerrc",
                "--group", "Greeter",
                "--group", "Wallpaper",
                "--group", "org.kde.image",
                "--group", "General",
                "--key", "Image",
                file_url,
            ],
            check=True,
            capture_output=True,
        )
        # Set the wallpaper plugin
        subprocess.run(
            [
                kwc,
                "--file", "kscreenlockerrc",
                "--group", "Greeter",
                "--group", "Wallpaper",
                "--key", "WallpaperPlugin",
                "--type", "string",
                "org.kde.image",
            ],
            check=True,
            capture_output=True,
        )
        print(f"  Lock screen wallpaper set: {file_url}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"  Warning: kwriteconfig failed: {e}", file=sys.stderr)
        return False


def get_lockscreen_wallpaper() -> str | None:
    """Read the current lock screen wallpaper path."""
    kwc = find_kwriteconfig()
    if kwc is None:
        return None

    try:
        result = subprocess.run(
            [
                kwc,
                "--file", "kscreenlockerrc",
                "--group", "Greeter",
                "--group", "Wallpaper",
                "--group", "org.kde.image",
                "--group", "General",
                "--key", "Image",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        path = result.stdout.strip()
        if path.startswith("file://"):
            path = path[7:]
        return path or None
    except subprocess.CalledProcessError:
        return None


def enable_systemd_timer() -> bool:
    """Enable the prayer-lockscreen systemd user timer."""
    cmds = [
        ["systemctl", "--user", "daemon-reload"],
        ["systemctl", "--user", "enable", "prayer-lockscreen.timer"],
        ["systemctl", "--user", "start", "prayer-lockscreen.timer"],
    ]
    for cmd in cmds:
        try:
            subprocess.run(cmd, capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    return True


def disable_systemd_timer() -> bool:
    """Disable the prayer-lockscreen systemd user timer."""
    for cmd in (
        ["systemctl", "--user", "stop", "prayer-lockscreen.timer"],
        ["systemctl", "--user", "disable", "prayer-lockscreen.timer"],
    ):
        try:
            subprocess.run(cmd, capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    return True
