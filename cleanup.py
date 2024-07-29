import os
import shutil
import winshell
import logging
from tqdm import tqdm

def user_confirmation(message):
    while True:
        response = input(f"{message} (y/n): ").lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' or 'n'.")

def clean_directory(directory, description):
    if not user_confirmation(f"Do you want to clean the {description}?"):
        print(f"Skipping {description} cleaning.")
        return

    total_items = sum(1 for _ in os.scandir(directory))
    with tqdm(total=total_items, desc=f"Cleaning {description}", unit="item") as pbar:
        for entry in os.scandir(directory):
            try:
                if entry.is_file():
                    os.unlink(entry.path)
                elif entry.is_dir():
                    shutil.rmtree(entry.path)
            except Exception as e:
                logging.error(f"Error deleting {entry.path}: {e}")
            pbar.update(1)

def empty_recycle_bin():
    if not user_confirmation("Do you want to empty the Recycle Bin?"):
        print("Skipping Recycle Bin emptying.")
        return

    try:
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
        print("Recycle Bin emptied successfully")
    except Exception as e:
        logging.error(f"Error emptying Recycle Bin: {e}")

def main():
    logging.basicConfig(filename='cleanup.log', level=logging.ERROR,
                        format='%(asctime)s - %(levelname)s - %(message)s')

    desktop = os.path.expanduser("~/Desktop")
    temp = os.path.expandvars('%TEMP%')

    empty_recycle_bin()
    clean_directory(temp, "Temp folder")

    print("Cleaning completed")
    print("Check 'cleanup.log' for any errors encountered during the process.")

if __name__ == "__main__":
    main()