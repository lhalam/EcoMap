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

class UserProfileNavigationLocator:
    USER_INFO_TAB = (By.XPATH, "/html/body/div[1]/div[4]/div[1]/div/div/div/div/div/div[1]/ul/li[1]/a")
    MY_SUBSCRIPTIONS_TAB = (By.XPATH, "/html/body/div[1]/div[4]/div[1]/div/div/div/div/div/div[1]/ul/li[4]/a")


class UserProfileInfoLocator(UserProfileNavigationLocator):
    URL = "/#/user_profile/info"


class UserProfileSubscriptionsLocator(UserProfileNavigationLocator):
    URL = "/#/user_profile/subscriptions"
    HEADER_LABEL = (By.XPATH, "/html/body/div[1]/div[4]/div[1]/div/div/div/div/div/div[2]/div/div[1]/div[1]/h3")
    FIRST_SHOW_SUBSCRIPTION_LINK = (By.XPATH, "/html/body/div[1]/div[4]/div[1]/div/div/div/div/div/div[2]/div/table/tbody/tr[1]/td[8]/a")

class DetailedProblemLocator(LogoLocator, NavigationLocator, MapLocator):
    PROBLEM_IMPORTANCE = (By.XPATH, "/html/body/div[1]/div[4]/div[2]/div/div[1]/div[2]/form/div[1]/select")
    PROBLEM_STATUS = (By.XPATH, "/html/body/div[1]/div[4]/div[2]/div/div[1]/div[2]/form/div[2]/select")
    CHANGE_BTN = (By.XPATH, "/html/body/div[1]/div[4]/div[2]/div/div[1]/div[2]/form/div[2]/button")
    CHANGE_SUCCESSFUL_POP_UP_WND = (By.XPATH, '//*[@id="toast-container"]/div/div[2]/div')

class FirstDetailedProblemLocator(DetailedProblemLocator):
    URL = "/#/detailedProblem/1"
