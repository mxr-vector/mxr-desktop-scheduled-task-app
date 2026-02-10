from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt6.QtCore import Qt
from core.constants import THEME_DARK

class CustomNotification(QDialog):
    def __init__(self, task, parent=None, is_dark_mode=False):
        super().__init__(parent)
        self.task = task
        self.is_dark_mode = is_dark_mode
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("📅 定期提醒")
        self.setFixedSize(400, 220)
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Dialog | Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Container with border radius
        container = QLabel(self)
        container.setFixedSize(400, 220)
        bg_color = "#2d2d2d" if self.is_dark_mode else "#ffffff"
        text_color = "#ffffff" if self.is_dark_mode else "#1a1a1a"
        border_color = "#444444" if self.is_dark_mode else "#dddddd"
        
        container.setStyleSheet(f"""
            QLabel {{
                background-color: {bg_color};
                color: {text_color};
                border: 1px solid {border_color};
                border-radius: 12px;
            }}
        """)

        layout = QVBoxLayout(container)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(15)

        # Header
        header_layout = QHBoxLayout()
        time_label = QLabel(f"⏰ {self.task['time']}")
        time_label.setStyleSheet("font-size: 16pt; font-weight: bold; border: none; background: transparent;")
        header_layout.addWidget(time_label)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        # Content
        content_label = QLabel(self.task['content'])
        content_label.setWordWrap(True)
        content_label.setStyleSheet("font-size: 11pt; border: none; background: transparent;")
        layout.addWidget(content_label)

        layout.addStretch()

        # Button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        ok_btn = QPushButton("知道了")
        accent_color = "#0078d4" if self.is_dark_mode else "#0067c0"
        ok_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {accent_color};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 10px 25px;
                font-size: 10pt;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background-color: {"#1084d8" if self.is_dark_mode else "#1075cc"};
            }}
        """)
        ok_btn.clicked.connect(self.accept)
        btn_layout.addWidget(ok_btn)
        layout.addLayout(btn_layout)
        
        # Centering the notification manually if needed, or rely on parent
