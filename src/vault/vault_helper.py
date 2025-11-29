import json
import base64
import os
from pathlib import Path
from typing import Dict, Any, List, Optional
from platformdirs import user_data_dir, user_downloads_dir

# --- Configuration Constants ---
MAX_FILE_SIZE_MB = 20
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
VAULT_FILE_NAME = "vault_data.json"
APP_NAME = "HobbyVault"
APP_AUTHOR = "MyCompany"  # Or your own name/alias


def get_vault_directory() -> Path:
    """
    Returns the absolute, platform-specific path where application data
    (like vault.json) should be stored.
    """

    # user_data_dir() finds the correct OS-specific data path:
    # Windows: ...\AppData\Roaming\HobbyVault
    # macOS: .../Library/Application Support/HobbyVault
    # Linux: .../.local/share/HobbyVault

    # We use 'ensure_exists=True' to create the directory if it doesn't exist
    vault_dir = Path(
        user_data_dir(appname=APP_NAME, appauthor=APP_AUTHOR, ensure_exists=True)
    )

    print(f"Using vault directory: {vault_dir}")
    return vault_dir


FileRecord = Dict[str, str]


class VaultHelper:
    """
    A class to manage files by converting them to Base64 strings for storage
    in a single JSON file. This is for portability/packaging, not security.
    """

    def __init__(self, password: str = "vault", should_delete_originals: bool = False):
        """
        Initializes the vault, loading existing data from the JSON file
        or creating a new vault structure.

        Args:
            password: The password to be stored in the vault metadata.
            should_delete_originals: Flag for deleting original files after adding.
        """
        self.password = password
        self.should_delete_originals = should_delete_originals
        self.file_records: List[FileRecord] = []
        self._load_vault()

    def _get_file_type(self, filepath: Path) -> str:
        """Determines the file category based on its extension."""
        extension = filepath.suffix.lower()
        if extension in [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"]:
            return "photo"
        elif extension in [".mp4", ".mov", ".avi", ".wmv"]:
            return "video"
        elif extension in [".mp3", ".wav", ".flac", ".ogg"]:
            return "audio"
        elif extension in [".pdf", ".doc", ".docx", ".txt", ".rtf", ".md"]:
            return "document"
        else:
            return "other"

    def _load_vault(self):
        """Attempts to load the vault data from the JSON file."""
        vault_path = Path(os.path.join(get_vault_directory(), VAULT_FILE_NAME))
        if vault_path.exists():
            try:
                with open(vault_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                # Load configuration and file records
                self.password = data.get("password", self.password)
                self.should_delete_originals = data.get(
                    "should_delete_originals", self.should_delete_originals
                )
                self.file_records = data.get("file_records", [])
                print(
                    f"Vault loaded successfully from {VAULT_FILE_NAME}. {len(self.file_records)} files found."
                )
            except Exception as e:
                print(f"Error loading vault file: {e}. Starting with an empty vault.")
        else:
            print(f"No existing vault file found. Starting new vault.")

    def save_vault(self):
        """Saves the entire vault state (metadata + files) to the JSON file."""
        vault_path = Path(os.path.join(get_vault_directory(), VAULT_FILE_NAME))
        vault_data = {
            "password": self.password,
            "should_delete_originals": self.should_delete_originals,
            "file_records": self.file_records,
        }

        try:
            with open(vault_path, "w", encoding="utf-8") as f:
                json.dump(vault_data, f, indent=4)
            print(f"Vault saved successfully to {VAULT_FILE_NAME}")
        except Exception as e:
            print(f"ERROR: Could not save vault data. Reason: {e}")

    def add_file(self, filepath: Path, should_delete: Optional[bool] = None) -> bool:
        """
        Reads a file, converts it to Base64, and adds it to the records.

        Args:
            filepath: The path to the file to be added.
            should_delete: Overrides the vault's default delete flag for this file.

        Returns:
            True if the file was added, False otherwise.
        """
        filepath = Path(filepath)
        if not filepath.exists():
            print(f"Error: File not found at {filepath}")
            return False

        file_size = os.path.getsize(filepath)
        if file_size > MAX_FILE_SIZE_BYTES:
            print(
                f"FAILURE: File size ({file_size / (1024*1024):.2f} MB) exceeds the {MAX_FILE_SIZE_MB} MB limit. File not added."
            )
            return False

        try:
            # 1. Read and Base64 encode the file content
            with open(filepath, "rb") as f:
                raw_data = f.read()
                base64_data = base64.b64encode(raw_data).decode("utf-8")

            # 2. Check for duplicate filename (simple check)
            if any(r["filename"] == filepath.name for r in self.file_records):
                print(
                    f"Warning: File with name '{filepath.name}' already exists in the vault. Skipping."
                )
                return False

            # 3. Create the new record
            new_record: FileRecord = {
                "filename": filepath.name,
                "data": base64_data,
                "type": self._get_file_type(filepath),
            }
            self.file_records.append(new_record)

            # 4. Handle deletion
            delete_flag = (
                should_delete
                if should_delete is not None
                else self.should_delete_originals
            )
            if delete_flag:
                os.remove(filepath)
                print(
                    f"SUCCESS: '{filepath.name}' added (Base64), original file deleted."
                )
            else:
                print(
                    f"SUCCESS: '{filepath.name}' added (Base64), original file retained."
                )
            self.save_vault()
            return True
        except Exception as e:
            print(f"An error occurred while adding file: {e}")
            return False

    def delete_file(self, filename: str) -> bool:
        """Deletes a single file record from the vault by filename."""
        initial_count = len(self.file_records)
        self.file_records = [r for r in self.file_records if r["filename"] != filename]

        if len(self.file_records) < initial_count:
            print(f"Deleted file record: '{filename}'")
            self.save_vault()
            return True
        else:
            print(f"Error: File record '{filename}' not found.")
            return False

    def delete_at(self, pos: int) -> bool:
        """Deletes a single file record at the given position"""
        del self.file_records[pos]
        self.save_vault()

    def delete_all(self) -> int:
        """Deletes all file records from the vault."""
        count = len(self.file_records)
        self.file_records = []
        print(f"Deleted all {count} file records from the vault.")
        self.save_vault()
        return count

    def decode_and_save_file(
        self, filename: str, output_dir: Path = None
    ) -> Optional[Path]:
        """
        Decodes the Base64 data of a file record and saves it to disk.

        Args:
            filename: The filename of the record to decode.
            output_dir: The directory where the file should be saved.

        Returns:
            The path to the newly saved file, or None if failed.
        """
        if not output_dir:
            output_dir = Path(user_downloads_dir())

        record = next((r for r in self.file_records if r["filename"] == filename), None)

        if record is None:
            print(f"Error: File record '{filename}' not found in vault.")
            return None

        output_path = output_dir / record["filename"]

        try:
            # 1. Decode the Base64 data
            raw_data = base64.b64decode(record["data"])

            # 2. Write the raw binary data back to disk
            with open(output_path, "wb") as f_out:
                f_out.write(raw_data)

            print(
                f"Successfully decoded and saved '{filename}' to {output_path.resolve()}"
            )
            return output_path
        except Exception as e:
            print(f"An error occurred during decoding/saving: {e}")
            return None

    def get_files(self):
        records = []
        for rec in self.file_records:
            record = rec
            record["name"] = rec["filename"]
            records.append(record)
        return records


# --- Example Usage Demonstration ---
def run_vault_demonstration():
    """Demonstrates the functionality of the HobbyVault class."""

    # Clean up previous run files if they exist
    for f in [
        Path("test_file_1.txt"),
        Path("test_file_2.py"),
        Path("recovered_file.txt"),
        Path(VAULT_FILE_NAME),
    ]:
        if f.exists():
            os.remove(f)

    print("--- Starting Vault Demonstration ---")

    # 1. Setup - Create dummy files
    file1_path = Path("test_file_1.txt")
    file2_path = Path("test_file_2.py")

    with open(file1_path, "w") as f:
        f.write("A simple text document.")
    with open(file2_path, "w") as f:
        f.write("print('Hello Vault!')\n# This is a Python file")

    print(f"Created dummy files: {file1_path.name}, {file2_path.name}")

    # 2. Initialize and Add Files
    vault = VaultHelper(password="MySecretVaultKey", should_delete_originals=False)

    # Add first file (retaining original)
    vault.add_file(file1_path, should_delete=False)

    # Add second file (deleting original)
    vault.add_file(file2_path, should_delete=True)

    # 3. Check if original files were deleted/retained
    print(f"Original {file1_path.name} exists: {file1_path.exists()}")
    print(f"Original {file2_path.name} exists: {file2_path.exists()}")

    # 4. Attempt to add a file that's too big (simulated check)
    # Since we can't create a real 20MB file easily, we'll manually check the size logic.
    vault._load_vault = lambda: None  # Mock load to prevent overwriting during test
    print(f"\n--- Testing max file size limit ({MAX_FILE_SIZE_MB}MB) ---")

    # Temporarily override size check to simulate failure with a small temp file
    if os.path.exists("temp_large.bin"):
        os.remove("temp_large.bin")
    Path("temp_large.bin").touch()

    original_getsize = os.path.getsize
    # Mock file size to be over the limit (e.g., 25MB)
    os.path.getsize = lambda p: MAX_FILE_SIZE_BYTES + 5 * 1024 * 1024
    vault.add_file(Path("temp_large.bin"))

    # Restore original function
    os.path.getsize = original_getsize
    if os.path.exists("temp_large.bin"):
        os.remove("temp_large.bin")

    print("\n--- Current Vault State ---")
    print(f"Files in vault: {[r['filename'] for r in vault.file_records]}")

    # 5. Save the vault state to disk
    vault.save_vault()

    # 6. Initialize a new vault instance to test loading from JSON
    print("\n--- Loading Vault from JSON ---")
    vault_loaded = VaultHelper(
        password="AnyOldPassword"
    )  # Password loading from JSON will overwrite this initial value
    print(f"Loaded records: {[r['filename'] for r in vault_loaded.file_records]}")
    print(f"Loaded password: {vault_loaded.password}")

    # 7. Decode and Save File
    print("\n--- Decoding and Saving File ---")
    saved_path = vault_loaded.decode_and_save_file("test_file_1.txt", Path("."))

    # 8. Test delete file
    vault_loaded.delete_file("test_file_2.py")
    vault_loaded.save_vault()

    # 9. Clean up
    if saved_path and saved_path.exists():
        os.remove(saved_path)
    if file1_path.exists():
        os.remove(file1_path)
    if Path(VAULT_FILE_NAME).exists():
        os.remove(VAULT_FILE_NAME)
    print("\n--- Demonstration Complete ---")


if __name__ == "__main__":
    run_vault_demonstration()
