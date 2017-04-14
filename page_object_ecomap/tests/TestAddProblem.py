import unittest
from page_object_ecomap.tests.TestBase import TestBase
from page_object_ecomap.framework.Pages import*
import random


class AddProblemTestAdmin(TestBase):

    def setUp(self):
        super(AddProblemTestAdmin, self).setUpClass()
        self.add_problem = AddProblemPage(self.driver)
        self.login_page = LoginPage(self.driver)
        self.home_page.get_login_page()
        self.home_user_page = self.login_page.login(self.test_data.get("email"), self.test_data.get("password"))

    def test_add_problem_without_photo_using_find_me_admin(self):
        self.go_to_add_problem_page()
        self.locate_problem_with_find_me()
        self.fill_necessary_fields()
        self.publish_problem()
        self.assertEqual('Проблема упішно додана та проходить модерацію. Очікуйте повідомлення.',
                         self.add_problem.confirmation_message())

    def test_add_problem_without_photo_using_search_admin(self):
        self.go_to_add_problem_page()
        self.locate_problem_with_search_button()
        self.fill_necessary_fields()
        self.publish_problem()
        self.assertEqual('Проблема упішно додана та проходить модерацію. Очікуйте повідомлення.',
                         self.add_problem.confirmation_message())

   # def test_add_problem_with_photo_using_find_me(self):
    #    self.go_to_add_problem_page()
     #   self.locate_problem_with_find_me()
      #  self.fill_necessary_fields()
       # self.upload_photo()
        #self.publish_problem()

    def go_to_add_problem_page(self):
        # check if "Add problem" tab is present
        self.assertTrue(self.home_user_page.get_current_url(), self.home_user_page.get_expected_url())
        self.assertTrue(self.home_user_page.is_add_problem_tab_present())

        # go to Add problem page
        add_problem = self.home_user_page.click_on_add_problem()
        self.assertEqual(add_problem.get_current_url(), add_problem.get_expected_url())

    def locate_problem_with_find_me(self):
        self.add_problem.click_on_find_me()
        self.assertTrue(self.add_problem.is_coordinates_present())


    def locate_problem_with_search_button(self):
        self.assertTrue(self.add_problem.is_coordinates_present())
        self.add_problem.fill_coordinates('50.50', '50.50')

        self.add_problem.is_search_button_present()
        self.add_problem.click_on_search()

    def fill_necessary_fields(self):
        self.assertTrue(self.add_problem.is_title_field_present())
        self.add_problem.fill_title("title")

        self.assertTrue(self.add_problem.is_problems_items_present())
        self.add_problem.choose_forest_problem()

        self.assertTrue(self.add_problem.is_description_filed_present())
        self.add_problem.fill_description_of_problem("description")

        self.assertTrue(self.add_problem.is_proposal_filed_present())
        self.add_problem.fill_proposal_of_solving("proposal")

        self.assertTrue(self.add_problem.is_next_button_filed_present())
        self.add_problem.click_on_next()

    def publish_problem(self):
        self.assertTrue(self.add_problem.is_publish_button_filed_present())
        self.add_problem.click_on_publish()

    def upload_photo(self):
        self.assertTrue(self.add_problem.is_upload_photo_element_present())
        self.assertTrue(self.add_problem.is_description_of_photo_element_present())
        self.add_problem.add_photo_and_description("description")
        #Проблеми типу проблеми лісів в радіусі 500 вже існує.

    def generate_random_coordinates(self):
        return str(random.randint(1, 30)), str(random.randint(1, 30))

class AddProblemTestUser(AddProblemTestAdmin):

    def setUp(self):
        super(AddProblemTestAdmin, self).setUpClass()
        self.add_problem = AddProblemPage(self.driver)
        self.login_page = LoginPage(self.driver)
        self.home_page.get_login_page()
        self.home_user_page = self.login_page.login("analatysh@gmail.com", "123123")


if __name__ == '__main__':
    unittest.main()




