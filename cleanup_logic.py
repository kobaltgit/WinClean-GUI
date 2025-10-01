import os
import shutil
import winshell
import logging
import subprocess
import sys
import ctypes

# Настраиваем логирование для записи ошибок в файл
logging.basicConfig(
    filename='cleanup.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- Функции для работы с правами администратора ---

def is_admin():
    """Проверяет, запущен ли скрипт с правами администратора."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Перезапускает скрипт с запросом прав администратора."""
    try:
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join([f'"{arg}"' for arg in sys.argv]), None, 1
        )
    except Exception as e:
        logging.error(f"Failed to elevate privileges: {e}")
    sys.exit()

# --- Константы для путей ---

DIRECTORIES = {
    "desktop": (os.path.expanduser("~/Desktop"), "Desktop"),
    "temp": (os.path.expandvars('%TEMP%'), "Temp folder"),
    "appdata_roaming": (os.path.expandvars('%AppData%'), "AppData (Roaming) folder"),
    "appdata_local": (os.path.expandvars('%LocalAppData%'), "Local AppData folder")
}

# --- Основные функции очистки ---

def clean_directory(directory, progress_callback=None):
    """
    Очищает указанную директорию, удаляя все файлы и папки внутри.

    :param directory: Путь к директории для очистки.
    :param progress_callback: Функция обратного вызова для обновления прогресса.
                              Принимает (текущий_элемент, всего_элементов).
    """
    if not os.path.exists(directory):
        logging.warning(f"Directory does not exist: {directory}")
        return

    try:
        # Получаем список всех элементов для подсчета
        items = list(os.scandir(directory))
        total_items = len(items)
        
        for i, entry in enumerate(items):
            try:
                if entry.is_file() or entry.is_symlink():
                    os.unlink(entry.path)
                elif entry.is_dir():
                    shutil.rmtree(entry.path)
            except Exception as e:
                logging.error(f"Error deleting {entry.path}: {e}")
            
            # Вызываем колбэк для обновления прогресс-бара в GUI
            if progress_callback:
                progress_callback(i + 1, total_items)

    except Exception as e:
        logging.error(f"Error accessing directory {directory}: {e}")


def empty_recycle_bin():
    """Очищает корзину Windows."""
    try:
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
    except Exception as e:
        logging.error(f"Error emptying Recycle Bin: {e}")

def run_disk_cleanup():
    """Запускает системную утилиту 'Очистка диска'."""
    try:
        subprocess.Popen(["cleanmgr.exe"])
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logging.error(f"Disk Cleanup failed or not found: {e}")

def run_disk_defragmenter():
    """Запускает системную утилиту 'Дефрагментация диска'."""
    try:
        system_drive = os.environ.get("SystemDrive", "C:")
        # Используем Popen, чтобы не блокировать GUI
        subprocess.Popen(["dfrgui.exe", system_drive])
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logging.error(f"Disk Defragmenter failed or not found: {e}")