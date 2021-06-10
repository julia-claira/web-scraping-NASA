import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
from flask import Flask, jsonify
import time

def scrape():

    #setup splinter
    executable_path= {'executable_path': ChromeDriverManager().install()}
    browser= Browser('chrome', **executable_path, headless=False)

    #function to have beautifulSoup parse url
    def parser (theurl):
        
        #pull up url
        browser.visit(theurl)
        html = browser.html
        thesoup = BeautifulSoup(html, 'html.parser')

        return thesoup

    #1)Scrape the Mars News Site and collect the latest News Title and Paragraph Text
    url='https://redplanetscience.com/'
    soup=parser(url)

    #declare variables -- originally I read the above as finding all the latest News Titles and decided to keep it for practice
    mars_titles=[]
    mars_paragraphs=[]

    #scrape titles
    results=soup.find_all('div', class_='content_title')

    #append titles to list
    for result in results:
        mars_titles.append(result.text.strip())

    #assign the most recent title to a variable 
    news_title=mars_titles[0]
    #--------------------------------------------
    #scrape paragraph
    results=soup.find_all('div', 'article_teaser_body')

    #append paragraphs to list
    for result in results:
        mars_paragraphs.append(result.text.strip())
        
    #save 1st paragraph
    news_p=mars_paragraphs[0]
    #--------------------------------------------
    #2)Visit the url for the Featured Space Image site here.

    #parse feature image site
    url='https://spaceimages-mars.com/'
    soup=parser(url)

    #Use splinter to navigate the site and find the image url for the current Featured Mars Image
    browser.links.find_by_partial_text('FULL IMAGE').click()

    #store new html
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    #save feature image source
    result=soup.find('img', class_='fancybox-image')
    featured_image_url=url+result['src']

    #--------------------------------------------
    #Visit the Mars Facts webpage here and use Pandas to scrape the table

    url='https://galaxyfacts-mars.com/'
    tables=pd.read_html(url)

    #Use Pandas to convert the data to a HTML table string.
    the_table=tables[0].set_index(0)
    the_table.rename(columns={1:'Mars',2:'Earth'},inplace=True)
    the_table.index.names = ['Description']

    #set table to html
    the_table_html=the_table.to_html()

    #--------------------------------------------
    #function to pull the image url
    def imagePull(hemisphere):
        
        #click on link for hemisphere
        browser.links.find_by_partial_text(hemisphere).click()
        
        #parse the new browser
        html = browser.html
        temp = BeautifulSoup(html, 'html.parser')
        
        #find the large image file
        the_image=temp.find('a',text='Sample')
        
        #move back to original page
        browser.links.find_by_partial_text('Back').click()

        return the_image['href']

    #----------------------------------------------------
    #list to store dictionary of image url and title
    hemisphere_image_urls=[]

    #open the page
    url='https://marshemispheres.com/'
    soup=parser(url)

    #finds link names
    links=soup.find_all('h3')

    #loops through the first four links
    for link in links:
        if link.text !='Back':
            the_image_url=f'{url}{imagePull(link.text)}'
            
            #append the list with a dictionary
            hemisphere_image_urls.append({"title": link.text, "img_url":the_image_url})

    #--------------------------------------------
    
    #return a dictionary of all the scraped data
    scraped_data={
        "latest_title":news_title,"latest_p":news_p,
        "featured_image":featured_image_url,
        "the_table":the_table_html,
        "the_hemispheres":hemisphere_image_urls    
    }

    browser.quit()


    return scraped_data




