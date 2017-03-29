from github_olena.framework.PageBase import PageBase

class PageHome(PageBase):

    def open_sign_in_page(self):
        # self.assertIn("Python", driver.title)
        sign_in_link = self.driver.find_element_by_xpath("//a[text()='Sign in']")
        sign_in_link.click()


