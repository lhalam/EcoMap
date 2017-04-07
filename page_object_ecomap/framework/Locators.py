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
