import os
import shutil
import winshell
import logging
import subprocess
import sys
import ctypes
from datetime import datetime, timedelta

# Настраиваем логирование для записи ошибок в файл
logging.basicConfig(
    filename='cleanup.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# --- Функции для работы с правами администратора ---

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
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

def clean_directory(directory, exclusions=None, progress_callback=None):
    """
    Очищает указанную директорию, пропуская пути из списка исключений.
    
    :param directory: Путь к директории для очистки.
    :param exclusions: Список путей (файлов/папок), которые нужно пропустить.
    :param progress_callback: Функция обратного вызова для обновления прогресса.
    """
    if not os.path.exists(directory):
        logging.warning(f"Directory does not exist: {directory}")
        return

    # Нормализуем пути исключений для корректного сравнения
    exclusions = [os.path.normpath(ex).lower() for ex in exclusions or []]
    
    try:
        items_to_delete = []
        # Сначала собираем список того, что нужно удалить, проверяя исключения
        for entry in os.scandir(directory):
            normalized_path = os.path.normpath(entry.path).lower()
            # Проверяем, не начинается ли путь элемента с одного из путей исключений
            if not any(normalized_path.startswith(ex_path) for ex_path in exclusions):
                items_to_delete.append(entry)

        total_items = len(items_to_delete)
        for i, entry in enumerate(items_to_delete):
            try:
                if entry.is_file() or entry.is_symlink():
                    os.unlink(entry.path)
                elif entry.is_dir():
                    shutil.rmtree(entry.path)
            except Exception as e:
                logging.error(f"Error deleting {entry.path}: {e}")
            
            if progress_callback:
                progress_callback(i + 1, total_items)

    except Exception as e:
        logging.error(f"Error accessing directory {directory}: {e}")


def empty_recycle_bin():
    """Полностью очищает корзину Windows."""
    try:
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
    except Exception as e:
        logging.error(f"Error emptying Recycle Bin: {e}")


def empty_recycle_bin_by_age(days):
    """
    Удаляет из корзины только те элементы, которые старше указанного количества дней.
    """
    try:
        recycle_bin = winshell.recycle_bin()
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # winshell может возвращать элементы в виде генератора, преобразуем в список
        items_to_check = list(recycle_bin)
        
        for item in items_to_check:
            # recycle_date() может быть None для некоторых элементов
            if item.recycle_date() and item.recycle_date() < cutoff_date:
                try:
                    # Удаляем конкретный элемент
                    recycle_bin.dispose(item)
                except Exception as e:
                    logging.error(f"Could not dispose item {item.original_filename()}: {e}")
    except Exception as e:
        logging.error(f"Error during age-based Recycle Bin cleanup: {e}")


def run_disk_cleanup():
    """Запускает системную утилиту 'Очистка диска'."""
    try:
        subprocess.Popen(["cleanmgr.exe"])
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logging.error(f"Disk Cleanup failed or not found: {e}")

def run_disk_defragmenter():
    """Запускает системную утилиту 'Дефрагментация диска'."""
    try:
        subprocess.Popen(["dfrgui.exe"])
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        logging.error(f"Disk Defragmenter failed or not found: {e}")