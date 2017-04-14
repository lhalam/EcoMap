import unittest
import os
from framework.Pages import *
from framework.DriverWrapper import Driver


class TestBase(unittest.TestCase):
    driver = None

    @classmethod
    def setUpClass(cls):
        base_url = os.environ['ECOMAP_BASE_URL']
        cls.driver = Driver.get_driver()
        cls.driver.implicitly_wait(40)
        cls.driver.set_page_load_timeout(50)
        cls.driver.maximize_window()

        cls.home_page = HomePage(cls.driver, base_url)
        cls.home_page.open()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

