import sys
import socket
import datetime
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu
from PyQt6.QtCore import QTimer, QSettings, QSocketNotifier, Qt
from PyQt6.QtGui import QIcon, QAction

from core.constants import APP_NAME, SINGLE_INSTANCE_PORT, THEME_SYSTEM, THEME_DARK
from core.task_manager import TaskData
from ui.main_window import ModernMainWindow
from ui.settings_dialog import SettingsDialog
from ui.notification import CustomNotification
from utils.helpers import resource_path, is_windows_dark_mode

class TrayApplication(QApplication):
    def __init__(self, sys_argv, server_sock=None):
        super().__init__(sys_argv)
        self.setQuitOnLastWindowClosed(False)
        
        self.settings = QSettings("MyCompany", APP_NAME)
        self.task_data = TaskData()
        self.main_window = ModernMainWindow(self)
        self.settings_dialog = SettingsDialog()
        self.last_check_time = None

        self.server_socket = server_sock
        if self.server_socket:
            self.socket_notifier = QSocketNotifier(self.server_socket.fileno(), QSocketNotifier.Type.Read, self)
            self.socket_notifier.activated.connect(self.handle_socket_connection)

        self.setup_tray()
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_time_and_notify)
        self.timer.start(10000)
        
        print(f"应用已启动。已加载 {len(self.task_data.tasks)} 个任务。")

    def setup_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        icon_path = resource_path("assets/icon.ico")
        if os.path.exists(icon_path):
            self.tray_icon.setIcon(QIcon(icon_path))
        else:
            # Standard fallback icon
            from PyQt6.QtWidgets import QStyle
            self.tray_icon.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon))
        
        self.tray_menu = QMenu()
        self.tray_menu.addAction("显示主窗口", self.show_main_window)
        self.tray_menu.addAction("设置", self.show_settings_dialog)
        self.tray_menu.addSeparator()
        self.tray_menu.addAction("退出", self.quit_application)
        
        # Simple theme for menu
        theme = self.settings.value("theme", THEME_SYSTEM, type=str)
        is_dark = is_windows_dark_mode() if theme == THEME_SYSTEM else (theme == THEME_DARK)
        if is_dark:
            self.tray_menu.setStyleSheet("QMenu { background-color: #2d2d2d; color: white; border: 1px solid #444444; } QMenu::item:selected { background-color: #3d3d3d; }")
        
        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.activated.connect(self.on_tray_activated)
        self.tray_icon.show()

    def show_main_window(self):
        self.main_window.show()
        self.main_window.raise_()
        self.main_window.activateWindow()

    def show_settings_dialog(self):
        if self.settings_dialog.exec():
            self.main_window.apply_theme()
            # Reload tray menu style if theme changed?
            self.setup_tray()

    def on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.show_main_window()

    def check_time_and_notify(self):
        now = datetime.datetime.now().replace(second=0, microsecond=0)
        if self.last_check_time == now:
            return
        
        self.last_check_time = now
        weekday = now.weekday()
        time_str = now.strftime("%H:%M")
        
        for task in self.task_data.get_active_tasks():
            if weekday in task['weekdays'] and task['time'] == time_str:
                last_triggered = task.get('last_triggered')
                today_str = now.date().isoformat()
                
                if last_triggered != today_str:
                    self.show_custom_notification(task)
                    task['last_triggered'] = today_str
                    self.task_data.save_data()

    def show_custom_notification(self, task):
        # System Tray Message
        self.tray_icon.showMessage("📅 定期提醒", f"⏰ {task['time']}\n{task['content']}", QSystemTrayIcon.MessageIcon.Information, 5000)
        
        # Heavy Popup if enabled
        if self.settings.value("daily_popup", True, type=bool):
            theme = self.settings.value("theme", THEME_SYSTEM, type=str)
            is_dark = is_windows_dark_mode() if theme == THEME_SYSTEM else (theme == THEME_DARK)
            dialog = CustomNotification(task, is_dark_mode=is_dark)
            dialog.exec()

    def handle_socket_connection(self):
        try:
            client, _ = self.server_socket.accept()
            client.close()
            self.show_main_window()
        except: pass

    def quit_application(self):
        self.timer.stop()
        self.tray_icon.hide()
        if self.server_socket:
            self.server_socket.close()
        self.quit()

import os
def is_instance_running():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('127.0.0.1', SINGLE_INSTANCE_PORT))
        sock.listen(1)
        return False, sock
    except OSError:
        return True, None

def activate_existing_instance():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(('127.0.0.1', SINGLE_INSTANCE_PORT))
        sock.close()
    except: pass

if __name__ == "__main__":
    running, sock = is_instance_running()
    if running:
        activate_existing_instance()
        sys.exit(0)
    
    app = TrayApplication(sys.argv, server_sock=sock)
    app.show_main_window()
    sys.exit(app.exec())