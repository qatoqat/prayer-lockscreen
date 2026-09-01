/**
 * SPDX-FileCopyrightText: 2026 q4t <qatoqatt@gmail.com>
 * SPDX-License-Identifier: GPL-2.0-or-later
 */

#pragma once

#include <KQuickConfigModule>
#include <QJsonDocument>

class PrayerLockScreen : public KQuickConfigModule
{
    Q_OBJECT
    Q_PROPERTY(QString method READ method WRITE setMethod NOTIFY methodChanged)
    Q_PROPERTY(QString timezone READ timezone WRITE setTimezone NOTIFY timezoneChanged)
    Q_PROPERTY(QString zone READ zone WRITE setZone NOTIFY zoneChanged)
    Q_PROPERTY(int fontSize READ fontSize WRITE setFontSize NOTIFY fontSizeChanged)
    Q_PROPERTY(bool use24h READ use24h WRITE setUse24h NOTIFY use24hChanged)
    Q_PROPERTY(QString wallpaper READ wallpaper WRITE setWallpaper NOTIFY wallpaperChanged)
    Q_PROPERTY(bool detectLocation READ detectLocation WRITE setDetectLocation NOTIFY detectLocationChanged)
    Q_PROPERTY(double latitude READ latitude WRITE setLatitude NOTIFY latitudeChanged)
    Q_PROPERTY(double longitude READ longitude WRITE setLongitude NOTIFY longitudeChanged)

    public:
        PrayerLockScreen(QObject *parent, const KPluginMetaData &data);

        QString method() const { return m_method; }
        void setMethod(const QString &method);

        QString timezone() const { return m_timezone; }
        void setTimezone(const QString &tz);

        QString zone() const { return m_zone; }
        void setZone(const QString &zone);

        int fontSize() const { return m_fontSize; }
        void setFontSize(int size);

        bool use24h() const { return m_use24h; }
        void setUse24h(bool on);

        QString wallpaper() const { return m_wallpaper; }
        void setWallpaper(const QString &path);

        bool detectLocation() const { return m_detectLocation; }
        void setDetectLocation(bool on);

        double latitude() const { return m_latitude; }
        void setLatitude(double lat);

        double longitude() const { return m_longitude; }
        void setLongitude(double lon);

    Q_SIGNALS:
        void methodChanged();
        void timezoneChanged();
        void zoneChanged();
        void fontSizeChanged();
        void use24hChanged();
        void wallpaperChanged();
        void detectLocationChanged();
        void latitudeChanged();
        void longitudeChanged();

    private:
        void loadConfig();
        void saveConfig();

        QString m_method;
        QString m_timezone;
        QString m_zone;
        int m_fontSize = 24;
        bool m_use24h = false;
        QString m_wallpaper;
        bool m_detectLocation = true;
        double m_latitude = 0;
        double m_longitude = 0;
};
