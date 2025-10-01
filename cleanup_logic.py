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
    Рекурсивно очищает указанную директорию, пропуская пути из списка исключений.
    Сначала удаляет все не-исключенные файлы, затем пытается удалить пустые папки.
    Папки, содержащие исключенные элементы, останутся нетронутыми.

    :param directory: Путь к директории для очистки.
    :param exclusions: Список путей (файлов/папок), которые нужно пропустить.
    :param progress_callback: Функция обратного вызова для обновления прогресса.
    """
    if not os.path.exists(directory):
        logging.warning(f"Directory does not exist: {directory}")
        return

    # Нормализуем пути исключений для корректного сравнения (используем set для быстрой проверки)
    exclusions = {os.path.normpath(ex).lower() for ex in exclusions or []}

    files_to_delete = []
    dirs_to_process = []

    # Шаг 1: Собрать список всех файлов и папок для потенциального удаления
    # Проходим по дереву каталогов сверху вниз
    for root, dirs, files in os.walk(directory, topdown=True):
        # Оптимизация: если текущая папка находится в исключениях, не сканируем ее содержимое
        if os.path.normpath(root).lower() in exclusions:
            dirs[:] = []  # Не спускаться в подпапки
            continue

        # Собираем файлы для удаления
        for name in files:
            file_path = os.path.join(root, name)
            if os.path.normpath(file_path).lower() not in exclusions:
                files_to_delete.append(file_path)

        # Собираем папки для последующей обработки
        for name in dirs:
            dir_path = os.path.join(root, name)
            # Добавляем только те папки, которые сами не являются исключением
            if os.path.normpath(dir_path).lower() not in exclusions:
                dirs_to_process.append(dir_path)

    total_items = len(files_to_delete) + len(dirs_to_process)
    processed_count = 0

    # Шаг 2: Удалить все собранные файлы
    for file_path in files_to_delete:
        try:
            os.unlink(file_path)
        except OSError as e:
            logging.error(f"Error deleting file {file_path}: {e}")

        processed_count += 1
        if progress_callback:
            progress_callback(processed_count, total_items)

    # Шаг 3: Попытаться удалить папки, начиная с самых глубоких
    # Сортировка по длине пути в обратном порядке гарантирует, что мы сначала обработаем дочерние папки
    dirs_to_process.sort(key=len, reverse=True)

    for dir_path in dirs_to_process:
        try:
            os.rmdir(dir_path)
        except OSError:
            # Эта ошибка ожидаема, если папка не пуста (т.е. содержит исключенный файл или папку).
            # Просто пропускаем ее.
            logging.info(f"Directory not empty or could not be removed (likely contains exclusions): {dir_path}")
            pass

        processed_count += 1
        if progress_callback:
            progress_callback(processed_count, total_items)


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
