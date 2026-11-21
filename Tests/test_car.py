
import time

from selenium.webdriver.common.by import By

from config import EMAIL, PASSWORD
from Models.car import Car
from Pages.login_page import LoginPage
from Pages.car_page import CarPage
from Tests.base_test import BaseTest


class TestAddCar(BaseTest):

    def test_add_car(self):

        # Preconditions: login
        login_page = LoginPage(self.driver)
        login_page.open_login_page()
        login_page.login(EMAIL, PASSWORD)
        login_page.confirm_successful_login()

        # Test data
        car = Car(
            city="Tel Aviv",
            make="Toyota",
            model="Corolla",
            year=2020,
            fuel="petrol",
            seats=5,
            car_class="Sedan",
            registration_number=f"TEST{int(time.time())}",
            price=50
        )

        # Open car form
        car_page = CarPage(self.driver)
        car_page.open_car_page()

        # Fill car form
        car_page.fill_car_form(car)

        # Check required fields
        errors = car_page.get_form_validation_errors()

        assert not errors, (
            "Form validation errors: " + "; ".join(errors)
        )

        # Submit car
        car_page.submit_car()

        time.sleep(3)

        # Check result
        print("CURRENT URL:", self.driver.current_url)

        print(
            "PAGE TEXT:",
            self.driver.find_element(By.TAG_NAME, "body").text
        )

        print(
            "VALIDATION ERRORS:",
            car_page.get_form_validation_errors()
        )

        print(
            "FORM DISPLAYED:",
            car_page.is_car_form_displayed()
        )


