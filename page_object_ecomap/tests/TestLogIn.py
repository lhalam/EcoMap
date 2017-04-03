import unittest
from page_object_ecomap.tests.TestBase import TestBase
from page_object_ecomap.framework.Pages import *
from PIL import Image


class TestLogin(unittest.TestCase, TestBase):

    @classmethod
    def setUpClass(cls):
        TestBase.setUpClass(cls)

    @unittest.skip('skip login test')
    def test_log_in(self):
        self.assertTrue(self.home_page.is_logo_present())
        login_page = self.home_page.get_login_page()
        self.assertEqual(self.login_page.get_current_url(), self.login_page.get_expected_url())
        home_user_page = login_page.login(self.test_data.get("email"), self.test_data.get("password"))
        self.assertTrue(home_user_page.is_logout_btn_present())
        self.assertEqual(home_user_page.get_current_url(), home_user_page.get_expected_url())

    def test_map_displaying(self):
        element = self.home_page.find_element(*MapLocator.MAP)  # find part of the page you want image of
        location = element.location
        size = element.size
        self.driver.get_screenshot_as_file("screen_full.png")
        full_screen = Image.open('screen_full.png')  # uses PIL library to open image in memory

        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']

        map_img = full_screen.crop((left, top, right, bottom))
        map_img.save('full_map.png')  # saves new cropped image
        map_img = Image.open('full_map.png')
        colors = map_img.convert('P').getcolors() # mode 'P' - 8-bit pixels, mapped to any other mode using a color palette
        print("Colors by full map screenshot: \n{0}".format(colors))
        empty_map = Image.open('empty_map.png')
        colors = empty_map.convert('P').getcolors()
        print("Colors by empty map screenshot: \n{0}".format(colors))
        partial_map = Image.open('partial_map.png')
        colors = partial_map.convert('P').getcolors()
        print("Colors by partial map screenshot: \n{0}".format(colors))

    @classmethod
    def tearDownClass(cls):
        TestBase.tearDownClass(cls)

if __name__ == '__main__':
    unittest.main()
