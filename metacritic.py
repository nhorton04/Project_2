def critique(movie_titles):
    metascores = []
    audience_scores = []

    num_critics = []
    num_audience_ratings = []

    for title in movie_titles:
        print(f'Current Title: {title}')
        driver = webdriver.Chrome(chromedriver)
        driver.get(url)
        time.sleep((3.3+2*random.random()))
        search_box = driver.find_element_by_xpath('//*[@id="primary_search_box"]')
        search_box.clear()
        search_box.send_keys(title)
        time.sleep((3.2+2*random.random()))
        search_box.send_keys(Keys.RETURN)
        time.sleep((3.1+2*random.random()))
        try:
            select_movies = driver.find_element_by_xpath('//*[@id="main_content"]/div[1]/div[2]/div/div[2]/a/span[1]').click()
            time.sleep((3.4+2*random.random()))
        except:
            print('no movies button to click')
            pass
        try:
            driver.find_element_by_xpath('//*[@id="main_content"]/div[1]/div[3]/div[1]/ul/li[1]/div/div[2]/div/h3/a').click()
            time.sleep((3.1+2*random.random()))
            metascore = driver.find_element_by_xpath('//*[@id="main_content"]/div[1]/div[1]/div/table/tbody/tr/td[2]/div/table/tbody/tr/td[1]/div/div/div[2]/table/tbody/tr/td[2]/a/span').text
            if any(char.isdigit() for char in metascore):
                metascores.append(int(''.join(filter(str.isdigit, metascore))))
                time.sleep((3.4+2*random.random()))
                audience_score = driver.find_element_by_xpath('//*[@id="main_content"]/div[1]/div[1]/div/table/tbody/tr/td[2]/div/table/tbody/tr/td[1]/div/div/div[3]/div/table/tbody/tr/td[2]/a/span').text
                audience_scores.append(float(''.join(filter(str.isdigit, audience_score))))
                time.sleep((3.1+2*random.random()))
                critic_string = driver.find_element_by_xpath('//*[@id="main_content"]/div[1]/div[1]/div/table/tbody/tr/td[2]/div/table/tbody/tr/td[1]/div/div/div[2]/table/tbody/tr/td[1]/div[2]/span/a/span[2]').text
                critic_count = int(''.join(filter(str.isdigit, critic_string)))
                num_critics.append(critic_count)
                time.sleep((3.35+2*random.random()))
                audience_count_string = driver.find_element_by_xpath('//*[@id="main_content"]/div[1]/div[1]/div/table/tbody/tr/td[2]/div/table/tbody/tr/td[1]/div/div/div[3]/div/table/tbody/tr/td[1]/div[2]/span/a/span[2]').text
                audience_count = int(''.join(filter(str.isdigit, audience_count_string)))
                num_audience_ratings.append(audience_count)
            else:
                metascores.append('No score')
                audience_scores.append('No score')
                num_critics.append('No critics')
                num_audience_ratings.append('No audience ratings')
        except NoSuchElementException:
            print('thrown out of first loop - NoSuchElementException')
            try:
                metascore = driver.find_element_by_xpath('//*[@id="main_content"]/div[1]/div[3]/div/div[1]/table/tbody/tr[2]/td[1]/table/tbody/tr/td[1]/a/span').text
                metascores.append(int(metascore))
                time.sleep((3.14+2*random.random()))
                audience_score = driver.find_element_by_xpath('//*[@id="main_content"]/div[1]/div[3]/div/div[1]/table/tbody/tr[2]/td[2]/table/tbody/tr/td[1]/a/span').text
                audience_scores.append(float(audience_score))
                time.sleep((3.15+2*random.random()))
                critic_string = driver.find_element_by_xpath('//*[@id="main_content"]/div[1]/div[3]/div/div[1]/table/tbody/tr[2]/td[1]/table/tbody/tr/td[2]/div[2]/span/a/span[2]').text
                critic_count = int(''.join(filter(str.isdigit, critic_string)))
                num_critics.append(critic_count)
                time.sleep((3.51+2*random.random()))
                audience_count_string = driver.find_element_by_xpath('//*[@id="main_content"]/div[1]/div[3]/div/div[1]/table/tbody/tr[2]/td[2]/table/tbody/tr/td[2]/div[2]/span/a/span[2]').text
                audience_count = int(''.join(filter(str.isdigit, audience_count_string)))
                num_audience_ratings.append(audience_count)
                print(metascores, audience_scores, num_critics, num_audience_ratings)
            except NoSuchElementException:
                print('NoSuchElementException on second loop')
                try:
                    response = requests.get(driver.current_url)
                    page = response.text
                    soup = BeautifulSoup(page, 'lxml')
                    table = soup.find('td', class_='left inset_right2')
                    inner = table.find('span', class_='metascore_w').text
                    metascores.append(inner)
                except:
                    print('naw')
            metascores.append('No score')
            audience_scores.append('No score')
            num_critics.append('No critics')
            num_audience_ratings.append('No ratings')
        print(metascores, audience_scores, num_critics, num_audience_ratings)
        print(title)
        driver.close()

    score_titles = {}

    score_titles['metascores'] = metascores
    score_titles['audience rating'] = audience_scores
    score_titles['number of critics'] = num_critics
    score_titles['number of audience ratings'] = num_audience_ratings
