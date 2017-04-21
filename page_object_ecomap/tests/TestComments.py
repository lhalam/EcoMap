import unittest
from tests.TestBase import TestBase
from framework.Pages import *
from framework.Dictionary import DICTIONARY as TEST_DATA


class TestAddCommentsAsAdmin(TestBase):
    @classmethod
    def setUpClass(cls):
        super(TestAddCommentsAsAdmin, cls).setUpClass()
        # login as admin
        cls.home_user_page = HomePage(cls.driver).get_login_page().login(
            TEST_DATA.get("email"), TEST_DATA.get("password"))
        cls.assertTrue(cls.home_user_page.is_logout_btn_present(), 'Logout button is absent')
        cls.comment_text = TEST_DATA.get('comment_text')
        cls.answer_text = TEST_DATA.get('answer_text')

    def setUp(self):
        user_profile_page = self.home_user_page.get_user_profile_page()
        self.assertEqual(user_profile_page.get_current_url(), user_profile_page.get_expected_url())
        problem_user_profile_page = user_profile_page.get_problems_user_profile_page()
        self.assertEqual(problem_user_profile_page.get_current_url(), problem_user_profile_page.get_expected_url())
        self.edit_problem_page = problem_user_profile_page.get_edit_problem_page()
        self.assertTrue(self.edit_problem_page.is_logout_btn_present())
        self.edit_problem_page.click_on_comment_tab()

    def test_add_comment_non_anonymous(self):
        self.is_add_comment_elements_present()
        self.edit_problem_page.add_comment(self.comment_text)
        self.assertTrue(self.edit_problem_page.is_success_popup_present(), "Success popup is not present")
        self.assertEqual(self.edit_problem_page.get_comment_nickname(), TEST_DATA.get("admin_nickname"))
        self.assertAlmostEqual(self.edit_problem_page.get_comment_datetime(),
                               self.edit_problem_page.get_current_datetime(),
                               delta=self.edit_problem_page.get_timedelta())
        self.assertEqual(self.edit_problem_page.get_comment_text(), self.comment_text)
        self.is_created_comment_elements_present(anonymous=False)

    def test_add_comment_as_anonymous(self):
        nickname = TEST_DATA.get("anonymous_nickname")
        self.is_add_comment_elements_present()
        self.edit_problem_page.add_comment_anonymous(self.comment_text)
        self.assertTrue(self.edit_problem_page.is_success_popup_present(), "Success popup is not present")
        self.assertEqual(self.edit_problem_page.get_comment_nickname(), nickname)
        self.assertAlmostEqual(self.edit_problem_page.get_comment_datetime(),
                               self.edit_problem_page.get_current_datetime(),
                               delta=self.edit_problem_page.get_timedelta())
        self.assertEqual(self.edit_problem_page.get_comment_text(), self.comment_text)
        self.is_created_comment_elements_present(anonymous=True)

    def test_add_answer_non_anonymous(self):
        self.edit_problem_page.add_comment(self.comment_text)
        self.assertTrue(self.edit_problem_page.is_success_popup_present(), "Success popup is not present")
        self.edit_problem_page.click_on_answer_link()
        self.edit_problem_page.type_answer(self.answer_text)
        self.edit_problem_page.click_on_add_answer_btn()
        self.assertTrue(self.edit_problem_page.is_success_popup_present(), "Success popup is not present")
        self.assertEqual(self.edit_problem_page.get_answer_text(), self.answer_text)
        self.assertEqual(self.edit_problem_page.get_answer_nickname(), TEST_DATA.get('admin_nickname'))

    def tearDown(self):
        user_profile_page = self.home_user_page.get_user_profile_page()
        self.assertEqual(user_profile_page.get_current_url(), user_profile_page.get_expected_url())
        comments_profile_page = user_profile_page.get_comments_user_profile_page()
        self.assertEqual(comments_profile_page.get_current_url(), comments_profile_page.get_expected_url())
        comments_profile_page.click_on_delete_btn()
        self.assertTrue(comments_profile_page.is_success_popup_present())

    def is_add_comment_elements_present(self):
        self.assertTrue(self.edit_problem_page.is_comment_textarea_visible())
        self.assertTrue(self.edit_problem_page.is_add_comment_btn_visible())
        self.assertTrue(self.edit_problem_page.is_anonymously_checkbox_visible())

    def is_created_comment_elements_present(self, anonymous=False):
        self.assertTrue(self.edit_problem_page.is_comment_answer_link_visible(),
                        "Answer link is not present in the comment")
        self.assertTrue(self.edit_problem_page.is_comment_link_visible(), "Link on comment is not present")
        if anonymous:
            self.assertTrue(self.edit_problem_page.is_comment_edit_link_invisible(),
                            "Edit link should not be visible in the comment")
        else:
            self.assertTrue(self.edit_problem_page.is_comment_edit_link_visible(),
                            "Edit link is not present in the comment")

if __name__ == '__main__':
    unittest.main()
