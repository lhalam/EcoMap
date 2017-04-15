from page_object_ecomap.tests.TestBase import TestBase
import unittest
from selenium import webdriver
from page_object_ecomap.framework.Pages import *
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



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
        '''_d = self.browser
        wait = WebDriverWait(self.browser, 100)
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//ul[1][contains(@class,'all-statistic')]/li[1][text() != '']")))
        _problems = int(
            self.browser.find_element_by_css_selector("ul.all-statistic:nth-child(1) > li:nth-child(1)").text)
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//ul[2][contains(@class,'all-statistic')]/li[1][text() != '']")))
        _subscriptions = int(
            self.browser.find_element_by_css_selector("ul.all-statistic:nth-child(2) > li:nth-child(1)").text)
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//ul[3][contains(@class,'all-statistic')]/li[1][text() != '']")))
        _comments = int(
            self.browser.find_element_by_css_selector("ul.all-statistic:nth-child(3) > li:nth-child(1)").text)
        wait.until(
            EC.presence_of_element_located((By.XPATH, "//ul[4][contains(@class,'all-statistic')]/li[1][text() != '']")))
        _photos = int(
            self.browser.find_element_by_css_selector("ul.all-statistic:nth-child(4) > li:nth-child(1)").text)
        wait.until(lambda _d: _d.find_elements_by_xpath("//ul[@ng-repeat = 'subscription in subscriptions']"))
        elements_in_subscription = self.browser.find_elements_by_xpath("//ul[@ng-repeat = 'subscription in subscriptions']")
        wait.until(lambda _d: _d.find_elements_by_xpath("//ul[@ng-repeat = 'severity in severities']"))
        elements_in_severities = self.browser.find_elements_by_xpath("//ul[@ng-repeat = 'severity in severities']")
        if _comments > 0:
            wait.until(lambda _d: _d.find_elements_by_xpath("//ul[@ng-repeat = 'problemcomm in problCommStats']"))
            elements_in_commented = self.browser.find_elements_by_xpath("//ul[@ng-repeat = 'problemcomm in problCommStats']")
        else: elements_in_commented = []'''

        self.assertTrue(self.statistic_page.verify_subscription())
        self.assertTrue(self.statistic_page.verify_severities())
        self.assertTrue(self.statistic_page.verify_comments())

    
    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()


if __name__ == '__main__':
    unittest.main()
