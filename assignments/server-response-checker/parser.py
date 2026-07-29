import argparse


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="host-checker",
        description="Утилита командной строки для измерения доступности веб-ресурсов, HTTP-статусов и задержки",
        epilog="Пример использования: python checker.py -H https://google.com -C 3",
    )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "-H",
        "--hosts",
        nargs="+",
        help="Один или несколько URL/хостов для тестирования (через запятую или пробел) (https://google.com,https://example.com)",
    )

    group.add_argument(
        "-F",
        "--file",
        help="Имя файла с хостами",
    )

    parser.add_argument(
        "-C",
        "--count",
        type=int,
        default=1,
        help="Количество запросов к каждому хосту (по умолчанию: 1)",
    )

    parser.add_argument("-O", "--output", help="Имя файла с результатами проверки")

    return parser.parse_args()
