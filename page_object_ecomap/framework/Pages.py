#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains

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

    def is_login_link_present(self):
        return self.is_element_present(*HomePageLocator.LOG_IN)


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
        self.click(*HomeUserPageLocator.USER_PROFILE_LINK)
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

    def get_problems_page(self):
        """go to user's problems page
        please use this implementation of click() function on tab
        because errors occur sometimes with standard click(). To
        resolve this bug we have to simulate a mouse move action
        """
        actions = ActionChains(self.driver)
        problems_tab = self.find_element(*UserProfileNavigationLocator.PROBLEMS_TAB)
        actions.move_to_element(problems_tab).perform()
        problems_tab.click()
        return UserProfileProblemsPage(self.driver)

    def is_problems_tab_present(self):
        return self.is_element_present(UserProfileNavigationLocator.PROBLEMS_TAB)


class UserProfileProblemsPage(BasePage):
    """user profile tab where the list of created problems is located"""
    def get_expected_url(self):
        return self.base_url + UserProfileProblemsLocator.URL

    def edit_first_problem(self):
        self.click(*UserProfileProblemsLocator.FIRST_PROBLEM_EDIT_LINK)
        return ProblemPage(self.driver)

    def get_first_problem_status(self):
        return self.find_element(*UserProfileProblemsLocator.FIRST_PROBLEM_STATUS).text

    def is_first_problem_present(self):
        return self.is_element_present(*UserProfileProblemsLocator.FIRST_PROBLEM_EDIT_LINK)


class ProblemPage(BasePage):
    """Page where the detailed information about problem is shown.
       There is a map on it and section where you can edit an problem
    """
    def is_importance_field_present(self):
        if self.is_element_present(*ProblemLocator.IMPORTANCE_DROP_DOWN):
            return True
        return False

    def is_status_field_present(self):
        if self.is_element_present(*ProblemLocator.STATUS_DROP_DOWN):
            return True
        return False

    def is_change_button_present(self):
        if self.is_element_present(*ProblemLocator.CHANGE_BTN):
            return True
        return False

    def change_importance(self, value):
        select = Select(self.find_element(*ProblemLocator.IMPORTANCE_DROP_DOWN))
        select.select_by_visible_text(value)

    def change_status(self, status):
        select = Select(self.find_element(*ProblemLocator.STATUS_DROP_DOWN))
        select.select_by_visible_text(status)

    def submit_change(self):
        self.click(*ProblemLocator.CHANGE_BTN)

    def is_success_popup_present(self):
        """has problem edit success pop-up appeared?"""
        _d = self.driver
        try:
            WebDriverWait(_d, 10).until(lambda _d: _d.find_element(*ProblemLocator.POP_UP_WINDOW_SUCCESSFUL_CHANGE))
        except Exception:
            return False
        return True

    def get_importance(self):
        """get current importance value in importance field """
        my_select = Select(self.find_element(*ProblemLocator.IMPORTANCE_DROP_DOWN))
        option = my_select.first_selected_option
        return option.text

    def get_status(self):
        """get current status value in the status field"""
        my_select = Select(self.find_element(*ProblemLocator.STATUS_DROP_DOWN))
        option = my_select.first_selected_option
        return option.text

    def get_another_importance_from_options(self, value):
        """generate new importance from options"""
        my_select = Select(self.find_element(*ProblemLocator.IMPORTANCE_DROP_DOWN))
        for i in range(len(my_select.options)):
            if value != my_select.options[i].text:
                return my_select.options[i].text
        return ""

    def get_another_status_from_options(self, old_status):
        """generate new status from options"""
        my_select = Select(self.find_element(*ProblemLocator.STATUS_DROP_DOWN))
        for i in range(len(my_select.options)):
            if old_status != my_select.options[i].text:
                return my_select.options[i].text
        return ""

    def get_current_importance_info(self):
        """get importance from the label in the problem header"""
        info = self.find_element(*ProblemLocator.IMPORTANCE_INFO).text
        return info.split(' ', 1)[0]

    def get_current_status_info(self):
        """get status from the label in the problem header"""
        return self.find_element(*ProblemLocator.STATUS_INFO).text

    def get_home_user_page(self):
        """go to home page"""
        self.click(*ProblemLocator.LOGO)
        return HomeUserPage(self.driver)
