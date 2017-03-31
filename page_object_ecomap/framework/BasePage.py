from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from page_object_ecomap.framework.Locators import HomePageLocator, LogoLocator


class BasePage:

    def __init__(self, driver, base_url = HomePageLocator.BASE_URL):
        self.driver = driver
        self.base_url = base_url

    def open(self, url=""):
        url = self.base_url + url
        self.driver.get(url)

    def check_logo_present(self, *locator):
        return self.isElementPresent(*LogoLocator.LOGO)

    def find_element(self, *locator):
        return self.driver.find_element(*locator)

    def click(self, *locator):
        self.driver.find_element(*locator).click()

    def type(self, text, *locator):
        element = self.driver.find_element(*locator)
        #element.clear("")
        element.send_keys(text)

    def getTitle(self):
        return self.driver.title

    def get_current_url(self):
        return self.driver.current_url

    def hover(self, *locator):
        element = self.findElement(*locator)
        hover = ActionChains(self.driver).move_to_element(element)
        hover.perform()

    def isElementPresent(self, *locator):
        try:
            self.find_element(*locator)
        except NoSuchElementException:
            return False
        return True
