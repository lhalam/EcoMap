import random

from tests import TestLoginAsAdmin
from framework.Pages import HomeUserPage

class TestEditIssueAdmin(TestLoginAsAdmin.TestLoginAsAdmin):
    @classmethod
    def setUpClass(cls):
        super(TestEditIssueAdmin, cls).setUpClass()
        cls.home_user_page = HomeUserPage(cls.driver)

    def test_3_check_issue_edit(self):
        #select issue
        user_profile_page = self.home_user_page.get_user_profile_page()
        issues_page = user_profile_page.get_issues_page()
        issue_page = issues_page.edit_first_issue()
        #edit issue
        old_importance = issue_page.get_importance()
        new_importance = issue_page.get_another_importance_from_options(old_importance)
        issue_page.change_importance(new_importance)
        self.assertNotEqual(old_importance, issue_page.get_importance())
        old_status = issue_page.get_status()
        new_status = issue_page.get_another_status_from_options(old_status)
        issue_page.change_status(new_status)
        issue_page.submit_change()
        #verify success
        self.assertTrue(issue_page.is_success_popup_present())
        self.assertEqual(new_importance, issue_page.get_current_importance_info())
        self.assertEqual(new_status, issue_page.get_current_status_info())
        self.status = new_status
        self.home_user_page = issue_page.get_home_user_page()
        self.assertTrue(self.home_user_page.is_user_profile_link_present())
        issues_page = self.home_user_page.get_user_profile_page().get_issues_page()
        self.assertEqual(self.status, issues_page.get_first_issue_status())


