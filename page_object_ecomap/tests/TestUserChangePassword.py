import unittest
from page_object_ecomap.tests.TestBase import TestBase
from page_object_ecomap.framework.Pages import *
from tests.TestLogIn import TestLogin


class TestUserChangePassword(unittest.TestCase, TestBase):

    @classmethod
    def setUpClass(cls):
        TestBase.setUpClass(cls)

    def user_change_pass(self):
        TestLogin.test_log_in(self)
        user_profile_page = self.home_page.get_user_profile_page()
        user_profile_page.change_pwd(self.test_data.get("change_password_old_pass"),
                                     self.test_data.get("change_password_new_pass"),
                                     self.test_data.get("change_password_new_pass_repeat"))
        self.assertTrue(user_profile_page.is_success_popup_present())

    @classmethod
    def tearDownClass(cls):
        TestBase.tearDownClass(cls)


if __name__ == '__main__':
    unittest.main()
