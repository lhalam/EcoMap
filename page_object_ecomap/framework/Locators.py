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
    MESSAGE_EMAIL = (By.XPATH, '//*[@id="registerForm"]/div[1]/div[2]/div[1]/div/p')
    MESSAGE_NAME = (By.XPATH, '//*[@id="registerForm"]/div[1]/div[2]/div[2]/div/p')
    MESSAGE_SURNAME = (By.XPATH, '//*[@id="registerForm"]/div[1]/div[2]/div[3]/div/p')
    MESSAGE_NICKNAME = (By.XPATH, '//*[@id="registerForm"]/div[1]/div[2]/div[4]/div/p')


class HomeUserPageLocator(LogoLocator, NavigationLocator, MapLocator):
    URL = BASE_URL + "/#/map"
    USER_PROFILE_LINK = (By.XPATH, '//*[@id="navMenu"]/ul[2]/li[1]/a')
    LOGOUT_LINK = (By.XPATH, "//a[@ng-click='Logout()']")
    USER_CREDENTIALS = (By.XPATH, '//*[@id="navMenu"]/ul[2]/li[1]/a')

class AddProblemPageLocator:
    URL = BASE_URL + '/#/addProblem'
    TITLE = (By.XPATH, '//*[@id="title"]')
    PROBLEMS_LIST = (By.XPATH, '//*[@id="problem_type_id"]/ul/li')
    FOREST_PROBLEM = (By.XPATH, '//*[@id="problem_type_id"]/ul/li[1]')
    WATER = (By.XPATH, '//li[4]/span')
    PROBLEM_DESCRIPTION = (By.XPATH, '//*[@id="problemContent"]')
    PROPOSAL = (By.XPATH, '//*[@id="proposal"]')
    NEXT = (By.XPATH, '//*[@name="addProblemForm"]/button')
    PUBLISH = (By.XPATH, '//*[@name="uploadProblemPhoto"]/button')
    SEARCH = (By.XPATH, '//input[@value="Пошук"]')
    ADD_PHOTO = (By.XPATH, '//*[@class="fa fa-plus"]')
    INPUT = (By.XPATH, '//input[@name="file"]')
    CHECK_UPLOADED_PHOTO = (By.XPATH, '//div[@class="thumb"]/img')
    PHOTO_DESCRIPTION = (By.XPATH, '//textarea[@name="description"]')
    CONFIRMATION_MESSAGE = (By.XPATH, '//*[@id="toast-container"]/div[1]/div[2]/div')
    ERROR_MESSAGE = (By.XPATH, '//*[@id="toast-container"]/div/div[2]/div')

    ERROR_EMPTY_COORDINATES = (By.XPATH, '//form[@name="addProblemForm"]/div/div[2]/div/p')
    ERROR1_EMPTY_COORDINATES = (By.XPATH, '//form[@name="addProblemForm"]/div/div[3]/div/p')
    TITLE_ERROR = (By.XPATH, '//form[@name="addProblemForm"]/div[3]/div/p')
    PHOTO_DESCRIPTION_ERROR = (By.XPATH, '//form[@name="addProblemForm"]/div[5]/div/p')
    PROPOSAL_ERROR = (By.XPATH, '//form[@name="addProblemForm"]/div[6]/div/p')


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
    ERR_MSG_PRESENT = (By.XPATH, '//div[@ng-messages="changePasswordForm.new_pass_confirm.$error"]')
    ERR_MSG_PASS_NOT_MATCH = By.XPATH, (ERR_MSG_PRESENT.__getitem__(1) + '/p[text()="Паролі не співпадають."]')
    ERR_MSG_PASS_IS_NECESSARY = (By.XPATH, ERR_MSG_PRESENT.__getitem__(1) + '/p[text()="Це поле є обов\'язковим."]')
    USER_PHOTO = (By.XPATH, '/html/body/div[1]/div[4]/div[1]/div/div/div/div/div/div[2]/div[1]/div[1]/div/span')


class UserProfileNavigationLocator:
    USER_INFO_TAB = (By.XPATH, "/html/body/div[1]/div[4]/div[1]/div/div/div/div/div/div[1]/ul/li[1]/a")
    PROBLEMS_TAB = (By.XPATH, "/html/body/div[1]/div[4]/div[1]/div/div/div/div/div/div[1]/ul/li[2]/a")
    SUBSCRIPTIONS_TAB = (By.XPATH, "/html/body/div[1]/div[4]/div[1]/div/div/div/div/div/div[1]/ul/li[4]/a")
    ADMIN_TAB = (By.XPATH, '//uib-tab-heading[text()[contains(.,"Адміністрування")]]')


