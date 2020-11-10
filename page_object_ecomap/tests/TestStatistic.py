from page_object_ecomap.tests.TestBase import TestBase
import unittest
from selenium import webdriver
from page_object_ecomap.framework.Pages import *

class TestStatistic(TestBase):

    @classmethod
    def setUpClass(cls):
        cls.browser = webdriver.Firefox(firefox_binary="/usr/bin/firefox",
                                    executable_path="/home/svyshnevskyy/newdisk/geckodriver/geckodriver")
        cls.browser.maximize_window()
        cls.browser.get("http://localhost/#/map")
        cls.statistic_page = StatisticPage(cls.browser )

    def test_1_assert_statistic_page_is_open(self):
        self.statistic_page.set_driver(self.browser)
        self.statistic_page.goToStatisticPage()
        self.assertEqual(self.statistic_page.get_expected_url(), self.statistic_page.get_current_url())

    def test_2_assert_valid_stat_in_all_top(self):

        self.assertTrue(self.statistic_page.verify_subscription())
        self.assertTrue(self.statistic_page.verify_severities())
        self.assertTrue(self.statistic_page.verify_comments())

    
    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()


if __name__ == '__main__':
    unittest.main()
