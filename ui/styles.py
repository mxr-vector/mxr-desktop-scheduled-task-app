from core.constants import THEME_LIGHT, THEME_DARK

def get_style_sheet(is_dark=False):
    if is_dark:
        return f"""
        QMainWindow {{
            background-color: #1c1c1c;
            color: #ffffff;
        }}
        QLabel {{
            color: #ffffff;
        }}
        #titleLabel {{
            font-size: 20pt;
            font-weight: 600;
            color: #ffffff;
            padding: 10px;
            margin-bottom: 5px;
        }}
        QGroupBox {{
            font-size: 11pt;
            font-weight: 600;
            color: #ffffff;
            border: 1px solid #333333;
            border-radius: 8px;
            margin-top: 15px;
            padding-top: 10px;
            background-color: #252525;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
        }}
        QTextEdit, QLineEdit, QTimeEdit, QComboBox {{
            border: 1px solid #3d3d3d;
            border-radius: 4px;
            padding: 6px;
            background-color: #2d2d2d;
            color: #ffffff;
            font-size: 10pt;
        }}
        QTextEdit:focus, QLineEdit:focus, QTimeEdit:focus, QComboBox:focus {{
            border: 2px solid #0078d4;
        }}
        QPushButton {{
            background-color: #333333;
            color: #ffffff;
            border: 1px solid #444444;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: 500;
        }}
        QPushButton:hover {{
            background-color: #444444;
        }}
        QPushButton:pressed {{
            background-color: #222222;
        }}
        #addButton {{
            background-color: #0078d4;
            color: white;
            border: none;
        }}
        #addButton:hover {{
            background-color: #1084d8;
        }}
        #taskList {{
            border: 1px solid #333333;
            border-radius: 8px;
            background-color: #252525;
            color: #ffffff;
        }}
        QListWidget::item {{
            padding: 12px;
            border-bottom: 1px solid #333333;
        }}
        QListWidget::item:hover {{
            background-color: #3d3d3d;
        }}
        QListWidget::item:selected {{
            background-color: #0078d4;
            color: white;
        }}
        QCheckBox {{
            spacing: 8px;
        }}
        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border-radius: 4px;
            border: 1px solid #555555;
            background: #2d2d2d;
        }}
        QCheckBox::indicator:checked {{
            background-color: #0078d4;
            border-color: #0078d4;
            image: url(assets/check_white.png); /* Fallback to color if missing */
        }}
        """
    else:
        return f"""
        QMainWindow {{
            background-color: #f3f3f3;
            color: #1a1a1a;
        }}
        QLabel {{
            color: #1a1a1a;
        }}
        #titleLabel {{
            font-size: 20pt;
            font-weight: 600;
            color: #1a1a1a;
            padding: 10px;
            margin-bottom: 5px;
        }}
        QGroupBox {{
            font-size: 11pt;
            font-weight: 600;
            color: #1a1a1a;
            border: 1px solid #d2d2d2;
            border-radius: 8px;
            margin-top: 15px;
            padding-top: 10px;
            background-color: #ffffff;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            left: 10px;
            padding: 0 5px;
        }}
        QTextEdit, QLineEdit, QTimeEdit, QComboBox {{
            border: 1px solid #cccccc;
            border-radius: 4px;
            padding: 6px;
            background-color: #ffffff;
            color: #1a1a1a;
            font-size: 10pt;
        }}
        QTextEdit:focus, QLineEdit:focus, QTimeEdit:focus, QComboBox:focus {{
            border: 2px solid #0067c0;
        }}
        QPushButton {{
            background-color: #ffffff;
            color: #1a1a1a;
            border: 1px solid #cccccc;
            border-radius: 4px;
            padding: 8px 16px;
            font-weight: 500;
        }}
        QPushButton:hover {{
            background-color: #f9f9f9;
        }}
        QPushButton:pressed {{
            background-color: #efefef;
        }}
        #addButton {{
            background-color: #0067c0;
            color: white;
            border: none;
        }}
        #addButton:hover {{
            background-color: #1075cc;
        }}
        #taskList {{
            border: 1px solid #d2d2d2;
            border-radius: 8px;
            background-color: #ffffff;
            color: #1a1a1a;
        }}
        QListWidget::item {{
            padding: 12px;
            border-bottom: 1px solid #f0f0f0;
        }}
        QListWidget::item:hover {{
            background-color: #f5f5f5;
        }}
        QListWidget::item:selected {{
            background-color: #0067c0;
            color: white;
        }}
        """
