
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config import EMAIL, PASSWORD
from Tests.base_test import BaseTest


URL = "https://icarro-v1.netlify.app/login"

SUBMIT = (By.CSS_SELECTOR, "button[type='submit']")

ERROR = (
    By.XPATH,
    "//*[contains(text(), 'Login or Password incorrect')]"
)

SUCCESS_DIALOG = (By.CSS_SELECTOR, "[role='dialog']")

SUCCESS_OK = (
    By.XPATH,
    "//*[@role='dialog']//*[normalize-space(text())='OK']"
)


class TestLogin(BaseTest):

    def test_successful_login(self):
        self.driver.get(URL)
        self.fill_form(EMAIL, PASSWORD)

        self.wait.until(
            EC.element_to_be_clickable(SUBMIT)
        ).click()

        self.wait.until(
            EC.visibility_of_element_located(SUCCESS_DIALOG)
        )

        ok_button = self.wait.until(
            EC.element_to_be_clickable(SUCCESS_OK)
        )

        self.driver.execute_script(
            "arguments[0].click();", ok_button
        )

        self.wait.until(EC.url_contains("/search"))

        assert "/search" in self.driver.current_url

    def test_login_wrong_password(self):
        self.driver.get(URL)
        self.fill_form(EMAIL, "WrongPass123!")

        self.wait.until(
            EC.element_to_be_clickable(SUBMIT)
        ).click()

        error = self.wait.until(
            EC.visibility_of_element_located(ERROR)
        )

        assert error.is_displayed()
        assert "/login" in self.driver.current_url

    def test_login_empty_password(self):
        self.driver.get(URL)
        self.fill_form(EMAIL, "")

        submit_button = self.driver.find_element(*SUBMIT)

        assert not submit_button.is_enabled()
        assert "/login" in self.driver.current_url

    def test_login_invalid_email(self):
        self.driver.get(URL)
        self.fill_form("nika.gmail.com", PASSWORD)

        submit_button = self.driver.find_element(*SUBMIT)

        assert not submit_button.is_enabled()
        assert "/login" in self.driver.current_url

