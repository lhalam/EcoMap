from selenium.common.exceptions import TimeoutException
from framework.BasePage import BasePage
from framework.Locators import *
from math import fabs

from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
import requests
import json


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

    def is_user_profile_link_present(self):
        return self.is_element_present(*HomeUserPageLocator.USER_PROFILE_LINK)

    def click_on_add_problem(self):
        self.driver.find_element(*NavigationLocator.ADD_PROBLEM).click()
        return AddProblemPage(self.driver)

    def is_add_problem_tab_present(self):
        return self.is_element_present(*NavigationLocator.ADD_PROBLEM)

    def get_user_profile_page(self):
        self.click(*HomePageLocator.USER_PROFILE)
        return UserProfilePage(self.driver)


class LoginPage(BasePage):
    def login(self, login_name, password):
        self.type(login_name, *LoginPageLocator.EMAIL)
        self.type(password, *LoginPageLocator.PASSWORD)
        self.click(*LoginPageLocator.SUBMIT)
        return HomeUserPage(self.driver)

    def get_expected_url(self):
        return self.base_url + LoginPageLocator.URL

    def is_email_field_present(self):
        return self.is_element_present(*LoginPageLocator.EMAIL)

    def is_password_field_present(self):
        return self.is_element_present(*LoginPageLocator.PASSWORD)

    def is_submit_button_present(self):
        return self.is_element_present(*LoginPageLocator.SUBMIT)

class AddProblemPage(BasePage):

    def check_presence_of_coordinates(self, driver):
        try:
            latitude = driver.find_element(*Location_Locator.LATITUDE).get_attribute("value")
            longitude = driver.find_element(*Location_Locator.LONGITUDE).get_attribute("value")
            return float(latitude), float(longitude)
        except (TypeError, ValueError):
            return False

    def click_on_find_me(self):
        try:
            self.driver.find_element(*Location_Locator.FIND_ME).click()
            latitude, longitude = WebDriverWait(self.driver, 5).until(self.check_presence_of_coordinates)
            found_coordinates = [latitude, longitude]
            return found_coordinates
        except TimeoutException:
            return None

    def check_location(self, found_coordinates, actual_coordinates):
        try:
            if fabs(actual_coordinates[0] - found_coordinates[0]) < 0.1 \
                    and fabs(actual_coordinates[1] - found_coordinates[1]) < 0.1:
                return True
            else:
                return False
        except (IndexError, TypeError):
            return False

    def get_actual_coordinates(self):
        try:
            send_url = 'http://freegeoip.net/json/'
            r = requests.get(send_url)
            j = json.loads(r.text)
            lat = j['latitude']
            lon = j['longitude']
            # ip = j['ip']
            actual_coordinates = [lat, lon]
        except Exception:
            actual_coordinates = None
        return actual_coordinates

    def is_location_widget_present(self):
        return self.is_element_present(*Location_Locator.LOCATION_WIDGET)

    def get_reason_of_fail(self):
        actual_coordinates = self.get_actual_coordinates()
        found_coordinates = self.click_on_find_me()
        if found_coordinates is None and actual_coordinates is None:
            message = "Can't find coordinates by application and outside service"
        elif actual_coordinates is None:
            message = "Can't find coordinates by outside service"
        elif found_coordinates is None:
            message = "Can't find coordinates by application"
        else:
            message = "Actual coordinates don't equal found coordinates"
        return message

    def get_expected_url(self):
        return self.base_url + AddProblemPageLocator.URL


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

    def get_issues_page(self):
        self.click(*UserProfileNavigationLocator.ISSUES_TAB)
        return UserProfileIssuesPage(self.driver)


class UserProfileIssuesPage(BasePage):
    def get_expected_url(self):
        return self.base_url + UserProfileIssuesLocator.URL

    def edit_first_issue(self):
        self.click(*UserProfileIssuesLocator.FIRST_ISSUE_EDIT_LINK)
        return IssuePage(self.driver)


class DetailedIssuePage(BasePage):
    '''page where the detailed information about issue is shown'''
    def check_importance_field_is_present(self):
        if self.is_element_present(IssueLocator.IMPORTANCE):
            return True
        return False

    def check_status_field_is_present(self):
        if self.is_element_present(IssueLocator.STATUS):
            return True
        return False

    def check_change_button_is_present(self):
        if self.is_element_present(IssueLocator.CHANGE_BTN):
            return True
        return False

    def change_importance(self, value):
        select = Select(self.find_element(*IssueLocator.IMPORTANCE))
        select.select_by_index(value - 1)

    def change_status(self, is_unsolved):
        select = Select(self.find_element(*IssueLocator.STATUS))
        if is_unsolved:
            select.select_by_visible_text("Не вирішено")
        else:
            select.select_by_visible_text("Вирішено")

    def submit_change_and_report_success(self):
        self.click(*IssueLocator.CHANGE_BTN)

    def is_success_popup_present(self):
        _d = self.driver
        try:
            WebDriverWait(_d, 5).until(lambda _d: _d.find_element(*IssueLocator.POP_UP_WINDOW_SUCCESSFUL_CHANGE))
        except Exception:
            return False
        return True