class UserProfileProblemsLocator(UserProfileNavigationLocator):
    URL = os.environ.get('ECOMAP_BASE_URL') + "/#/user_profile/subscriptions"
    HEADER_LABEL = (By.XPATH, "/html/body/div[1]/div[4]/div[1]/div/div/div/div/div/div[2]/div/div[1]/h3")
    FIRST_PROBLEM_EDIT_LINK = (By.XPATH, "/html/body/div[1]/div[4]/div[1]/div/div/div/div/div/div[2]/div/div[3]/table/tbody/tr[1]/td[9]/a[1]")
    FIRST_PROBLEM_STATUS = (By.XPATH, '/html/body/div[1]/div[4]/div[1]/div/div/div/div/div/div[2]/div/div[3]/table/tbody/tr[1]/td[6]')
    TOTAL_AMOUNT_OF_PROBLEMS = (By.XPATH, '//span[@class="ng-binding"]')

class UserProfileSubscriprionLocator(UserProfileNavigationLocator):
    SUBSCRIPTIONS_INFO = (By.XPATH, '/html/body/div[1]/div[4]/div[1]/div/div/div/div/div/div[2]/div/h3')
    TITLE_1 = (By.XPATH, '/html/body/div[1]/div[4]/div[1]/div/div/div/div/div/div[2]/div/table/tbody/tr/td[3]')
    COUNT = (By.XPATH, '/html/body/div[1]/div[4]/div[1]/div/div/div/div/div/div[2]/div/p/span')
    VIEW = (By.XPATH, '/html/body/div[1]/div[4]/div[1]/div/div/div/div/div/div[2]/div/table/tbody/tr/td[8]/a')

class ProblemLocator(LogoLocator, NavigationLocator, MapLocator):
    IMPORTANCE_INFO = (By.XPATH, '/html/body/div[1]/div[4]/div[2]/div/div[1]/div[1]/div[1]/div/div')
    STATUS_INFO = (By.XPATH, '/html/body/div[1]/div[4]/div[2]/div/div[1]/div[1]/div[2]/div/strong/span')
    IMPORTANCE_DROP_DOWN = (By.XPATH, "/html/body/div[1]/div[4]/div[2]/div/div[1]/div[2]/form/div[1]/select")
    STATUS_DROP_DOWN = (By.XPATH, "/html/body/div[1]/div[4]/div[2]/div/div[1]/div[2]/form/div[2]/select")
    CHANGE_BTN = (By.XPATH, "/html/body/div[1]/div[4]/div[2]/div/div[1]/div[2]/form/div[2]/button")
    POP_UP_WINDOW_SUCCESSFUL_CHANGE = (By.XPATH, '//*[@id="toast-container"]/div/div[2]/div')
    POP_UP_WINDOW_TITLE = (By.XPATH, '//*[@id="toast-container"]/div/div[1]')
    DETAILED_TITLE = (By.XPATH, '/html/body/div[1]/div[4]/div[2]/div/h3')

class Statistics:
    URL = os.environ.get('ECOMAP_BASE_URL') + "/#/statistic"
    TOP_FIRST_ISSUE = (By.XPATH, '/html/body/div[1]/div[4]/div[1]/div/div[1]/div/div[2]/ul[1]/a/li')
    EYE = (By.XPATH, '/html/body/div[1]/div[4]/div[2]/div/div[1]/div[1]/div[3]/div/span')




class AdministerTabLocator:
    ISSUE_TYPE_TAB = (By.XPATH, '//a[text()[contains(.,"Тип проблеми")]]')
    FIRST_ISSUE_CHANGE_STATUS_BUTTON = (By.XPATH, "/html/body/div/div[4]/div[1]/div/div/div/div[3]/div/div[1]/table/tbody/tr[1]/td[4]/button[2]")
    ISSUE_TYPE_FIELD = (By.XPATH, '/html/body/div[1]/div[4]/div[1]/div/div/div/div[3]/div/div[3]/div/div/div[2]/form/div[1]/div/div/input')
    SUBMIT_BUTTON = (By.XPATH, '/html/body/div[1]/div[4]/div[1]/div/div/div/div[3]/div/div[3]/div/div/div[2]/form/div[4]/div/div[2]/button')
    TYPE_CHANGED_SUCCES_POPUP = (By.XPATH, '//*[@id="toast-container"]/div/div[2]/div')

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
