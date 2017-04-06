import unittest
import os
from selenium import webdriver
from page_object_ecomap.framework.Pages import *
from page_object_ecomap.tests.TestData import TestData


class TestBase(unittest.TestCase):
    driver = None

    @classmethod
    def setUpClass(cls):
        cls.test_data = TestData(os.path.dirname(os.path.abspath(__file__)) + "/test_data_file.txt")
        base_url = cls.test_data.get("base_url")
        cls.path = os.path.dirname(os.path.abspath(__file__)) + "/chromedriver"
        cls.driver = webdriver.Chrome(cls.path)
        cls.driver.implicitly_wait(40)
        cls.driver.set_page_load_timeout(50)
        cls.driver.maximize_window()

        cls.home_page = HomePage(cls.driver, base_url)
        cls.home_page.open()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

