import unittest
from tests.TestBase import TestBase
from framework.Pages import*
from framework.Dictionary import DICTIONARY as test_data
from framework.Utils import generate_random_word
from framework.Utils import generate_random_number


class AddProblemTestAdmin(TestBase):

    @classmethod
    def setUpClass(cls):
        super(AddProblemTestAdmin, cls).setUpClass()
        cls.add_problem = AddProblemPage(cls.driver)
        cls.login_page = LoginPage(cls.driver)
        cls.home_page.get_login_page()
        cls.home_user_page = cls.login_page.login(test_data.get("email"), test_data.get("password"))


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

    def test_add_problem_with_photo_using_find_me(self):
        amnt_of_prblms_before_adding_prbl = self.check_amount_of_problems()
        self.go_to_add_problem_page()
        self.locate_problem_with_find_me()
        self.fill_necessary_fields()
        self.upload_photo(generate_random_word())
        self.publish_problem()
        amnt_of_prblms_after_adding_prbl = self.check_amount_of_problems()
        self.assertEqual(amnt_of_prblms_before_adding_prbl + 1, amnt_of_prblms_after_adding_prbl)

    def test_add_problem_with_photo_using_search_button(self):
        amnt_of_prblms_before_adding_prbl = self.check_amount_of_problems()
        self.go_to_add_problem_page()
        self.locate_problem_with_search_button()
        self.fill_necessary_fields()
        self.upload_photo(generate_random_word())
        self.publish_problem()
        amnt_of_prblms_after_adding_prbl = self.check_amount_of_problems()
        self.assertEqual(amnt_of_prblms_before_adding_prbl + 1, amnt_of_prblms_after_adding_prbl)

    def go_to_add_problem_page(self):
        # check if "Add problem" tab is present
        self.assertTrue(self.home_user_page.get_current_url(), self.home_user_page.get_expected_url())
        self.assertTrue(self.home_user_page.is_add_problem_tab_present())

        # go to Add problem page
        add_problem = self.home_user_page.click_on_add_problem()
        self.assertEqual(add_problem.get_current_url(), add_problem.get_expected_url())

    def locate_problem_with_find_me(self):
        self.assertTrue(self.add_problem.is_find_me_button_present())
        self.add_problem.click_on_find_me()
        self.assertTrue(self.add_problem.is_coordinates_present())

    def locate_problem_with_search_button(self):
        self.assertTrue(self.add_problem.is_coordinates_present())
        self.add_problem.fill_coordinates(generate_random_number('float', 99.99), generate_random_number('float', 99.99))

        self.add_problem.is_search_button_present()
        self.add_problem.click_on_search()

    def fill_necessary_fields(self):
        self.assertTrue(self.add_problem.is_title_field_present())
        self.add_problem.fill_title(generate_random_word())

        self.assertTrue(self.add_problem.is_problems_items_present())
        self.add_problem.choose_forest_problem()

        self.assertTrue(self.add_problem.is_description_filed_present())
        self.add_problem.fill_description_of_problem(generate_random_word())

        self.assertTrue(self.add_problem.is_proposal_filed_present())
        self.add_problem.fill_proposal_of_solving(generate_random_word())

        self.assertTrue(self.add_problem.is_next_button_filed_present())
        self.add_problem.click_on_next()

    def publish_problem(self):
        self.assertTrue(self.add_problem.is_publish_button_filed_present())
        self.add_problem.click_on_publish()
        message = self.add_problem.get_confirmation_message()
        self.assertEqual(message,
                         "Проблема упішно додана та проходить модерацію. Очікуйте повідомлення.")

    def upload_photo(self, description):
        self.add_problem.add_photo_and_description(description)

        self.assertTrue(self.add_problem.is_add_photo_element_present())
        self.assertTrue(self.add_problem.is_description_of_photo_present())
        self.assertTrue(self.add_problem.is_photo_uploaded())

    def check_amount_of_problems(self):
        problems_page = self.home_user_page.get_user_profile_page().get_problems_page()
        return int(problems_page.get_total_amount_of_problems())

    def tearDown(self):
        self.home_user_page.open()


class AddProblemTestUser(AddProblemTestAdmin):

    @classmethod
    def setUpClass(cls):
        super(AddProblemTestAdmin, cls).setUpClass()
        cls.add_problem = AddProblemPage(cls.driver)
        cls.login_page = LoginPage(cls.driver)
        cls.home_page.get_login_page()
        cls.home_user_page = cls.login_page.login(test_data.get('user_for_add_problem'), test_data.get('password_for_add_problem_user'))

if __name__ == '__main__':
    unittest.main()










