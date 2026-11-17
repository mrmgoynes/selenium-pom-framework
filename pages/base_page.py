import allure
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    """Base Page Object containing reusable explicit-wait wrappers for all pages."""

    def __init__(self, driver: WebDriver, timeout: int = 10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    @allure.step("Navigate to URL: {url}")
    def open(self, url: str) -> None:
        self.driver.get(url)

    def find_visible(self, locator: tuple):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_clickable(self, locator: tuple):
        return self.wait.until(EC.element_to_be_clickable(locator))

    @allure.step("Click element: {locator}")
    def click(self, locator: tuple) -> None:
        self.find_clickable(locator).click()

    @allure.step("Enter text '{text}' into element: {locator}")
    def enter_text(self, locator: tuple, text: str) -> None:
        element = self.find_visible(locator)
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple) -> str:
        return self.find_visible(locator).text
