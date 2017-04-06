import unittest
from page_object_ecomap.tests.TestBase import TestBase
from page_object_ecomap.framework.Pages import *


class TestLogin(unittest.TestCase, TestBase):

    @classmethod
    def setUpClass(cls):
        TestBase.setUpClass(cls)

    def test_log_in(self):
        login_page = self.home_page.get_login_page()
        home_user_page = login_page.login(self.test_data.get("change_password_email"),
                                          self.test_data.get("change_password_password"))
        self.assertEqual(home_user_page.get_current_url(), home_user_page.get_expected_url())

    @classmethod
    def tearDownClass(cls):
        TestBase.tearDownClass(cls)


if __name__ == '__main__':
    unittest.main()
