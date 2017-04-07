from tests.TestBase import TestBase
import unittest
from framework.Pages import*


class testLocation(TestBase):

    @classmethod
    def setUpClass(cls):
        super(testLocation, cls).setUpClass()
        cls.home_page = HomePage(cls.driver)
        cls.add_problem = AddProblemPage(cls.driver)

    def test_1_check_correctness_of_url(self):
        # login
        login_page = self.home_page.get_login_page()
        login_page.login(self.test_data.get("email"), self.test_data.get("password"))

        # go to page where we can check our coordinates
        add_problem = login_page.click_on_add_problem()
        self.assertEqual(add_problem.get_current_url(), add_problem.get_expected_url())

    def test_2_compare_coordinates(self):

        # get coordinates by application
        found_coordinates = self.add_problem.click_on_find_me()

        # get actual coordinates from outside service
        actual_coordinates = self.add_problem.get_actual_coordinates()

        self.assertTrue(self.add_problem.check_location(found_coordinates, actual_coordinates),
                        self.add_problem.get_reason_of_fail())

    def test_3_check_widget(self):

        self.add_problem.click_on_find_me()
        self.assertTrue(self.add_problem.is_location_widget_present())


if __name__ == '__main__':
    unittest.main()





