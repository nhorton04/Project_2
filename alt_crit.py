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

def metacritic(titles):
    scores = {'metascores': [], 'audience_scores': [], 'critic_count': [], 'num_audience_ratings': []}

    for title in titles:
        # Open selenium browser
        driver = webdriver.Chrome(chromedriver)
        driver.get(url)

        #Search for current movie title
        perform_search(title, driver)
        time.sleep(1)
        filter_by_movies(driver)
        #Check the first and second links to see if metascore is valid. If so, click on it.
        check_links(driver)


        scores['metascores'] += [get_score(driver, '//*[@id="main_content"]/div[1]/div[1]/div/table/tbody/tr/td[2]/div/table/tbody/tr/td[1]/div/div/div[2]/table/tbody/tr/td[2]/a/span')]
        time.sleep((3.3+2*random.random()))
        scores['audience_scores'] += [get_score(driver, '//*[@id="main_content"]/div[1]/div[1]/div/table/tbody/tr/td[2]/div/table/tbody/tr/td[1]/div/div/div[3]/div/table/tbody/tr/td[2]/a/span')]
        time.sleep((3.3+2*random.random()))
        scores['critic_count'] += [get_score(driver, '//*[@id="main_content"]/div[1]/div[1]/div/table/tbody/tr/td[2]/div/table/tbody/tr/td[1]/div/div/div[2]/table/tbody/tr/td[1]/div[2]/span/a/span[2]')]
        time.sleep((3.3+2*random.random()))
        scores['num_audience_ratings'] += [get_score(driver, '//*[@id="main_content"]/div[1]/div[1]/div/table/tbody/tr/td[2]/div/table/tbody/tr/td[1]/div/div/div[3]/div/table/tbody/tr/td[1]/div[2]/span/a/span[2]')]

        print(scores['metascores'], scores['audience_scores'], scores['critic_count'], scores['num_audience_ratings'])
        driver.close()

def perform_search(title, driver):
    # Enter title into search box, press enter
    search_box = driver.find_element_by_xpath('//*[@id="primary_search_box"]')
    time.sleep((3.3+2*random.random()))
    search_box.clear()
    search_box.send_keys(title)
    search_box.send_keys(Keys.RETURN)

    #After search is performed, click on "Movies" in left bar to filter out games, etc

def filter_by_movies(driver):
    time.sleep(2)
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
    time.sleep(2)
    score = driver.find_element_by_xpath(xpath).text
    if any(char.isdigit() for char in score):
        return score
    else:
        return 'No score'


def check_links(driver):
    # Check if first result has a valid metascore
    score = driver.find_element_by_xpath('//*[@id="main_content"]/div[1]/div[3]/div[1]/ul/li[1]/div/div[2]/div/span').text
    time.sleep(1)
    #If it has a valid metascore, click on the link
    if is_valid_score(score):
        driver.find_element_by_xpath('//*[@id="main_content"]/div[1]/div[3]/div[1]/ul/li[1]/div/div[2]/div/h3/a').click()
    else:
        score = driver.find_element_by_xpath('//*[@id="main_content"]/div[1]/div[3]/div[1]/ul/li[2]/div/div[2]/div/span').text
        #If it has a valid metascore, click on the link
        if is_valid_score(score):
            time.sleep((3.3+2*random.random()))
            driver.find_element_by_xpath('//*[@id="main_content"]/div[1]/div[3]/div[1]/ul/li[2]/div/div[2]/div/h3/a').click()

# //*[@id="main_content"]/div[1]/div[3]/div[1]/ul/li[1]/div/div[2]/div/h3/a
