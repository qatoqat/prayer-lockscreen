"""IP-based geolocation for auto-detecting user coordinates."""

import json
import urllib.request
from dataclasses import dataclass


@dataclass
class Location:
    lat: float
    lon: float
    timezone: str
    city: str = ""
    region: str = ""
    country: str = ""


def detect_location() -> Location | None:
    """Detect location from IP. Returns None on failure."""
    apis = [
        (
            "https://ipinfo.io/json",
            lambda d: Location(
                lat=float(d["loc"].split(",")[0]),
                lon=float(d["loc"].split(",")[1]),
                timezone=d.get("timezone", "UTC"),
                city=d.get("city", ""),
                region=d.get("region", ""),
                country=d.get("country", ""),
            ),
        ),
        (
            "https://ipapi.co/json/",
            lambda d: Location(
                lat=float(d["latitude"]),
                lon=float(d["longitude"]),
                timezone=d.get("timezone", "UTC"),
                city=d.get("city", ""),
                region=d.get("region", ""),
                country=d.get("country_name", ""),
            ),
        ),
        (
            "https://ip-api.com/json/?fields=status,country,regionName,city,timezone,lat,lon",
            lambda d: Location(
                lat=float(d["lat"]),
                lon=float(d["lon"]),
                timezone=d.get("timezone", "UTC"),
                city=d.get("city", ""),
                region=d.get("regionName", ""),
                country=d.get("country", ""),
            ),
        ),
    ]

    for url, parser in apis:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "prayer-lockscreen/0.1"})
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode())
                loc = parser(data)
                if loc.lat and loc.lon:
                    return loc
        except Exception:
            continue

    return None
