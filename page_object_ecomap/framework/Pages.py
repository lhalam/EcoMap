#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium.common.exceptions import TimeoutException
from framework.BasePage import BasePage
from framework.Locators import *
from math import fabs
from selenium.webdriver.support.wait import WebDriverWait
import requests
import json
from datetime import datetime
from datetime import timedelta


class HomePage(BasePage):
    def get_login_page(self):
        self.click(*HomePageLocator.LOG_IN)
        return LoginPage(self.driver)

    def get_expected_url(self):
        return HomePageLocator.URL

    def get_registration_page(self):
        self.click(*HomePageLocator.REGISTER)
        return Registration(self.driver)

    def is_login_link_present(self):
        return self.is_element_present(*HomePageLocator.LOG_IN)


class HomeUserPage(BasePage):
    def get_expected_url(self):
        return HomeUserPageLocator.URL

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
        if self.is_element_present(*HomeUserPageLocator.USER_PROFILE_LINK):
            self.click(*HomeUserPageLocator.USER_PROFILE_LINK)
            return UserProfilePage(self.driver)
        else:
            return None


class LoginPage(BasePage):
    def login(self, login_name, password):
        self.type(login_name, *LoginPageLocator.EMAIL)
        self.type(password, *LoginPageLocator.PASSWORD)
        self.click(*LoginPageLocator.SUBMIT)
        return HomeUserPage(self.driver)

    def get_expected_url(self):
        return LoginPageLocator.URL

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
        return AddProblemPageLocator.URL


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
        return RegisterPageLocator.REG_URL

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
        return UserProfileLocator.URL

    def get_problems_user_profile_page(self):
        if self.is_element_present(*ProblemsUserProfileLocator.PROBLEMS_TAB):
            self.click(*ProblemsUserProfileLocator.PROBLEMS_TAB)
            return ProblemsUserProfilePage(self.driver)
        else:
            return None

    def get_comments_user_profile_page(self):
        if self.is_element_present(*CommentsUserProfileLocator.MY_COMMENTS_TAB):
            self.click(*CommentsUserProfileLocator.MY_COMMENTS_TAB)
            return CommentsUserProfilePage(self.driver)
        else:
            return None


class ProblemsUserProfilePage(BasePage):

    def get_expected_url(self):
        return ProblemsUserProfileLocator.URL

    def get_edit_problem_page(self):
        if self.is_element_present(*ProblemsUserProfileLocator.EDIT_LINK_BY_PROMLEM_TITLE):
            self.click(*ProblemsUserProfileLocator.EDIT_LINK_BY_PROMLEM_TITLE)
            return EditProblemPage(self.driver)
        else:
            return None


class EditProblemPage(HomeUserPage):

    def add_comment_anonymous(self, text):
        self.click_on_anonymous_checkbox()
        self.add_comment(text)

    def add_comment(self, text):
        self.type_comment(text)
        self.click_on_add_comment_btn()

    def click_on_comment_tab(self):
        self.click(*EditProblemLocator.COMMENT_TAB)

    def type_comment(self, text):
        self.type(text, *EditProblemLocator.COMMENT_TEXTAREA)

    def is_comment_textarea_visible(self):
        return self.is_element_visible(*EditProblemLocator.COMMENT_TEXTAREA)

    def is_anonymously_checkbox_visible(self):
        return self.is_element_visible(*EditProblemLocator.ANONYMOUSLY_CHECKBOX)

    def is_add_comment_btn_visible(self):
        return self.is_element_visible(*EditProblemLocator.ADD_COMMENT_BTN)

    def click_on_add_comment_btn(self):
        self.click(*EditProblemLocator.ADD_COMMENT_BTN)

    def get_comment_nickname(self):
        return self.get_text(*EditProblemLocator.COMMENT_NICKNAME)

    def get_comment_datetime(self):
        if self.is_element_visible(*EditProblemLocator.COMMENT_DATETIME):
            element = self.find_element(*EditProblemLocator.COMMENT_DATETIME)
            return datetime.strptime(element.text, '%d/%m/%Y %H:%M')
        else:
            return None

    def get_current_datetime(self):
        return datetime.strptime(datetime.now().strftime('%d/%m/%Y %H:%M'), '%d/%m/%Y %H:%M')

    def get_comment_text(self):
        return self.get_text(*EditProblemLocator.COMMENT_TEXT)

    def get_timedelta(self):
        return timedelta(seconds=10)

    def is_comment_answer_link_visible(self):
        return self.is_element_visible(*EditProblemLocator.COMMENT_ANSWER_LINK)

    def is_success_popup_present(self):
        return self.is_popup_present(*CommonLocator.SUCCESS_POPUP)

    def is_comment_edit_link_visible(self):
        return self.is_element_visible(*EditProblemLocator.COMMENT_EDIT_LINK)

    def is_comment_edit_link_invisible(self):
        return self.is_element_invisible(*EditProblemLocator.COMMENT_EDIT_LINK_HIDDEN)

    def is_comment_link_visible(self):
        return self.is_element_visible(*EditProblemLocator.COMMENT_LINK)

    def click_on_anonymous_checkbox(self):
        self.click(*EditProblemLocator.ANONYMOUSLY_CHECKBOX)

    def click_on_answer_link(self):
        self.click(*EditProblemLocator.COMMENT_ANSWER_LINK)

    def type_answer(self, text):
        self.type(text, *EditProblemLocator.ANSWER_TEXTAREA)

    def click_on_add_answer_btn(self):
        self.click(*EditProblemLocator.ADD_ANSWER_BTN)

    def is_answer_textarea_visible(self):
        self.is_element_visible(*EditProblemLocator.ANSWER_TEXTAREA)

    def get_answer_text(self):
        return self.get_text(*EditProblemLocator.ANSWER_TEXT)

    def get_answer_nickname(self):
        return self.get_text(*EditProblemLocator.ANSWER_NICKNAME)


class CommentsUserProfilePage(BasePage):
    def get_expected_url(self):
        return CommentsUserProfileLocator.URL

    def click_on_delete_btn(self):
        self.click(*CommentsUserProfileLocator.DELETE_LINK_BY_COMMENT_TITLE)

    def is_success_popup_present(self):
        return self.is_popup_present(*CommonLocator.SUCCESS_POPUP)


