import pytest

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

def test_login_negative(login_page, username, password, expected_error):

    login_page.login_as(username, password)
    assert login_page.get_error_message() == expected_error

def test_login_positive(login_page):

    inventory_page = login_page.login_as('standard_user','secret_sauce')    
    assert inventory_page.get_current_url().endswith(inventory_page.PATH)
    assert len(inventory_page.get_inventory_items()) > 0