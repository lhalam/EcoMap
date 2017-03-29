from selenium.webdriver.common.keys import Keys

class PageBase():
    def __init__(self, webdriver):
        self.driver = webdriver
        self.driver.implicitly_wait(1)

    def open_page(self, url):
        self.driver.get(url)

    def quit_browser(self):
        self.driver.close()