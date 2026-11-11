import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from confing import EMAIL, PASSWORD


URL = "https://icarro-v1.netlify.app/login"

SUBMIT = (By.CSS_SELECTOR, "button[type='submit']")

ERROR = (
    By.XPATH,
    "//*[contains(text(), 'Login or Password incorrect')]"
)

SUCCESS_DIALOG = (
    By.CSS_SELECTOR,
    "[role='dialog']"
)

SUCCESS_OK = (
    By.XPATH,
    "//*[@role='dialog']//*[normalize-space(text())='OK']"
)


@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(URL)

    yield driver

    driver.quit()


def fill_form(driver, email, password):
    """Fill in the login form."""

    wait = WebDriverWait(driver, 15)

    email_field = wait.until(
        EC.visibility_of_element_located((By.NAME, "username"))
    )
    email_field.clear()
    email_field.send_keys(email)

    password_field = driver.find_element(By.NAME, "password")
    password_field.clear()
    password_field.send_keys(password)


class TestLogin:

    def test_successful_login(self, driver):
        """Valid email and password: user successfully logs in."""

        wait = WebDriverWait(driver, 15)

        fill_form(driver, EMAIL, PASSWORD)

        wait.until(
            EC.element_to_be_clickable(SUBMIT)
        ).click()

        # Wait for successful login message
        wait.until(
            EC.visibility_of_element_located(SUCCESS_DIALOG)
        )

        # Find and click OK
        ok_button = wait.until(
            EC.visibility_of_element_located(SUCCESS_OK)
        )

        wait.until(
            EC.element_to_be_clickable(SUCCESS_OK)
        )

        driver.execute_script(
            "arguments[0].click();", ok_button
        )

        # Check that user was redirected to search page
        wait.until(EC.url_contains("/search"))

        assert "/search" in driver.current_url, (
            "User was not redirected to the search page"
        )


    def test_login_wrong_password(self, driver):
        """Registered email and wrong password."""

        wait = WebDriverWait(driver, 15)

        fill_form(driver, EMAIL, "WrongPass123!")

        wait.until(
            EC.element_to_be_clickable(SUBMIT)
        ).click()

        error = wait.until(
            EC.visibility_of_element_located(ERROR)
        )

        assert error.is_displayed(), (
            "Login error message was not displayed"
        )

        assert "/login" in driver.current_url, (
            "User must stay on the login page"
        )


    def test_login_empty_password(self, driver):
        """Valid email and empty password."""

        fill_form(driver, EMAIL, "")

        submit_button = driver.find_element(*SUBMIT)

        assert not submit_button.is_enabled(), (
            "Submit button must be disabled when password is empty"
        )

        assert "/login" in driver.current_url, (
            "User must stay on the login page"
        )


    def test_login_invalid_email(self, driver):
        """Invalid email format and valid password."""

        fill_form(driver, "nika.gmail.com", PASSWORD)

        submit_button = driver.find_element(*SUBMIT)

        assert not submit_button.is_enabled(), (
            "Submit button must be disabled when email is invalid"
        )

        assert "/login" in driver.current_url, (
            "User must stay on the login page"
        )
