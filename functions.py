import dateutil.parser
import requests
import time, os
import re

from bs4 import BeautifulSoup
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chromedriver = "/usr/bin/chromedriver" # path to the chromedriver executable
os.environ["webdriver.chrome.driver"] = chromedriver

def money_to_int(moneystring):
    if type(moneystring) != float:
        moneystring = moneystring.replace('$', '').replace(',', '')
    return int(moneystring)

def runtime_to_minutes(runtimestring):
    if runtimestring != None:
        runtime = runtimestring.split()
    try:
        minutes = int(runtime[0])*60 + int(runtime[2])
        return minutes
    except:
        return None

def to_date(datestring):
    if datestring:
        date = dateutil.parser.parse(datestring)
    else:
        date = None
    return date

def get_movie_value(soup, field_name):

    '''Grab a value from Box Office Mojo HTML

    Takes a string attribute of a movie on the page and returns the string in
    the next sibling object (the value for that attribute) or None if nothing is found.
    '''

    obj = soup.find(text=re.compile(field_name))
    if not obj:
        return None

    # this works for most of the values
    next_element = obj.findNext()
    if next_element:
        return next_element.text
    else:
        return None

def get_movie_dict(link):
    '''
    From BoxOfficeMojo link stub, request movie html, parse with BeautifulSoup, and
    collect
        - title
        - domestic gross
        - runtime
        - MPAA rating
        - full release date
    Return information as a dictionary.
    '''

    base_url = 'https://www.boxofficemojo.com'

    #Create full url to scrape
    url = base_url + link

    #Request HTML and parse
    response = requests.get(url)
    page = response.text
    soup = BeautifulSoup(page,"lxml")


    headers = ['movie_title', 'domestic_total_gross',
               'runtime_minutes', 'rating', 'release_date', 'budget']

    #Get title
    title_string = soup.find('title').text
    title = title_string.split('-')[0].strip()

    #Get domestic gross
    try:
        raw_domestic_total_gross = (soup.find(class_='mojo-performance-summary-table')
                                    .find_all('span', class_='money')[0]
                                    .text
                               )
    except:
        raw_domestic_total_gross = float("NaN")

    if type(raw_domestic_total_gross) == float or type(raw_domestic_total_gross) == 'NoneType':
        print('This is NaN')
        domestic_total_gross = float("NaN")
    else:
        domestic_total_gross = money_to_int(raw_domestic_total_gross)

    #Get runtime
    raw_runtime = get_movie_value(soup,'Running')
    if type(raw_runtime) != float and type(raw_runtime) != 'NoneType':
        runtime = runtime_to_minutes(raw_runtime)

    #Get rating
    rating = get_movie_value(soup,'MPAA')

    #Get release date
    if '-' in get_movie_value(soup, 'Release Date'):
        raw_release_date = get_movie_value(soup,'Release Date').split('-')[0]
    elif '(' in get_movie_value(soup, 'Release Date'):
        raw_release_date = get_movie_value(soup,'Release Date').split('(')[0]
    else:
        raw_release_date = get_movie_value(soup,'Release Date').split('(')[0]
    release_date = to_date(raw_release_date)



    # Get budget alt
    raw_budget = get_movie_value(soup,'Budget')
    if raw_budget:
        budget = money_to_int(raw_budget)
    else:
        budget = 0

    #Create movie dictionary and return
    movie_dict = dict(zip(headers,[title,
                                domestic_total_gross,
                                runtime,
                                rating,
                                release_date,
                                budget]))

    return movie_dict

def magic_movie_title(title):
    words = title.split(' ')
    return "%20".join(words)

