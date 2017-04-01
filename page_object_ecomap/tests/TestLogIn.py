import unittest
import os
from selenium import webdriver
from page_object_ecomap.framework.Pages import *
from page_object_ecomap.tests.TestData import TestData


class LoginTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_data = TestData("TestData.txt")
        base_url = cls.test_data.get("base_url")
        cls.path = os.path.dirname(os.path.abspath(__file__)) + "/chromedriver"
        cls.driver = webdriver.Chrome(cls.path)
        cls.driver.implicitly_wait(40)
        cls.home_page = HomePage(cls.driver, base_url)
        cls.login_page = LoginPage(cls.driver)

    def test_log_in(self):
        self.home_page.open()
        self.home_page.is_logo_present()
        login_page = self.home_page.get_login_page()
        self.assertEqual(self.login_page.get_current_url(), self.login_page.get_expected_url())
        home_user_page = login_page.login(self.test_data.get("email"), self.test_data.get("password"))
        self.assertTrue(home_user_page.is_logout_btn_present())
        self.assertEqual(home_user_page.get_expected_url(), home_user_page.get_current_url())

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

if __name__ == '__main__':
    unittest.main()
