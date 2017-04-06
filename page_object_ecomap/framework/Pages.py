from page_object_ecomap.framework.BasePage import BasePage
from page_object_ecomap.framework.Locators import *
from selenium.webdriver.support.ui import WebDriverWait


class HomePage(BasePage):
    def get_login_page(self):
        self.click(*HomePageLocator.LOG_IN)
        return LoginPage(self.driver)

    def get_user_profile_page(self):
        self.click(*HomePageLocator.USER_PROFILE)
        return UserProfilePage(self.driver)

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

    def get_expected_url(self):
        return self.base_url + LoginPageLocator.URL


class UserProfilePage(BasePage):
    def change_pwd(self, old_password, new_password, confirm_password):
        self.type(old_password, *UserProfileLocator.OLD_PASS)
        self.type(new_password, *UserProfileLocator.NEW_PASS)
        self.type(confirm_password, *UserProfileLocator.NEW_PASS_CONFIRM)
        self.click(*UserProfileLocator.SUBMIT)
        return HomeUserPage(self.driver)

    def is_success_popup_present(self):
        _d = self.driver
        try:
            WebDriverWait(_d, 5).until(lambda _d: _d.find_element(*UserProfileLocator.SUCCESS_POPUP))
        except Exception:
            return False
        return True

    def get_expected_url(self):
        return self.base_url + UserProfileLocator.URL
