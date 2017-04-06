from selenium.webdriver.support.wait import WebDriverWait

from page_object_ecomap.framework.BasePage import BasePage
from page_object_ecomap.framework.Locators import *


class HomePage(BasePage):
    def get_login_page(self):
        self.click(*HomePageLocator.LOG_IN)
        return LoginPage(self.driver)

    def get_expected_url(self):
        return self.base_url

    def get_registration_page(self):
        self.click(*HomePageLocator.REGISTER)
        return Registration(self.driver)


class HomeUserPage(BasePage):
    def get_expected_url(self):
        return self.base_url + HomeUserPageLocator.URL

    def is_logout_btn_present(self):
        return self.is_element_present(*HomeUserPageLocator.LOGOUT_LINK)

    def user_credentials_btn_is_present(self):
        return self.find_element(*HomeUserPageLocator.USER_CREDENTIALS).text



class LoginPage(BasePage):
    def login(self, login_name, password):
        self.type(login_name, *LoginPageLocator.EMAIL)
        self.type(password, *LoginPageLocator.PASSWORD)
        self.click(*LoginPageLocator.SUBMIT)
        return HomeUserPage(self.driver)

    def get_expected_url(self):
        return self.base_url + LoginPageLocator.URL

class Registration(BasePage):
    def reg(self, email, name, surname, nickname, password, confirmpassword):
        self.type(email, *RegisterPageLocator.EMAIL)
        self.type(name, *RegisterPageLocator.NAME)
        self.type(surname, *RegisterPageLocator.SURNAME)
        self.type(nickname, *RegisterPageLocator.NICKNAME)
        self.type(password, *RegisterPageLocator.PASSWORD)
        self.type(confirmpassword, *RegisterPageLocator.CONFIRMPASSWORD)
        self.click(*RegisterPageLocator.SUBMIT_BUTTON)

    def get_expected_reg_url(self):
        return self.base_url + RegisterPageLocator.REG_URL

    def wait_linked_text_changed(self):
        _driver = self.driver
        WebDriverWait(self.driver, 5).until(lambda _driver: _driver.find_element(*HomeUserPageLocator.USER_CREDENTIALS).text != 'УВІЙТИ')








