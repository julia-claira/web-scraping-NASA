#!/usr/bin/env python
# coding: utf-8

# In[64]:


import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
from flask import Flask, jsonify
import time


# In[30]:


#setup splinter
executable_path= {'executable_path': ChromeDriverManager().install()}
browser= Browser('chrome', **executable_path, headless=False)


# In[3]:


#function to have beautifulSoup parse url
def parser (theurl):
    
    #pull up url
    browser.visit(theurl)
    html = browser.html
    thesoup = BeautifulSoup(html, 'html.parser')

    return thesoup


# In[4]:


#1)Scrape the Mars News Site and collect the latest News Title and Paragraph Text
url='https://redplanetscience.com/'
soup=parser(url)

#declare variables
mars_titles=[]
mars_paragraphs=[]

#scrape titles
results=soup.find_all('div', class_='content_title')

#append titles to list
for result in results:
    mars_titles.append(result.text.strip())

#print results to verify
mars_titles


# In[5]:


#scrape paragraph
results=soup.find_all('div', 'article_teaser_body')

#append paragraphs to list
for result in results:
    mars_paragraphs.append(result.text.strip())
    
#print 1st paragraph to verify it worked
print(mars_paragraphs[0])

2)Visit the url for the Featured Space Image site here.

Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.

Make sure to find the image url to the full size .jpg image.

Make sure to save a complete url string for this image.
# In[9]:


#2)Visit the url for the Featured Space Image site here.

#parse feature image site
url='https://spaceimages-mars.com/'
soup=parser(url)


# In[10]:


#Use splinter to navigate the site and find the image url for the current Featured Mars Image
browser.links.find_by_partial_text('FULL IMAGE').click()

#store new html
html = browser.html
soup = BeautifulSoup(html, 'html.parser')

#save feature image source
result=soup.find('img', class_='fancybox-image')
featured_image_url=url+result['src']

print(featured_image_url)

3)Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.

Use Pandas to convert the data to a HTML table string.
# In[20]:


#Visit the Mars Facts webpage here and use Pandas to scrape the table

url='https://galaxyfacts-mars.com/'
tables=pd.read_html(url)


# In[27]:


#Use Pandas to convert the data to a HTML table string.
the_table=tables[1].set_index(0)
the_table_html=the_table.to_html()


# In[81]:


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

hemisphere_image_urls


# In[ ]:


browser.quit()

