# Desktop-Cleaner-Script

## Description
This Python script automates the process of cleaning up your Windows desktop, emptying the Recycle Bin, and clearing temporary files. It's designed to help you maintain a tidy system with minimal effort.

## Features
- Cleans the desktop by removing all files and folders
- Empties the Recycle Bin
- Clears temporary files from the %TEMP% folder

## Requirements
- Python 3.x
- Windows operating system
- `winshell` library (install with `pip install winshell`)

## Usage
1. Ensure you have Python installed on your system.
2. Install the required `winshell` library.
3. Run the script.

## Warning
This script permanently deletes files and folders. Use with caution and ensure you have backups of important data before running.

## Functions

### `clean_desktop()`
Removes all files and folders from the user's desktop.

### `empty_recycle_bin()`
Empties the Windows Recycle Bin without confirmation.

### `clean_temp_folder()`
Deletes all files and folders from the Windows temporary folder.

## Error Handling
The script includes basic error handling and will print messages for any errors encountered during the cleaning process.

## Customization
You can modify the script to exclude certain files or folders from deletion by adding conditions to the respective functions.

## Contributing
Contributions, issues, and feature requests are welcome. Feel free to check [issues page] if you want to contribute.

## License
This project is licensed under the MIT License.

## Disclaimer
This script is provided as-is, without any warranties. The author is not responsible for any data loss or system damage resulting from the use of this script.
      
