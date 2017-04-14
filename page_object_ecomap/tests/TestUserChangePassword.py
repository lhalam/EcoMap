import unittest
from page_object_ecomap.framework.Utils import generate_random_number
from page_object_ecomap.tests.TestBase import TestBase
from page_object_ecomap.framework.Dictionary import DICTIONARY as test_data
from page_object_ecomap.framework.Pages import *


class TestUserChangePassword(TestBase):

    @classmethod
    def setUpClass(cls):
        super(TestUserChangePassword, cls).setUpClass()
        cls.home_page = HomePage(cls.driver)
        cls.user_page = HomeUserPage(cls.driver)
        cls.login_page = LoginPage(cls.driver)
        cls.user_profile_page = UserProfilePage(cls.driver)

        registration_page = cls.home_page.get_registration_page()
        registration_page.reg(test_data.get("registration_email") % generate_random_number(),
                              test_data.get("registration_name"),
                              test_data.get("registration_surname"),
                              test_data.get("registration_nickname") % generate_random_number(),
                              test_data.get("change_password_old_pass"),
                              test_data.get("change_password_old_pass"))


    def test_user_change_pass(self):
        self.user_profile_page = self.home_page.get_user_profile_page()
        self.user_profile_page.change_pwd(test_data.get("change_password_old_pass"),
                                          test_data.get("change_password_new_pass"),
                                          test_data.get("change_password_new_pass_repeat"))

        self.assertTrue(self.user_profile_page.is_success_popup_present())



if __name__ == '__main__':
    unittest.main()
