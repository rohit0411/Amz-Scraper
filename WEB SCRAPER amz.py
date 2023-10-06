from bs4 import BeautifulSoup as soup
import mysql.connector
from urllib.request import urlopen as uReq 
from time import sleep
from random import randint

search_url = ('https://www.amazon.in/s?k=' + "+".join(input("WHICH ITEM DO YOU WANT? : ").split()) +'&ref=nb_sb_noss_')

HEADERS = ({'User-Agent':
                "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Mobile Safari/537.36",
                'Accept-Language': 'en-US'})

print("WHICH METHOD DO YOU WANT TO PROCEED WITH ")
print()
print("PYTHON / SQL / EXCEL")
task = input("TYPE ITS NAME  ")

alpha = task.lower()

def PRODUCT_NAME(container):
      try:
         x = container.div.span.div.div.find("span", {"class": "a-size-medium a-color-base a-text-normal"}).text.strip().replace("|"," ").replace(","," ")
        
      except AttributeError:
                 x = "Not Available" 
      return x
def PRICE(container):
     try:
      u = container.div.span.div.div.find("span", {"class": "a-price-whole"}).text.strip()
     except AttributeError:
         u = "Not Available"
     return u  
def RATINGS(container):
     try:
      j = container.find("span", {"class": "a-icon-alt"}).text.strip()
     except AttributeError:
         j = "Not Available"
     return j
def AVAILABILITY(container):
     try:
      l = container.find("span", {"class": "a-color-price"}).text.strip()
     except AttributeError:
         l = " Available"
     return l
def parse_page(next_url):
    uClient = uReq(next_url)
    bs = soup(uClient.read(), "lxml")
    uClient.close()
    containers = bs.find_all("div", {"class": "s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col sg-col-12-of-16"})
    for container in containers:
     print("PRODUCT_NAME: " ,PRODUCT_NAME(container))
     print("PRICE: " ,'\u20B9',PRICE(container))
     print("RATINGS: " ,RATINGS(container))
     print("AVAILABILITY: ",AVAILABILITY(container))
     print()
     sleep(randint(1,2))
    xy = bs.find("div",{"class" : "s-main-slot s-result-list s-search-results sg-row"}).find("ul",attrs={"class" : "a-pagination"})
    y = xy.find("li",{"class": "a-last"}).find("a")
    next_page_partial = (y.get('href')).strip()
    next_page_url = ("https://www.amazon.in" + next_page_partial)
    sleep(8)
    parse_page(next_page_url) 
def parse_pagesql(next_url):
    uClient = uReq(next_url)
    bs = soup(uClient.read(), "lxml")
    uClient.close()
    containers = bs.find_all("div", {"class": "s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col sg-col-12-of-16"})
    for container in containers:
     mycur.execute("""INSERT INTO WEB_SCRAPER VALUES(%s, %s, %s, %s) """,(PRODUCT_NAME(container), PRICE(container), RATINGS(container), AVAILABILITY(container)))
     mydb.commit()
     print("PRODUCT_NAME: " ,PRODUCT_NAME(container))
     print("PRICE: " ,'\u20B9',PRICE(container))
     print("RATINGS: " ,RATINGS(container))
     print("AVAILABILITY: ",AVAILABILITY(container))
     print()
     sleep(randint(1,2))
    xy = bs.find("div",{"class" : "s-main-slot s-result-list s-search-results sg-row"}).find("ul",attrs={"class" : "a-pagination"})
    y = xy.find("li",{"class": "a-last"}).find("a")
    next_page_partial = (y.get('href')).strip()
    next_page_url = ("https://www.amazon.in" + next_page_partial)
    sleep(6)
    parse_pagesql(next_page_url)
def parse_pageexcel(next_url):
    uClient = uReq(next_url)
    bs = soup(uClient.read(), "lxml")
    uClient.close()
    containers = bs.find_all("div", {"class": "s-result-item s-asin sg-col-0-of-12 sg-col-16-of-20 sg-col sg-col-12-of-16"})
    for container in containers:  
     f.write(PRODUCT_NAME(container) + ", " + PRICE(container) + ", " + RATINGS(container) + "," + AVAILABILITY(container) + "\n")
     print("PRODUCT_NAME: " ,PRODUCT_NAME(container))
     print("PRICE: " ,'\u20B9',PRICE(container))
     print("RATINGS: " ,RATINGS(container))
     print("AVAILABILITY: ",AVAILABILITY(container))
     print()
    sleep(randint(0,1))
    xy = bs.find("div",{"class" : "s-main-slot s-result-list s-search-results sg-row"}).find("ul",attrs={"class" : "a-pagination"})
    y = xy.find("li",{"class": "a-last"}).find("a")
    next_page_partial = (y.get('href')).strip()
    next_page_url = ("https://www.amazon.in" + next_page_partial)
    sleep(2)
    parse_pageexcel(next_page_url)
if alpha =="python":
    print()
    parse_page(search_url)   
elif alpha =="sql":
     mydb=mysql.connector.connect(host='localhost', user='root', passwd=(input("ENTER YOUR SQL PASSWORD : ")), database='hotel')
     mycur=mydb.cursor()
     mycur.execute("drop table if exists web_scraper")
     mycur.execute("create table WEB_SCRAPER(PRODUCT_NAME varchar(900), PRICE varchar(90), RATING varchar(90),AVAILABILITY varchar(90))")
     parse_pagesql(search_url)    
elif alpha =="excel":
    headers = "PRODUCT_NAME, PRICE, RATINGS, AVAILABILITY \n"
    f = open('AMAZON PRODUCTS.csv' , "w" ,encoding="utf-8")
    f.write(headers)
    parse_pageexcel(search_url)
