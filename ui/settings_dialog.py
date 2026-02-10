from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QComboBox, QPushButton, QMessageBox
from PyQt6.QtCore import QSettings
from core.constants import APP_NAME, THEME_SYSTEM, THEME_LIGHT, THEME_DARK
from utils.helpers import is_windows_dark_mode

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("设置")
        self.setMinimumWidth(350)
        self.settings = QSettings("MyCompany", APP_NAME)
        self.setup_ui()
        self.apply_theme()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(30, 30, 30, 30)

        # Popup setting
        self.daily_popup_checkbox = QCheckBox("启用每日弹窗提醒")
        self.daily_popup_checkbox.setChecked(self.settings.value("daily_popup", True, type=bool))
        layout.addWidget(self.daily_popup_checkbox)

        # Theme setting
        theme_layout = QHBoxLayout()
        theme_layout.addWidget(QLabel("应用主题:"))
        self.theme_combo = QComboBox()
        self.theme_combo.addItem("跟随系统", THEME_SYSTEM)
        self.theme_combo.addItem("浅色模式", THEME_LIGHT)
        self.theme_combo.addItem("深色模式", THEME_DARK)
        
        current_theme = self.settings.value("theme", THEME_SYSTEM, type=str)
        index = self.theme_combo.findData(current_theme)
        if index >= 0:
            self.theme_combo.setCurrentIndex(index)
            
        theme_layout.addWidget(self.theme_combo)
        layout.addLayout(theme_layout)

        layout.addStretch()

        # Save button
        self.save_button = QPushButton("保存设置")
        self.save_button.setObjectName("addButton") # Use accent style
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

    def save_settings(self):
        self.settings.setValue("daily_popup", self.daily_popup_checkbox.isChecked())
        self.settings.setValue("theme", self.theme_combo.currentData())
        QMessageBox.information(self, "设置已保存", "设置已成功保存！重启应用以完全应用主题。")
        self.accept()

    def apply_theme(self):
        theme = self.settings.value("theme", THEME_SYSTEM, type=str)
        is_dark = is_windows_dark_mode() if theme == THEME_SYSTEM else (theme == THEME_DARK)
        
        bg_color = "#1c1c1c" if is_dark else "#f3f3f3"
        text_color = "#ffffff" if is_dark else "#1a1a1a"
        
        self.setStyleSheet(f"""
            QDialog {{ background-color: {bg_color}; color: {text_color}; }}
            QLabel {{ color: {text_color}; }}
            QCheckBox {{ color: {text_color}; }}
            QComboBox {{ 
                background-color: {"#2d2d2d" if is_dark else "#ffffff"};
                color: {text_color};
                border: 1px solid {"#3d3d3d" if is_dark else "#cccccc"};
                padding: 5px;
            }}
            QPushButton {{
                background-color: {"#333333" if is_dark else "#ffffff"};
                color: {text_color};
                border: 1px solid {"#444444" if is_dark else "#cccccc"};
                padding: 10px;
                border-radius: 4px;
            }}
            #addButton {{
                background-color: {"#0078d4" if is_dark else "#0067c0"};
                color: white;
                border: none;
            }}
        """)
