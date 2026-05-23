from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    BASE_URL = "https://www.saucedemo.com/"

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout=10)

    def open_url(self, path=""):
        self.driver.get(f"{self.BASE_URL}{path}")
