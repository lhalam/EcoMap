from page_object_ecomap.tests.TestBase import TestBase
import unittest


class testLocation(TestBase):

    def test_location(self):
        # login
        login_page = self.home_page.get_login_page()
        login_page.login(self.test_data.get("email"), self.test_data.get("password"))

        # go to page where we can check our coordinates
        add_problem = login_page.click_on_add_problem()
        self.assertEqual(add_problem.get_current_url(), add_problem.get_expected_url())

        # get coordinates by application
        found_coordinates = add_problem.click_on_find_me()
        self.assertTrue(add_problem.is_location_widget_present())

        # get actual coordinates from outside service
        actual_coordinates = add_problem.get_actual_coordinates()

        self.assertTrue(add_problem.check_location(found_coordinates, actual_coordinates),
                        add_problem.get_reason_of_fail())

if __name__ == '__main__':
    unittest.main()



