"""Prayer time calculation with API fallback."""

import json
import math
import urllib.request
from datetime import datetime

try:
    import zoneinfo
except ImportError:
    zoneinfo = None

try:
    from dateutil import tz as tz_module
except ImportError:
    tz_module = None


PRAYER_NAMES = {
    "fajr": "Fajr",
    "sunrise": "Sunrise",
    "dhuhr": "Dhuhr",
    "asr": "Asr",
    "maghrib": "Maghrib",
    "isha": "Isha",
}

PRAYER_ORDER = ["fajr", "sunrise", "dhuhr", "asr", "maghrib", "isha"]

# Aladhan API method IDs
ALADHAN_METHODS = {
    "ISNA": 2,
    "MWL": 3,
    "Egypt": 5,
    "Karachi": 1,
    "Tehran": 7,
    "Gulf": 8,
    "Kuwait": 9,
    "Qatar": 10,
    "JAKIM": 17,
}

# Malaysia bounding box (approx)
MALAYSIA_BOUNDS = {
    "lat_min": 0.8,
    "lat_max": 7.4,
    "lon_min": 99.6,
    "lon_max": 119.3,
}


def _is_malaysia(lat: float, lon: float) -> bool:
    """Check if coordinates are in Malaysia."""
    return (
        MALAYSIA_BOUNDS["lat_min"] <= lat <= MALAYSIA_BOUNDS["lat_max"]
        and MALAYSIA_BOUNDS["lon_min"] <= lon <= MALAYSIA_BOUNDS["lon_max"]
    )


def _fetch_aladhan(date: datetime, lat: float, lon: float, method: str) -> dict | None:
    """Fetch prayer times from Aladhan API. Returns dict or None on failure."""
    date_str = date.strftime("%d-%m-%Y")
    method_id = ALADHAN_METHODS.get(method, 3)

    url = f"https://api.aladhan.com/v1/timings/{date_str}?latitude={lat}&longitude={lon}&method={method_id}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "prayer-lockscreen/0.1"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())

        if data.get("code") != 200:
            return None

        timings = data["data"]["timings"]
        return {
            "fajr": _parse_aladhan_time(timings["Fajr"]),
            "sunrise": _parse_aladhan_time(timings["Sunrise"]),
            "dhuhr": _parse_aladhan_time(timings["Dhuhr"]),
            "asr": _parse_aladhan_time(timings["Asr"]),
            "maghrib": _parse_aladhan_time(timings["Maghrib"]),
            "isha": _parse_aladhan_time(timings["Isha"]),
        }
    except Exception:
        return None


def _parse_aladhan_time(time_str: str) -> float:
    """Parse HH:MM time string to minutes from midnight."""
    parts = time_str.split(":")
    h, m = int(parts[0]), int(parts[1])
    return h * 60 + m


def _sun_position(date: datetime) -> tuple[float, float]:
    """Calculate sun declination (radians) and equation of time (minutes)."""
    n = date.timetuple().tm_yday
    gamma = (2 * math.pi / 365) * (n - 1)

    decl = (
        0.006918
        - 0.399912 * math.cos(gamma)
        + 0.070257 * math.sin(gamma)
        - 0.006758 * math.cos(2 * gamma)
        + 0.000907 * math.sin(2 * gamma)
        - 0.002697 * math.cos(3 * gamma)
        + 0.00148 * math.sin(3 * gamma)
    )

    eqtime = 229.18 * (
        0.000075
        + 0.001868 * math.cos(gamma)
        - 0.032077 * math.sin(gamma)
        - 0.014615 * math.cos(2 * gamma)
        - 0.04089 * math.sin(2 * gamma)
    )

    return decl, eqtime


def _hour_angle(decl_rad: float, lat_deg: float, angle_deg: float) -> float | None:
    """Hour angle (degrees) for a given solar altitude. None if no solution."""
    lat_rad = math.radians(lat_deg)
    angle_rad = math.radians(angle_deg)

    cos_ha = (math.sin(angle_rad) - math.sin(lat_rad) * math.sin(decl_rad)) / (
        math.cos(lat_rad) * math.cos(decl_rad)
    )

    if cos_ha < -1 or cos_ha > 1:
        return None

    return math.degrees(math.acos(cos_ha))


