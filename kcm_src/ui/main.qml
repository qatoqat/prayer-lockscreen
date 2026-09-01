// SPDX-FileCopyrightText: 2026 q4t <qatoqatt@gmail.com>
// SPDX-License-Identifier: GPL-2.0-or-later

import QtQuick
import QtQuick.Controls as Controls
import QtQuick.Layouts

import org.kde.kirigami as Kirigami
import org.kde.kcmutils as KCM

KCM.ScrollViewKCM {
    id: root

    // JAKIM zones for Malaysia
    readonly property var zones: [
        { code: "JHR01", name: "JHR01 - Pulau Aur & Pemanggil", state: "Johor" },
        { code: "JHR02", name: "JHR02 - JB, Kota Tinggi, Mersing, Kulai", state: "Johor" },
        { code: "JHR03", name: "JHR03 - Kluang, Pontian", state: "Johor" },
        { code: "JHR04", name: "JHR04 - Batu Pahat, Muar, Segamat, Tangkak", state: "Johor" },
        { code: "KDH01", name: "KDH01 - Kota Setar, Kubang Pasu, Pokok Sena", state: "Kedah" },
        { code: "KDH02", name: "KDH02 - Kuala Muda, Yan, Pendang", state: "Kedah" },
        { code: "KDH03", name: "KDH03 - Padang Terap, Sik", state: "Kedah" },
        { code: "KDH04", name: "KDH04 - Baling", state: "Kedah" },
        { code: "KDH05", name: "KDH05 - Bandar Baharu, Kulim", state: "Kedah" },
        { code: "KDH06", name: "KDH06 - Langkawi", state: "Kedah" },
        { code: "KDH07", name: "KDH07 - Puncak Gunung Jerai", state: "Kedah" },
        { code: "KTN01", name: "KTN01 - Bachok, KB, Machang, Pasir Mas, etc", state: "Kelantan" },
        { code: "KTN02", name: "KTN02 - Gua Musang, Jeli, Lojing", state: "Kelantan" },
        { code: "MLK01", name: "MLK01 - Seluruh Negeri Melaka", state: "Melaka" },
        { code: "NGS01", name: "NGS01 - Tampin, Jempol", state: "N. Sembilan" },
        { code: "NGS02", name: "NGS02 - Jelebu, Kuala Pilah, Rembau", state: "N. Sembilan" },
        { code: "NGS03", name: "NGS03 - Port Dickson, Seremban", state: "N. Sembilan" },
        { code: "PHG01", name: "PHG01 - Pulau Tioman", state: "Pahang" },
        { code: "PHG02", name: "PHG02 - Kuantan, Pekan, Muadzam Shah", state: "Pahang" },
        { code: "PHG03", name: "PHG03 - Jerantut, Temerloh, Maran, Bera", state: "Pahang" },
        { code: "PHG04", name: "PHG04 - Bentong, Lipis, Raub", state: "Pahang" },
        { code: "PHG05", name: "PHG05 - Genting Sempah, Janda Baik", state: "Pahang" },
        { code: "PHG06", name: "PHG06 - Cameron Highlands, Bukit Fraser", state: "Pahang" },
        { code: "PHG07", name: "PHG07 - Rompin, Endau, Pontian", state: "Pahang" },
        { code: "PLS01", name: "PLS01 - Kangar, Padang Besar, Arau", state: "Perlis" },
        { code: "PNG01", name: "PNG01 - Seluruh Negeri Pulau Pinang", state: "Penang" },
        { code: "PRK01", name: "PRK01 - Tapah, Slim River, Tanjung Malim", state: "Perak" },
        { code: "PRK02", name: "PRK02 - KL, Sg. Siput, Ipoh, Batu Gajah", state: "Perak" },
        { code: "PRK03", name: "PRK03 - Lenggong, Pengkalan Hulu, Grik", state: "Perak" },
        { code: "PRK04", name: "PRK04 - Temengor, Belum", state: "Perak" },
        { code: "PRK05", name: "PRK05 - Teluk Intan, Bagan Datuk, Sitiawan", state: "Perak" },
        { code: "PRK06", name: "PRK06 - Selama, Taiping, Bagan Serai, Parit Buntar", state: "Perak" },
        { code: "PRK07", name: "PRK07 - Bukit Larut", state: "Perak" },
        { code: "SBH01", name: "SBH01 - Sandakan, Bukit Garam, Sukau", state: "Sabah" },
        { code: "SBH02", name: "SBH02 - Beluran, Telupid, Pinangah", state: "Sabah" },
        { code: "SBH03", name: "SBH03 - Lahad Datu, Kunak, Semporna", state: "Sabah" },
        { code: "SBH04", name: "SBH04 - Tawau, Balong, Merotai", state: "Sabah" },
        { code: "SBH05", name: "SBH05 - Kudat, Kota Marudu, Pitas", state: "Sabah" },
        { code: "SBH06", name: "SBH06 - Gunung Kinabalu", state: "Sabah" },
        { code: "SBH07", name: "SBH07 - Kota Kinabalu, Ranau, Tuaran", state: "Sabah" },
        { code: "SBH08", name: "SBH08 - Keningau, Tambunan, Nabawan", state: "Sabah" },
        { code: "SBH09", name: "SBH09 - Beaufort, Tenom, Sipitang", state: "Sabah" },
        { code: "SGR01", name: "SGR01 - Gombak, Petaling, Sepang, Hulu Langat", state: "Selangor" },
        { code: "SGR02", name: "SGR02 - Kuala Selangor, Sabak Bernam", state: "Selangor" },
        { code: "SGR03", name: "SGR03 - Klang, Kuala Langat", state: "Selangor" },
        { code: "SWK01", name: "SWK01 - Limbang, Lawas, Sundar, Trusan", state: "Sarawak" },
        { code: "SWK02", name: "SWK02 - Miri, Niah, Bekenu, Sibuti", state: "Sarawak" },
        { code: "SWK03", name: "SWK03 - Pandan, Belaga, Bintulu", state: "Sarawak" },
        { code: "SWK04", name: "SWK04 - Sibu, Mukah, Dalat, Song, Kapit", state: "Sarawak" },
        { code: "SWK05", name: "SWK05 - Sarikei, Julau, Rajang, Bintangor", state: "Sarawak" },
        { code: "SWK06", name: "SWK06 - Sri Aman, Betong, Saratok", state: "Sarawak" },
        { code: "SWK07", name: "SWK07 - Serian, Samarahan, Sebuyau", state: "Sarawak" },
        { code: "SWK08", name: "SWK08 - Kuching, Bau, Lundu, Sematan", state: "Sarawak" },
        { code: "SWK09", name: "SWK09 - Kampung Patarikan", state: "Sarawak" },
        { code: "TRG01", name: "TRG01 - Kuala Terengganu, Marang", state: "Terengganu" },
        { code: "TRG02", name: "TRG02 - Besut, Setiu", state: "Terengganu" },
        { code: "TRG03", name: "TRG03 - Hulu Terengganu", state: "Terengganu" },
        { code: "TRG04", name: "TRG04 - Dungun, Kemaman", state: "Terengganu" },
        { code: "WLY01", name: "WLY01 - Kuala Lumpur, Putrajaya", state: "W.P. Kuala Lumpur" },
        { code: "WLY02", name: "WLY02 - Labuan", state: "W.P. Labuan" },
    ]

    Kirigami.FormLayout {
        anchors.fill: parent

        // Detection mode
        Controls.CheckBox {
            id: detectCheck
            Kirigami.FormData.label: i18n("Location:")
            text: i18n("Auto-detect from IP")
            checked: kcm.detectLocation
            onToggled: kcm.detectLocation = checked
        }

        // Manual coordinates (when not detecting)
        RowLayout {
            Kirigami.FormData.label: i18n("Coordinates:")
            visible: !detectCheck.checked
            spacing: Kirigami.Units.smallSpacing

            Controls.TextField {
                id: latField
                placeholderText: i18n("Latitude")
                text: kcm.latitude !== 0 ? kcm.latitude.toFixed(4) : ""
                onEditingFinished: {
                    var val = parseFloat(text)
                    if (!isNaN(val)) kcm.latitude = val
                }
                implicitWidth: Kirigami.Units.gridUnit * 6
            }
            Controls.Label { text: "," }
            Controls.TextField {
                id: lonField
                placeholderText: i18n("Longitude")
                text: kcm.longitude !== 0 ? kcm.longitude.toFixed(4) : ""
                onEditingFinished: {
                    var val = parseFloat(text)
                    if (!isNaN(val)) kcm.longitude = val
                }
                implicitWidth: Kirigami.Units.gridUnit * 6
            }
        }

        // JAKIM Zone selector
        Controls.ComboBox {
            id: zoneCombo
            Kirigami.FormData.label: i18n("JAKIM Zone:")
            Layout.fillWidth: true
            model: root.zones
            textRole: "name"
            currentIndex: {
                for (var i = 0; i < root.zones.length; i++) {
                    if (root.zones[i].code === kcm.zone) return i;
                }
                return -1;
            }
            onActivated: (index) => {
                kcm.zone = root.zones[index].code;
            }
        }

        Kirigami.Separator {
            Kirigami.FormData.isSection: true
            Kirigami.FormData.label: i18n("Calculation")
        }

        Controls.ComboBox {
            id: methodCombo
            Kirigami.FormData.label: i18n("Method:")
            model: [
                { text: i18n("ISNA - Islamic Society of North America"), value: "ISNA" },
                { text: i18n("MWL - Muslim World League"), value: "MWL" },
                { text: i18n("Egypt - Egyptian General Authority"), value: "Egypt" },
                { text: i18n("Karachi - University of Islamic Sciences"), value: "Karachi" },
                { text: i18n("Gulf - Gulf region"), value: "Gulf" },
                { text: i18n("JAKIM - Malaysia"), value: "JAKIM" }
            ]
            textRole: "text"
            currentIndex: {
                for (var i = 0; i < model.length; i++) {
                    if (model[i].value === kcm.method) return i;
                }
                return 0;
            }
            onActivated: (index) => {
                kcm.method = model[index].value;
            }
        }

        Controls.ComboBox {
            id: timezoneCombo
            Kirigami.FormData.label: i18n("Timezone:")
            model: [
                { text: i18n("Asia/Kuala_Lumpur - Peninsular Malaysia (UTC+8)"), value: "Asia/Kuala_Lumpur" },
                { text: i18n("Asia/Kuching - Sabah & Sarawak (UTC+8)"), value: "Asia/Kuching" }
            ]
            textRole: "text"
            currentIndex: {
                for (var i = 0; i < model.length; i++) {
                    if (model[i].value === kcm.timezone) return i;
                }
                return 0;
            }
            onActivated: (index) => {
                kcm.timezone = model[index].value;
            }
        }

        Kirigami.Separator {
            Kirigami.FormData.isSection: true
            Kirigami.FormData.label: i18n("Display")
        }

        Controls.SpinBox {
            id: fontSizeSpin
            Kirigami.FormData.label: i18n("Font size:")
            from: 12
            to: 72
            value: kcm.fontSize
            onValueModified: kcm.fontSize = value
            suffix: " px"
        }

        Controls.CheckBox {
            id: use24hCheck
            Kirigami.FormData.label: i18n("Time format:")
            text: i18n("Use 24-hour format")
            checked: kcm.use24h
            onToggled: kcm.use24h = checked
        }

        Kirigami.Separator {
            Kirigami.FormData.isSection: true
            Kirigami.FormData.label: i18n("Wallpaper")
        }

        Controls.TextField {
            id: wallpaperField
            Kirigami.FormData.label: i18n("Source:")
            placeholderText: i18n("/path/to/wallpaper.jpg")
            text: kcm.wallpaper
            onEditingFinished: kcm.wallpaper = text
            Layout.fillWidth: true
        }
    }
}
