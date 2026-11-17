import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run Chrome in headless mode for CI/Docker execution",
    )


@pytest.fixture(scope="function")
def driver(request):
    headless = request.config.getoption("--headless")
    options = Options()

    if headless:
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
    else:
        options.add_argument("--start-maximized")

    # Disable Chrome password manager popups during automated runs
    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
    }
    options.add_experimental_option("prefs", prefs)

    web_driver = webdriver.Chrome(options=options)
    yield web_driver
    web_driver.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Automatically capture and attach a screenshot to Allure when a test fails."""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        web_driver = item.funcargs.get("driver")
        if web_driver:
            allure.attach(
                web_driver.get_screenshot_as_png(),
                name=f"Failure_{item.name}",
                attachment_type=allure.attachment_type.PNG,
            )
