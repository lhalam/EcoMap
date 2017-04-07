from tests.TestBase import TestBase
import unittest
from framework.Locators import *
from framework.Pages import *



class TestLoginAsAdmin(TestBase):
    @classmethod
    def setUpClass(cls):
        super(TestLoginAsAdmin, cls).setUpClass()
        cls.login_page = LoginPage(cls.driver)
        cls.home_user_page = HomeUserPage(cls.driver)

    def test_1_open_login_page(self):
        self.assertEqual(self.home_page.get_current_url(), self.home_page.get_expected_url())
        self.assertTrue(self.home_page.is_element_present(*HomePageLocator.LOG_IN))
        self.home_page.get_login_page()

    def test_2_assert_login_elements_are_present(self):
        self.assertTrue(self.login_page.is_element_present(*LoginPageLocator.EMAIL))
        self.assertTrue(self.login_page.is_element_present(*LoginPageLocator.PASSWORD))
        self.assertTrue(self.login_page.is_element_present(*LoginPageLocator.SUBMIT))

    def test_3_log_in_as_admin(self):
        self.login_page.type(self.test_data.get("email"), *LoginPageLocator.EMAIL)
        self.login_page.type(self.test_data.get("password"), *LoginPageLocator.PASSWORD)
        self.login_page.click(*LoginPageLocator.SUBMIT)
        self.assertTrue(self.home_page.is_element_present(*HomeUserPageLocator.LOGOUT_LINK))

    def test_4_assert_login_success(self):
        self.assertTrue(self.home_page.is_element_present(*HomeUserPageLocator.USER_PROFILE_LINK))


if __name__ == '__main__':
    unittest.main()