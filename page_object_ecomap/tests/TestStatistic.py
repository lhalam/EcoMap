from page_object_ecomap.tests.TestBase import TestBase
import unittest
import selenium.webdriver.support.ui as ui
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
        _d = self.browser
        wait = ui.WebDriverWait(self.browser, 40)
        wait.until(lambda _d: _d.find_element_by_css_selector("ul.nav:nth-child(1) > li:nth-child(2) > a:nth-child(1)"))
        element = self.browser.find_element_by_css_selector("ul.nav:nth-child(1) > li:nth-child(2) > a:nth-child(1)")
        element.click()
        self.assertEqual(self.statistic_page.get_expected_url(), self.statistic_page.get_current_url())

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()


if __name__ == '__main__':
    unittest.main()
