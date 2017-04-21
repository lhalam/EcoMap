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
from datetime import datetime
from datetime import timedelta
from selenium.webdriver.support import expected_conditions as EC


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

    def get_statistics_page(self):
        return self.click(*NavigationLocator.STATISTIC)

    def logout(self):
        return self.find_element(*HomeUserPageLocator.LOGOUT_LINK).click()


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
    """This page where user can add new problem"""

    """try to get value of coordinates from fields latitude and longitude"""
    def check_presence_of_coordinates(self, driver):
        try:
            latitude = driver.find_element(*Location_Locator.LATITUDE).get_attribute("value")
            longitude = driver.find_element(*Location_Locator.LONGITUDE).get_attribute("value")
            return float(latitude), float(longitude)
        except (TypeError, ValueError):
            return False

    """click on 'Find me' button and return found coordinates"""
    def click_on_find_me(self):
        try:
            self.driver.find_element(*Location_Locator.FIND_ME).click()
            latitude, longitude = WebDriverWait(self.driver, 5).until(self.check_presence_of_coordinates)
            found_coordinates = [latitude, longitude]
            return found_coordinates
        except TimeoutException:
            return None

    """Validate that coordinates found by applications equal your actual coordinates
    or deviates from actual not more then 11 km"""
    def check_location(self, found_coordinates, actual_coordinates):
        try:
            if fabs(actual_coordinates[0] - found_coordinates[0]) < 0.1 \
                    and fabs(actual_coordinates[1] - found_coordinates[1]) < 0.1:
                return True
            else:
                return False
        except (IndexError, TypeError):
            return False

    """return actual coordinates which is found by outside service"""
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

    def is_coordinates_present(self):
        return self.is_element_present(*Location_Locator.LATITUDE) and \
               self.is_element_present(*Location_Locator.LONGITUDE)

    def is_find_me_button_present(self):
        return self.is_element_present(*Location_Locator.FIND_ME)

    def fill_coordinates(self, latitude, longitude):
        self.driver.find_element(*Location_Locator.LATITUDE).clear()
        self.type(latitude, *Location_Locator.LATITUDE)
        self.driver.find_element(*Location_Locator.LONGITUDE).clear()
        self.type(longitude, *Location_Locator.LONGITUDE)

    """Return the reason of why found coordinates don't equal actual coordinates"""
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

    def is_title_field_present(self):
        return self.is_element_present(*AddProblemPageLocator.TITLE)

    def fill_title(self, title):
        self.driver.find_element(*AddProblemPageLocator.TITLE).clear()
        self.type(title, *AddProblemPageLocator.TITLE)

    def is_problems_items_present(self):
        return self.is_element_present(*AddProblemPageLocator.PROBLEMS_LIST)

    def choose_forest_problem(self):
        self.driver.find_element(*AddProblemPageLocator.PROBLEMS_LIST).click()
        self.driver.find_element(*AddProblemPageLocator.FOREST_PROBLEM).click()

    def is_description_filed_present(self):
        return self.is_element_present(*AddProblemPageLocator.PROBLEM_DESCRIPTION)

    def fill_description_of_problem(self, description):
        self.driver.find_element(*AddProblemPageLocator.PROBLEM_DESCRIPTION).clear()
        self.type(description, *AddProblemPageLocator.PROBLEM_DESCRIPTION)

    def is_proposal_filed_present(self):
        return self.is_element_present(*AddProblemPageLocator.PROPOSAL)

    def fill_proposal_of_solving(self, proposal):
        self.driver.find_element(*AddProblemPageLocator.PROPOSAL).clear()
        self.type(proposal, *AddProblemPageLocator.PROPOSAL)

    def is_next_button_filed_present(self):
        return self.is_element_present(*AddProblemPageLocator.NEXT)

    def click_on_next(self):
        self.driver.find_element(*AddProblemPageLocator.NEXT).click()

    def is_publish_button_filed_present(self):
        return self.is_element_present(*AddProblemPageLocator.PUBLISH)

    def is_search_button_present(self):
        return self.is_element_present(*AddProblemPageLocator.SEARCH)

    def click_on_publish(self):
        self.driver.find_element(*AddProblemPageLocator.PUBLISH).click()

    def click_on_search(self):
        self.driver.find_element(*AddProblemPageLocator.SEARCH).click()

    def is_add_photo_element_present(self):
        return self.is_element_present(*AddProblemPageLocator.ADD_PHOTO)

    def is_description_of_photo_present(self):
        return self.is_element_present(*AddProblemPageLocator.PHOTO_DESCRIPTION)

    """Upload photo using path to image from environment variable PYTHONPATH
    and add description to it"""
    def add_photo_and_description(self, description):
        input_field = self.driver.find_element(*AddProblemPageLocator.INPUT)
        pythonpath = os.environ.get('PYTHONPATH')
        pythonpath1 = pythonpath.lstrip(':')
        input_field.send_keys(pythonpath1 + '/tests/test_img.png')
        self.driver.find_element(*AddProblemPageLocator.PHOTO_DESCRIPTION).clear()
        self.type(description, *AddProblemPageLocator.PHOTO_DESCRIPTION)

    def is_photo_uploaded(self):
        return self.is_element_present(*AddProblemPageLocator.CHECK_UPLOADED_PHOTO)

    """Return top notification after adding new problem"""
    def get_confirmation_message(self):
        if self.is_element_present(*AddProblemPageLocator.ERROR_MESSAGE):
            return self.driver.find_element(*AddProblemPageLocator.ERROR_MESSAGE).text
        return self.driver.find_element(*AddProblemPageLocator.CONFIRMATION_MESSAGE).text


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

    def get_message_for_email_field(self):
        return self.find_element(*RegisterPageLocator.MESSAGE_EMAIL).text

    def get_message_for_name_field(self):
        return self.find_element(*RegisterPageLocator.MESSAGE_NAME).text

    def get_message_for_surname_field(self):
        return self.find_element(*RegisterPageLocator.MESSAGE_SURNAME).text

    def get_message_for_nickname_field(self):
        return self.find_element(*RegisterPageLocator.MESSAGE_NICKNAME).text



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

    def is_err_msg_pass_not_match(self):
        if "ng-active" in self.driver.find_element(*UserProfileLocator.ERR_MSG_PRESENT).get_attribute("class"):
            if self.driver.find_element(*UserProfileLocator.ERR_MSG_PASS_NOT_MATCH):
                return True
        return False

    def is_err_msg_pass_is_necessary(self):
        if "ng-active" in self.driver.find_element(*UserProfileLocator.ERR_MSG_PRESENT).get_attribute("class"):
            if self.driver.find_element(*UserProfileLocator.ERR_MSG_PASS_IS_NECESSARY):
                return True
        return False

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

    def get_admin_tab(self):
        self.click(*UserProfileNavigationLocator.ADMIN_TAB)

    def wait_until_page_is_loaded(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_all_elements_located)

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



    def get_admin_tab(self):
        self.click(*UserProfileNavigationLocator.ADMIN_TAB)

    def wait_until_page_is_loaded(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_all_elements_located)

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

    def get_total_amount_of_problems(self):
        return self.driver.find_element(*UserProfileProblemsLocator.TOTAL_AMOUNT_OF_PROBLEMS).text

