import os
from selenium import webdriver

class Driver:
    def __init__(self, name):
        self.name = name
        self.path = os.path.dirname(os.path.abspath(__file__)) + "/chromedriver"
        self.driver = webdriver.Chrome(self.path)



