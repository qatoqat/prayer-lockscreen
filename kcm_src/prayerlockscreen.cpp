/**
 * SPDX-FileCopyrightText: 2026 q4t <qatoqatt@gmail.com>
 * SPDX-License-Identifier: GPL-2.0-or-later
 */

#include "prayerlockscreen.h"

#include <KPluginFactory>

K_PLUGIN_CLASS_WITH_JSON(PrayerLockScreen, "kcm_prayerlockscreen.json")

PrayerLockScreen::PrayerLockScreen(QObject *parent, const KPluginMetaData &data)
    : KQuickConfigModule(parent, data)
{
    setButtons(Help | Apply | Default);
}

#include "prayerlockscreen.moc"
