import os
import platform
from tkinter import filedialog as fd


def getUserName():
    try:
        name = os.getlogin()
    except:
        name = "User"
    return name.capitalize()


def tryParseInt(no: str, defVal):
    try:
        return int(no)
    except:
        return defVal


def is_linux():
    return platform.system() == "Linux"


def open_file_chooser():
    """Opens a dialog to select a single file for reading."""
    filetypes = (
        ("All files", "*.*"),
        ("Text files", "*.txt"),
        ("Python files", "*.py"),
    )

    # Returns the full path to the selected file, or an empty string if cancelled.
    filename = fd.askopenfilename(
        title="Open a file",
        initialdir="/",  # Start directory (e.g., user's home or root)
        filetypes=filetypes,
    )
    if filename:
        print(f"Selected file: {filename}")
    else:
        print("File selection cancelled.")
    return filename
