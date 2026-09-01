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

# JAKIM zones with approximate center coordinates
# Source: https://www.e-solat.gov.my/
ZONE_CENTERS = {
    "JHR01": (2.45, 104.15),
    "JHR02": (1.55, 103.75),
    "JHR03": (1.85, 103.25),
    "JHR04": (2.15, 102.75),
    "KDH01": (6.10, 100.35),
    "KDH02": (5.75, 100.45),
    "KDH03": (6.20, 100.75),
    "KDH04": (5.45, 100.75),
    "KDH05": (5.20, 100.55),
    "KDH06": (6.35, 99.85),
    "KDH07": (5.80, 100.40),
    "KTN01": (6.10, 102.25),
    "KTN02": (4.90, 101.85),
    "MLK01": (2.20, 102.25),
    "NGS01": (2.70, 102.25),
    "NGS02": (2.80, 102.05),
    "NGS03": (2.75, 101.90),
    "PHG01": (2.80, 104.20),
    "PHG02": (3.90, 103.40),
    "PHG03": (3.80, 102.25),
    "PHG04": (4.20, 101.90),
    "PHG05": (3.50, 101.85),
    "PHG06": (4.50, 101.40),
    "PHG07": (2.80, 103.60),
    "PLS01": (6.45, 100.20),
    "PNG01": (5.40, 100.35),
    "PRK01": (4.20, 101.30),
    "PRK02": (4.60, 101.10),
    "PRK03": (5.40, 101.00),
    "PRK04": (5.50, 101.30),
    "PRK05": (4.10, 100.70),
    "PRK06": (4.90, 100.75),
    "PRK07": (4.50, 101.05),
    "SBH01": (5.60, 117.80),
    "SBH02": (5.80, 116.80),
    "SBH03": (5.00, 118.50),
    "SBH04": (4.30, 117.90),
    "SBH05": (6.90, 116.80),
    "SBH06": (6.05, 116.55),
    "SBH07": (5.95, 116.10),
    "SBH08": (5.30, 115.50),
    "SBH09": (5.10, 115.60),
    "SGR01": (3.20, 101.65),
    "SGR02": (3.50, 101.30),
    "SGR03": (2.90, 101.50),
    "SWK01": (4.85, 115.40),
    "SWK02": (3.80, 113.80),
    "SWK03": (3.20, 113.20),
    "SWK04": (2.30, 112.30),
    "SWK05": (2.00, 111.80),
    "SWK06": (1.50, 110.80),
    "SWK07": (1.20, 110.50),
    "SWK08": (1.55, 110.35),
    "SWK09": (1.40, 109.90),
    "TRG01": (5.30, 103.15),
    "TRG02": (5.60, 102.80),
    "TRG03": (5.10, 102.70),
    "TRG04": (4.70, 103.40),
    "WLY01": (3.15, 101.70),
    "WLY02": (5.30, 115.25),
}

# Malaysia bounding box
MALAYSIA_BOUNDS = {
    "lat_min": 0.8,
    "lat_max": 7.4,
    "lon_min": 99.6,
    "lon_max": 119.3,
}


def _is_malaysia(lat: float, lon: float) -> bool:
    return (
        MALAYSIA_BOUNDS["lat_min"] <= lat <= MALAYSIA_BOUNDS["lat_max"]
        and MALAYSIA_BOUNDS["lon_min"] <= lon <= MALAYSIA_BOUNDS["lon_max"]
    )


def detect_zone(lat: float, lon: float) -> str | None:
    """Find the nearest JAKIM zone for given coordinates."""
    if not _is_malaysia(lat, lon):
        return None

    best_zone = None
    best_dist = float("inf")
    for zone, (zlat, zlon) in ZONE_CENTERS.items():
        dlat = lat - zlat
        dlon = lon - zlon
        dist = dlat * dlat + dlon * dlon
        if dist < best_dist:
            best_dist = dist
            best_zone = zone
    return best_zone


def _ts_to_minutes(ts: int) -> float:
    """Convert Unix timestamp to minutes from midnight (UTC)."""
    from datetime import timezone
    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    return dt.hour * 60 + dt.minute


def _fetch_waktusolat(zone: str, timezone_str: str = "Asia/Kuala_Lumpur") -> dict | None:
    """Fetch today's prayer times from waktusolat.app (official JAKIM data).

    Returns times as minutes from midnight in the given timezone.
    """
    url = f"https://api.waktusolat.app/v2/solat/{zone}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "prayer-lockscreen/0.1"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())

        # Get timezone offset
        try:
            if zoneinfo is not None:
                tz_obj = zoneinfo.ZoneInfo(timezone_str)
            elif tz_module is not None:
                tz_obj = tz_module.gettz(timezone_str)
            else:
                tz_obj = None
            offset_min = datetime.now(tz=tz_obj).utcoffset().total_seconds() / 60 if tz_obj else 480
        except Exception:
            offset_min = 480  # default UTC+8

        today = datetime.now().day
        for day_data in data.get("prayers", []):
            if day_data.get("day") == today:
                return {
                    "fajr": _ts_to_minutes(day_data["fajr"]) + offset_min,
                    "sunrise": _ts_to_minutes(day_data["syuruk"]) + offset_min,
                    "dhuhr": _ts_to_minutes(day_data["dhuhr"]) + offset_min,
                    "asr": _ts_to_minutes(day_data["asr"]) + offset_min,
                    "maghrib": _ts_to_minutes(day_data["maghrib"]) + offset_min,
                    "isha": _ts_to_minutes(day_data["isha"]) + offset_min,
                }
    except Exception:
        pass
    return None


