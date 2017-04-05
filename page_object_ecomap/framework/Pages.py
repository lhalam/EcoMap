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

    def click_on_add_problem(self):
        self.driver.find_element(*NavigationLocator.ADD_PROBLEM).click()
        return AddProblemPage(self.driver)


class AddProblemPage(BasePage):

    def check_presence_of_coordinates(self, driver):
        latitude = driver.find_element(*Location_Locator.LATITUDE).get_attribute("value")
        longitude = driver.find_element(*Location_Locator.LONGITUDE).get_attribute("value")
        if latitude == '' or longitude == '':
            return False
        return float(latitude), float(longitude)

    def click_on_find_me(self):
        self.driver.find_element(*Location_Locator.FIND_ME).click()
        latitude, longitude = WebDriverWait(self.driver, 10).until(self.check_presence_of_coordinates)
        coordinates = [latitude, longitude]
        return coordinates

    def check_location(self, found_coordinates, actual_coordinates):
        # http://www.movable-type.co.uk/scripts/latlong.html
        try:
            if actual_coordinates is not None:
                if fabs(actual_coordinates[0] - found_coordinates[0]) < 0.1 \
                        and fabs(actual_coordinates[1] - found_coordinates[1]) < 0.1:
                    return True
                else:
                    return False
        except IndexError:
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
        if actual_coordinates is None:
            message = "Can't find actual location"
        else:
            message = "Actual coordinates don't equal found coordinates"
        return message

    def get_expected_url(self):
        return self.base_url + AddProblemPageLocator.URL

