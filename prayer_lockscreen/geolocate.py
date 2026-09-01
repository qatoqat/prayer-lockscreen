"""IP-based geolocation for auto-detecting user coordinates."""

import json
import urllib.request


def detect_location() -> tuple[float | None, float | None, str | None]:
    """Detect (lat, lon, timezone) from IP. Returns (None, None, None) on failure."""
    apis = [
        ("https://ipapi.co/json/", lambda d: (d["latitude"], d["longitude"], d["timezone"])),
        ("https://ip-api.com/json/", lambda d: (d["lat"], d["lon"], d["timezone"])),
        ("https://ipinfo.io/json", lambda d: (d["loc"].split(",")[0], d["loc"].split(",")[1], d["timezone"])),
    ]

    for url, parser in apis:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "prayer-lockscreen/0.1"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode())
                lat, lon, tz_str = parser(data)
                return float(lat), float(lon), tz_str
        except Exception:
            continue

    return None, None, None
