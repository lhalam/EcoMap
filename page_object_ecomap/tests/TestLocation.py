from tests.TestBase import TestBase
import unittest
from framework.Pages import*
from framework.Dictionary import DICTIONARY as test_data


class testLocation(TestBase):

    @classmethod
    def setUpClass(cls):
        super(testLocation, cls).setUpClass()
        cls.home_page = HomePage(cls.driver)
        cls.add_problem = AddProblemPage(cls.driver)
        cls.login_page = LoginPage(cls.driver)
        cls.home_page.get_login_page()
        cls.home_user_page = cls.login_page.login(test_data.get("email"), test_data.get("password"))

    def test_check_location(self):

        # check if "Add problem" tab is present
        self.assertTrue(self.home_user_page.get_current_url(), self.home_user_page.get_expected_url())
        self.assertTrue(self.home_user_page.is_add_problem_tab_present())

        # go to Add problem page
        add_problem = self.home_user_page.click_on_add_problem()
        self.assertEqual(add_problem.get_current_url(), add_problem.get_expected_url())

        # get coordinates by application
        found_coordinates = self.add_problem.click_on_find_me()

        # get actual coordinates from outside service
        actual_coordinates = self.add_problem.get_actual_coordinates()

        self.assertTrue(self.add_problem.check_location(found_coordinates, actual_coordinates),
                        self.add_problem.get_reason_of_fail())

        self.assertTrue(self.add_problem.is_location_widget_present())


if __name__ == '__main__':
    unittest.main()







