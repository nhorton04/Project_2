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

chromedriver = "/usr/bin/chromedriver" # path to the chromedriver executable
os.environ["webdriver.chrome.driver"] = chromedriver
url = 'https://www.metacritic.com/'

capabilities = DesiredCapabilities().CHROME
capabilities["pageLoadStrategy"] = "none"

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--enable-automation")
options.add_argument("--no-sandbox")
options.add_argument("--headless")
#     options.add_argument("--disable-infobars") #dqn cause errors
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-browser-side-navigation")
options.add_argument("--disable-gpu")
options.add_argument("--disable-features=VizDisplayCompositor") #super necessary for windows linux subsystem

driver = webdriver.Chrome(options=options)

def metacritic(titles):
    scores = {'metascores': [], 'audience_scores': [], 'critic_count': [], 'num_audience_ratings': []}

    for title in titles:
        # Open selenium browser
        driver = webdriver.Chrome(options=options)
        driver.get(url)

        #Search for current movie title
        perform_search(title, driver)
        WebDriverWait(driver, 10)
        filter_by_movies(driver)
        #Check the first and second links to see if metascore is valid. If so, click on it.
        check_links(driver)

        try:
            scores['metascores'] += [get_score(driver, '//*[@id="main_content"]/div[1]/div[1]/div/table/tbody/tr/td[2]/div/table/tbody/tr/td[1]/div/div/div[2]/table/tbody/tr/td[2]/a/span')]
            WebDriverWait(driver, 10)
        except:
            try:
                scores['metascores'] += [get_score(driver, '//*[@id="main_content"]/div[1]/div[1]/div/div/div[2]/div/table/tbody/tr/td[2]/a/span')]
                WebDriverWait(driver, 10)
            except:
                scores['metascores'] += ['No score']
        try:
            scores['audience_scores'] += [get_score(driver, '//*[@id="main_content"]/div[1]/div[1]/div/table/tbody/tr/td[2]/div/table/tbody/tr/td[1]/div/div/div[3]/div/table/tbody/tr/td[2]/a/span')]
            WebDriverWait(driver, 10)
        except:
            try:
                scores['audience_scores'] += [get_score(driver, '//*[@id="main_content"]/div[1]/div[1]/div/div/div[4]/div[1]/div/table/tbody/tr/td[2]/a/span')]
                WebDriverWait(driver, 10)
            except:
                scores['audience_scores'] += ['No score']
        try:
            scores['critic_count'] += [get_score(driver, '//*[@id="main_content"]/div[1]/div[1]/div/table/tbody/tr/td[2]/div/table/tbody/tr/td[1]/div/div/div[2]/table/tbody/tr/td[1]/div[2]/span/a/span[2]')]
            WebDriverWait(driver, 10)
        except:
            try:
                scores['critic_count'] += [get_score(driver, '//*[@id="main_content"]/div[1]/div[1]/div/div/div[2]/div/table/tbody/tr/td[1]/div[2]/span/a/span[2]')]
                WebDriverWait(driver, 10)
            except:
                scores['critic_count'] += ['No critics']
        try:
            scores['num_audience_ratings'] += [get_score(driver, '//*[@id="main_content"]/div[1]/div[1]/div/table/tbody/tr/td[2]/div/table/tbody/tr/td[1]/div/div/div[3]/div/table/tbody/tr/td[1]/div[2]/span/a/span[2]')]
        except:
            try:
                scores['num_audience_ratings'] += [get_score(driver, '//*[@id="main_content"]/div[1]/div[1]/div/div/div[4]/div[1]/div/table/tbody/tr/td[1]/div[2]/span/a/span[2]')]
            except:
                scores['num_audience_ratings'] += ['No ratings']
        print(scores['metascores'], scores['audience_scores'], scores['critic_count'], scores['num_audience_ratings'])
        driver.close()

def perform_search(title, driver):
    # Enter title into search box, press enter
    search_box = driver.find_element_by_xpath('//*[@id="primary_search_box"]')
    WebDriverWait(driver, 10)
    search_box.clear()
    search_box.send_keys(title)
    search_box.send_keys(Keys.RETURN)

    #After search is performed, click on "Movies" in left bar to filter out games, etc

def strip_string(string):
    return int(''.join(filter(str.isdigit, string)))

def strip_movies(scores):
    for dict in scores:
        scores['']



    return int(''.join(filter(str.isdigit, string)))

def filter_by_movies(driver):
    WebDriverWait(driver, 10)
    driver.find_element_by_xpath('//*[@id="main_content"]/div[1]/div[2]/div/div[2]/a/span[1]').click()

def is_valid_score(score):
    return bool(any(char.isdigit() for char in score))

# def get_score(driver, xpath):
#     score = driver.find_element_by_xpath(xpath).text
#     time.sleep(2)
#     if any(char.isdigit() for char in score):
#         print(score)
#         print(int(''.join(filter(str.isdigit, score))))
#         return int(''.join(filter(str.isdigit, score)))
#     else:
#         print("DIDNT WORK _______")
#         print(score)
#         print(int(''.join(filter(str.isdigit, score))))
#         return 'No score'

def get_score(driver, xpath):
    WebDriverWait(driver, 10)
    score = driver.find_element_by_xpath(xpath).text
    if any(char.isdigit() for char in score):
        return score
    else:
        return 'No score'


def check_links(driver):
    # Check if first result has a valid metascore
    score = driver.find_element_by_xpath('//*[@id="main_content"]/div[1]/div[3]/div[1]/ul/li[1]/div/div[2]/div/span').text
    WebDriverWait(driver, 10)
    #If it has a valid metascore, click on the link
    if is_valid_score(score):
        driver.find_element_by_xpath('//*[@id="main_content"]/div[1]/div[3]/div[1]/ul/li[1]/div/div[2]/div/h3/a').click()
    else:
        score = driver.find_element_by_xpath('//*[@id="main_content"]/div[1]/div[3]/div[1]/ul/li[2]/div/div[2]/div/span').text
        #If it has a valid metascore, click on the link
        if is_valid_score(score):
            WebDriverWait(driver, 10)
            driver.find_element_by_xpath('//*[@id="main_content"]/div[1]/div[3]/div[1]/ul/li[2]/div/div[2]/div/h3/a').click()

# //*[@id="main_content"]/div[1]/div[3]/div[1]/ul/li[1]/div/div[2]/div/h3/a
