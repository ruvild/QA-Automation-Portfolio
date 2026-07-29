from selene import have
from pages.tensor_pages.base_page import BasePage


class AboutPage(BasePage):
    ENDPOINT = "about"

    def __init__(self, browser):
        super().__init__(browser)

        self.working_block_images = (
            self.browser.all("[class*='tensor_ru-container']")
            .element_by(have.text("Работаем"))
            .all("img")
        )

    @property
    def first_image_dimensions(self):

        return self.working_block_images.first.locate().size