def _tz_offset(date: datetime, timezone_str: str) -> float:
    """UTC offset in minutes for the given timezone on the given date."""
    try:
        if zoneinfo is not None:
            tz_obj = zoneinfo.ZoneInfo(timezone_str)
        elif tz_module is not None:
            tz_obj = tz_module.gettz(timezone_str)
        else:
            return 0

        if tz_obj is not None:
            local_dt = date.replace(tzinfo=tz_obj)
            return local_dt.utcoffset().total_seconds() / 60
    except Exception:
        pass
    return 0


def _calc_local(date: datetime, lat: float, lng: float, method: str, timezone_str: str) -> dict[str, float]:
    """Fallback: calculate prayer times using astronomical formulas."""
    decl, eqtime = _sun_position(date)

    utc_noon = 720 + (-4 * lng) - eqtime
    local_noon = utc_noon + _tz_offset(date, timezone_str)

    fajr_angles = {
        "ISNA": 15.0, "MWL": 18.0, "Egypt": 19.5,
        "Karachi": 18.0, "Tehran": 17.7, "Jafari": 16.0,
        "Gulf": 19.5, "Kuwait": 18.0, "Qatar": 18.0, "JAKIM": 20.0,
    }
    isha_angles = {
        "ISNA": 15.0, "MWL": 17.0, "Egypt": 17.5,
        "Karachi": 18.0, "Tehran": 14.0, "Jafari": 14.0,
        "Gulf": 17.5, "Kuwait": 17.5, "Qatar": 18.0, "JAKIM": 18.0,
    }

    fajr_angle = fajr_angles.get(method, 15.0)
    isha_angle = isha_angles.get(method, 15.0)

    times: dict[str, float] = {}

    sunset_ha = _hour_angle(decl, lat, -0.833)
    if sunset_ha is not None:
        times["sunrise"] = local_noon - sunset_ha * 4
        times["maghrib"] = local_noon + sunset_ha * 4

    fajr_ha = _hour_angle(decl, lat, -fajr_angle)
    if fajr_ha is not None:
        times["fajr"] = local_noon - fajr_ha * 4

    times["dhuhr"] = local_noon + 1

    lat_rad = math.radians(lat)
    decl_diff = abs(lat_rad - decl)
    asr_angle_rad = math.atan(1.0 / (1.0 + math.tan(decl_diff)))
    asr_ha = _hour_angle(decl, lat, math.degrees(asr_angle_rad))
    if asr_ha is not None:
        times["asr"] = local_noon + asr_ha * 4

    isha_ha = _hour_angle(decl, lat, -isha_angle)
    if isha_ha is not None:
        times["isha"] = local_noon + isha_ha * 4

    return times


def format_time(minutes: float, use_24h: bool = False) -> str:
    """Format minutes-from-midnight as a readable time string."""
    minutes = round(minutes) % 1440
    h = int(minutes // 60)
    m = int(minutes % 60)
    if use_24h:
        return f"{h:02d}:{m:02d}"
    period = "AM" if h < 12 else "PM"
    h12 = h % 12 or 12
    return f"{h12}:{m:02d} {period}"


def get_prayer_times(
    date: datetime,
    lat: float,
    lon: float,
    method: str = "ISNA",
    timezone_str: str = "UTC",
) -> dict[str, float]:
    """Get prayer times. Tries Aladhan API first, falls back to calculation.

    For Malaysia coordinates, automatically uses JAKIM method.
    """
    # Auto-detect JAKIM for Malaysia
    if _is_malaysia(lat, lon):
        method = "JAKIM"

    # Try API first
    result = _fetch_aladhan(date, lat, lon, method)
    if result is not None:
        return result

    # Fallback to calculation
    return _calc_local(date, lat, lon, method, timezone_str)


def next_prayer(prayer_times: dict[str, float], now_minutes: float) -> str:
    """Return the name of the next upcoming prayer."""
    for name in PRAYER_ORDER:
        if name in prayer_times and prayer_times[name] > now_minutes:
            return name
    return "fajr"


def current_prayer(prayer_times: dict[str, float], now_minutes: float) -> str:
    """Return the name of the current active prayer."""
    current = "fajr"
    for name in PRAYER_ORDER:
        if name in prayer_times and prayer_times[name] <= now_minutes:
            current = name
    return current
