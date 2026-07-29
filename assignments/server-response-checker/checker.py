import requests
from requests.exceptions import RequestException
from concurrent.futures import ThreadPoolExecutor
from parser import parse_arguments
from functools import partial
import json
from utils import parse_hosts, file_read, file_write


def check_host(url: str, count: int = 5) -> dict:
    times = []
    successes = 0
    failures = 0
    errors = 0
    error_messages = []

    for _ in range(count):
        try:
            res = requests.get(url, timeout=5)
            times.append(res.elapsed.total_seconds() * 1000)
            if res.ok:
                successes += 1
            else:
                failures += 1
                error_messages.append(f"HTTP {res.status_code}: {res.reason}")
        except RequestException as e:
            errors += 1
            error_messages.append(str(e))

    return {
        "host": url,
        "success": successes,
        "failed": failures,
        "errors": errors,
        "min": round(min(times), 2) if times else 0,
        "max": round(max(times), 2) if times else 0,
        "avg": round(sum(times) / len(times), 2) if times else 0,
        "error_messages": error_messages,
    }


def main() -> None:
    args = parse_arguments()

    if args.hosts:
        urls = parse_hosts(args.hosts)
    else:
        raw_hosts = file_read(args.file)
        urls = parse_hosts(raw_hosts)

    worker_func = partial(check_host, count=args.count)

    with ThreadPoolExecutor() as executor:
        raw_results = list(executor.map(worker_func, urls))

    formatted_json = json.dumps(raw_results, indent=4)

    if args.output:
        file_write(args.output, formatted_json)
    else:
        print(formatted_json)


if __name__ == "__main__":
    main()
