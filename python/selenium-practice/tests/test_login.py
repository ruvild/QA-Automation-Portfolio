import pytest
from pages.login_page import LoginPage
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.parametrize(
    "username, password, expected_error",
    [
        pytest.param(
            "locked_out_user",
            "secret_sauce",
            "Epic sadface: Sorry, this user has been locked out.",
            id="locked_out",
        ),
        pytest.param(
            "invalid_user",
            "secret_sauce",
            "Epic sadface: Username and password do not match any user in this service",
            id="invalid_user",
        ),
        pytest.param(
            "standard_user",
            "wrong_password",
            "Epic sadface: Username and password do not match any user in this service",
            id="wrong_pass",
        ),
        pytest.param(
            "", "secret_sauce", "Epic sadface: Username is required", id="empty_user"
        ),
        pytest.param(
            "standard_user", "", "Epic sadface: Password is required", id="empty_pass"
        ),
    ],
)
def test_login_negative(driver, username, password, expected_error):

    login_page = LoginPage(driver)
    login_page.open()
    login_page.login_as(username, password)
    actual_error = login_page.get_error_message()
    assert actual_error == expected_error

def test_login_positive(driver):

    login_page = LoginPage(driver)
    login_page.open()
    inventory_page = login_page.login_as('standard_user','secret_sauce')
    
    assert inventory_page.get_current_url().endswith(inventory_page.PATH)
    visible_items = inventory_page.wait.until(EC.visibility_of_all_elements_located(inventory_page.inventory_items))
    assert len(visible_items) > 0