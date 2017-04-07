import unittest
from page_object_ecomap.tests.TestBase import TestBase
from page_object_ecomap.framework.Pages import *


class TestUserChangePassword(TestBase):

    @classmethod
    def setUpClass(cls):
        super(TestUserChangePassword, cls).setUpClass()
        cls.user_page = HomeUserPage(cls.driver)
        cls.login_page = LoginPage(cls.driver)
        cls.user_profile_page = UserProfilePage(cls.driver)


    def user_change_pass(self):
        self.home_page.get_login_page()

        self.login_page.login(self.test_data.get("email_for_change_pass"),
                              self.test_data.get("pass_for_change_pass"))

        self.user_profile_page = self.home_page.get_user_profile_page()
        self.user_profile_page.change_pwd(self.test_data.get("change_password_old_pass"),
                                     self.test_data.get("change_password_new_pass"),
                                     self.test_data.get("change_password_new_pass_repeat"))

        self.assertTrue(self.user_profile_page.is_success_popup_present())


if __name__ == '__main__':
    unittest.main()
