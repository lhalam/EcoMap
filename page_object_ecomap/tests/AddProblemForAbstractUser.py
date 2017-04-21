from tests.TestBase import TestBase
from framework.Pages import*
from framework.Dictionary import DICTIONARY as test_data
from framework.Utils import generate_random_word
from framework.Utils import generate_random_number


class AddProblem(TestBase):

    @classmethod
    def setUpClass(cls):
        super(AddProblem, cls).setUpClass()
        cls.add_problem = AddProblemPage(cls.driver)
        cls.home_page = HomePage(cls.driver)
        cls.login_page = cls.home_page.get_login_page()

    def login_as(self, user):
        if user == 'admin':
            self.home_user_page = self.login_page.login(
                test_data.get('email'), test_data.get('password'))
        else:
            self.home_user_page = self.login_page.login(
                test_data.get('user_for_add_problem'), test_data.get('password_for_add_problem_user'))

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

        self.click_on_next()

    def click_on_next(self):
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
        if problems_page.get_total_amount_of_problems() == '':
            return 0
        return int(problems_page.get_total_amount_of_problems())

    def check_error_messages_if_coordinates_is_empty(self):
        errors = self.add_problem.get_errors_if_coordinates_is_empty()
        for i in errors:
            self.assertEqual(i, "Це поле є обов'язковим.")
            self.assertEqual(i, "Це поле є обов'язковим.")

    def check_error_messages_if_fields_are_empty(self):
        errors = self.add_problem.get_errors_if_incorrect_data_in_fields()
        for i in errors:
            self.assertEqual(i, "Це поле є обов'язковим.")

    def tearDown(self):
        self.home_user_page.open()

    def fill_necessary_fields_with_short_data(self):
        self.assertTrue(self.add_problem.is_title_field_present())
        self.add_problem.fill_title(generate_random_word(length_of_word=1))

        self.assertTrue(self.add_problem.is_problems_items_present())
        self.add_problem.choose_forest_problem()

        self.assertTrue(self.add_problem.is_description_filed_present())
        self.add_problem.fill_description_of_problem(generate_random_word(length_of_word=1))

        self.assertTrue(self.add_problem.is_proposal_filed_present())
        self.add_problem.fill_proposal_of_solving(generate_random_word(length_of_word=1))

        self.click_on_next()

    def fill_necessary_fields_with_long_data(self):
        self.assertTrue(self.add_problem.is_title_field_present())
        self.add_problem.fill_title(generate_random_word(length_of_word=300))

        self.assertTrue(self.add_problem.is_problems_items_present())
        self.add_problem.choose_forest_problem()

        self.assertTrue(self.add_problem.is_description_filed_present())
        self.add_problem.fill_description_of_problem(generate_random_word(length_of_word=300))

        self.assertTrue(self.add_problem.is_proposal_filed_present())
        self.add_problem.fill_proposal_of_solving(generate_random_word(length_of_word=300))

        self.click_on_next()

    def check_error_messages_if_fields_are_too_short(self):
        errors = self.add_problem.get_errors_if_incorrect_data_in_fields()
        for i in errors:
            self.assertEqual(i, "Занадто коротке поле.")

    def check_error_messages_if_fields_are_too_long(self):
        errors = self.add_problem.get_errors_if_incorrect_data_in_fields()
        for i in errors:
            self.assertEqual(i, "Занадто довге поле.")



