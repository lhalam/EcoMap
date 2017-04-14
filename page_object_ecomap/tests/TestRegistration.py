import unittest
from framework.Locators import RegisterPageLocator
from framework.Utils import generate_random_number
from framework.Dictionary import DICTIONARY as test_data
from tests.TestBase import TestBase, HomeUserPage, Registration


class TestRegistration(TestBase):
    @classmethod
    def setUpClass(cls):
        super(TestRegistration, cls).setUpClass()
        cls.user_page = HomeUserPage(cls.driver)
        cls.reg_page = Registration(cls.driver)
        cls.home_page.get_registration_page()


    def test_1_check_registration_page(self):
        self.assertEqual(self.reg_page.get_current_url(), self.reg_page.get_expected_reg_url())
        self.assertTrue(self.reg_page.is_element_present(*RegisterPageLocator.REG_BLOCK))
        self.assertTrue(self.reg_page.is_element_present(*RegisterPageLocator.EMAIL))
        self.assertTrue(self.reg_page.is_element_present(*RegisterPageLocator.NAME))
        self.assertTrue(self.reg_page.is_element_present(*RegisterPageLocator.SURNAME))
        self.assertTrue(self.reg_page.is_element_present(*RegisterPageLocator.NICKNAME))
        self.assertTrue(self.reg_page.is_element_present(*RegisterPageLocator.PASSWORD))
        self.assertTrue(self.reg_page.is_element_present(*RegisterPageLocator.CONFIRMPASSWORD))
        self.assertTrue(self.reg_page.is_element_present(*RegisterPageLocator.SUBMIT_BUTTON))

    def test_2_check_registered_user_page(self):
        self.reg_page.reg(test_data.get("registration_email") % generate_random_number(),
                          test_data.get("registration_name"),
                          test_data.get("registration_surname"),
                          test_data.get("registration_nickname") % generate_random_number(),
                          test_data.get("registration_password"),
                          test_data.get("registration_confirm_password"))

        self.reg_page.wait_linked_text_changed()
        user_name = test_data.get("registration_name") + " " + test_data.get("registration_surname")
        att = self.user_page.user_credentials_btn_is_present()
        self.assertEqual(user_name.upper(), att)
        self.assertTrue(self.user_page.is_logout_btn_present())


if __name__ == '__main__':
        unittest.main()
