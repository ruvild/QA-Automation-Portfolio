from urllib.parse import urljoin
from selene import Browser, have


class MainBasePage:
    BASE_URL = ""
    ENDPOINT = ""

    def __init__(self, browser: Browser):
        self.browser = browser

    @property
    def url(self):
        return urljoin(self.BASE_URL, self.ENDPOINT)

    def open(self):
        self.browser.open(self.url)

    def switch_to_next_tab(self):
        self.browser.should(have.tabs_number(2))
        window_handles = self.browser.driver.window_handles
        self.browser.switch_to.window(window_handles[1])
