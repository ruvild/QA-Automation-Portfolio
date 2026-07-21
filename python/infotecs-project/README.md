# Host Checker CLI

Утилита командной строки (CLI) на Python для измерения доступности веб-ресурсов, HTTP-статусов и задержки с поддержкой многопоточности.

## Описание работы программы

Инструмент позволяет выполнять сетевую диагностику списка хостов. Вы можете передавать целевые URL напрямую через аргументы командной строки или загружать их из текстового файла. 

Для ускорения обработки всех запросов используется многопоточность (`ThreadPoolExecutor`). Текстовые файлы с хостами и результатами хранятся в директории `data/` (`hosts.txt` уже существует с примерами хостов; файл для результатов создается автоматически при выборе записи в файл).

### Основные возможности
* **Мульти-ввод:** Поддержка одиночных/множественных URL через флаговую команду или загрузка списка из файла.
* **Автоматическое исправление схем:** Если хост указан без протокола (например, `google.com`), программа автоматически добавит `https://`.
* **Параллельная проверка:** Выполнение запросов в несколько потоков для быстрой работы.
* **Метрики задержки:** Расчет минимального (`min`), максимального (`max`) и среднего (`avg`) времени отклика в миллисекундах.
* **Экспорт результатов:** Вывод в формате JSON в консоль или сохранение в файл.
* **Вывод ошибок:** Ошибки выводятся в читаемом формате.

---

## Инструкция по запуску

### 1. Требования и установка
* **Python** версии 3.9 или выше.
* Установка зависимости `requests`:

```bash
pip install requests
```

### 2. Примеры использования

* Проверка хостов, переданных через аргументы (-H / --hosts). Можно вводить несколько хостов через запятую или пробел:
```bash
python checker.py -H https://google.com,github.com
```
* Выбор количества запросов к хосту (-C / --count). Значение по умолчанию - 1:
```bash
python checker.py -H https://google.com -C 3
```
* Проверка хостов из файла (-F / --file). Создайте файл в директории data и укажите в нем хосты по одному на строку:

```bash
python checker.py -F hosts.txt
```
* Сохранение результатов в файл (-O / --output). Результат будет сохранен в директории data:
```bash
python checker.py -H https://google.com -O results.txt
```

### 3. Примеры вывода
Вывод в консоль (stdout) при выполнении команды:
```bash
python checker.py -H google.com,https://mock.httpstatus.io/401,https://nonexistent.domain -C 2
```
Программа выведет структурированный JSON:

```JSON
[
    {
        "host": "https://google.com",
        "success": 2,
        "failed": 0,
        "errors": 0,
        "min": 801.29,
        "max": 928.83,
        "avg": 865.06,
        "error_messages": []
    },    
    {
        "host": "https://mock.httpstatus.io/401",
        "success": 0,
        "failed": 2,
        "errors": 0,
        "min": 958.96,
        "max": 1287.75,
        "avg": 1123.36,
        "error_messages": [
            "HTTP 401: Unauthorized",
            "HTTP 401: Unauthorized"
        ]
    },
    {
        "host": "https://nonexistent.domain",
        "success": 0,
        "failed": 0,
        "errors": 2,
        "min": 0,
        "max": 0,
        "avg": 0,
        "error_messages": [
            "HTTPSConnectionPool(host='nonexistent.domain', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLEOFError(8, '[SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1081)')))",
            "HTTPSConnectionPool(host='nonexistent.domain', port=443): Max retries exceeded with url: / (Caused by SSLError(SSLEOFError(8, '[SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violation of protocol (_ssl.c:1081)')))"
        ]
    }
]
```
