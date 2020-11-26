from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd
import requests

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

mars_info = {}

#info for latest mars news
def scrape_info():
    browser = init_browser()

    # Visit website
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    #Find the latest news title and news paragraph
    mars_info["news_title"]= soup.find("div", class_="bottom_gradient").get_text()
    mars_info["news_p"] = soup.find("div", class_="article_teaser_body").get_text()

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_info

#info for Feature Mars Images
def scrape_info2():
    browser = init_browser()

    # Visit website
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    #get url link
    mars_info["image"]='https://www.jpl.nasa.gov' + (soup.find_all('div', class_='carousel_items')[0].a.get('data-fancybox-href'))
    
    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_info

#info for Mars Fact
def scrape_info3():

    #get url link
    mars_fact_url = "https://space-facts.com/mars/"
    
    #read the url
    tables = pd.read_html(mars_fact_url)  

    #get only the first table in the url
    df = tables[0]

    #set columns name
    df.columns = ['Description','Mars']

    #set index
    df.set_index('Description', inplace = True)

    #convert dataframe to html
    mars_facts_html = df.to_html()

    #store html table
    mars_info['facts'] = mars_facts_html

    # Return results
    return mars_info

#info for hemisphere
def scrape_info4():
    browser = init_browser()

    # Visit website
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    #get titles and image url
    hemiphere = soup.find_all('img',attrs={'class':'thumb'})
    hemiphere_img =[]

    for img in hemiphere:
        title = img.attrs['alt']
        url = 'https://astrogeology.usgs.gov' + (img.attrs['src'])
        hemiphere_img.append({'title':title,'img_url':url})
    
    mars_info["hemi"] = hemiphere_img

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_info