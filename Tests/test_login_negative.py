
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config import EMAIL, PASSWORD
from Tests.base_test import BaseTest
from logging_config import logger


URL = "https://icarro-v1.netlify.app/login"

SUBMIT = (By.CSS_SELECTOR, "button[type='submit']")

ERROR_MESSAGE = (
    By.XPATH,
    "//*[contains(text(), 'Login or Password incorrect')]"
)


class TestLoginNegative(BaseTest):

    def test_empty_email(self):
        logger.info("Starting test: empty email")

        self.driver.get(URL)
        self.fill_form("", PASSWORD)

        logger.debug("Login form filled with empty email")

        submit_button = self.driver.find_element(*SUBMIT)

        assert not submit_button.is_enabled()

        logger.warning("Empty email rejected as expected")

    def test_empty_password(self):
        logger.info("Starting test: empty password")

        self.driver.get(URL)
        self.fill_form(EMAIL, "")

        logger.debug("Login form filled with empty password")

        submit_button = self.driver.find_element(*SUBMIT)

        assert not submit_button.is_enabled()

        logger.warning("Empty password rejected as expected")

    def test_invalid_email(self):
        logger.info("Starting test: invalid email")

        self.driver.get(URL)
        self.fill_form("sofiabor2826gmail.com", PASSWORD)

        logger.debug("Login form filled with invalid email")

        submit_button = self.driver.find_element(*SUBMIT)

        assert not submit_button.is_enabled()

        logger.warning("Invalid email rejected as expected")

    def test_email_without_domain(self):
        logger.info("Starting test: email without domain")

        self.driver.get(URL)
        self.fill_form("sofiabor2826@", PASSWORD)

        logger.debug("Login form filled with email without domain")

        submit_button = self.driver.find_element(*SUBMIT)

        assert not submit_button.is_enabled()

        logger.warning("Email without domain rejected as expected")

    def test_wrong_password(self):
        logger.info("Starting test: wrong password")

        self.driver.get(URL)
        self.fill_form(EMAIL, "WrongPassword123!")

        self.wait.until(
            EC.element_to_be_clickable(SUBMIT)
        ).click()

        logger.debug("Login submitted with wrong password")

        error = self.wait.until(
            EC.visibility_of_element_located(ERROR_MESSAGE)
        )

        assert error.is_displayed()
        assert "/login" in self.driver.current_url

        logger.warning("Wrong password rejected as expected")

    def test_unregistered_email(self):
        logger.info("Starting test: unregistered email")

        self.driver.get(URL)
        self.fill_form(
            "sofiabor2826_test123@gmail.com",
            PASSWORD
        )

        self.wait.until(
            EC.element_to_be_clickable(SUBMIT)
        ).click()

        logger.debug("Login submitted with unregistered email")

        error = self.wait.until(
            EC.visibility_of_element_located(ERROR_MESSAGE)
        )

        assert error.is_displayed()
        assert "/login" in self.driver.current_url

        logger.warning("Unregistered email rejected as expected")

