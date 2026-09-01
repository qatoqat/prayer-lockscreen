/**
 * SPDX-FileCopyrightText: 2026 q4t <qatoqatt@gmail.com>
 * SPDX-License-Identifier: GPL-2.0-or-later
 */

#pragma once

#include <KQuickConfigModule>

class PrayerLockScreen : public KQuickConfigModule
{
    Q_OBJECT
    public:
        PrayerLockScreen(QObject *parent, const KPluginMetaData &data);
};
