import os
import shutil
import winshell
import logging
import subprocess
import sys
import ctypes
from tqdm import tqdm

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
        print("Failed to elevate privileges. Please run the script as an administrator manually.")
    sys.exit()

def user_confirmation(message):
    while True:
        response = input(f"{message} (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        else:
            print("Please enter 'y' or 'n'.")

def clean_directory(directory, description):
    if not os.path.exists(directory):
        logging.warning(f"Directory does not exist: {directory}")
        print(f"Directory does not exist: {description}. Skipping.")
        return

    if not user_confirmation(f"Do you want to clean the {description}?"):
        print(f"Skipping {description} cleaning.")
        return

    try:
        total_items = sum(1 for _ in os.scandir(directory))
        with tqdm(total=total_items, desc=f"Cleaning {description}", unit="item") as pbar:
            for entry in os.scandir(directory):
                try:
                    if entry.is_file() or entry.is_symlink():
                        os.unlink(entry.path)
                    elif entry.is_dir():
                        shutil.rmtree(entry.path)
                except Exception as e:
                    logging.error(f"Error deleting {entry.path}: {e}")
                pbar.update(1)
        print(f"Finished cleaning {description}.")
    except Exception as e:
        logging.error(f"Error accessing {description} directory: {e}")
        print(f"An error occurred while cleaning {description}. Check the log for details.")

def empty_recycle_bin():
    if not user_confirmation("Do you want to empty the Recycle Bin?"):
        print("Skipping Recycle Bin emptying.")
        return

    try:
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
        print("Recycle Bin emptied successfully.")
    except Exception as e:
        logging.error(f"Error emptying Recycle Bin: {e}")
        print("An error occurred while emptying the Recycle Bin. Check the log for details.")

def run_disk_cleanup():
    if not user_confirmation("Do you want to run Windows Disk Cleanup?"):
        print("Skipping Disk Cleanup.")
        return

    try:
        print("Starting Disk Cleanup...")
        subprocess.run(["cleanmgr.exe"], check=True)
        print("Disk Cleanup completed.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Disk Cleanup failed: {e}")
        print("An error occurred while running Disk Cleanup. Check the log for details.")
    except FileNotFoundError:
        logging.error("Disk Cleanup utility not found.")
        print("Disk Cleanup utility not found on this system.")

def run_disk_defragmenter():
    if not user_confirmation("Do you want to run Windows Disk Defragmenter?"):
        print("Skipping Disk Defragmenter.")
        return

    try:
        system_drive = os.environ.get("SystemDrive", "C:")
        print(f"Starting Disk Defragmenter on {system_drive}...")
        subprocess.run(["defrag.exe", system_drive, "/O", "/V", "/U"], check=True)
        print("Disk Defragmenter completed.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Disk Defragmenter failed: {e}")
        print("An error occurred while running Disk Defragmenter. Check the log for details.")
    except FileNotFoundError:
        logging.error("Disk Defragmenter utility not found.")
        print("Disk Defragmenter utility not found on this system.")

def display_menu():
    menu = """
    === System Cleanup and Maintenance Menu ===
    Please select an option by entering the corresponding number:

    1. Clean Desktop
    2. Clean Temp Folder
    3. Clean AppData (Roaming) Folder
    4. Clean Local AppData Folder
    5. Empty Recycle Bin
    6. Run Disk Cleanup
    7. Run Disk Defragmenter
    8. Exit

    """
    print(menu)

def get_user_choice():
    while True:
        try:
            choice = int(input("Enter your choice (1-8): ").strip())
            if 1 <= choice <= 8:
                return choice
            else:
                print("Please enter a number between 1 and 8.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 8.")

def main():
    logging.basicConfig(
        filename='cleanup.log',
        level=logging.ERROR,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Defined directories to clean with their descriptions.
    directories_to_clean = {
        1: (os.path.expanduser("~/Desktop"), "Desktop"),
        2: (os.path.expandvars('%TEMP%'), "Temp folder"),
        3: (os.path.expandvars('%AppData%'), "AppData (Roaming) folder"),
        4: (os.path.expandvars('%LocalAppData%'), "Local AppData folder")
    }

    while True:
        display_menu()
        choice = get_user_choice()

        if choice == 1:
            directory, description = directories_to_clean[1]
            clean_directory(directory, description)
        elif choice == 2:
            directory, description = directories_to_clean[2]
            clean_directory(directory, description)
        elif choice == 3:
            directory, description = directories_to_clean[3]
            clean_directory(directory, description)
        elif choice == 4:
            directory, description = directories_to_clean[4]
            clean_directory(directory, description)
        elif choice == 5:
            empty_recycle_bin()
        elif choice == 6:
            run_disk_cleanup()
        elif choice == 7:
            run_disk_defragmenter()
        elif choice == 8:
            print("Exiting the cleanup script. Goodbye!")
            break

        print("\nOperation completed. Returning to the main menu...\n")

if __name__ == "__main__":
    if not is_admin():
        print("This script requires administrative privileges. Attempting to elevate...")
        run_as_admin()
    else:
        main()
