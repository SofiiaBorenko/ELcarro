
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Pages.base_page import BasePage
from logging_config import logger


class CarPage(BasePage):

    URL = "https://icarro-v1.netlify.app/let-car-work"

    CITY = (By.ID, "city")
    MAKE = (By.NAME, "manufacture")
    MODEL = (By.NAME, "model")
    YEAR = (By.NAME, "year")
    FUEL = (By.NAME, "fuel")
    GEAR = (By.NAME, "gear")
    WD = (By.NAME, "wheelsDrive")
    DOORS = (By.NAME, "doors")
    SEATS = (By.NAME, "seats")
    CAR_CLASS = (By.NAME, "carClass")
    SERIAL_NUMBER = (By.NAME, "serialNumber")
    PRICE = (By.NAME, "pricePerDay")
    ABOUT = (By.NAME, "about")
    IMAGE_URL = (By.NAME, "image")
    SUBMIT = (By.XPATH, "//button[normalize-space()='Submit']")

    def open_car_page(self):
        logger.info("Opening car form page")
        self.driver.get(self.URL)
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.CITY)
        )
        logger.info("Car form page opened successfully")

    def select_option(self, locator, value):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(locator)
            )
            Select(element).select_by_value(value)
            logger.debug("Selected option: %s", value)
        except Exception:
            logger.exception("Failed to select option: %s", locator)
            raise

    def fill_car_form(self, car):
        logger.info("Filling car form")

        self.input_text(self.CITY, car.city)
        self.input_text(self.MAKE, car.make)
        self.input_text(self.MODEL, car.model)
        self.input_text(self.YEAR, str(car.year))
        self.select_option(self.FUEL, car.fuel)
        self.input_text(self.SEATS, str(car.seats))
        self.input_text(self.CAR_CLASS, car.car_class)
        self.input_text(self.SERIAL_NUMBER, car.registration_number)
        self.input_text(self.PRICE, str(car.price))

        logger.info("Car form filled")

    def get_form_validation_errors(self):
        errors = self.driver.execute_script("""
            const form = document.querySelector('form');

            if (!form) {
                return ['Car form was not found'];
            }

            return Array.from(
                form.querySelectorAll('input, select, textarea')
            )
            .filter(element => !element.checkValidity())
            .map(element =>
                (element.name || element.id) + ': ' +
                element.validationMessage
            );
        """)

        if errors:
            logger.warning("Car form validation errors: %s", errors)
        else:
            logger.debug("No car form validation errors")

        return errors

    def submit_car(self):
        logger.info("Submitting car form")
        self.click_element(self.SUBMIT)

    def is_car_form_displayed(self):
        result = self.is_element_visible(self.CITY, timeout=3)
        logger.debug("Car form displayed: %s", result)
        return result
