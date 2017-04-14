from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from framework.Locators import HomePageLocator, LogoLocator
import os


class BasePage:

    def __init__(self, driver, base_url=os.environ.get('ECOMAP_BASE_URL')):
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
