from page_object_ecomap.framework.BasePage import BasePage
from page_object_ecomap.framework.Locators import *
from selenium.webdriver.support.ui import WebDriverWait


class HomePage(BasePage):
    def get_login_page(self):
        self.click(*HomePageLocator.LOG_IN)
        return LoginPage(self.driver)

    def get_expected_url(self):
        return self.base_url


class HomeUserPage(BasePage):
    def get_expected_url(self):
        return self.base_url + HomeUserPageLocator.URL

    def is_logout_btn_present(self):
        return self.is_element_present(*HomeUserPageLocator.LOGOUT_LINK)


class LoginPage(BasePage):
    def login(self, login_name, password):
        self.type(login_name, *LoginPageLocator.EMAIL)
        self.type(password, *LoginPageLocator.PASSWORD)
        self.click(*LoginPageLocator.SUBMIT)
        return HomeUserPage(self.driver)
    def wait_until_home_page_is_loaded(self):
        _driver = self.driver
        WebDriverWait(self.driver, 30).until(lambda _driver: _driver.find_element(*MapLocator.MAP))

    def get_expected_url(self):
        return self.base_url + LoginPageLocator.URL



