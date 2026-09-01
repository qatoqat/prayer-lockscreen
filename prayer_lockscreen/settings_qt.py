#!/usr/bin/env python3
"""KDE System Settings module for prayer-lockscreen."""

import json
import sys
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

CONFIG_DIR = Path.home() / ".config" / "prayer-lockscreen"

PRAYER_METHODS = [
    ("ISNA", "ISNA (Islamic Society of North America)"),
    ("MWL", "MWL (Muslim World League)"),
    ("Egypt", "Egypt (Egyptian General Authority)"),
    ("Karachi", "Karachi (University of Islamic Sciences)"),
    ("Gulf", "Gulf (Gulf region)"),
    ("JAKIM", "JAKIM (Malaysia)"),
]

MALAYSIA_TIMEZONES = [
    ("Asia/Kuala_Lumpur", "Peninsular Malaysia (UTC+8)"),
    ("Asia/Kuching", "Sabah & Sarawak (UTC+8)"),
]

GLOBAL_TIMEZONES = [
    ("Asia/Kuala_Lumpur", "Malaysia - Peninsular (UTC+8)"),
    ("Asia/Kuching", "Malaysia - Sabah & Sarawak (UTC+8)"),
    ("Asia/Jakarta", "Indonesia - Western (UTC+7)"),
    ("Asia/Makassar", "Indonesia - Central (UTC+8)"),
    ("Asia/Jayapura", "Indonesia - Eastern (UTC+9)"),
    ("Asia/Brunei", "Brunei (UTC+8)"),
    ("Asia/Singapore", "Singapore (UTC+8)"),
    ("Asia/Kolkata", "India (UTC+5:30)"),
    ("Asia/Dubai", "UAE (UTC+4)"),
    ("Asia/Riyadh", "Saudi Arabia (UTC+3)"),
    ("Europe/London", "UK (UTC+0/+1)"),
    ("Europe/Paris", "Central Europe (UTC+1/+2)"),
    ("America/New_York", "US Eastern (UTC-5/-4)"),
    ("America/Los_Angeles", "US Pacific (UTC-8/-7)"),
]


def _load_config() -> dict:
    config_path = CONFIG_DIR / "config.json"
    if not config_path.exists():
        return {}
    with open(config_path) as f:
        return json.load(f)


def _save_config(config: dict) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_DIR / "config.json", "w") as f:
        json.dump(config, f, indent=4)


def _is_malaysia(lat, lon) -> bool:
    if lat is None or lon is None:
        return False
    return 0.8 <= lat <= 7.4 and 99.6 <= lon <= 119.3


class PrayerSettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Prayer Lock Screen Settings")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)

        self.config = _load_config()
        self._init_ui()
        self._load_values()

    def _init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # ── Prayer Method ──
        grp_method = QGroupBox("Prayer Calculation Method")
        form_method = QFormLayout(grp_method)
        self.combo_method = QComboBox()
        for key, label in PRAYER_METHODS:
            self.combo_method.addItem(label, key)
        form_method.addRow("Method:", self.combo_method)
        layout.addWidget(grp_method)

        # ── Timezone ──
        grp_tz = QGroupBox("Timezone")
        form_tz = QFormLayout(grp_tz)
        self.combo_tz = QComboBox()

        lat = self.config.get("latitude")
        lon = self.config.get("longitude")
        if _is_malaysia(lat, lon):
            tz_list = MALAYSIA_TIMEZONES
            grp_tz.setTitle("Timezone (Malaysia)")
        else:
            tz_list = GLOBAL_TIMEZONES

        for tz_val, tz_label in tz_list:
            self.combo_tz.addItem(tz_label, tz_val)
        form_tz.addRow("Timezone:", self.combo_tz)
        layout.addWidget(grp_tz)

        # ── Display Settings ──
        grp_display = QGroupBox("Display Settings")
        form_display = QFormLayout(grp_display)

        self.spin_font = QSpinBox()
        self.spin_font.setRange(12, 72)
        self.spin_font.setSuffix(" px")
        form_display.addRow("Font size:", self.spin_font)

        self.chk_24h = QCheckBox("Use 24-hour format")
        form_display.addRow(self.chk_24h)

        layout.addWidget(grp_display)

        # ── Wallpaper ──
        grp_wall = QGroupBox("Wallpaper")
        form_wall = QFormLayout(grp_wall)
        self.edit_wall = QLineEdit()
        self.edit_wall.setPlaceholderText("/path/to/wallpaper.jpg")
        form_wall.addRow("Source wallpaper:", self.edit_wall)
        layout.addWidget(grp_wall)

        # ── Buttons ──
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        btn_save = QPushButton("Save")
        btn_save.clicked.connect(self._save)
        btn_layout.addWidget(btn_save)

        btn_cancel = QPushButton("Cancel")
        btn_cancel.clicked.connect(self.close)
        btn_layout.addWidget(btn_cancel)

        layout.addLayout(btn_layout)
        layout.addStretch()

    def _load_values(self):
        # Method
        method = self.config.get("method", "ISNA")
        idx = self.combo_method.findData(method)
        if idx >= 0:
            self.combo_method.setCurrentIndex(idx)

        # Timezone
        tz = self.config.get("timezone", "Asia/Kuala_Lumpur")
        idx = self.combo_tz.findData(tz)
        if idx >= 0:
            self.combo_tz.setCurrentIndex(idx)

        # Display
        self.spin_font.setValue(self.config.get("font_size", 24))
        self.chk_24h.setChecked(self.config.get("use_24h", False))

        # Wallpaper
        self.edit_wall.setText(self.config.get("source_wallpaper", ""))

    def _save(self):
        self.config["method"] = self.combo_method.currentData()
        self.config["timezone"] = self.combo_tz.currentData()
        self.config["font_size"] = self.spin_font.value()
        self.config["use_24h"] = self.chk_24h.isChecked()
        self.config["source_wallpaper"] = self.edit_wall.text()
        _save_config(self.config)

        QMessageBox.information(self, "Settings Saved", "Prayer lock screen settings saved successfully.")
        self.close()


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("Prayer Lock Screen Settings")
    app.setOrganizationName("prayer-lockscreen")

    window = PrayerSettingsWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
