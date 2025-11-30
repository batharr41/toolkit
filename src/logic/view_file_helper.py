import os
import sys
import subprocess
from pathlib import Path


def open_file_with_default_viewer(filepath: str | Path) -> bool:
    """
    Opens a file using the system's default application viewer.
    """
    file_to_open = Path(filepath).resolve()

    if not file_to_open.exists():
        print(f"Error: File not found at {file_to_open}")
        return False

    platform = sys.platform

    try:
        if platform.startswith("darwin"):
            # macOS uses the 'open' command
            subprocess.run(["open", file_to_open], check=True)
            print(f"Opened file on macOS: {file_to_open}")

        elif platform.startswith("win32"):
            # Windows uses os.startfile
            os.startfile(file_to_open)
            print(f"Opened file on Windows: {file_to_open}")

        elif platform.startswith("linux"):
            # Linux (most desktops) uses xdg-open
            subprocess.run(["xdg-open", file_to_open], check=True)
            print(f"Opened file on Linux: {file_to_open}")

        else:
            print(f"Error: Unsupported operating system: {platform}")
            return False

        return True

    except FileNotFoundError:
        # This catches errors if the required command (e.g., 'open', 'xdg-open')
        # is not available in the system's PATH.
        print(
            f"Error: System command not found. Ensure the necessary components are installed."
        )
        return False
    except subprocess.CalledProcessError as e:
        # Catches errors if the command failed (e.g., file permissions)
        print(f"Error executing system command: {e}")
        return False
    except Exception as e:
        # Catch any other unexpected errors
        print(f"An unexpected error occurred: {e}")
        return False
