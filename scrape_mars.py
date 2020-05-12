# dependencies

import pandas as pd
from bs4 import BeautifulSoup
import requests
from splinter import Browser
import time
import re

# define this function first and use within scrape_info()
def init_browser():
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape_info():

# ## Part 1: NASA Mars News

    browser = init_browser()

    news_url = 'https://mars.nasa.gov/news/'
    browser.visit(news_url)

    time.sleep(5)  # wait for 5 seconds

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    title_splinter = soup.find_all('div', class_ = 'content_title')[1].text
    paragraph_splinter = soup.find('div', class_ = 'article_teaser_body').text.strip()

    browser.quit() # close this browser

# ## Part 2: JPL Mars Space Images - Featured Image
    browser = init_browser()

    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)

    time.sleep(5)  # wait for 5 seconds

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    result = soup.find('article', class_='carousel_item')

    featured_image = result['style'].split("'")[1]
    featured_image_url = 'https://www.jpl.nasa.gov' + featured_image

    browser.quit() # close this browser

# ## Part 3: Mars Weather
    twitter_url = 'https://twitter.com/marswxreport?lang=en'

    page = requests.get(twitter_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    # use the html text to extract the text frrom tweets that describe the weather 
    # take advantage of the fact that a tweet cannot exceed a certain number of characters

    # grab first line of text
    tweet1 = re.findall(r'InSight sol.............................................................', soup.prettify())[0]
    # grab second line of text
    tweet2 = re.findall(r'winds.................................................................', soup.prettify())[0]
    # grab third line of text
    tweet3 = re.findall(r'pressure............', soup.prettify())[0]

    mars_weather_tweet = tweet1 + " " + tweet2 +  " " + tweet3

# ## Part 4: Mars Facts
    facts_url = 'https://space-facts.com/mars/'
    mars_tables = pd.read_html(facts_url)
    mars_facts_df = mars_tables[0]
    mars_facts_df = mars_facts_df[1:].rename(columns = {0: 'Description', 1: 'Value'})
    html_table = mars_facts_df.to_html()

# ## Part 5: Mars Hemispheres

    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    cerberus_img = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg'
    schiaparelli_img = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg'
    syrtis_img = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg'
    valles_img = 'https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg'

    cerberus_dict = {'title': "Cerberus Hemisphere",
                    'img_url': cerberus_img,}
 
    schiaparelli_dict = {'title': "Schiaparelli Hemisphere",
                        'img_url': schiaparelli_img}

    syrtis_dict = {'title': "Syrtis Major Hemisphere",
                'img_url': syrtis_img}

    vallues_dict = {'title': "Valles Marineris Hemisphere",
                'img_url': valles_img}

    hemispheres_list = [cerberus_dict, schiaparelli_dict, syrtis_dict, vallues_dict]

    # Store all data in a dictionary
    mars_dictionary = {
        "title_splinter": title_splinter,
        "paragraph_splinter": paragraph_splinter,
        "featured_image_url": featured_image_url,
        "mars_weather_tweet": mars_weather_tweet,
        "html_table": html_table,
        "hemispheres_list": hemispheres_list,
        "cerberus_img": cerberus_img,
        "schiaparelli_img": schiaparelli_img,
        "syrtis_img": syrtis_img,
        "valles_img": valles_img}

    # Return results
    return mars_dictionary