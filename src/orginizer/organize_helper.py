from pathlib import Path
from typing import List, Tuple
from logic import config
import shutil
import os


def extract_files_from_folder(
    root_folder: str, max_depth: int
) -> Tuple[List[Path], List[Path]]:

    root_path = Path(root_folder).resolve()
    file_paths: List[Path] = []

    def _extract_recursive(current_path: Path, current_depth: int):
        if current_depth > max_depth:
            return

        for item in current_path.iterdir():
            if item.is_file():
                file_paths.append(item)
            elif item.is_dir():
                _extract_recursive(item, current_depth + 1)

    _extract_recursive(root_path, 0)

    return file_paths


def group_files_by_extension(paths: list[str]):
    ext_map = config.getExtensionMap()
    path_group: list[tuple[str, str]] = []
    for path in paths:
        path_obj = Path(path)
        file_ext = path_obj.suffix
        ext = ext_map[file_ext] if file_ext in ext_map else "Others"
        path_group.append((path, ext))
    return path_group


def move_grouped_files(base_path: Path, groups: list[tuple[str, str]]):
    base_path = Path(base_path)
    for file_path_str, group_name in groups:
        try:
            source_path = Path(file_path_str)
            destination_dir = base_path / group_name
            destination_path = destination_dir / source_path.name
            destination_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source_path), str(destination_path))
            print(f"✅ Moved: '{source_path.name}' -> '{group_name}/'")
        except FileNotFoundError:
            print(f"❌ ERROR: Source file not found: {file_path_str}")
        except Exception as e:
            print(f"❌ ERROR moving {file_path_str}: {e}")


def delete_empty_folders(dir_path: str):
    if not os.path.isdir(dir_path):
        print(f"Error: '{dir_path}' is not a valid directory.")
        return

    childs_count = {}
    print(f"Scanning directory: {dir_path}")
    for root, dirnames, filenames in os.walk(dir_path, topdown=False):
        num_children = len(dirnames) + len(filenames)
        childs_count[root] = num_children

    print("\n--- Folder Child Count Map ---")
    for folder, count in childs_count.items():
        print(f"Folder: {folder} | Children: {count}")
    print("------------------------------\n")

    deleted_count = 0
    print("Attempting to delete empty folders...")
    for folder, count in childs_count.items():
        if count == 0 and folder != dir_path:
            try:
                os.rmdir(folder)
                print(f"🗑️ Successfully deleted empty folder: {folder}")
                deleted_count += 1

                parent_dir = os.path.dirname(folder)
                if parent_dir in childs_count:
                    childs_count[parent_dir] -= 1

            except OSError as e:
                print(f"⚠️ Error deleting folder {folder}: {e}")

    print(f"\n--- Deletion Summary ---")
    print(f"Total empty folders deleted: **{deleted_count}**")
    print("--------------------------")


def run_organize(root_dirs: list[str], depth: int, logger):
    for dir in root_dirs:
        logger(f"Extracting files from: {dir}")
        paths = extract_files_from_folder(dir, depth - 1)
        grouped_paths = group_files_by_extension(paths)
        logger(f"Found {len(paths)} files:")
        move_grouped_files(dir, grouped_paths)
        delete_empty_folders(dir)

    logger(f"Operation complete!")


def main():
    roots = ["/home/me/Downloads", "/home/me/Documents", "/home/me/Desktop"]
    roots = ["/home/me/Downloads"]
    run_organize(roots, 1, lambda x: print(x))
