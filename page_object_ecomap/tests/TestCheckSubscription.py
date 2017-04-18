import unittest

from framework.Locators import RegisterPageLocator
from framework.Utils import generate_random_number
from framework.Dictionary import DICTIONARY as test_data
from tests.TestBase import TestBase, HomeUserPage, Registration, UserProfilePage, UserProfileSubscriptionPage, \
    StatisticPage, ProblemPage


class TestRegistration(TestBase):
    @classmethod
    def setUpClass(cls):
        super(TestRegistration, cls).setUpClass()
        cls.user_page = HomeUserPage(cls.driver)
        cls.reg_page = Registration(cls.driver)
        cls.user_profile_page = UserProfilePage(cls.driver)
        cls.user_profile_subscription_page = UserProfileSubscriptionPage(cls.driver)
        cls.statistic = StatisticPage(cls.driver)
        cls.problem_page = ProblemPage(cls.driver)
        cls.home_page.get_registration_page()
        cls.reg_page.reg(test_data.get("registration_email") % generate_random_number(),
                          test_data.get("registration_name"),
                          test_data.get("registration_surname"),
                          test_data.get("registration_nickname") % generate_random_number(),
                          test_data.get("registration_password"),
                          test_data.get("registration_confirm_password"))
        cls.reg_page.wait_linked_text_changed()


    def test_1_check_subscription_page(self):
        self.user_page.get_user_profile_page()
        self.user_profile_subscription_page.open_subscription_page()
        self.assertEqual(self.user_profile_subscription_page.get_number_subscription(), 'Підписки відсутні.')

    def test_2_start_subscribe_issue(self):
        self.user_page.get_statistics_page()
        self.statistic.open_top_first_issue()

        self.driver.switch_to.window(self.driver.window_handles[1])
        title = self.problem_page.check_title()
        self.problem_page.tap_subscription()
        self.assertTrue(self.problem_page.is_success_popup_present)
        self.assertEqual(self.problem_page.get_popup_text(), "Додавання")
        self.user_page.get_user_profile_page()

        self.user_profile_subscription_page.open_subscription_page()

        self.assertEqual(title, self.user_profile_subscription_page.get_title_1())
        self.assertEqual(self.user_profile_subscription_page.get_count(), "1")

    def test_3_unsubscribe_issue(self):
        title = self.user_profile_subscription_page.get_title_1()
        self.user_profile_subscription_page.open_view()
        self.driver.switch_to.window(self.driver.window_handles[2])
        self.assertEqual(title, self.problem_page.check_title())
        self.problem_page.tap_subscription()
        self.assertTrue(self.problem_page.is_success_popup_present)
        self.assertEqual(self.problem_page.get_popup_text(), "Видалення")
        self.user_page.get_user_profile_page()
        self.user_profile_subscription_page.open_subscription_page()
        self.assertEqual(self.user_profile_subscription_page.get_number_subscription(), 'Підписки відсутні.')


if __name__ == '__main__':
        unittest.main()
