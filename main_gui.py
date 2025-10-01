import sys
import json
from PySide6.QtCore import QObject, Signal, QThread, QSettings, QSize, Qt
from PySide6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                               QWidget, QLabel, QTextEdit, QProgressBar, QGridLayout,
                               QDialog, QCheckBox, QMessageBox, QHBoxLayout, QStyle,
                               QFileDialog, QListWidget, QListWidgetItem, QInputDialog,
                               QSpinBox, QFormLayout, QTabWidget)
import cleanup_logic as logic

# --- Диалоговое окно настроек ---
class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.settings = QSettings("WinClean-GUI", "App")
        self.setMinimumWidth(500)

        main_layout = QVBoxLayout(self)
        tabs = QTabWidget()
        main_layout.addWidget(tabs)

        # Создаем вкладки
        tabs.addTab(self._create_general_tab(), "General")
        tabs.addTab(self._create_exclusions_tab(), "Exclusions")
        tabs.addTab(self._create_custom_folders_tab(), "Custom Folders")

        # Кнопки OK / Cancel
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)
        main_layout.addLayout(button_layout)

    def _create_general_tab(self):
        widget = QWidget()
        layout = QFormLayout(widget)

        self.confirm_checkbox = QCheckBox("Ask for confirmation before cleaning")
        self.confirm_checkbox.setChecked(self.settings.value("confirm_cleanup", True, type=bool))
        layout.addRow(self.confirm_checkbox)

        # Настройка очистки корзины
        self.rb_age_checkbox = QCheckBox("Only empty Recycle Bin items older than (days):")
        self.rb_age_spinbox = QSpinBox()
        self.rb_age_spinbox.setRange(1, 365)
        self.rb_age_spinbox.setEnabled(False)
        
        self.rb_age_checkbox.setChecked(self.settings.value("recycle_bin_age_enabled", False, type=bool))
        self.rb_age_spinbox.setValue(self.settings.value("recycle_bin_age_days", 30, type=int))
        self.rb_age_spinbox.setEnabled(self.rb_age_checkbox.isChecked())
        self.rb_age_checkbox.toggled.connect(self.rb_age_spinbox.setEnabled)

        layout.addRow(self.rb_age_checkbox, self.rb_age_spinbox)
        return widget
    
    def _create_exclusions_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("Files and folders in this list will be ignored during cleanup."))

        self.exclusions_list = QListWidget()
        exclusions = self.settings.value("exclusions", [], type=list)
        self.exclusions_list.addItems(exclusions)
        layout.addWidget(self.exclusions_list)

        btn_layout = QHBoxLayout()
        add_file_btn = QPushButton("Add File...")
        add_file_btn.clicked.connect(self.add_exclusion_file)
        add_folder_btn = QPushButton("Add Folder...")
        add_folder_btn.clicked.connect(self.add_exclusion_folder)
        remove_btn = QPushButton("Remove")
        remove_btn.clicked.connect(self.remove_exclusion)
        
        btn_layout.addWidget(add_file_btn)
        btn_layout.addWidget(add_folder_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(remove_btn)
        layout.addLayout(btn_layout)
        return widget

    def _create_custom_folders_tab(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel("Add custom folders to appear as new buttons on the main screen."))
        
        self.custom_folders_list = QListWidget()
        folders_str = self.settings.value("custom_folders", [], type=list)
        for f_str in folders_str:
            try:
                folder_data = json.loads(f_str)
                item = QListWidgetItem(f"{folder_data['name']} ({folder_data['path']})")
                item.setData(Qt.ItemDataRole.UserRole, folder_data)
                self.custom_folders_list.addItem(item)
            except json.JSONDecodeError:
                continue
        
        layout.addWidget(self.custom_folders_list)

        btn_layout = QHBoxLayout()
        add_btn = QPushButton("Add Folder...")
        add_btn.clicked.connect(self.add_custom_folder)
        remove_btn = QPushButton("Remove")
        remove_btn.clicked.connect(self.remove_custom_folder)
        
        btn_layout.addWidget(add_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(remove_btn)
        layout.addLayout(btn_layout)
        return widget

    def add_exclusion_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Exclude")
        if file_path: self.exclusions_list.addItem(file_path)

    def add_exclusion_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder to Exclude")
        if folder_path: self.exclusions_list.addItem(folder_path)

    def remove_exclusion(self):
        for item in self.exclusions_list.selectedItems():
            self.exclusions_list.takeItem(self.exclusions_list.row(item))
            
    def add_custom_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select a Custom Folder to Clean")
        if not folder_path: return
        
        name, ok = QInputDialog.getText(self, "Folder Name", "Enter a name for this button:")
        if ok and name:
            folder_data = {'name': name, 'path': folder_path}
            item = QListWidgetItem(f"{name} ({folder_path})")
            item.setData(Qt.ItemDataRole.UserRole, folder_data)
            self.custom_folders_list.addItem(item)

    def remove_custom_folder(self):
        for item in self.custom_folders_list.selectedItems():
            self.custom_folders_list.takeItem(self.custom_folders_list.row(item))

    def accept(self):
        self.settings.setValue("confirm_cleanup", self.confirm_checkbox.isChecked())
        self.settings.setValue("recycle_bin_age_enabled", self.rb_age_checkbox.isChecked())
        self.settings.setValue("recycle_bin_age_days", self.rb_age_spinbox.value())
        
        exclusions = [self.exclusions_list.item(i).text() for i in range(self.exclusions_list.count())]
        self.settings.setValue("exclusions", exclusions)

        custom_folders = []
        for i in range(self.custom_folders_list.count()):
            item = self.custom_folders_list.item(i)
            folder_data = item.data(Qt.ItemDataRole.UserRole)
            custom_folders.append(json.dumps(folder_data))
        self.settings.setValue("custom_folders", custom_folders)
        
        super().accept()

class Worker(QObject):
    finished = Signal()
    progress = Signal(int, int)
    log = Signal(str)

    def __init__(self, target_function, *args, **kwargs):
        super().__init__()
        self.target_function = target_function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        try:
            if "progress_callback" in self.target_function.__code__.co_varnames:
                self.kwargs["progress_callback"] = lambda current, total: self.progress.emit(current, total)
            self.target_function(*self.args, **self.kwargs)
        except Exception as e:
            self.log.emit(f"Error: {str(e)}")
            logic.logging.error(f"Error in worker thread: {e}")
        finally:
            self.finished.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = QSettings("WinClean-GUI", "App")
        
        self.setWindowTitle("WinClean-GUI")
        self.setGeometry(100, 100, 600, 700)

        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
                font-family: 'Segoe UI';
                font-size: 10pt;
            }
            QPushButton {
                background-color: #4a4a4a;
                border: 1px solid #5a5a5a;
                padding: 8px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5a5a5a;
                border: 1px solid #6a6a6a;
            }
            QPushButton:pressed {
                background-color: #6a6a6a;
            }
            QLabel#title {
                font-size: 18pt;
                font-weight: bold;
                padding-bottom: 10px;
            }
            QTextEdit {
                background-color: #202020;
                border: 1px solid #4a4a4a;
                border-radius: 5px;
            }
            QProgressBar {
                border: 1px solid #5a5a5a;
                border-radius: 5px;
                text-align: center;
                background-color: #4a4a4a;
            }
            QProgressBar::chunk {
                background-color: #0078d4;
                border-radius: 4px;
            }
        """)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)

        title_label = QLabel("WinClean-GUI")
        title_label.setObjectName("title")
        self.main_layout.addWidget(title_label)
        
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.main_layout.addWidget(self.grid_widget)
        
        self.repopulate_buttons()
        
        self.settings_button = QPushButton("Settings")
        self.settings_button.setIcon(QApplication.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogDetailedView))
        self.settings_button.setCursor(Qt.PointingHandCursor)
        self.settings_button.clicked.connect(self.open_settings_dialog)
        self.main_layout.addWidget(self.settings_button)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.main_layout.addWidget(self.progress_bar)
        
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.main_layout.addWidget(self.log_output)
        
        self.append_log("Welcome to WinClean-GUI! Please select an action.")
        self.thread = None
        self.worker = None

    def repopulate_buttons(self):
        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        self.buttons = {}
        style = QApplication.style()

        tasks = [
            {'name': 'clean_desktop', 'text': 'Clean Desktop', 'func': logic.clean_directory, 'args_provider': lambda: [logic.DIRECTORIES["desktop"][0]], 'tooltip': 'Deletes all files and folders from your desktop.', 'icon': QStyle.StandardPixmap.SP_DesktopIcon, 'destructive': True},
            {'name': 'clean_temp', 'text': 'Clean Temp Folder', 'func': logic.clean_directory, 'args_provider': lambda: [logic.DIRECTORIES["temp"][0]], 'tooltip': 'Deletes temporary system files.', 'icon': QStyle.StandardPixmap.SP_DirIcon, 'destructive': True},
            {'name': 'clean_appdata_roaming', 'text': 'Clean AppData Roaming', 'func': logic.clean_directory, 'args_provider': lambda: [logic.DIRECTORIES["appdata_roaming"][0]], 'tooltip': 'Clears roaming application data.', 'icon': QStyle.StandardPixmap.SP_DirIcon, 'destructive': True},
            {'name': 'clean_appdata_local', 'text': 'Clean Local AppData', 'func': logic.clean_directory, 'args_provider': lambda: [logic.DIRECTORIES["appdata_local"][0]], 'tooltip': 'Clears local application data and cache.', 'icon': QStyle.StandardPixmap.SP_DirIcon, 'destructive': True},
            {'name': 'empty_recycle_bin', 'text': 'Empty Recycle Bin', 'func_provider': self.get_recycle_bin_function, 'args_provider': self.get_recycle_bin_args, 'tooltip': 'Permanently deletes items in the Recycle Bin.', 'icon': QStyle.StandardPixmap.SP_TrashIcon, 'destructive': True},
            {'name': 'disk_cleanup', 'text': 'Run Disk Cleanup', 'func': logic.run_disk_cleanup, 'args_provider': lambda: [], 'tooltip': 'Launches the built-in Windows Disk Cleanup utility.', 'icon': QStyle.StandardPixmap.SP_DriveHDIcon, 'destructive': False},
            {'name': 'disk_defrag', 'text': 'Run Disk Defragmenter', 'func': logic.run_disk_defragmenter, 'args_provider': lambda: [], 'tooltip': 'Launches the Windows Drive Optimizer.', 'icon': QStyle.StandardPixmap.SP_DriveHDIcon, 'destructive': False}
        ]
        
        custom_folders_str = self.settings.value("custom_folders", [], type=list)
        for f_str in custom_folders_str:
            folder_data = json.loads(f_str)
            task = {
                'name': f"custom_{folder_data['name']}", 
                'text': folder_data['name'], 
                'func': logic.clean_directory, 
                'args_provider': lambda p=folder_data['path']: [p],
                'tooltip': f"Cleans the folder: {folder_data['path']}", 
                'icon': QStyle.StandardPixmap.SP_DirOpenIcon,
                'destructive': True
            }
            tasks.append(task)

        positions = [(i, j) for i in range((len(tasks) + 1) // 2) for j in range(2)]
        for task, pos in zip(tasks, positions):
            button = QPushButton(task['text'])
            button.setIcon(style.standardIcon(task['icon']))
            button.setIconSize(QSize(24, 24))
            button.setToolTip(task['tooltip'])
            button.setCursor(Qt.PointingHandCursor)
            button.clicked.connect(lambda checked, t=task: self.run_task(t))
            self.grid_layout.addWidget(button, pos[0], pos[1])
            self.buttons[task['name']] = button

    def get_recycle_bin_function(self):
        if self.settings.value("recycle_bin_age_enabled", False, type=bool):
            return logic.empty_recycle_bin_by_age
        return logic.empty_recycle_bin

    def get_recycle_bin_args(self):
        if self.settings.value("recycle_bin_age_enabled", False, type=bool):
            days = self.settings.value("recycle_bin_age_days", 30, type=int)
            return [days]
        return []

    def open_settings_dialog(self):
        dialog = SettingsDialog(self)
        if dialog.exec():
            self.append_log("Settings updated. Button layout has been refreshed.")
            self.repopulate_buttons()

    def run_task(self, task):
        if task['destructive'] and self.settings.value("confirm_cleanup", True, type=bool):
            reply = QMessageBox.question(self, 'Confirmation', f"Are you sure you want to run '{task['text']}'?\nThis action cannot be undone.",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.No:
                self.append_log(f"Cancelled: {task['text']}.")
                return

        if 'func_provider' in task:
            func = task['func_provider']()
        else:
            func = task['func']
        args_provider = task.get('args_provider')
        args = args_provider() if args_provider else []
        
        kwargs = {}
        if func == logic.clean_directory:
            kwargs['exclusions'] = self.settings.value("exclusions", [], type=list)
        
        self.toggle_buttons(False)
        self.progress_bar.setValue(0)
        is_progress_task = "progress_callback" in func.__code__.co_varnames
        self.progress_bar.setVisible(is_progress_task)
        self.append_log(f"Starting: {task['text']}...")

        self.thread = QThread()
        self.worker = Worker(func, *args, **kwargs)
        self.worker.moveToThread(self.thread)

        self.worker.progress.connect(self.update_progress)
        self.worker.log.connect(self.append_log)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(lambda: self.on_task_finished(task['text']))

        self.thread.start()

    def update_progress(self, current, total):
        if total > 0:
            percentage = int((current / total) * 100)
            self.progress_bar.setValue(percentage)

    def append_log(self, message):
        self.log_output.append(message)

    def on_task_finished(self, task_name):
        self.append_log(f"Finished: {task_name}.")
        self.progress_bar.setValue(100)
        self.toggle_buttons(True)
        
    def toggle_buttons(self, enabled):
        for button in self.buttons.values():
            button.setEnabled(enabled)
        self.settings_button.setEnabled(enabled)

if __name__ == "__main__":
    if not logic.is_admin():
        logic.run_as_admin()
    
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())