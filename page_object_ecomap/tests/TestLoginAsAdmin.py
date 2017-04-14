from tests.TestBase import TestBase
import unittest
from framework.Pages import *
from framework.Dictionary import DICTIONARY as test_data


class TestLoginAsAdmin(TestBase):

    def test_1_assert_home_page_is_open(self):
        self.assertEqual(self.home_page.get_current_url(), self.home_page.get_expected_url())
        self.assertTrue(self.home_page.is_element_present(*HomePageLocator.LOG_IN))

    def test_2_log_in_as_admin_and_assert_success(self):
        login_page = self.home_page.get_login_page()
        self.assertTrue(login_page.is_element_present(*LoginPageLocator.EMAIL))
        self.assertTrue(login_page.is_element_present(*LoginPageLocator.PASSWORD))
        self.assertTrue(login_page.is_element_present(*LoginPageLocator.SUBMIT))
        home_user_page = login_page.login(test_data.get("email"), test_data.get("password"))
        self.assertTrue(home_user_page.is_logout_btn_present())
        self.assertTrue(home_user_page.is_user_profile_link_present())

if __name__ == '__main__':
    unittest.main()
