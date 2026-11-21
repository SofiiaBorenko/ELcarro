
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class BaseTest:

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def fill_form(self, email, password):
        email_field = self.wait.until(
            EC.visibility_of_element_located((By.NAME, "username"))
        )
        email_field.clear()
        email_field.send_keys(email)

        password_field = self.driver.find_element(
            By.NAME, "password"
        )
        password_field.clear()
        password_field.send_keys(password)

