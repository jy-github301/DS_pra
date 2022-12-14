import requests # http requests
from bs4 import BeautifulSoup # Webscrape
import pandas as pd 


# start chrome service
from selenium.webdriver.chrome.service import Service
service = Service("/Users/jyang19/Downloads/chromedriver") # download chromedriver,get the path
service.start()

# define driver
from selenium import webdriver
driver = webdriver.Remote(service.service_url)


# Get webpage using *requests*

driver.get("https://www.linkedin.com/jobs/search")

# input position
elem = driver.find_element_by_name("keywords")
elem.clear()
elem.send_keys("data scientist")


# elem=driver.find_element_by_name("location")
# elem.clear()
# elem.send_keys("Houston, TX")

# return
from selenium.webdriver.common.keys import Keys
elem.send_keys(Keys.RETURN)

# Get current link
url = driver.current_url


# make the current link the url to open for Crawler
import requests

url = driver.current_url
req = requests.get(url)
webpage = req.text

# Get specific contents using BeatifulSoup
soup = BeautifulSoup(webpage, 'html.parser')


# 3 Prettify the webpage
soup.prettify()



#  Get all the contex
all_link =soup.find_all("a")

job_page_links = []

for item in all_link:
    if "jobs/view" in str(item):
        link = item.get('href')
        job_page_links.append(link)
 

#  search other 5 pages
pages=[1,2,3,4]
for i in pages:
    url = url+"&start"+str(i*25)
    req = requests.get(url)
    webpage = req.text
    soup = BeautifulSoup(webpage, 'html.parser')
    soup.prettify()
    all_link = soup.find_all("a")
    for item in all_link:
        if "jobs/view" in str(item):
            link = item.get('href')
            job_page_links.append(link)

#  get context
from random import random
import time

job_title = []

for i in range(len(job_page_links)):
    req = requests.get(job_page_links[i])
    webpage = req.text
    soup = BeautifulSoup(webpage, 'html.parser')
    try:
        
        job_title.append(soup.find("title").getText())
    except:
        print("except:",i)
        pass
 
    t = 1 + 2 * random()
    time.sleep(t)
    
print("done")

#  make dataframe and output

data = pd.DataFrame()
data["link"]=job_page_links
data["detail"]=job_title

data.to_csv("jobs.csv")

# quit driver
driver.quit()
