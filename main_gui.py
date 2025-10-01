import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
import cleanup_logic as logic

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # --- Настройка главного окна ---
        self.setWindowTitle("System Cleaner")
        self.setGeometry(100, 100, 400, 500) # x, y, ширина, высота

        # --- Центральный виджет и компоновка ---
        # Все элементы интерфейса будут размещаться на центральном виджете
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Мы будем использовать вертикальную компоновку (элементы друг под другом)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # --- Создание элементов интерфейса ---
        # Пока создадим простой заголовок и одну кнопку для примера
        
        title_label = QLabel("FluentCleaner") # Используем наше новое название
        # Устанавливаем стиль для заголовка
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; padding: 10px;")
        
        # Пример кнопки
        clean_temp_button = QPushButton("Clean Temp Folder")
        clean_temp_button.setFixedSize(200, 40) # Зададим фиксированный размер

        # --- Добавление элементов в компоновку ---
        layout.addWidget(title_label)
        layout.addWidget(clean_temp_button)
        
        # --- Подключение сигналов к слотам (обработка нажатий) ---
        # Пока оставим это пустым, мы добавим логику на следующем шаге.
        # clean_temp_button.clicked.connect(self.clean_temp_action)


# --- Точка входа в приложение ---
if __name__ == "__main__":
    # Проверяем права администратора перед запуском GUI
    if not logic.is_admin():
        logic.run_as_admin()
    
    # Создаем экземпляр приложения
    app = QApplication(sys.argv)
    
    # Создаем и показываем главное окно
    window = MainWindow()
    window.show()
    
    # Запускаем главный цикл приложения
    sys.exit(app.exec())