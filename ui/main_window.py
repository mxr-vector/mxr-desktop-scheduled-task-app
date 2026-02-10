from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QGroupBox, QTextEdit, QCheckBox, QTimeEdit, QPushButton, 
    QListWidget, QListWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt, QTime
from core.constants import WEEKDAY_NAMES, THEME_SYSTEM, THEME_DARK
from utils.helpers import is_startup_enabled, toggle_startup, is_windows_dark_mode
from ui.styles import get_style_sheet

class ModernMainWindow(QMainWindow):
    def __init__(self, tray_app):
        super().__init__()
        self.tray_app = tray_app
        self.task_data = tray_app.task_data
        self.setup_ui()
        self.apply_theme()
        self.load_tasks()

    def setup_ui(self):
        self.setWindowTitle("定期提醒工具")
        self.setMinimumSize(700, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(30, 20, 30, 30)

        # Title
        self.title_label = QLabel("📅 定期提醒任务管理")
        self.title_label.setObjectName("titleLabel")
        main_layout.addWidget(self.title_label)

        # Add Task Group
        add_group = QGroupBox("添加新任务")
        add_layout = QVBoxLayout(add_group)
        add_layout.setSpacing(15)

        # Content Input
        content_box = QVBoxLayout()
        content_box.addWidget(QLabel("提醒内容:"))
        self.content_input = QTextEdit()
        self.content_input.setMaximumHeight(80)
        self.content_input.setPlaceholderText("在这里输入提醒内容...")
        content_box.addWidget(self.content_input)
        add_layout.addLayout(content_box)

        # Weekdays
        week_box = QVBoxLayout()
        week_box.addWidget(QLabel("重复周期:"))
        week_layout = QHBoxLayout()
        self.weekday_checkboxes = []
        for i, day in enumerate(WEEKDAY_NAMES):
            checkbox = QCheckBox(day)
            self.weekday_checkboxes.append(checkbox)
            week_layout.addWidget(checkbox)
        week_box.addLayout(week_layout)
        add_layout.addLayout(week_box)

        # Time and Action
        time_action_layout = QHBoxLayout()
        time_box = QHBoxLayout()
        time_box.addWidget(QLabel("提醒时间:"))
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setTime(QTime(9, 0))
        time_box.addWidget(self.time_edit)
        time_action_layout.addLayout(time_box)
        
        time_action_layout.addStretch()

        self.add_btn = QPushButton("➕ 添加任务")
        self.add_btn.setObjectName("addButton")
        self.add_btn.clicked.connect(self.add_task)
        time_action_layout.addWidget(self.add_btn)
        add_layout.addLayout(time_action_layout)

        main_layout.addWidget(add_group)

        # Task List
        list_group = QGroupBox("当前任务列表")
        list_layout = QVBoxLayout(list_group)
        self.task_list = QListWidget()
        self.task_list.setObjectName("taskList")
        self.task_list.itemDoubleClicked.connect(self.remove_task)
        list_layout.addWidget(self.task_list)
        main_layout.addWidget(list_group)

        # Footer Actions
        footer_layout = QHBoxLayout()
        
        self.startup_checkbox = QCheckBox("开机自启动")
        self.startup_checkbox.setChecked(is_startup_enabled())
        self.startup_checkbox.stateChanged.connect(self._toggle_startup)
        footer_layout.addWidget(self.startup_checkbox)

        footer_layout.addStretch()

        self.test_btn = QPushButton("🔔 测试通知")
        self.test_btn.clicked.connect(self.show_test_notification)
        footer_layout.addWidget(self.test_btn)

        self.minimize_btn = QPushButton("🔽 最小化")
        self.minimize_btn.clicked.connect(self.hide)
        footer_layout.addWidget(self.minimize_btn)

        self.close_btn = QPushButton("❌ 退出程序")
        self.close_btn.clicked.connect(self.tray_app.quit_application)
        footer_layout.addWidget(self.close_btn)

        main_layout.addLayout(footer_layout)

    def apply_theme(self):
        theme = self.tray_app.settings.value("theme", THEME_SYSTEM, type=str)
        is_dark = is_windows_dark_mode() if theme == THEME_SYSTEM else (theme == THEME_DARK)
        self.setStyleSheet(get_style_sheet(is_dark))

    def load_tasks(self):
        self.task_list.clear()
        for task in self.task_data.tasks:
            weekdays_str = ", ".join([WEEKDAY_NAMES[w] for w in task['weekdays']])
            status = "✅" if task['enabled'] else "❌"
            item_text = f"{status} {task['content'][:25]}... | {weekdays_str} | {task['time']}"
            
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, task['id'])
            self.task_list.addItem(item)

    def add_task(self):
        content = self.content_input.toPlainText().strip()
        if not content:
            QMessageBox.warning(self, "警告", "提醒内容不能为空！")
            return

        selected_weekdays = [i for i, cb in enumerate(self.weekday_checkboxes) if cb.isChecked()]
        if not selected_weekdays:
            QMessageBox.warning(self, "警告", "请至少选择一个重复周期！")
            return

        time_str = self.time_edit.time().toString("HH:mm")
        self.task_data.add_task(content, selected_weekdays, time_str)
        self.load_tasks()
        self.content_input.clear()
        for cb in self.weekday_checkboxes: cb.setChecked(False)
        QMessageBox.information(self, "成功", "任务已保存！")

    def remove_task(self, item):
        task_id = item.data(Qt.ItemDataRole.UserRole)
        reply = QMessageBox.question(self, "确认删除", "任务删除后无法恢复，确定吗？",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.task_data.remove_task(task_id)
            self.load_tasks()

    def _toggle_startup(self):
        success, msg = toggle_startup(self.startup_checkbox.isChecked())
        if not success:
            QMessageBox.warning(self, "错误", msg)
            self.startup_checkbox.setChecked(not self.startup_checkbox.isChecked())
        else:
            QMessageBox.information(self, "设置更新", msg)

    def show_test_notification(self):
        test_task = {
            'content': '这是一条测试通知',
            'time': QTime.currentTime().toString("HH:mm")
        }
        self.tray_app.show_custom_notification(test_task)

    def closeEvent(self, event):
        self.hide()
        event.ignore()
