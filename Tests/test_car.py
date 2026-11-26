
import time

from config import EMAIL, PASSWORD
from Models.car import Car
from Pages.login_page import LoginPage
from Pages.car_page import CarPage
from Tests.base_test import BaseTest
from logging_config import logger


class TestAddCar(BaseTest):

    def test_add_car(self):
        logger.info("Starting test: add car")

        try:
            # Preconditions: login
            logger.info("Logging in before adding a car")

            login_page = LoginPage(self.driver)
            login_page.open_login_page()
            login_page.login(EMAIL, PASSWORD)
            login_page.confirm_successful_login()

            logger.info("Login successful")

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

            logger.debug("Car test data created")

            # Open car form
            car_page = CarPage(self.driver)
            car_page.open_car_page()

            # Fill car form
            logger.info("Filling car form")
            car_page.fill_car_form(car)

            # Check required fields
            errors = car_page.get_form_validation_errors()

            if errors:
                logger.error("Form validation errors: %s", errors)

            assert not errors, (
                "Form validation errors: " + "; ".join(errors)
            )

            logger.info("Car form validation passed")

            # Submit car
            logger.info("Submitting car")
            car_page.submit_car()

            time.sleep(3)

            # Check result
            logger.debug("Current URL: %s", self.driver.current_url)

            validation_errors = car_page.get_form_validation_errors()
            logger.debug("Validation errors after submit: %s", validation_errors)

            form_displayed = car_page.is_car_form_displayed()
            logger.info("Car form displayed after submit: %s", form_displayed)

            logger.info("Test add car completed")

        except Exception:
            logger.exception("Test add car failed")
            raise



