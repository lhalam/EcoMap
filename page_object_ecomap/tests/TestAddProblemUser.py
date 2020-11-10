import unittest
from tests.AddProblemForAbstractUser import AddProblem
from framework.Utils import generate_random_word


class AddProblemTestUser(AddProblem):

    @classmethod
    def setUpClass(cls):
        super(AddProblemTestUser, cls).setUpClass()
        cls.login_as(cls, 'user')

    def test_add_problem_without_photo_using_find_me(self):
        amnt_of_prblms_before_adding_prbl = self.check_amount_of_problems()
        self.go_to_add_problem_page()
        self.locate_problem_with_find_me()
        self.fill_necessary_fields()
        self.publish_problem()
        amnt_of_prblms_after_adding_prbl = self.check_amount_of_problems()
        self.assertEqual(amnt_of_prblms_before_adding_prbl+1, amnt_of_prblms_after_adding_prbl)

    def test_add_problem_without_photo_using_search(self):
        amnt_of_prblms_before_adding_prbl = self.check_amount_of_problems()
        self.go_to_add_problem_page()
        self.locate_problem_with_search_button()
        self.fill_necessary_fields()
        self.publish_problem()
        amnt_of_prblms_after_adding_prbl = self.check_amount_of_problems()
        self.assertEqual(amnt_of_prblms_before_adding_prbl + 1, amnt_of_prblms_after_adding_prbl)

    @unittest.expectedFailure
    def test_add_problem_with_photo_using_find_me(self):
        amnt_of_prblms_before_adding_prbl = self.check_amount_of_problems()
        self.go_to_add_problem_page()
        self.locate_problem_with_find_me()
        self.fill_necessary_fields()
        self.upload_photo(generate_random_word())
        self.publish_problem()
        amnt_of_prblms_after_adding_prbl = self.check_amount_of_problems()
        self.assertEqual(amnt_of_prblms_before_adding_prbl + 1, amnt_of_prblms_after_adding_prbl)

    @unittest.expectedFailure
    def test_add_problem_with_photo_using_search_button(self):
        amnt_of_prblms_before_adding_prbl = self.check_amount_of_problems()
        self.go_to_add_problem_page()
        self.locate_problem_with_search_button()
        self.fill_necessary_fields()
        self.upload_photo(generate_random_word())
        self.publish_problem()
        amnt_of_prblms_after_adding_prbl = self.check_amount_of_problems()
        self.assertEqual(amnt_of_prblms_before_adding_prbl + 1, amnt_of_prblms_after_adding_prbl)

if __name__ == '__main__':
    unittest.main()
