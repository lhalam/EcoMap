from page_object_ecomap.tests import TestLoginAsAdmin
from page_object_ecomap.framework.Pages import *

class TestEditIssueAdmin(TestLoginAsAdmin.TestLoginAsAdmin):
    @classmethod
    def setUpClass(cls):
        super(TestEditIssueAdmin, cls).setUpClass()


    def test_check_issue_edit(self):
        #log in as admin
        user_profile_page = self.home_page.get_user_profile_page()
        subscriptions_page = user_profile_page.get_issues_page()
        issue_page = subscriptions_page.edit_first_issue()
        old_importance = 1
        issue_page.change_importance(4)
        issue_page.submit_change()
        self.assertTrue(issue_page.submit_change())

