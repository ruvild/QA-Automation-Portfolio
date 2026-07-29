from urllib.parse import urlparse
from pathlib import Path
import sys


def _is_valid_url(url: str) -> bool:
    try:
        result = urlparse(url)
        return all([result.scheme in ("http", "https"), result.netloc])
    except ValueError:
        return False


def parse_hosts(raw_hosts: list[str]) -> list[str]:

    parsed_hosts = []
    for entry in raw_hosts:
        for host in entry.split(","):
            cleaned = host.strip()

            if cleaned and "://" not in cleaned:
                cleaned = f"https://{cleaned}"

            if _is_valid_url(cleaned):
                parsed_hosts.append(cleaned)
            else:
                print(f"[Warning] Пропускаю неправильный формат URL: '{host}'")

    return parsed_hosts


def _dynamic_path(file_name: str) -> Path:
    script_dir = Path(__file__).resolve().parent
    data_dir = script_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir / file_name


def file_read(file_name: str) -> list[str]:
    dynamic_path = _dynamic_path(file_name)

    try:
        with open(dynamic_path, "r", encoding="utf-8") as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"[Error] Файл не найден: '{dynamic_path}'", file=sys.stderr)
        sys.exit(1)


def file_write(file_name: str, content) -> None:
    dynamic_path = _dynamic_path(file_name)

    with open(dynamic_path, "w") as file:
        file.write(content)
