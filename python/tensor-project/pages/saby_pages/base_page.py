from selene import by, be, command
from pages.main_base_page import MainBasePage
from pages.saby_pages.downloads_page import DownloadsPage


class BasePage(MainBasePage):
    BASE_URL = "https://saby.ru/"

    def __init__(self, browser):
        super().__init__(browser)

        self.contacts_header = self.browser.element(".sbisru-Header").element(
            by.text("Контакты")
        )

        self.contacts_offices = self.browser.element("#popup").element(
            "[href='/contacts']"
        )

        self.footer_container = self.browser.element(".sbisru-Footer__container")

        self.footer_contacts = self.footer_container.element("[href='/contacts']")

        self.footer_downloads = self.footer_container.element("[href='/download']")

    def go_to_contacts_via_header(self):
        from pages.saby_pages.contacts_page import ContactsPage

        self.contacts_header.should(be.clickable)
        self.contacts_header.hover()
        self.contacts_offices.click()
        return ContactsPage(self.browser)

    def go_to_contacts_via_footer(self):
        from pages.saby_pages.contacts_page import ContactsPage

        self.footer_contacts.should(be.clickable).perform(command.js.click())
        return ContactsPage(self.browser)

    def go_to_downloads(self):
        self.footer_downloads.click()
        return DownloadsPage(self.browser)
