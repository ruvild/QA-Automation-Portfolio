import time
from pathlib import Path
import re


def extract_size_mb(text: str) -> float:
    match = re.search(r"(\d+(?:\.\d+)?)\s*МБ", text).group(1)
    return float(match)


def set_download_folder(download_dir):
    download_dir = Path(download_dir)
    download_dir.mkdir(exist_ok=True)

    old_files = set(download_dir.iterdir())
    return download_dir, old_files


def wait_for_download(download_dir, old_files, timeout=60):

    timeout_time = time.time() + timeout

    while time.time() < timeout_time:
        new_file: set[Path] = set(download_dir.iterdir()) - old_files
        for file in new_file:
            if (
                file.suffix not in (".crdownload", ".tmp", ".part")
                and file.stat().st_size != 0
            ):
                return file
        time.sleep(0.5)

    raise TimeoutError("Загрузка не выполнена до обозначенного времени")
