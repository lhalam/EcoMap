import os
from selenium.common.exceptions import TimeoutException
from page_object_ecomap.framework.BasePage import BasePage
from page_object_ecomap.framework.Locators import *
from math import fabs
from selenium.webdriver.support.wait import WebDriverWait
import requests
import json


class HomePage(BasePage):
    def get_login_page(self):
        self.click(*HomePageLocator.LOG_IN)
        return LoginPage(self.driver)

    def get_user_profile_page(self):
        self.click(*HomePageLocator.USER_PROFILE)
        return UserProfilePage(self.driver)

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


class LoginPage(BasePage):
    def login(self, login_name, password):
        self.type(login_name, *LoginPageLocator.EMAIL)
        self.type(password, *LoginPageLocator.PASSWORD)
        self.click(*LoginPageLocator.SUBMIT)
        return HomeUserPage(self.driver)

    def get_expected_url(self):
        return self.base_url + LoginPageLocator.URL


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

    def is_title_field_present(self):
        return self.is_element_present(*AddProblemPageLocator.TITLE)

    def fill_title(self, title):
        self.driver.find_element(*AddProblemPageLocator.TITLE).clear()
        self.type(title, *AddProblemPageLocator.TITLE)

    def is_problems_items_present(self):
        return self.is_element_present(*AddProblemPageLocator.PROBLEMS_LIST) and\
        self.is_element_present(*AddProblemPageLocator.FOREST_PROBLEM)

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

    def add_photo_and_description(self, description):
        input_field = self.driver.find_element(*AddProblemPageLocator.INPUT)
        input_field.send_keys(os.getcwd()+"/test_img.png")
        self.driver.find_element(*AddProblemPageLocator.PHOTO_DESCRIPTION).clear()
        self.type(description, *AddProblemPageLocator.PHOTO_DESCRIPTION)

    def is_photo_uploaded(self):
        return self.is_element_present(*AddProblemPageLocator.CHECK_UPLOADED_PHOTO)

    def get_amount_of_messages(self):
        second_message = self.is_element_present(*AddProblemPageLocator.CONFIRMATION_MESSAGE2)
        first_message = self.is_element_present(*AddProblemPageLocator.CONFIRMATION_MESSAGE)
        if second_message is True and first_message is True:
            return 2
        elif second_message is True or first_message is True:
            return 1
        else:
            return 0

    def get_confirmation_message(self):
        amount_of_message = self.get_amount_of_messages()
        if amount_of_message == 2:
            return self.driver.find_element(*AddProblemPageLocator.CONFIRMATION_MESSAGE).text
        elif amount_of_message == 1:
            return self.driver.find_element(*AddProblemPageLocator.CONFIRMATION_MESSAGE2).text
        else:
            return ""

    def close_message(self):
        self.driver.find_element(*AddProblemPageLocator.CONFIRMATION_MESSAGE).click()


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
