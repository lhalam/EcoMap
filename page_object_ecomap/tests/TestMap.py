import unittest
from tests.TestBase import TestBase
from framework.Pages import *
from framework.Screenshot import Screenshot
from framework.Dictionary import DICTIONARY as test_data

class TestMap(TestBase):

    def test_full_map(self):
        screenshot = Screenshot(self.driver)
        self.assertTrue(self.home_page.is_element_present(*MapLocator.MAP), "Map element is not present on Home page")
        map_img = screenshot.get_cropped_image("screen_full.png", "screen_cropped.png", MapLocator.MAP)
        grey_pixels = screenshot.get_pixels_by_color('L', 227, map_img)
        white_pixels = screenshot.get_pixels_by_color('L', 255, map_img)
        all_pixels = screenshot.get_pixels_count(map_img)
        grey_percent = screenshot.get_pixels_percentage(grey_pixels, all_pixels)
        white_percent = screenshot.get_pixels_percentage(white_pixels, all_pixels)
        self.assertLess(grey_percent, 10, 'Map isn''t displayed properly (too much of grey color)')
        self.assertLess(white_percent, 10, 'Map isn''t displayed properly (too much of white color)')


class TestMapLoggedIn(TestMap):

    def setUp(self):
        home_user_page = HomePage(self.driver).get_login_page().login(
            test_data.get("email"), test_data.get("password"))
        self.assertTrue(home_user_page.is_logout_btn_present())

if __name__ == '__main__':
    unittest.main()
