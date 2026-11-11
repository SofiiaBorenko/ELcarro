import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from confing import EMAIL, PASSWORD


URL = "https://icarro-v1.netlify.app/login"

EMAIL_FIELD = (By.NAME, "username")
PASSWORD_FIELD = (By.NAME, "password")
SUBMIT = (By.CSS_SELECTOR, "button[type='submit']")

ERROR_MESSAGE = (
    By.XPATH,
    "//*[contains(text(), 'Login or Password incorrect')]"
)


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(URL)

    yield driver

    driver.quit()


def fill_form(driver, email, password):
    wait = WebDriverWait(driver, 15)

    email_input = wait.until(
        EC.visibility_of_element_located(EMAIL_FIELD)
    )
    email_input.clear()
    email_input.send_keys(email)

    password_input = driver.find_element(*PASSWORD_FIELD)
    password_input.clear()
    password_input.send_keys(password)


class TestLoginNegative:

    def test_empty_email(self, driver):
        """Empty email with correct password."""

        fill_form(driver, "", PASSWORD)

        submit_button = driver.find_element(*SUBMIT)

        assert not submit_button.is_enabled(), (
            "Login button should be disabled when email is empty"
        )

    def test_empty_password(self, driver):
        """Correct email with empty password."""

        fill_form(driver, EMAIL, "")

        submit_button = driver.find_element(*SUBMIT)

        assert not submit_button.is_enabled(), (
            "Login button should be disabled when password is empty"
        )

    def test_invalid_email(self, driver):
        """Invalid email format with correct password."""

        fill_form(driver, "sofiabor2826gmail.com", PASSWORD)

        submit_button = driver.find_element(*SUBMIT)

        assert not submit_button.is_enabled(), (
            "Login button should be disabled for invalid email"
        )

    def test_email_without_domain(self, driver):
        """Email without domain with correct password."""

        fill_form(driver, "sofiabor2826@", PASSWORD)

        submit_button = driver.find_element(*SUBMIT)

        assert not submit_button.is_enabled(), (
            "Login button should be disabled when email has no domain"
        )

    def test_wrong_password(self, driver):
        """Correct email with incorrect password."""

        fill_form(driver, EMAIL, "WrongPassword123!")

        wait = WebDriverWait(driver, 15)

        wait.until(
            EC.element_to_be_clickable(SUBMIT)
        ).click()

        error = wait.until(
            EC.visibility_of_element_located(ERROR_MESSAGE)
        )

        assert error.is_displayed(), (
            "Error message should appear for incorrect password"
        )

        assert "/login" in driver.current_url, (
            "User should remain on the login page"
        )

    def test_unregistered_email(self, driver):
        """Unregistered email with correct password."""

        fill_form(
            driver,
            "sofiabor2826_test123@gmail.com",
            PASSWORD
        )

        wait = WebDriverWait(driver, 15)

        wait.until(
            EC.element_to_be_clickable(SUBMIT)
        ).click()

        error = wait.until(
            EC.visibility_of_element_located(ERROR_MESSAGE)
        )

        assert error.is_displayed(), (
            "Error message should appear for unregistered email"
        )

        assert "/login" in driver.current_url, (
            "User should remain on the login page"
        )
