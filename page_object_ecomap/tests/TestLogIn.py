import unittest
from page_object_ecomap.tests.TestBase import TestBase


class TestLogin(unittest.TestCase, TestBase):

    @classmethod
    def setUpClass(cls):
        TestBase.setUpClass(cls)

    def test_log_in(self):
        self.assertTrue(self.home_page.is_logo_present())
        login_page = self.home_page.get_login_page()
        self.assertEqual(self.login_page.get_current_url(), self.login_page.get_expected_url())
        home_user_page = login_page.login(self.test_data.get("email"), self.test_data.get("password"))
        self.assertTrue(home_user_page.is_logout_btn_present())
        self.assertEqual(home_user_page.get_current_url(), home_user_page.get_expected_url())

    @classmethod
    def tearDownClass(cls):
        TestBase.tearDownClass(cls)

if __name__ == '__main__':
    unittest.main()
