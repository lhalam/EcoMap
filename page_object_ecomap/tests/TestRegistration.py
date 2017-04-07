import random
import unittest
from page_object_ecomap.framework.Locators import RegisterPageLocator
from page_object_ecomap.tests.TestBase import TestBase, HomeUserPage, Registration


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
        self.reg_page.reg(self.test_data.get("registration_email") % self.generate_random_email(),
                          self.test_data.get("registration_name"),
                          self.test_data.get("registration_surname"),
                          self.test_data.get("registration_nickname") % self.generate_random_email(),
                          self.test_data.get("registration_password"),
                          self.test_data.get("registration_confirmpassword"))
        self.reg_page.wait_linked_text_changed()
        user_name = self.test_data.get("registration_name") + " " + self.test_data.get("registration_surname")
        att = self.user_page.user_credentials_btn_is_present()
        self.assertEqual(user_name.upper(), att)
        self.assertTrue(self.user_page.is_logout_btn_present())

    def generate_random_email(self):
        return str(random.randint(1, 1000))

if __name__ == '__main__':
        unittest.main()
