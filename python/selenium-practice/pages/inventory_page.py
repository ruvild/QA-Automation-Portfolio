from pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

class InventoryPage(BasePage):
    PATH = 'inventory.html'

    def __init__(self,driver):
        super().__init__(driver)

        self.inventory_items = (By.CSS_SELECTOR, "div[data-test='inventory-item']")

    def get_current_url(self):
        self.wait.until(EC.url_contains(self.PATH))
        return self.driver.current_url
    