class UserProfileSubscriptionPage(BasePage):
    def get_expected_url(self):
        return UserProfileProblemsLocator.URL

    def open_subscription_page(self):
        self.wait_until_invisibility_of_element_located(CommonLocator.SUCCESS_POPUP, timeout=10)
        return self.click(*UserProfileNavigationLocator.SUBSCRIPTIONS_TAB)

    def get_number_subscription(self):
        return self.find_element(*UserProfileSubscriprionLocator.SUBSCRIPTIONS_INFO).text

    def get_title_1(self):
        return self.find_element(*UserProfileSubscriprionLocator.TITLE_1).text

    def get_count(self):
        return self.find_element(*UserProfileSubscriprionLocator.COUNT).text

    def open_view(self):
        return self.click(*UserProfileSubscriprionLocator.VIEW)


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

    def get_popup_text(self):
        return self.find_element(*ProblemLocator.POP_UP_WINDOW_TITLE).text

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

    def tap_subscription(self):
        return self.find_element(*Statistics.EYE).click()

    def check_title(self):
        return self.find_element(*ProblemLocator.DETAILED_TITLE).text


class StatisticPage(BasePage):
    def get_current_url(self):
        return Statistics.URL

    def open_top_first_issue(self):
        return self.click(*Statistics.TOP_FIRST_ISSUE)


class AdministerTabPage(BasePage):
    def get_issue_type_tab(self):
        self.click(*AdministerTabLocator.ISSUE_TYPE_TAB)

    def click_first_issue_changetype_button(self):
        self.click(*AdministerTabLocator.FIRST_ISSUE_CHANGE_STATUS_BUTTON)

    def change_issue_type(self, new_type):
        self.wait_until_element_is_visible(AdministerTabLocator.ISSUE_TYPE_FIELD, timeout=10)
        self.type(new_type, *AdministerTabLocator.ISSUE_TYPE_FIELD)
        self.wait_until_element_is_visible(AdministerTabLocator.SUBMIT_BUTTON, timeout=10)
        self.click(*AdministerTabLocator.SUBMIT_BUTTON)

    def is_success_popup_present(self):
        _d = self.driver
        try:
            WebDriverWait(_d, 5).until(lambda _d: _d.find_element(*AdministerTabLocator.TYPE_CHANGED_SUCCES_POPUP))
        except Exception:
            return False
        return True
