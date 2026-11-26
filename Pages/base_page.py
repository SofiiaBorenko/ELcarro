
from selenium.webdriver import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from logging_config import logger


class BasePage:

    def __init__(self, driver):
        self.driver = driver

    def is_element_visible(self, locator, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            logger.debug("Element is visible: %s", locator)
            return True
        except TimeoutException:
            logger.warning("Element is not visible: %s", locator)
            return False

    def click_element(self, locator, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            logger.info("Clicked element: %s", locator)
        except Exception:
            logger.exception("Failed to click element: %s", locator)
            raise

    def input_text(self, locator, text, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            element.click()
            element.clear()

            if text:
                element.send_keys(text)

            element.send_keys(Keys.TAB)
            logger.debug("Entered text into element: %s", locator)
        except Exception:
            logger.exception("Failed to enter text into element: %s", locator)
            raise

    def get_element_text(self, locator, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            text = element.text
            logger.debug("Got text from element: %s", locator)
            return text
        except Exception:
            logger.exception("Failed to get text from element: %s", locator)
            raise

    def is_element_disabled(self, locator, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return not element.is_enabled()
        except TimeoutException:
            logger.warning("Element was not found: %s", locator)
            return False
