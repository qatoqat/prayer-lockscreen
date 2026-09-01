// SPDX-FileCopyrightText: 2026 q4t <qatoqatt@gmail.com>
// SPDX-License-Identifier: GPL-2.0-or-later

import QtQuick
import QtQuick.Controls as Controls
import QtQuick.Layouts

import org.kde.kirigami as Kirigami
import org.kde.kcmutils as KCMUtils

KCMUtils.SimpleKCM {
    id: root

    Kirigami.FormLayout {
        anchors.fill: parent

        Controls.ComboBox {
            id: methodCombo
            Kirigami.FormData.label: i18n("Prayer Calculation Method:")
            model: [
                { text: "ISNA (Islamic Society of North America)", value: "ISNA" },
                { text: "MWL (Muslim World League)", value: "MWL" },
                { text: "Egypt (Egyptian General Authority)", value: "Egypt" },
                { text: "Karachi (University of Islamic Sciences)", value: "Karachi" },
                { text: "Gulf (Gulf region)", value: "Gulf" },
                { text: "JAKIM (Malaysia)", value: "JAKIM" }
            ]
            textRole: "text"
        }

        Controls.ComboBox {
            id: timezoneCombo
            Kirigami.FormData.label: i18n("Timezone:")
            model: [
                { text: "Asia/Kuala_Lumpur - Peninsular Malaysia (UTC+8)", value: "Asia/Kuala_Lumpur" },
                { text: "Asia/Kuching - Sabah & Sarawak (UTC+8)", value: "Asia/Kuching" }
            ]
            textRole: "text"
        }

        Controls.SpinBox {
            id: fontSizeSpin
            Kirigami.FormData.label: i18n("Font Size (px):")
            from: 12
            to: 72
            value: 24
        }

        Controls.CheckBox {
            id: use24hCheck
            Kirigami.FormData.label: i18n("Display:")
            text: i18n("Use 24-hour format")
        }

        Controls.TextField {
            id: wallpaperField
            Kirigami.FormData.label: i18n("Source Wallpaper:")
            placeholderText: "/path/to/wallpaper.jpg"
            Layout.fillWidth: true
        }
    }
}
