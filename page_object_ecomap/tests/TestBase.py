import unittest
from framework.Pages import *
from framework.DriverWrapper import Driver


class TestBase(unittest.TestCase):
    driver = None

    @classmethod
    def setUpClass(cls):
        base_url = os.environ['ECOMAP_BASE_URL']
        cls.driver = Driver.get_driver()

        cls.home_page = HomePage(cls.driver, base_url)
        cls.home_page.open()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

