/**
 * SPDX-FileCopyrightText: 2026 q4t <qatoqatt@gmail.com>
 * SPDX-License-Identifier: GPL-2.0-or-later
 */

#include "prayerlockscreen.h"

#include <KPluginFactory>
#include <QFile>
#include <QJsonDocument>
#include <QJsonObject>
#include <QStandardPaths>

K_PLUGIN_CLASS_WITH_JSON(PrayerLockScreen, "kcm_prayerlockscreen.json")

PrayerLockScreen::PrayerLockScreen(QObject *parent, const KPluginMetaData &data)
    : KQuickConfigModule(parent, data)
{
    setButtons(Help | Apply | Default);
    loadConfig();
}

void PrayerLockScreen::save()
{
    saveConfig();
    setNeedsSave(false);
}

void PrayerLockScreen::loadConfig()
{
    QString configPath = QStandardPaths::writableLocation(QStandardPaths::ConfigLocation)
        + QStringLiteral("/prayer-lockscreen/config.json");

    QFile file(configPath);
    if (!file.open(QIODevice::ReadOnly))
        return;

    QJsonDocument doc = QJsonDocument::fromJson(file.readAll());
    QJsonObject obj = doc.object();

    m_method = obj.value(QStringLiteral("method")).toString(QStringLiteral("ISNA"));
    m_timezone = obj.value(QStringLiteral("timezone")).toString(QStringLiteral("Asia/Kuala_Lumpur"));
    m_zone = obj.value(QStringLiteral("zone")).toString();
    m_fontSize = obj.value(QStringLiteral("font_size")).toInt(24);
    m_use24h = obj.value(QStringLiteral("use_24h")).toBool(false);
    m_wallpaper = obj.value(QStringLiteral("source_wallpaper")).toString();
    m_detectLocation = obj.value(QStringLiteral("detect_location")).toBool(true);
    m_latitude = obj.value(QStringLiteral("latitude")).toDouble(0);
    m_longitude = obj.value(QStringLiteral("longitude")).toDouble(0);
}

void PrayerLockScreen::saveConfig()
{
    QString configPath = QStandardPaths::writableLocation(QStandardPaths::ConfigLocation)
        + QStringLiteral("/prayer-lockscreen/config.json");

    QJsonObject obj;
    obj[QStringLiteral("method")] = m_method;
    obj[QStringLiteral("timezone")] = m_timezone;
    obj[QStringLiteral("zone")] = m_zone;
    obj[QStringLiteral("font_size")] = m_fontSize;
    obj[QStringLiteral("use_24h")] = m_use24h;
    obj[QStringLiteral("source_wallpaper")] = m_wallpaper;
    obj[QStringLiteral("detect_location")] = m_detectLocation;
    obj[QStringLiteral("latitude")] = m_latitude;
    obj[QStringLiteral("longitude")] = m_longitude;

    QFile file(configPath);
    if (file.open(QIODevice::WriteOnly)) {
        file.write(QJsonDocument(obj).toJson());
    }
}

void PrayerLockScreen::setMethod(const QString &method)
{
    if (m_method != method) {
        m_method = method;
        Q_EMIT methodChanged();
        setNeedsSave(true);
    }
}

void PrayerLockScreen::setTimezone(const QString &tz)
{
    if (m_timezone != tz) {
        m_timezone = tz;
        Q_EMIT timezoneChanged();
        setNeedsSave(true);
    }
}

void PrayerLockScreen::setZone(const QString &zone)
{
    if (m_zone != zone) {
        m_zone = zone;
        Q_EMIT zoneChanged();
        setNeedsSave(true);
    }
}

void PrayerLockScreen::setFontSize(int size)
{
    if (m_fontSize != size) {
        m_fontSize = size;
        Q_EMIT fontSizeChanged();
        setNeedsSave(true);
    }
}

void PrayerLockScreen::setUse24h(bool on)
{
    if (m_use24h != on) {
        m_use24h = on;
        Q_EMIT use24hChanged();
        setNeedsSave(true);
    }
}

void PrayerLockScreen::setWallpaper(const QString &path)
{
    if (m_wallpaper != path) {
        m_wallpaper = path;
        Q_EMIT wallpaperChanged();
        setNeedsSave(true);
    }
}

void PrayerLockScreen::setDetectLocation(bool on)
{
    if (m_detectLocation != on) {
        m_detectLocation = on;
        Q_EMIT detectLocationChanged();
        setNeedsSave(true);
    }
}

void PrayerLockScreen::setLatitude(double lat)
{
    if (!qFuzzyCompare(m_latitude, lat)) {
        m_latitude = lat;
        Q_EMIT latitudeChanged();
        setNeedsSave(true);
    }
}

void PrayerLockScreen::setLongitude(double lon)
{
    if (!qFuzzyCompare(m_longitude, lon)) {
        m_longitude = lon;
        Q_EMIT longitudeChanged();
        setNeedsSave(true);
    }
}

#include "prayerlockscreen.moc"
