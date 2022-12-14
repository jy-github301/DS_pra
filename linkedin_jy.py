import requests # http requests
from bs4 import BeautifulSoup # Webscrape
import pandas as pd 

# 1. Get webpage using *requests*

url="https://www.linkedin.com/jobs/search/?currentJobId=3392182631&geoId=103644278&keywords=data%20scientist&location=United%20States&refresh=true"
req = requests.get(url)

webpage = req.text

# 2. Get specific contents using BeatifulSoup

soup = BeautifulSoup(webpage, 'html.parser')

# 3 Prettify the webpage
​
soup.prettify()

 # 4 Get all the contex

all_link =soup.find_all("a")

job_page_links = []

for item in all_link:
    if "jobs/view" in str(item):
        link = item.get('href')
        job_page_links.append(link)
 
 # 5 search other 5 pages

pages=[1,2,3,4]
url="https://www.linkedin.com/jobs/search/?currentJobId=3392182631&geoId=103644278&keywords=data%20scientist&location=United%20States&refresh=true"
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

# 6 get context
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

# 6 make dataframe and output

data = pd.DataFrame()
data["link"]=job_page_links
data["detail"]=job_title

data.to_csv("jobs.csv")

