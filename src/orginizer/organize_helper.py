from pathlib import Path
from typing import List, Tuple
from logic import config
import shutil


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


def run_organize(root_dirs: list[str], depth: int, logger):
    for dir in root_dirs:
        logger(f"Extracting files from: {dir}")
        paths = extract_files_from_folder(dir, depth - 1)
        grouped_paths = group_files_by_extension(paths)
        logger(f"Found {len(paths)} files:")
        move_grouped_files(dir, grouped_paths)

    logger(f"Operation complete!")


if __name__ == "__main__":
    roots = ["/home/me/Downloads", "/home/me/Documents", "/home/me/Desktop"]
    roots = ["/home/me/Downloads"]

    run_organize(roots, 1, lambda x: print(x))
