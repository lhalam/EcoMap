import random
import unittest
from page_object_ecomap.framework.Locators import RegisterPageLocator, HomeUserPageLocator
from page_object_ecomap.tests.TestBase import TestBase, HomeUserPage, Registration


class TestRegistration(TestBase):
    @classmethod
    def setUpClass(cls):
        super(TestRegistration, cls).setUpClass()
        cls.user_page = HomeUserPage(cls.driver)
        cls.reg_page = Registration(cls.driver)

    def test1_registration(self):
        self.home_page.get_registration_page()
        self.assertTrue(self.reg_page.is_element_present(*RegisterPageLocator.REG_BLOCK))
        self.assertTrue(self.reg_page.is_element_present(*RegisterPageLocator.EMAIL))
        self.assertTrue(self.reg_page.is_element_present(*RegisterPageLocator.NAME))
        self.assertTrue(self.reg_page.is_element_present(*RegisterPageLocator.SURNAME))
        self.assertTrue(self.reg_page.is_element_present(*RegisterPageLocator.NICKNAME))
        self.assertTrue(self.reg_page.is_element_present(*RegisterPageLocator.PASSWORD))
        self.assertTrue(self.reg_page.is_element_present(*RegisterPageLocator.CONFIRMPASSWORD))
        self.assertTrue(self.reg_page.is_element_present(*RegisterPageLocator.SUBMIT_BUTTON))

        enter_value = self.reg_page.reg(self.test_data.get("registration_email") % self.generate_random_email(), self.test_data.get("registration_name"),
                                     self.test_data.get("registration_surname"), self.test_data.get("registration_nickname") % self.generate_random_email(),
                                     self.test_data.get("registration_password"),self.test_data.get("registration_confirmpassword"))

    def test2_check_correct_url(self):
        self.assertEqual(self.home_page.get_current_url(), self.reg_page.get_expected_reg_url())


    def test3_check_user_button(self):
        self.reg_page.wait_linked_text_changed()
        user_name = self.test_data.get("registration_name") + " " + self.test_data.get("registration_surname")
        att = self.user_page.user_credentials_btn_is_present()
        self.assertEqual(user_name.upper(), att)
        self.assertTrue(self.user_page.is_element_present(*HomeUserPageLocator.LOGOUT_LINK))

    def generate_random_email(self):
        return str(random.randint(1, 100000))


if __name__ == '__main__':
        unittest.main()
