from selenium.webdriver.common.by import By


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
    BASE_URL = "http://localhost"
    URL = BASE_URL + "/#/map"
    LOG_IN = (By.XPATH, "//a[contains(@href,'login')]")
    REGISTER = (By.XPATH, "//a[contains(@href,'register')]")
    USER_PROFILE = (By.XPATH, "//a[@href='/#/user_profile/info']")
    STATISTIC_PAGE_UNREGISTERED = "ul.nav:nth-child(1) > li:nth-child(2) > a:nth-child(1)"


class LoginPageLocator:
    EMAIL = (By.XPATH, "//input[@type='email']")
    PASSWORD = (By.XPATH, "//input[@type='password']")
    SUBMIT = (By.XPATH, "//button[@type='submit']")
    URL = "/#/login"

class RegisterPageLocator:
    REG_URL = "/#/register"
    REG_BLOCK = (By.XPATH, '//*[@id="registerForm"]')
    EMAIL = (By.XPATH, '//*[@id="email"]')
    NAME = (By.XPATH, '//*[@id="name"]')
    SURNAME = (By.XPATH, '//*[@id="surname"]')
    NICKNAME = (By.XPATH, '//*[@id="nickname"]')
    PASSWORD = (By.XPATH, '//*[@id="password"]')
    CONFIRMPASSWORD = (By.XPATH, '//*[@id="pass_confirm"]')
    SUBMIT_BUTTON = (By.XPATH, '//*[@id="registerForm"]/div[1]/div[2]/button')

class HomeUserPageLocator(LogoLocator, NavigationLocator, MapLocator):
    URL = "/#/map"
    USER_PROFILE_LINK = (By.ID, "navMenu")
    LOGOUT_LINK = (By.XPATH, "//a[@ng-click='Logout()']")
    USER_CREDENTIALS = (By.XPATH, '//*[@id="navMenu"]/ul[2]/li[1]/a')

class AddProblemPageLocator:
    URL = '/#/addProblem'

class Location_Locator(object):
    FIND_ME = (By.XPATH, "//*[@class = 'form-group col-lg-6']")
    LATITUDE = (By.XPATH, '//*[@id="latitude"]')
    LONGITUDE = (By.XPATH, '//*[@id="longitude"]')
    LOCATION_WIDGET = (By.XPATH, '//*[@class ="gmnoprint"]')


class UserProfileLocator(object):
    URL = "/#/user_profile/info"
    OLD_PASS = (By.XPATH, "//input[@id='old_pass']")
    NEW_PASS = (By.XPATH, "//input[@id='new_pass']")
    NEW_PASS_CONFIRM = (By.XPATH, "//input[@id='new_pass_confirm']")
    SUBMIT = (By.XPATH, "//button[@type='submit']")
    SUCCESS_POPUP = (By.XPATH, '//*[@id="toast-container"]/div')

class StatisticPageLocator(object):
    URL = "/#/statistic"
    COMMENTS_XPATH = "//ul[3][contains(@class,'all-statistic')]/li[1][text() != '']"
    COMMENTS_CSS = "ul.all-statistic:nth-child(3) > li:nth-child(1)"
    COMMENTS_LIST_XPATH = "//ul[@ng-repeat = 'problemcomm in problCommStats']"
    SUBSCRIPTIONS_XPATH = "//ul[2][contains(@class,'all-statistic')]/li[1][text() != '']"
    SUBSCRIPTIONS_CSS = "ul.all-statistic:nth-child(2) > li:nth-child(1)"
    SUBSCRIPTIONS_LIST_XPATH = "//ul[@ng-repeat = 'subscription in subscriptions']"
    PROBLEMS_XPATH = "//ul[1][contains(@class,'all-statistic')]/li[1][text() != '']"
    PROBLEMS_CSS = "ul.all-statistic:nth-child(1) > li:nth-child(1)"
    IN_SEVERITIES_LIST_XPATH = "//ul[@ng-repeat = 'severity in severities']"

