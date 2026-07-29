from pages.saby_pages.base_page import BasePage as SabyBase
from pages.tensor_pages.base_page import BasePage as TensorBase
from selene import by, be, command


class ContactsPage(SabyBase):
    ENDPOINT = "contacts"

    def __init__(self, browser):
        super().__init__(browser)
        self.tensor_banner = self.browser.element("a[title='tensor.ru']")
        self.region_header = self.browser.element("[class*='Region-Chooser']")

        self.partner_contacts = self.browser.element("[data-qa='list']")

        self.dialog = self.browser.element("[name='dialog']")

        self.loading_overlay = self.browser.element("[name='loadingOverlay']")

    def go_to_tensor(self):
        self.tensor_banner.click()
        return TensorBase(self.browser)

    def switch_region(self, region):

        self.loading_overlay.should(be.not_.visible)
        self.region_header.should(be.clickable)
        self.region_header.locate().click()
        region_link = self.dialog.element(by.partial_text(region))
        region_link.should(be.clickable).perform(command.js.click())
        return self