def get_selenium_dict(driver):
    current_url = driver.current_url
    response = requests.get(current_url)
    page = response.text
    soup = BeautifulSoup(page,"lxml")
    headers = ['movie_title', 'domestic_total_gross',
               'runtime_minutes', 'rating', 'budget']

    #Get title
    title_string = soup.find('title').text
    title = title_string.split('-')[0].strip()

    #Get domestic gross
    try:
        raw_domestic_total_gross = (soup.find(class_='mojo-performance-summary-table')
                                    .find_all('span', class_='money')[0]
                                    .text
                               )
    except:
        raw_domestic_total_gross = float("NaN")

    if raw_domestic_total_gross == None or type(raw_domestic_total_gross) == float:
        domestic_total_gross = float("NaN")
    else:
        domestic_total_gross = money_to_int(raw_domestic_total_gross)

    #Get runtime
    raw_runtime = get_movie_value(soup,'Running')
    if type(raw_runtime) != float and raw_runtime != None:
        runtime = runtime_to_minutes(raw_runtime)
    else:
        runtime = raw_runtime

    #Get rating
    rating = get_movie_value(soup,'MPAA')

    #Get release date

    # try:
    #     raw_release_date
    #     if '-' in get_movie_value(soup, 'Release Date'):
    #         raw_release_date = get_movie_value(soup,'Release Date').split('-')[0]
    #     elif '(' in get_movie_value(soup, 'Release Date'):
    #         raw_release_date = get_movie_value(soup,'Release Date').split('(')[0]
    #     elif '\n' in get_movie_value(soup, 'Release Date'):
    #         raw_release_date = get_movie_value(soup,'Release Date').split('\n')[0]
    # except:
    #     raw_release_date = None
    #
    # release_date = to_date(raw_release_date)

    # Get budget alt
    obj = soup.find(text=re.compile('Budget'))
    if not obj:
        obj = None
    if obj:
        next_element = obj.findNext()
    else:
        next_element = None
    if next_element:
        raw_budget = next_element.text
    else:
        raw_budget = None
    if raw_budget != None:
        budget = money_to_int(raw_budget)
    else:
        budget = 0

    #Create movie dictionary and return
    movie_dict = dict(zip(headers,[title,
                                domestic_total_gross,
                                runtime,
                                rating,
                                budget]))
    print(movie_dict)
    return movie_dict

def get_movie_dict2(link):

    base_url = 'https://www.rottentomatoes.com'

    #Create full url to scrape
    url = base_url + link

    #Request HTML and parse
    response = requests.get(url)
    page = response.text
    soup = BeautifulSoup(page,"lxml")


    headers = ['Movie Title', 'Tomatometer', 'Tomatometer Count',
               'Audience Score', 'Verified Ratings']

    #Get title
    title_string = soup.find('title').text
    title = title_string.split('(')[0]
    print(title)

    #Get ratings
    try:
        tomato_rating_div = soup.find('div', class_='mop-ratings-wrap__half')
        tomato_score = (tomato_rating_div
                        .find(class_='mop-ratings-wrap__percentage')
                        .text
                        .strip()
                        .split('%')[0]
                       )
        print(tomato_score)

        audience_rating_div = soup.find('div', class_= 'mop-ratings-wrap__half audience-score')
        audience_percent = (audience_rating_div
                            .find(class_='mop-ratings-wrap__percentage')
                            .text
                            .strip()
                            .split('%')[0]
                           )
        print(audience_percent)

    except:
        tomato_score, audience_percent = 'No score', 'No score'

#Get number of ratings
    try:
        tomato_count_div = soup.find('div', class_='mop-ratings-wrap__review-totals')
        tomato_count = (tomato_rating_div
                        .find(class_='mop-ratings-wrap__text--small')
                        .text
                        .strip()
                        .split(':')[-1]
                       )
        print(tomato_count)

        audience_count_div = soup.find('div', class_= 'mop-ratings-wrap__review-totals mop-ratings-wrap__review-totals--not-released')

        audience_count = (audience_rating_div
                            .find(class_='mop-ratings-wrap__text--small')
                            .text
                            .strip()
                            .split(':')[-1]
                           )
        print(audience_count)

    except:
        tomato_score, audience_percent = 'No score', 'No score'

    #Get runtime
    raw_runtime = get_movie_value(soup,'Running')
    if type(raw_runtime) != float and type(raw_runtime) != 'NoneType':
        runtime = runtime_to_minutes(raw_runtime)

    #Get rating
    rating = get_movie_value(soup,'MPAA')

    #Get release date
    if '-' in get_movie_value(soup, 'Release Date'):
        raw_release_date = get_movie_value(soup,'Release Date').split('-')[0]
    elif '(' in get_movie_value(soup, 'Release Date'):
        raw_release_date = get_movie_value(soup,'Release Date').split('(')[0]
    else:
        raw_release_date = get_movie_value(soup,'Release Date').split('(')[0]
    release_date = to_date(raw_release_date)



    # Get budget alt
    raw_budget = get_movie_value(soup,'Budget')
    budget = money_to_int(raw_budget)

    #Create movie dictionary and return
    movie_dict = dict(zip(headers,[title,
                                domestic_total_gross,
                                runtime,
                                rating,
                                release_date,
                                budget]))

    return movie_dict
