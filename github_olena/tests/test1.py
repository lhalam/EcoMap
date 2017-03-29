import unittest
import os
from selenium import webdriver
from github_olena.framework.PageSign_In import PageSingIn
from github_olena.framework.PageHome import PageHome
from github_olena.framework.PageHomeUser import PageHomeUser
class TestGitHubLogIn(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
       # path = os.path.dirname(os.path.abspath(__file__)) + "/geckodriver"
       # cls.driver = webdriver.Firefox(firefox_binary="/usr/bin/firefox", executable_path=path)
       cls.path = os.path.dirname(os.path.abspath(__file__)) + "/chromedriver"
       cls.driver = webdriver.Chrome(cls.path)
       cls.page_home = PageHome(cls.driver)
       cls.page_signin = PageSingIn(cls.driver)
       cls.page_home_user = PageHomeUser(cls.driver)
       cls.page_home.open_page('https://github.com/')

    def test_sign_in_github(self):
        self.page_home.open_sign_in_page()
        self.page_signin.sign_in('olenakhom', 'CatGun62')
        self.page_home_user.sign_out()

        #assert "No results found." not in driver.page_source

    @classmethod
    def tearDownClass(cls):
        cls.page_home.quit_browser()

if __name__ == "__main__":
    unittest.main()