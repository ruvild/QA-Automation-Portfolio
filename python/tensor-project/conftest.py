import pytest
from selenium import webdriver
from selene import Browser, Config
from pages.saby_pages.base_page import BasePage
from utils.file_helpers import set_download_folder
from pathlib import Path

DOWNLOAD_PATH = Path("./downloads").resolve()


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Запуск тестов в headless режиме",
    )
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=["chrome", "firefox"],
        help="Выбор браузера",
    )


@pytest.fixture(scope="function")
def browser(request):
    browser_name = request.config.getoption("--browser")
    is_headless = request.config.getoption("--headless")

    if browser_name == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--window-size=1920,1080")
        if is_headless:
            options.add_argument("--headless=new")
        prefs = {
            "download.default_directory": str(DOWNLOAD_PATH),
            "download.prompt_for_download": False,
            "safebrowsing.enabled": True,
        }
        options.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(options=options)

    elif browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
        if is_headless:
            options.add_argument("--headless")

        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.dir", str(DOWNLOAD_PATH))
        options.set_preference(
            "browser.helperApps.neverAsk.saveToDisk", "application/octet-stream"
        )
        driver = webdriver.Firefox(options=options)

    else:
        raise pytest.UsageError("--browser должен быть 'chrome' или 'firefox'")

    browser_instance = Browser(Config(driver=driver, timeout=10))
    yield browser_instance
    browser_instance.quit()


@pytest.fixture(scope="function")
def saby_main(browser):
    page = BasePage(browser)
    page.open()
    return page


@pytest.fixture()
def download_manager():
    download_dir, old_files = set_download_folder(str(DOWNLOAD_PATH))

    yield download_dir, old_files

    current_files = set(download_dir.iterdir())
    for file in current_files:
        if file not in old_files:
            file.unlink()
