from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.inventory_page import InventoryPage


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

        self.username_textbox = (By.ID, "user-name")
        self.password_textbox = (By.ID, "password")
        self.login_button = (By.ID, "login-button")
        self.error_element = (By.CSS_SELECTOR, "[data-test='error']")

    def open(self):
        self.open_url()

    def login_as(self, username, password):

        self.wait.until(
            EC.visibility_of_element_located(self.username_textbox)
        ).send_keys(username)
        self.wait.until(
            EC.visibility_of_element_located(self.password_textbox)
        ).send_keys(password)
        self.wait.until(EC.element_to_be_clickable(self.login_button)).click()

        return InventoryPage(self.driver)

    def get_error_message(self):
        error_banner = self.wait.until(
            EC.visibility_of_element_located(self.error_element)
        )
        return error_banner.text
