import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions


def pytest_addoption(parser):
    """Registers the custom --browser terminal option."""
    parser.addoption(
        "--browser_selenium",
        action="store",
        default="chrome",
        help="Choose browser: chrome, firefox, or edge",
    )

    parser.addoption(
        "--headless_selenium",
        action="store_true",
        default=False,
        help="Run tests in headless mode without opening a browser window",
    )


@pytest.fixture()
def driver(request):
    browser_name = request.config.getoption('browser_selenium').lower()
    is_headless = request.config.getoption('headless_selenium')
    if browser_name == 'chrome':
        options = ChromeOptions()
        if is_headless:
            options.add_argument("--headless=new")
        driver = webdriver.Chrome(options=options)

    elif browser_name == 'firefox':
        options = FirefoxOptions()
        if is_headless:
            options.add_argument('-headless')
        driver = webdriver.Firefox(options=options)

    elif browser_name == 'edge':
        options = EdgeOptions()
        if is_headless:
            options.add_argument('--headless=new')
        driver = webdriver.Edge(options=options)
    else:
        raise pytest.UsageError(f"--browser '{browser_name}' is not supported!")

    yield driver
    driver.quit()
