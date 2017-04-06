from page_object_ecomap.tests import TestBase
from page_object_ecomap.framework import Pages
from page_object_ecomap.framework.Locators import *


class TestEditIssueAsAdmin(TestBase.TestBase):
    @classmethod
    def setUpClass(cls):
        super(TestEditIssueAsAdmin, cls).setUpClass()
        cls.home_user_page = Pages.HomeUserPage(cls.driver)
        cls.login_page = Pages.LoginPage(cls.driver)
        cls.user_profile_info_page = Pages.UserProfileInfoPage(cls.driver)
        cls.user_profile_subscriptions_page = Pages.UserProfileSubscriptionsPage(cls.driver)
        cls.first_problem_page = Pages.FirstDetailedProblemPage(cls.driver)

    def test_1_login_as_admin(self):
        self.home_page.get_login_page()
        self.login_page.type(self.test_data.get("email"), *LoginPageLocator.EMAIL)
        self.login_page.type(self.test_data.get("password"), *LoginPageLocator.PASSWORD)
        self.login_page.click(*LoginPageLocator.SUBMIT)

    def test_2_go_to_subscriptions(self):
        self.assertTrue(self.home_user_page.is_element_present(*HomeUserPageLocator.USER_PROFILE_LINK))
        self.home_user_page.get_user_profile_page()
        self.user_profile_info_page.get_my_subscriptions_page()

    def test_3_go_to_first_subscription(self):
        self.assertTrue(self.user_profile_subscriptions_page.is_element_present(*UserProfileSubscriptionsLocator.FIRST_SHOW_SUBSCRIPTION_LINK))
        self.user_profile_subscriptions_page.click(*UserProfileSubscriptionsLocator.FIRST_SHOW_SUBSCRIPTION_LINK)
        self.first_problem_page = Pages.FirstDetailedProblemPage(self.driver)
        #eself.first_problem_page.change_problem_importance(4)
