from page_object_ecomap.tests.TestBase import TestBase
import unittest
from page_object_ecomap.framework.Locators import *
from page_object_ecomap.framework.Pages import HomeUserPage



class TestLoginAsAdmin(unittest.TestCase, TestBase):
    @classmethod
    def setUpClass(cls):
        TestBase.setUpClass(cls)
        cls.home_user_page = HomeUserPage(cls.driver)

    def test_log_in_as_admin(self):
        self.assertEqual(self.home_page.get_current_url(), self.home_page.get_expected_url())
        self.assertTrue(self.home_page.is_element_present(*HomePageLocator.LOG_IN))
        self.home_page.get_login_page()

        self.assertTrue(self.login_page.is_element_present(*LoginPageLocator.EMAIL))
        self.assertTrue(self.login_page.is_element_present(*LoginPageLocator.PASSWORD))
        self.assertTrue(self.login_page.is_element_present(*LoginPageLocator.SUBMIT))

        self.login_page.type(self.test_data.get("email"), *LoginPageLocator.EMAIL)
        self.login_page.type(self.test_data.get("password"), *LoginPageLocator.PASSWORD)
        self.login_page.click(*LoginPageLocator.SUBMIT)
        self.login_page.wait_until_home_page_is_loaded()

        self.assertEqual(self.home_page.get_current_url(), self.home_user_page.get_expected_url())
        self.assertTrue(self.home_page.is_element_present(*HomeUserPageLocator.LOGOUT_LINK))
        self.assertTrue(self.home_page.is_element_present(*HomeUserPageLocator.USER_PROFILE_LINK))

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == '__main__':
    unittest.main()