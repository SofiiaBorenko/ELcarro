
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from Pages.base_page import BasePage


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
        self.driver.get(self.URL)
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(self.CITY)
        )

    def select_option(self, locator, value):
        element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(locator)
        )
        Select(element).select_by_value(value)

    def fill_car_form(self, car):
        self.input_text(self.CITY, car.city)
        self.input_text(self.MAKE, car.make)
        self.input_text(self.MODEL, car.model)
        self.input_text(self.YEAR, str(car.year))
        self.select_option(self.FUEL, car.fuel)
        self.input_text(self.SEATS, str(car.seats))
        self.input_text(self.CAR_CLASS, car.car_class)
        self.input_text(self.SERIAL_NUMBER, car.registration_number)
        self.input_text(self.PRICE, str(car.price))

    def get_form_validation_errors(self):
        return self.driver.execute_script("""
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

    def submit_car(self):
        self.click_element(self.SUBMIT)

    def is_car_form_displayed(self):
        return self.is_element_visible(self.CITY, timeout=3)
