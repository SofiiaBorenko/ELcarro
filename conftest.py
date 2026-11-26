
import pytest
from selenium import webdriver

from logging_config import logger


@pytest.fixture
def driver():
    logger.info("Starting Chrome browser")
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        yield driver
    except Exception:
        logger.exception("An error occurred while running a test")
        raise
    finally:
        logger.info("Closing Chrome browser")
        driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        if report.passed:
            logger.info("TEST PASSED: %s", item.nodeid)
        elif report.failed:
            logger.error(
                "TEST FAILED: %s\n%s",
                item.nodeid,
                report.longrepr
            )
