import unittest

from tests.TestBase import TestBase
from framework.Dictionary import DICTIONARY as test_data
from framework.Pages import *


class TestEditIssueType(TestBase):
    @classmethod
    def setUpClass(cls):
        super(TestEditIssueType, cls).setUpClass()
        cls.home_page = HomePage(cls.driver)
        cls.user_page = HomeUserPage(cls.driver)
        cls.login_page = LoginPage(cls.driver)
        cls.user_profile_page = UserProfilePage(cls.driver)
        cls.administer_page = AdministerTabPage(cls.driver)

    @unittest.expectedFailure
    def test_admin_changes_issue_type(self):
        self.home_page.get_login_page()
        self.login_page.login(test_data.get("email"), test_data.get("password"))
        self.user_page.get_user_profile_page()
        self.user_profile_page.get_problems_page()
        self.user_profile_page.get_admin_tab()
        self.administer_page.get_issue_type_tab()
        self.administer_page.click_first_issue_changetype_button()
        self.administer_page.change_issue_type(test_data.get("new_issue_type"))
        self.assertTrue(self.administer_page.is_success_popup_present())
