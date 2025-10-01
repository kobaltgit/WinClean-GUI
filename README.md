# WinClean-GUI

A powerful system maintenance and cleanup utility for Windows, rebuilt with a modern and intuitive graphical user interface inspired by Windows 11's Fluent Design.

This project takes a functional command-line script and elevates it into a user-friendly desktop application, making system maintenance tasks easier and more accessible for everyone.

## ✨ Key Features

- **Intuitive Interface**: A clean and modern UI that is easy to navigate.
- **Selective Cleaning**: Choose exactly what you want to clean:
  - Desktop
  - Temporary Files (`%TEMP%`)
  - AppData Folders (`Roaming` & `Local`)
- **System Tools Integration**:
  - Empty the Recycle Bin with a single click.
  - Launch Windows Disk Cleanup (`cleanmgr.exe`).
  - Run the Disk Defragmenter and Optimizer (`dfrgui.exe`).
- **Safe and Transparent**: The application requires administrative privileges only for necessary tasks and logs all operations for review.
- **Built with Python**: Developed using Python and the powerful PySide6 framework for the GUI.
- **Customizable**: Add your own folders to the cleanup list and create exclusion lists to protect important files.

## 📸 Screenshot

<img src="https://i.ibb.co/cccGNLB3/2025-10-01-120225.png" alt="2025-10-01-120225" border="0">


## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

- [Python 3.8+](https://www.python.org/downloads/)
- `pip` (usually comes with Python)

### Installation & Running

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/kobaltgit/WinClean-GUI
    ```

2.  **Navigate to the project directory:**
    ```sh
    cd WinClean-GUI
    ```

3.  **Install the required dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```sh
    python main_gui.py
    ```
    > **Note:** The application will request administrative privileges upon launch to perform system-level tasks. Please approve the UAC prompt.

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

---
_This project is a fork and a complete GUI redesign of the [original console-based script](https://github.com/Catefishh/Desktop-Cleaner-Script)._
