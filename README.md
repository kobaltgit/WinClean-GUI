# Desktop-Cleaner-Script

## Description
This Python script automates the process of cleaning up various directories on your Windows system, emptying the Recycle Bin, and performing system maintenance tasks like Disk Cleanup and Disk Defragmentation. It's designed to help you maintain a tidy and optimized system with minimal effort through an interactive menu-driven interface.

## Features
- **Menu-Driven Interface**: Select specific cleanup and maintenance operations from a numbered list.
- **Cleans Multiple Directories**:
  - Desktop
  - Temporary Files (`%TEMP%` folder)
  - AppData (Roaming) folder (`%AppData%`)
  - Local AppData folder (`%LocalAppData%`)
- **Empties Recycle Bin**: Permanently removes all items from the Windows Recycle Bin.
- **Runs Disk Cleanup**: Executes the built-in Windows Disk Cleanup utility to free up space.
- **Runs Disk Defragmenter**: Optimizes the system drive for better performance.
- **Automatic Administrative Privilege Elevation**: Requests elevated permissions to perform system-level tasks.
- **Progress Indicators**: Visual feedback using progress bars during cleanup operations.
- **Logging**: Logs errors and warnings to `cleanup.log` for troubleshooting.

## Requirements
- **Operating System**: Windows
- **Python Version**: Python 3.x
- **Python Libraries**:
  - [`winshell`](https://pypi.org/project/winshell/) (Install with `pip install winshell`)
  - [`tqdm`](https://pypi.org/project/tqdm/) (Install with `pip install tqdm`)
  - [`pywin32`](https://pypi.org/project/pywin32/) (Install with `pip install pywin32`)

## Installation
1. **Ensure Python is Installed**:
   - Download and install Python from the [official website](https://www.python.org/downloads/) if it's not already installed.

2. **Clone the Repository or Download the Script**:
   - Clone this repository using Git:
     ```bash
     git clone https://github.com/Catefishh/Desktop-Cleaner-Script.git
     ```
   - Or download the `cleanup_script.py` directly.

3. **Install Required Libraries**:
   - Open Command Prompt and navigate to the script's directory.
   - Install the necessary Python libraries:
     ```bash
     pip install winshell tqdm pywin32
     ```

## Usage
1. **Run the Script**:
   - Navigate to the script's directory in Command Prompt.
   - Execute the script:
     ```bash
     python cleanup_script.py
     ```
   - **Note**: The script will attempt to run with administrative privileges. If prompted by User Account Control (UAC), click "Yes" to grant the necessary permissions.

2. **Interact with the Menu**:
   - Upon running, the script displays a menu with numbered options.
   - Enter the number corresponding to the desired operation and press `Enter`.
   - Follow the on-screen prompts to confirm each action.

3. **Example Operations**:
   - **Clean Desktop**: Removes all files and folders from your Desktop.
   - **Empty Recycle Bin**: Permanently deletes all items in the Recycle Bin.
   - **Run Disk Cleanup**: Opens the Disk Cleanup utility to free up disk space.
   - **Run Disk Defragmenter**: Optimizes the system drive for improved performance.

4. **Exit the Script**:
   - Select the "Exit" option from the menu to terminate the script gracefully.

## Warning
**This script permanently deletes files and folders from selected directories. Use with caution and ensure you have backups of important data before running. Deleting system or application files can lead to system instability or loss of important settings.**

## Functions

### `clean_directory(directory, description)`
Removes all files and folders from the specified directory with a progress indicator.

### `empty_recycle_bin()`
Empties the Windows Recycle Bin without confirmation prompts.

### `run_disk_cleanup()`
Launches the Windows Disk Cleanup (`cleanmgr.exe`) utility to free up disk space.

### `run_disk_defragmenter()`
Runs the Windows Disk Defragmenter (`defrag.exe`) on the system drive to optimize performance.

### `is_admin()`
Checks if the script is running with administrative privileges.

### `run_as_admin()`
Attempts to restart the script with administrative privileges if not already running as an administrator.

### `display_menu()`
Displays the interactive menu of available cleanup and maintenance operations.

### `get_user_choice()`
Prompts the user to select an option from the menu and validates the input.

### `user_confirmation(message)`
Prompts the user for a yes/no confirmation before performing an action.

## Error Handling
The script includes comprehensive error handling and logs all errors and warnings to `cleanup.log` located in the script's directory. Review this log file for detailed information about any issues encountered during the cleanup process.

## Customization
You can modify the script to include or exclude specific directories by updating the `directories_to_clean` dictionary in the `main()` function. Additionally, you can adjust or add new cleanup operations by defining new functions and adding corresponding menu options.

## Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/yourusername/Desktop-Cleaner-Script/issues) if you want to contribute.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Disclaimer
This script is provided as-is, without any warranties. The author is not responsible for any data loss or system damage resulting from the use of this script. Use at your own risk.

