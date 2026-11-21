
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config import EMAIL, PASSWORD
from Tests.base_test import BaseTest


URL = "https://icarro-v1.netlify.app/login"

SUBMIT = (By.CSS_SELECTOR, "button[type='submit']")

ERROR_MESSAGE = (
    By.XPATH,
    "//*[contains(text(), 'Login or Password incorrect')]"
)


class TestLoginNegative(BaseTest):

    def test_empty_email(self):
        self.driver.get(URL)
        self.fill_form("", PASSWORD)

        submit_button = self.driver.find_element(*SUBMIT)

        assert not submit_button.is_enabled()

    def test_empty_password(self):
        self.driver.get(URL)
        self.fill_form(EMAIL, "")

        submit_button = self.driver.find_element(*SUBMIT)

        assert not submit_button.is_enabled()

    def test_invalid_email(self):
        self.driver.get(URL)
        self.fill_form("sofiabor2826gmail.com", PASSWORD)

        submit_button = self.driver.find_element(*SUBMIT)

        assert not submit_button.is_enabled()

    def test_email_without_domain(self):
        self.driver.get(URL)
        self.fill_form("sofiabor2826@", PASSWORD)

        submit_button = self.driver.find_element(*SUBMIT)

        assert not submit_button.is_enabled()

    def test_wrong_password(self):
        self.driver.get(URL)
        self.fill_form(EMAIL, "WrongPassword123!")

        self.wait.until(
            EC.element_to_be_clickable(SUBMIT)
        ).click()

        error = self.wait.until(
            EC.visibility_of_element_located(ERROR_MESSAGE)
        )

        assert error.is_displayed()
        assert "/login" in self.driver.current_url

    def test_unregistered_email(self):
        self.driver.get(URL)
        self.fill_form(
            "sofiabor2826_test123@gmail.com",
            PASSWORD
        )

        self.wait.until(
            EC.element_to_be_clickable(SUBMIT)
        ).click()

        error = self.wait.until(
            EC.visibility_of_element_located(ERROR_MESSAGE)
        )

        assert error.is_displayed()
        assert "/login" in self.driver.current_url


