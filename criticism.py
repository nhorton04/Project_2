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
        check_links()


        scores['metascores'] += get_score('//*[@id="main_content"]/div[1]/div[1]/div/table/tbody/tr/td[2]/div/table/tbody/tr/td[1]/div/div/div[2]/table/tbody/tr/td[2]/a/span')
        time.sleep((3.3+2*random.random()))
        scores['audience_scores'] += get_score('//*[@id="main_content"]/div[1]/div[1]/div/table/tbody/tr/td[2]/div/table/tbody/tr/td[1]/div/div/div[3]/div/table/tbody/tr/td[2]/a/span')
        time.sleep((3.3+2*random.random()))
        scores['critic_count'] += get_score('//*[@id="main_content"]/div[1]/div[1]/div/table/tbody/tr/td[2]/div/table/tbody/tr/td[1]/div/div/div[2]/table/tbody/tr/td[1]/div[2]/span/a/span[2]')
        time.sleep((3.3+2*random.random()))
        scores['num_audience_ratings'] += get_score('//*[@id="main_content"]/div[1]/div[1]/div/table/tbody/tr/td[2]/div/table/tbody/tr/td[1]/div/div/div[3]/div/table/tbody/tr/td[1]/div[2]/span/a/span[2]')

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
    print('crap')
    time.sleep(2)
    driver.find_element_by_xpath('//*[@id="main_content"]/div[1]/div[2]/div/div[2]/a/span[1]').click()
    print('.......')


def get_score(xpath):
    try:
        score.driver.find_element_by_xpath(xpath).text
        time.sleep(2)
        if any(char.isdigit() for char in score):
            return int(''.join(filter(str.isdigit, score)))
        else:
            return 'No score'
    except:
        return 'No score'



def check_links():
    # Check if first result has a valid metascore
    try:
        score = driver.find_element_by_xpath('//*[@id="main_content"]/div[1]/div[3]/div[1]/ul/li[1]/div/div[2]/div/span').text
        time.sleep((3.3+2*random.random()))
        #If it has a valid metascore, click on the link
        print('\n\n\n\n\n')
        print("LOOK HERE -------------------------------------------")
        print(f"if {int(''.join(filter(str.isdigit, score)))}:")
        if int(''.join(filter(str.isdigit, score))):
            driver.find_element_by_xpath('//*[@id="main_content"]/div[1]/div[3]/div[1]/ul/li[1]/div/div[2]/div/h3/a').click()

        # If not, try the second link
        else:
            print('\n\n\n\n\n')
            print("LOOK HERE -------------------------------------------")
            time.sleep((3.3+2*random.random()))
            score = driver.find_element_by_xpath('//*[@id="main_content"]/div[1]/div[3]/div[1]/ul/li[2]/div/div[2]/div/span').text
            print(f"if {int(''.join(filter(str.isdigit, score)))}:")
            #If it has a valid metascore, click on the link
            if int(''.join(filter(str.isdigit, score))):
                time.sleep((3.3+2*random.random()))
                driver.find_element_by_xpath('//*[@id="main_content"]/div[1]/div[3]/div[1]/ul/li[2]/div/div[2]/div/h3/a').click()

    except:
        print('Result not found')
        return 'Nope'

# //*[@id="main_content"]/div[1]/div[3]/div[1]/ul/li[1]/div/div[2]/div/h3/a
