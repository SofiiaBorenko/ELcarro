
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Pages.base_page import BasePage
from logging_config import logger


class LoginPage(BasePage):

    URL = "https://icarro-v1.netlify.app/login"

    EMAIL_FIELD = (By.NAME, "username")
    PASSWORD_FIELD = (By.NAME, "password")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    SUCCESS_DIALOG = (By.CSS_SELECTOR, "[role='dialog']")
    SUCCESS_OK = (
        By.XPATH,
        "//*[@role='dialog']//*[normalize-space(text())='OK']"
    )

    ERROR_MESSAGE = (
        By.XPATH,
        "//*[contains(text(), 'Login or Password incorrect')]"
    )

    def open_login_page(self):
        logger.info("Opening login page")
        self.driver.get(self.URL)

    def login(self, email, password):
        logger.info("Attempting login")
        self.input_text(self.EMAIL_FIELD, email)
        self.input_text(self.PASSWORD_FIELD, password)
        self.click_element(self.SUBMIT_BUTTON)

    def confirm_successful_login(self):
        logger.info("Confirming successful login")

        wait = WebDriverWait(self.driver, 15)

        try:
            wait.until(
                EC.visibility_of_element_located(self.SUCCESS_DIALOG)
            )

            ok_button = wait.until(
                EC.element_to_be_clickable(self.SUCCESS_OK)
            )

            self.driver.execute_script(
                "arguments[0].click();", ok_button
            )

            wait.until(EC.url_contains("/search"))
            logger.info("Login completed successfully")

        except Exception:
            logger.exception("Successful login confirmation failed")
            raise

    def is_login_error_displayed(self):
        result = self.is_element_visible(self.ERROR_MESSAGE)
        if result:
            logger.warning("Login error message is displayed")
        return result
