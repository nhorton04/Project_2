from bs4 import BeautifulSoup
import requests
import time, os
import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt
import functions
import random
import numpy as np

import movies
import criticism
import alt_crit

from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

chromedriver = "/usr/bin/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver

def get_mojo(url):
    i = 2
    driver = webdriver.Chrome(chromedriver)
    driver.get(url)
    response = requests.get(url)
    page = response.text
    soup = BeautifulSoup(page, 'lxml')

    movie_dicts = []

    while i < 910:
            driver.find_element_by_xpath('//*[@id="table"]/div/table[2]/tbody/tr[{}]/td[2]/a'.format(i)).click()
            WebDriverWait(driver, 10)
            time.sleep(2)
            current_movie = functions.get_selenium_dict(driver)
            WebDriverWait(driver, 10)
            movie_dicts.append(current_movie)
            i += 1
            print(current_movie)
            driver.back()

    return movie_dicts
