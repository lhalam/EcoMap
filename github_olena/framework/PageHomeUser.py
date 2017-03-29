from github_olena.framework.PageBase import PageBase

class PageHomeUser(PageBase):
    def sign_out(self):
        menu_dropdown = self.driver.find_element_by_xpath("//img[@class='avatar']/../span[@class='dropdown-caret']")
        menu_dropdown.click()
        sign_out_button = self.driver.find_element_by_xpath("//form[@class='logout-form']/button[@class='dropdown-item dropdown-signout']")
        sign_out_button.click()
