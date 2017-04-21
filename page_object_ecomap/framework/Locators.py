from selenium.webdriver.common.by import By
from framework.Dictionary import DICTIONARY as test_data
import os

BASE_URL = os.environ.get('ECOMAP_BASE_URL')

class CommonLocator:
    SUCCESS_POPUP = (By.XPATH, '//*[@id="toast-container"]/div')

class LogoLocator:
    LOGO = (By.XPATH, "//img[contains(@src, 'logo.png')]")


class NavigationLocator:
    NAV_BTN = (By.XPATH, "//button[@data-target='#navMenu']")
    RESOURCE = (By.XPATH, "//a[@ng-show='faqTitles']")
    STATISTIC = (By.XPATH, "//a[contains(@href, 'statistic')]")
    ADD_PROBLEM = (By.XPATH, '//*[@href="/#/addProblem"]')


class MapLocator:
    MAP = (By.ID, "map")


class Filter:
    FILTER_BTN = (By.XPATH, "//div[@class='filter-toogle']")
    # filter form

class HomePageLocator(LogoLocator, NavigationLocator, MapLocator):
    URL = BASE_URL + "/#/map"
    LOG_IN = (By.XPATH, "//a[contains(@href,'login')]")
    REGISTER = (By.XPATH, "//a[contains(@href,'register')]")

class LoginPageLocator:
    EMAIL = (By.XPATH, "//input[@type='email']")
    PASSWORD = (By.XPATH, "//input[@type='password']")
    SUBMIT = (By.XPATH, "//button[@type='submit']")
    URL = os.environ.get('ECOMAP_BASE_URL') + "/#/login"

class RegisterPageLocator:
    REG_URL = BASE_URL + "/#/register"
    REG_BLOCK = (By.XPATH, '//*[@id="registerForm"]')
    EMAIL = (By.XPATH, '//*[@id="email"]')
    NAME = (By.XPATH, '//*[@id="name"]')
    SURNAME = (By.XPATH, '//*[@id="surname"]')
    NICKNAME = (By.XPATH, '//*[@id="nickname"]')
    PASSWORD = (By.XPATH, '//*[@id="password"]')
    CONFIRMPASSWORD = (By.XPATH, '//*[@id="pass_confirm"]')
    SUBMIT_BUTTON = (By.XPATH, '//*[@id="registerForm"]/div[1]/div[2]/button')

class HomeUserPageLocator(LogoLocator, NavigationLocator, MapLocator):
    URL = BASE_URL + "/#/map"
    USER_PROFILE_LINK = (By.XPATH, '//*[@id="navMenu"]/ul[2]/li[1]/a')
    LOGOUT_LINK = (By.XPATH, "//a[@ng-click='Logout()']")
    USER_CREDENTIALS = (By.XPATH, '//*[@id="navMenu"]/ul[2]/li[1]/a')

class AddProblemPageLocator:
    URL = BASE_URL + '/#/addProblem'

class Location_Locator(object):
    FIND_ME = (By.XPATH, "//*[@class = 'form-group col-lg-6']")
    LATITUDE = (By.XPATH, '//*[@id="latitude"]')
    LONGITUDE = (By.XPATH, '//*[@id="longitude"]')
    LOCATION_WIDGET = (By.XPATH, '//*[@class ="gmnoprint"]')


class UserProfileLocator(object):
    URL = BASE_URL + "/#/user_profile/info"
    OLD_PASS = (By.XPATH, "//input[@id='old_pass']")
    NEW_PASS = (By.XPATH, "//input[@id='new_pass']")
    NEW_PASS_CONFIRM = (By.XPATH, "//input[@id='new_pass_confirm']")
    SUBMIT = (By.XPATH, "//button[@type='submit']")
    SUCCESS_POPUP = (By.XPATH, '//*[@id="toast-container"]/div')

class ProblemsUserProfileLocator:
    PROBLEMS_TAB = (By.XPATH, "//a[text()='Ecomap проблеми']")
    EDIT_LINK_BY_PROMLEM_TITLE = (By.XPATH, "//tr[td[text()='" + test_data.get('problem_title') + "']]//a[@ng-click='triggerEditModal(problem.id)']")
    URL = BASE_URL + "/#/user_profile/problems"


class CommentsUserProfileLocator:
    MY_COMMENTS_TAB = (By.XPATH, "//li[@heading='Мої коментарі']")
    URL = BASE_URL + "/#/user_profile/comments"
    DELETE_LINK_BY_COMMENT_TITLE = (
    By.XPATH, "//span[text()='" + test_data.get('comment_text') + "']/parent::div/parent::*//a[contains(@ng-click, 'deleteComment')][1]")


class EditProblemLocator:
    COMMENT_TAB = (By.XPATH, "//a[text()='Коментарі']")
    COMMENT_TEXTAREA = (By.XPATH, "//textarea[@placeholder='Ваш коментар']")
    ADD_COMMENT_BTN = (By.XPATH, "//input[@value='Додати коментар']")
    ANONYMOUSLY_CHECKBOX = (By.XPATH, "//input[@ng-model='comment.changeUser']")
    COMMENT_BLOCK = "//div[@ng-repeat='comment in comments'][last()]"
    COMMENT_NICKNAME = (By.XPATH, COMMENT_BLOCK + "//*[contains(@class,'comment-nickname')]")
    COMMENT_DATETIME = (By.XPATH, COMMENT_BLOCK + "//span[@ng-hide='comment.updated_date']")
    COMMENT_TEXT = (By.XPATH, COMMENT_BLOCK + "//div[@class='panel-body comment-block ng-binding']")
    COMMENT_ANSWER_LINK = (By.XPATH, COMMENT_BLOCK + "//div[1]/a[contains(@ng-click,'getSubComments')]")
    COMMENT_EDIT_LINK =(By.XPATH, COMMENT_BLOCK + "//span[@class='fa fa-pencil comment-update']")
    COMMENT_EDIT_LINK_HIDDEN = (By.XPATH, COMMENT_BLOCK + "//span[@class='fa fa-pencil comment-update ng-hide']")
    COMMENT_LINK = (By.XPATH, COMMENT_BLOCK + "//span[@ng-click='makeLink(comment.id)']")

    ANSWER_TEXTAREA = (By.XPATH, "//textarea[@placeholder='Ваша відповідь']")
    ADD_ANSWER_BTN = (By.XPATH, "//input[@value='Додати відповідь']")
    ANSWER_BLOCK = "//div[@ng-repeat='subcomment in subcomments'][last()]"
    ANSWER_NICKNAME = (By.XPATH, ANSWER_BLOCK + "//strong[@class='pull-left comment-nickname ng-binding']")
    ANSWER_TEXT = (By.XPATH, ANSWER_BLOCK + "//div[@ng-bind='subcomment.content']")
