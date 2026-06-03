from selene import have, by
from pages.main_base_page import MainBasePage


class BasePage(MainBasePage):
    BASE_URL = "https://tensor.ru/"

    def __init__(self, browser):
        super().__init__(browser)

        self.people_block = self.browser.all(
            "[class*='tensor_ru-container']"
        ).element_by(have.text("Сила в людях"))
        self.people_about_link = self.people_block.element(
            by.partial_link_text("Подробнее")
        )

    def go_to_about_page(self):
        from pages.tensor_pages.about_page import AboutPage

        self.people_about_link.click()
        return AboutPage(self.browser)
