import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


BROWSERS = {
    "chrome": DesiredCapabilities.CHROME,
    "firefox": DesiredCapabilities.FIREFOX,
    "phantomjs": DesiredCapabilities.PHANTOMJS
}


class Driver:

    @staticmethod
    def get_driver():
        driver = None
        if os.environ.get('SELENIUM_CONNECTION') == 'LOCAL':
            path = os.environ.get('SELENIUM_DRIVER_PATH')
            if os.environ.get('SELENIUM_BROWSER') == 'chrome':
                driver = webdriver.Chrome(executable_path=path)
            if os.environ.get('SELENIUM_BROWSER') == 'firefox':
                driver = webdriver.Firefox(firefox_binary=os.getenv('SELENIUM_FIREFOX_PATH', "/usr/bin/firefox"), executable_path=path)
            if os.environ.get('SELENIUM_BROWSER') == 'phantomjs':
                driver = webdriver.PhantomJS(executable_path=path)
        else:
            if os.environ.get('SELENIUM_CONNECTION') == 'REMOTE':
                driver = webdriver.Remote(
                    command_executor=os.environ.get('SELENIUM_RC_URL'),
                    desired_capabilities=BROWSERS[os.environ.get('SELENIUM_BROWSER')])
        return Driver.add_driver_settings(driver)

    @staticmethod
    def add_driver_settings(driver):
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(20)
        driver.set_window_size(1280, 1024)
        return driver
