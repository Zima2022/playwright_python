from allure import attachment_type, attach
import pytest
from playwright.sync_api import Page, sync_playwright

from pages.playwright_home_page import PlaywrightHomePage
from pages.playwright_languages_page import PlaywrightLanguagesPage

driver = None


@pytest.fixture(scope='function')
def chromium_page() -> Page:
    with sync_playwright() as playwright:
        global driver
        chromium = playwright.chromium.launch(headless=False)
        driver = chromium.new_page()
        yield driver


@pytest.fixture(scope='function')
def playwright_home_page(chromium_page: Page) -> PlaywrightHomePage:
    return PlaywrightHomePage(chromium_page)


@pytest.fixture(scope='function')
def playwright_languages_page(chromium_page: Page) -> PlaywrightLanguagesPage:
    return PlaywrightLanguagesPage(chromium_page)


def pytest_exception_interact(report):
    global driver
    if report.failed:
        try:
            attach(driver.screenshot(type='png'), 'screenshot', attachment_type.PNG)
        except Exception:
            attach('Failed to make screenshot', 'screenshot', attachment_type.PNG)
