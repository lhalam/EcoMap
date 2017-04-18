import string
import unittest
from page_object_ecomap.tests.TestBase import TestBase
from page_object_ecomap.framework.Pages import*
import random


class AddProblemTestAdmin(TestBase):

    @classmethod
    def setUpClass(cls):
        super(AddProblemTestAdmin, cls).setUpClass()
        cls.add_problem = AddProblemPage(cls.driver)
        cls.login_page = LoginPage(cls.driver)
        cls.home_page.get_login_page()
        cls.home_user_page = cls.login_page.login(cls.test_data.get("email"), cls.test_data.get("password"))

    def test_add_problem_without_photo_using_find_me(self):
        self.go_to_add_problem_page()
        self.locate_problem_with_find_me()
        self.fill_necessary_fields()
        self.publish_problem()

    def test_add_problem_without_photo_using_search(self):
        self.go_to_add_problem_page()
        self.locate_problem_with_search_button()
        self.fill_necessary_fields()
        self.publish_problem()

    def test_add_problem_with_photo_using_find_me(self):
        self.go_to_add_problem_page()
        self.locate_problem_with_find_me()
        self.fill_necessary_fields()
        self.upload_photo(self.random_word())
        self.publish_problem()

    def test_add_problem_with_photo_using_search_button(self):
        self.go_to_add_problem_page()
        self.locate_problem_with_search_button()
        self.fill_necessary_fields()
        self.upload_photo(self.random_word())
        self.publish_problem()

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
        self.add_problem.fill_coordinates(self.generate_random_coordinates(), self.generate_random_coordinates())

        self.add_problem.is_search_button_present()
        self.add_problem.click_on_search()

    def fill_necessary_fields(self):
        self.assertTrue(self.add_problem.is_title_field_present())
        self.add_problem.fill_title(self.random_word())

        self.assertTrue(self.add_problem.is_problems_items_present())
        self.add_problem.choose_forest_problem()

        self.assertTrue(self.add_problem.is_description_filed_present())
        self.add_problem.fill_description_of_problem(self.random_word())

        self.assertTrue(self.add_problem.is_proposal_filed_present())
        self.add_problem.fill_proposal_of_solving(self.random_word())

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

    def generate_random_coordinates(self):
        return str(random.randint(1, 30))

    def random_word(self):
        return ''.join(random.choice(string.ascii_lowercase + string.digits)for _ in range(10))

    def tearDown(self):
        self.home_page.open()


class AddProblemTestUser(AddProblemTestAdmin):

    @classmethod
    def setUpClass(cls):
        super(AddProblemTestAdmin, cls).setUpClass()
        cls.add_problem = AddProblemPage(cls.driver)
        cls.login_page = LoginPage(cls.driver)
        cls.home_page.get_login_page()
        cls.home_user_page = cls.login_page.login("analatysh@gmail.com", "123123")

if __name__ == '__main__':
    unittest.main()








