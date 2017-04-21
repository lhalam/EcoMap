from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from framework.Locators import LogoLocator
from framework.Locators import BASE_URL


class BasePage:

    def __init__(self, driver, base_url=BASE_URL):
        self.driver = driver
        self.base_url = base_url

    def open(self, url=""):
        url = self.base_url + url
        self.driver.get(url)

    def is_logo_present(self):
        return self.is_element_present(*LogoLocator.LOGO)

    def find_element(self, *locator):
        return self.driver.find_element(*locator)

    def click(self, *locator):
        self.wait_until_element_to_be_clickable(locator)
        self.driver.find_element(*locator).click()

    def type(self, text, *locator):
        element = self.driver.find_element(*locator)
        element.send_keys(text)

    def get_title(self):
        return self.driver.title

    def get_current_url(self):
        return self.driver.current_url

    def hover(self, *locator):
        element = self.driver.find_element(*locator)
        hover = ActionChains(self.driver).move_to_element(element)
        hover.perform()

    def is_element_present(self, *locator):
        try:
            self.find_element(*locator)
        except NoSuchElementException:
            return False
        return True

    def is_element_invisible(self, *locator):
        try:
            self.wait_until_invisibility_of_element_located(locator)
            self.find_element(*locator)
        except NoSuchElementException:
            return False
        return True

    def is_element_visible(self, *locator):
        try:
            self.wait_until_visibility_of_element_located(locator)
            self.find_element(*locator)
        except NoSuchElementException:
            return False
        return True

    def wait_until_element_to_be_clickable(self, *locator,  timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(*locator))
        except TimeoutException:
            raise AssertionError('It takes more than {} sec to load an element'.format(timeout))

    def wait_until_visibility_of_element_located(self, locator,  timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))
        except TimeoutException:
            raise AssertionError('It takes more than {} sec to load an element'.format(timeout))

    def wait_until_invisibility_of_element_located(self, locator,  timeout=5):
        try:
            WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located(locator))
        except TimeoutException:
            raise AssertionError('It takes more than {} sec to load an element'.format(timeout))

    def get_text(self, *locator):
        if self.is_element_visible(*locator):
            element = self.find_element(*locator)
            return element.text
        else:
            return None

    def is_popup_present(self, *locator, timeout=5):
        _d = self.driver
        try:
            WebDriverWait(_d, timeout).until(lambda _d: _d.find_element(*locator))
        except Exception:
            return False
        return True




