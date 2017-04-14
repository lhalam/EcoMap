from tests import TestLoginAsAdmin
from framework.Pages import HomeUserPage


class TestEditProblemAdmin(TestLoginAsAdmin.TestLoginAsAdmin):

    def test_3_check_problem_edit(self):
        # select problem
        home_user_page = HomeUserPage(self.driver)
        user_profile_page = home_user_page.get_user_profile_page()
        user_profile_page.wait_until_page_is_loaded()
        self.assertTrue(home_user_page.is_user_profile_link_present())
        user_problems_page = user_profile_page.get_problems_page()
        self.assertTrue(user_problems_page.is_first_problem_present())
        problem_page = user_problems_page.edit_first_problem()
        # edit problem
        self.assertTrue(problem_page.is_importance_field_present() and
                        problem_page.is_status_field_present() and
                        problem_page.is_change_button_present())
        old_importance = problem_page.get_importance()
        new_importance = problem_page.get_another_importance_from_options(old_importance)
        problem_page.change_importance(new_importance)
        self.assertNotEqual(old_importance, problem_page.get_importance())
        old_status = problem_page.get_status()
        new_status = problem_page.get_another_status_from_options(old_status)
        problem_page.change_status(new_status)
        problem_page.submit_change()
        # verify success
        self.assertTrue(problem_page.is_success_popup_present())
        self.assertEqual(new_importance, problem_page.get_current_importance_info())
        self.assertEqual(new_status, problem_page.get_current_status_info())
        # verify changes on the user's problems page
        home_user_page = problem_page.get_home_user_page()
        user_profile_page = home_user_page.get_user_profile_page()
        user_profile_page.wait_until_page_is_loaded()
        user_problems_page = user_profile_page.get_problems_page()
        self.assertEqual(new_status, user_problems_page.get_first_problem_status())
