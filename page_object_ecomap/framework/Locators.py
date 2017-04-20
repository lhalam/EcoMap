from selenium.webdriver.common.by import By
import os

BASE_URL = os.environ.get('ECOMAP_BASE_URL')


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
    USER_PROFILE_LINK = (By.XPATH, '//a[@href="/#/user_profile/info"]')
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


class ProblemLocator(LogoLocator, NavigationLocator, MapLocator):
    IMPORTANCE_INFO = (By.XPATH, '/html/body/div[1]/div[4]/div[2]/div/div[1]/div[1]/div[1]/div/div')
    STATUS_INFO = (By.XPATH, '/html/body/div[1]/div[4]/div[2]/div/div[1]/div[1]/div[2]/div/strong/span')
    IMPORTANCE_DROP_DOWN = (By.XPATH, "/html/body/div[1]/div[4]/div[2]/div/div[1]/div[2]/form/div[1]/select")
    STATUS_DROP_DOWN = (By.XPATH, "/html/body/div[1]/div[4]/div[2]/div/div[1]/div[2]/form/div[2]/select")
    CHANGE_BTN = (By.XPATH, "/html/body/div[1]/div[4]/div[2]/div/div[1]/div[2]/form/div[2]/button")
    POP_UP_WINDOW_SUCCESSFUL_CHANGE = (By.XPATH, '//*[@id="toast-container"]/div/div[2]/div')

class AdministerTabLocator:
    ISSUE_TYPE_TAB = (By.XPATH, '//a[text()[contains(.,"Тип проблеми")]]')
    FIRST_ISSUE_CHANGE_STATUS_BUTTON = (By.XPATH, "/html/body/div/div[4]/div[1]/div/div/div/div[3]/div/div[1]/table/tbody/tr[1]/td[4]/button[2]")
    ISSUE_TYPE_FIELD = (By.XPATH, '/html/body/div[1]/div[4]/div[1]/div/div/div/div[3]/div/div[3]/div/div/div[2]/form/div[1]/div/div/input')
    SUBMIT_BUTTON = (By.XPATH, '/html/body/div[1]/div[4]/div[1]/div/div/div/div[3]/div/div[3]/div/div/div[2]/form/div[4]/div/div[2]/button')
    TYPE_CHANGED_SUCCES_POPUP = (By.XPATH, '//*[@id="toast-container"]/div/div[2]/div')
