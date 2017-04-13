import unittest
from page_object_ecomap.tests.TestBase import TestBase
from page_object_ecomap.framework.Pages import*


class AddProblemTest(TestBase):

    @classmethod
    def setUpClass(cls):
        super(AddProblemTest, cls).setUpClass()
        cls.home_page = HomePage(cls.driver)
        cls.add_problem = AddProblemPage(cls.driver)
        cls.login_page = LoginPage(cls.driver)
        cls.home_page.get_login_page()
        cls.home_user_page = cls.login_page.login(cls.test_data.get("email"), cls.test_data.get("password"))

    def test_add_problem_without_photo_using_find_me(self):

        # check if "Add problem" tab is present
        self.assertTrue(self.home_user_page.get_current_url(), self.home_user_page.get_expected_url())
        self.assertTrue(self.home_user_page.is_add_problem_tab_present())

        # go to Add problem page
        add_problem = self.home_user_page.click_on_add_problem()
        self.assertEqual(add_problem.get_current_url(), add_problem.get_expected_url())

        self.add_problem.click_on_find_me()
        self.assertTrue(self.add_problem.is_coordinates_present())

        self.assertTrue(self.add_problem.is_title_field_present())
        add_problem.fill_title("title")

        self.assertTrue(self.add_problem.is_problems_items_present())
        add_problem.choose_forest_problem()

        self.assertTrue(self.add_problem.is_description_filed_present())
        add_problem.fill_description_of_problem("description")

        self.assertTrue(self.add_problem.is_proposal_filed_present())
        add_problem.fill_proposal_of_solving("proposal")

        self.assertTrue(self.add_problem.is_next_button_filed_present())
        add_problem.click_on_next()

        self.assertTrue(self.add_problem.is_publish_button_filed_present())
        add_problem.click_on_publish()


if __name__ == '__main__':
    unittest.main()


