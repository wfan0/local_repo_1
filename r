#import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import re
import csv

month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']	
#Next, the instance of Firefox WebDriver is created.
driver = webdriver.Firefox()


def find_Open_Ct (info) :
	#month_names already defined
	startCt = 0
	for line in info:
		startCt = startCt + 1
		if line.name == "span":
			for m in month_names:
				if m in line.text: 
					return startCt -1

def find_End_Ct (info) :
	#Ending looks like this: b'<span>AdChoices</span>' or like this: '<span id="yfs_params_vcr" style="display:none">{"yrb_token" : "YFT_MARKET_CLOSED", "tt" : "1380231285", "s" : "qcor", "k" : "a'
	EndCt = 0
	for line in info:
		EndCt = EndCt + 1
		if line.name == "span" and 'AdChoices' in line.text:
			return EndCt - 1
		if line.name == "span" and 'yrb_token' in line.text:
			return EndCt - 1

def parseDate(str):
	list = []
	out = []
	for i in range(len(str)):
		if ',' == str[i]:
			list.append(i)
	comma1 = list[0]
	comma2 = list[1]
	DayName = str[:comma1]	
	nameAndMonth = str[comma1+2:comma2]
	spaceLoc = nameAndMonth.find(' ')
	Month = nameAndMonth[:spaceLoc]
	DayNum = nameAndMonth[spaceLoc+1:]
	Year = str[comma2+2:]

	out = [DayName,Month,DayNum,Year]
	return out					

def enterTicker(ticker):
	driver.get("http://finance.yahoo.com/")
	elem = driver.find_element_by_id("txtQuotes")
	elem.send_keys(ticker)
	elem.send_keys(Keys.RETURN)
	time.sleep(1.5)

def Navigate_to_headlines():
	driver.find_element_by_partial_link_text("Headlines").click()
	time.sleep(1.5)

def click_get_older_news():
	TempSoup=BeautifulSoup(driver.page_source)
	info = TempSoup.find_all('a')
	for item in info:
		if "Older Headlines" in item.text:
			link = "http://finance.yahoo.com" + item.get('href')
			break
	#driver.get(link)
	driver.get(link)
	time.sleep(8)
	soup=BeautifulSoup(driver.page_source)
	return soup

def create_text_file_name(ticker):
	fileName = 'YahooHeadlines_' + ticker + '.csv'
	return fileName


enterTicker("QCOR")
fileName = create_text_file_name("QCOR")
Navigate_to_headlines()

#while True:
	#soup=BeautifulSoup(driver.page_source)
	#info = soup.find_all(['span', 'li'])
	#for item in info:
		#print(item.text.encode('utf-8'))
	#click_get_older_news()

soup=BeautifulSoup(driver.page_source)


info = soup.find_all(['span', 'li'])
for item in info:
	print(item.text.encode('utf-8'))
soup = click_get_older_news()


info = soup.find_all(['span', 'li'])
for item in info:
	print(item.text.encode('utf-8'))
soup = click_get_older_news()


info = soup.find_all(['span', 'li'])
for item in info:
	print(item.text.encode('utf-8'))
soup = click_get_older_news()


info = soup.find_all(['span', 'li'])
for item in info:
	print(item.text.encode('utf-8'))
soup = click_get_older_news()
