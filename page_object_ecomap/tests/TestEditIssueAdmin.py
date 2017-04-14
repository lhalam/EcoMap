from tests import TestLoginAsAdmin
from framework.Pages import HomeUserPage


class TestEditIssueAdmin(TestLoginAsAdmin.TestLoginAsAdmin):

    def test_3_check_issue_edit(self):
        # select issue
        home_user_page = HomeUserPage(self.driver)
        user_profile_page = home_user_page.get_user_profile_page()
        user_issues_page = user_profile_page.get_issues_page()
        self.assertTrue(user_issues_page.is_first_issue_present())
        issue_page = user_issues_page.edit_first_issue()
        # edit issue
        self.assertTrue(issue_page.is_importance_field_present() and
                        issue_page.is_status_field_present() and
                        issue_page.is_change_button_present())
        old_importance = issue_page.get_importance()
        new_importance = issue_page.get_another_importance_from_options(old_importance)
        issue_page.change_importance(new_importance)
        self.assertNotEqual(old_importance, issue_page.get_importance())
        old_status = issue_page.get_status()
        new_status = issue_page.get_another_status_from_options(old_status)
        issue_page.change_status(new_status)
        issue_page.submit_change()
        # verify success
        self.assertTrue(issue_page.is_success_popup_present())
        self.assertEqual(new_importance, issue_page.get_current_importance_info())
        self.assertEqual(new_status, issue_page.get_current_status_info())
        home_user_page = issue_page.get_home_user_page()
        self.assertTrue(home_user_page.is_user_profile_link_present())
        user_issues_page = home_user_page.get_user_profile_page().get_issues_page()
        self.assertEqual(new_status, user_issues_page.get_first_issue_status())
