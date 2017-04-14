import os
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


browsers = {
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
                driver = webdriver.Firefox(executable_path=path)
            if os.environ.get('SELENIUM_BROWSER') == 'phantomjs':
                driver = webdriver.Firefox(executable_path=path)
        else:
            if os.environ.get('SELENIUM_CONNECTION') == 'REMOTE':
                driver = webdriver.Remote(
                    command_executor=os.environ.get('SELENIUM_RC_URL'),
                    desired_capabilities=browsers[os.environ.get('SELENIUM_BROWSER')])
                return driver
        return Driver.add_driver_settings(driver)

    @staticmethod
    def add_driver_settings(driver):
        driver.implicitly_wait(40)
        driver.set_page_load_timeout(50)
        driver.maximize_window()
        return driver

