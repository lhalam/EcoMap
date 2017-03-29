from github_olena.framework.PageBase import PageBase

class PageSingIn(PageBase):

    def sign_in(self, login, password):
        # self.assertIn("Python", driver.title)
        login_textbox = self.driver.find_element_by_xpath("//input[@id='login_field']")
        login_textbox.send_keys(login)
        pass_textbox = self.driver.find_element_by_xpath("//input[@id='password']")
        pass_textbox.send_keys(password)
        sign_in_button = self.driver.find_element_by_xpath("//input[@value='Sign in']")
        sign_in_button.click()
