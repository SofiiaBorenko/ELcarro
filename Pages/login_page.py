
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from Pages.base_page import BasePage


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
        self.driver.get(self.URL)

    def login(self, email, password):
        self.input_text(self.EMAIL_FIELD, email)
        self.input_text(self.PASSWORD_FIELD, password)
        self.click_element(self.SUBMIT_BUTTON)

    def confirm_successful_login(self):
        self.wait = self.driver

        from selenium.webdriver.support.ui import WebDriverWait

        wait = WebDriverWait(self.driver, 15)

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

    def is_login_error_displayed(self):
        return self.is_element_visible(self.ERROR_MESSAGE)