def _fetch_aladhan(date: datetime, lat: float, lon: float) -> dict | None:
    """Fallback: fetch from Aladhan API with JAKIM method."""
    date_str = date.strftime("%d-%m-%Y")
    url = f"https://api.aladhan.com/v1/timings/{date_str}?latitude={lat}&longitude={lon}&method=17"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "prayer-lockscreen/0.1"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
        if data.get("code") != 200:
            return None
        t = data["data"]["timings"]
        return {
            "fajr": _parse_time(t["Fajr"]),
            "sunrise": _parse_time(t["Sunrise"]),
            "dhuhr": _parse_time(t["Dhuhr"]),
            "asr": _parse_time(t["Asr"]),
            "maghrib": _parse_time(t["Maghrib"]),
            "isha": _parse_time(t["Isha"]),
        }
    except Exception:
        return None


def _parse_time(s: str) -> float:
    h, m = s.split(":")
    return int(h) * 60 + int(m)


# ── fallback astronomical calculation ────────────────────────────────

def _sun_position(date: datetime) -> tuple[float, float]:
    n = date.timetuple().tm_yday
    g = (2 * math.pi / 365) * (n - 1)
    decl = (
        0.006918 - 0.399912 * math.cos(g) + 0.070257 * math.sin(g)
        - 0.006758 * math.cos(2 * g) + 0.000907 * math.sin(2 * g)
        - 0.002697 * math.cos(3 * g) + 0.00148 * math.sin(3 * g)
    )
    eq = 229.18 * (
        0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g)
        - 0.014615 * math.cos(2 * g) - 0.04089 * math.sin(2 * g)
    )
    return decl, eq


def _hour_angle(decl: float, lat: float, angle: float) -> float | None:
    lat_r = math.radians(lat)
    a_r = math.radians(angle)
    cos_h = (math.sin(a_r) - math.sin(lat_r) * math.sin(decl)) / (
        math.cos(lat_r) * math.cos(decl)
    )
    if cos_h < -1 or cos_h > 1:
        return None
    return math.degrees(math.acos(cos_h))


def _tz_offset(date: datetime, tz_str: str) -> float:
    try:
        if zoneinfo is not None:
            tz_obj = zoneinfo.ZoneInfo(tz_str)
        elif tz_module is not None:
            tz_obj = tz_module.gettz(tz_str)
        else:
            return 0
        if tz_obj is not None:
            return date.replace(tzinfo=tz_obj).utcoffset().total_seconds() / 60
    except Exception:
        pass
    return 0


def _calc_local(date: datetime, lat: float, lng: float, tz_str: str) -> dict[str, float]:
    decl, eq = _sun_position(date)
    utc_noon = 720 + (-4 * lng) - eq
    noon = utc_noon + _tz_offset(date, tz_str)

    fajr_a, isha_a = 20.0, 18.0  # JAKIM angles
    t: dict[str, float] = {}

    sha = _hour_angle(decl, lat, -0.833)
    if sha is not None:
        t["sunrise"] = noon - sha * 4
        t["maghrib"] = noon + sha * 4

    fha = _hour_angle(decl, lat, -fajr_a)
    if fha is not None:
        t["fajr"] = noon - fha * 4

    t["dhuhr"] = noon + 1

    lat_r = math.radians(lat)
    dd = abs(lat_r - decl)
    asr_a = math.atan(1.0 / (1.0 + math.tan(dd)))
    aha = _hour_angle(decl, lat, math.degrees(asr_a))
    if aha is not None:
        t["asr"] = noon + aha * 4

    iha = _hour_angle(decl, lat, -isha_a)
    if iha is not None:
        t["isha"] = noon + iha * 4

    return t


# ── public API ───────────────────────────────────────────────────────

def format_time(minutes: float, use_24h: bool = False) -> str:
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
    """Get prayer times. Tries waktusolat.app (JAKIM) → Aladhan → local calc."""
    zone = detect_zone(lat, lon)

    # 1. Official JAKIM data via waktusolat.app
    if zone:
        result = _fetch_waktusolat(zone, timezone_str)
        if result is not None:
            return result

    # 2. Aladhan API (JAKIM method=17)
    if _is_malaysia(lat, lon):
        result = _fetch_aladhan(date, lat, lon)
        if result is not None:
            return result

    # 3. Local astronomical calculation
    return _calc_local(date, lat, lon, timezone_str)


def next_prayer(prayer_times: dict[str, float], now_minutes: float) -> str:
    for name in PRAYER_ORDER:
        if name in prayer_times and prayer_times[name] > now_minutes:
            return name
    return "fajr"


def current_prayer(prayer_times: dict[str, float], now_minutes: float) -> str:
    current = "fajr"
    for name in PRAYER_ORDER:
        if name in prayer_times and prayer_times[name] <= now_minutes:
            current = name
    return current
