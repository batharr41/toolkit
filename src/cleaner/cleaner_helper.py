import shutil
import tempfile
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Callable, Dict, Any, List
from platformdirs import user_downloads_dir

# 500 MB (500 * 1024 * 1024 bytes)
LARGE_FILE_LIMIT_BYTES = 524288000
# 3 months (approx 90 days)
OLD_FILE_LIMIT_SECONDS = 90 * 24 * 60 * 60


def delete_file_safely(path: Path, logger: Callable[[str], None]):
    """Safely attempts to delete a file and logs the result."""
    try:
        if path.is_file():
            path.unlink()
            logger(f"  [DELETED] File: {path.name}")
        elif path.is_dir() and not list(path.iterdir()):
            # Only delete empty directories for temp folders
            path.rmdir()
            logger(f"  [DELETED] Empty Directory: {path.name}")

    except OSError as e:
        logger(f"  [FAILED] Could not delete {path.name}. Error: {e}")
    except Exception as e:
        logger(f"  [FAILED] Unexpected error with {path.name}. Error: {e}")


def run_clean_logic(options: Dict[str, bool], logger: Callable[[str], None]):
    """
    Runs safe, non-strict disk cleanup based on provided options.

    Args:
        options: A dictionary of cleaning options (e.g., {"temp_files": True}).
        logger: A function to output messages (e.g., print or a custom log function).
    """
    logger("=" * 40)
    logger(f"Cleanup Run Started at {datetime.now().strftime('%H:%M:%S')}")
    logger("=" * 40)

    files_deleted_count = 0
    now_ts = time.time()
    three_months_ago_ts = now_ts - OLD_FILE_LIMIT_SECONDS

    # --- 1. Clean Temporary Files ---
    if options.get("temp_files"):
        logger("\n[Task] Checking System Temporary Files...")
        temp_dir = Path(tempfile.gettempdir())

        if not temp_dir.exists():
            logger("  Temp directory not found or inaccessible.")

        for item in temp_dir.iterdir():
            # A safe check: only delete files older than 1 day to avoid
            # deleting temporary files used by currently running programs.
            try:
                if item.stat().st_mtime < (now_ts - 24 * 60 * 60):
                    delete_file_safely(item, logger)
                    files_deleted_count += 1
                else:
                    logger(
                        f"  [SKIPPED] {item.name}: Too recent (less than 24 hours old)."
                    )
            except Exception as e:
                logger(f"  [SKIPPED] Cannot access stats for {item.name}: {e}")

    # --- 2. Check Large & Old Files (Downloads Root Only) ---
    if options.get("large_old"):
        logger("\n[Task] Checking Large & Old Files in Downloads Root...")

        try:
            downloads_path = Path(user_downloads_dir())
        except Exception:
            logger("  Could not determine downloads directory path.")
            downloads_path = None

        if downloads_path and downloads_path.exists():
            for item in downloads_path.iterdir():
                if item.is_file():
                    try:
                        file_stat = item.stat()

                        # Check 1: Size > 500 MB
                        is_large = file_stat.st_size > LARGE_FILE_LIMIT_BYTES

                        # Check 2: Last accessed or modified time > 3 months ago
                        # Use max of st_atime (access) and st_mtime (modified) for robustness
                        last_activity_ts = max(file_stat.st_atime, file_stat.st_mtime)
                        is_old = last_activity_ts < three_months_ago_ts

                        if is_large and is_old:
                            logger(f"  [CANDIDATE] Found: {item.name}")
                            logger(
                                f"    Size: {round(file_stat.st_size / 1024 / 1024, 2)} MB. Age: > 3 months."
                            )

                            # Log action, but DO NOT DELETE YET (Crucial Safety Step)
                            # In a cleaner, files should be quarantined or confirmed.
                            # For this function, we just log it as a finding.

                        elif is_large:
                            logger(f"  [SKIPPED] {item.name}: Large, but too recent.")
                        elif is_old:
                            logger(f"  [SKIPPED] {item.name}: Old, but too small.")

                    except OSError as e:
                        logger(
                            f"  [SKIPPED] Cannot access file stats for {item.name}: {e}"
                        )

        elif downloads_path:
            logger(f"  Downloads directory does not exist at: {downloads_path}")

    # --- 3. Browser Cache (Not Implemented for Safety) ---
    if options.get("browser_cache"):
        logger("\n[Task] Checking Browser Cache...")
        logger("  [SKIPPED] Browser cache deletion is work in progress!!")

    logger("\n" + "=" * 40)
    logger(f"Cleanup Run Finished. Files deleted: {files_deleted_count}")
    logger("=" * 40)


# --- Demonstration ---
if __name__ == "__main__":

    # 1. Define the logger function (simple print output)
    def simple_logger(message):
        print(message)

    # 2. Define a dummy options map
    clean_options = {
        "temp_files": True,
        "browser_cache": True,
        "large_old": True,
    }

    # 3. Create a dummy file in the temp directory for demonstration
    # This file will be 1 day and 1 minute old, so it should be deleted
    # when the "temp_files" option is set to True.
    dummy_path = Path(tempfile.gettempdir()) / "test_old_log.tmp"
    with open(dummy_path, "w") as f:
        f.write("This is an old test file.")

    # Move the file's modification time back 2 days
    old_time = time.time() - (2 * 24 * 60 * 60)
    # The item's mtime must be manually updated for the check to work
    import os

    os.utime(dummy_path, (old_time, old_time))

    simple_logger(f"Created dummy temp file for test: {dummy_path}")

    # 4. Run the cleanup logic
    run_clean_logic(clean_options, simple_logger)

    # 5. Verify deletion
    if not dummy_path.exists():
        simple_logger("\nVerification: Dummy temp file was successfully deleted.")
    else:
        simple_logger(
            "\nVerification: Dummy temp file was NOT deleted (Check file age/permissions)."
        )
