import unittest
from tests.AddProblemForAbstractUser import AddProblem


class NegativeAddProblemTestAdmin(AddProblem):

    @classmethod
    def setUpClass(cls):
        super(NegativeAddProblemTestAdmin, cls).setUpClass()
        cls.login_as(cls, 'admin')

    def test_add_problem_with_empty_coordinates(self):
        self.go_to_add_problem_page()
        self.fill_necessary_fields()
        self.check_error_messages_if_coordinates_is_empty()

    def test_add_problem_with_empty_fields(self):
        self.go_to_add_problem_page()
        self.locate_problem_with_find_me()
        self.click_on_next()
        self.check_error_messages_if_fields_are_empty()


if __name__ == '__main__':
    unittest.main()


