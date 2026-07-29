from pages.tensor_pages.base_page import BasePage
from selene import have, by, be


class DownloadsPage(BasePage):
    ENDPOINT = "download"

    def __init__(self, browser):
        super().__init__(browser)

        self.corporate_mode_accordeon = self.browser.element(
            "[name='WindowsSpoiler'] .controls-Spoiler__title"
        )

    def download_block(self, app_name):
        return self.browser.all("[class*='DownloadNew-block']").element_by(
            have.text(app_name)
        )

    def download_link(self, app_name):
        return self.download_block(app_name).element(by.partial_link_text("Скачать"))

    def download_file(self, app_name):
        self.corporate_mode_accordeon.click()
        self.download_block(app_name).should(be.visible)
        self.download_link(app_name).click()
