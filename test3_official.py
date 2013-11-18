#import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import re
import csv

month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']	#Note, May is short enoug to not need abbreviation, so make sure we have full week name like Thursday instead of Thur for full date stamp. THIS stuff: "(Thu, May 30)" is ignored by reader
day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']


def Initiate_Driver() : #Next, the instance of Firefox WebDriver is created.
	driver = webdriver.Firefox()
	return driver

def Convert_2_Month_Num(str_month_name):
	month_names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
	return (month_names.index(str_month_name) + 1)

def Convert_2_YYYMMDD_Date(str_year, str_month, str_day):
	if len(str_month) == 1:
		str_month = "0" + str_month
	if len(str_day) == 1:
		str_day = "0" + str_day
	YYYMMDD_Date = str(str_year + str_month + str_day) #an example of Integer date (my b-day): 19910210 
	return YYYMMDD_Date


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
	print("THIS SHIT ==> " + str) #<======NEW SHIT
	list = []
	out = []
	for i in range(len(str)):
		if ',' == str[i]:
			list.append(i)
	comma1 = list[0]
	comma2 = list[1] #WHAT IF THE HEADLINE IS TWO LINES LONG?!?!?!?!?!?! HERE IS TEH PROBLEM, INITIATLED LINE 120. SEE FIRE FOX WINDOW
	DayName = str[:comma1]	
	nameAndMonth = str[comma1+2:comma2]
	spaceLoc = nameAndMonth.find(' ')
	Month = nameAndMonth[:spaceLoc]
	DayNum = nameAndMonth[spaceLoc+1:]
	Year = str[comma2+2:]

	out = [DayName,Month,DayNum,Year]
	return out					

def enterTicker(ticker):
	driver = Initiate_Driver()
	driver.get("http://finance.yahoo.com/")
	elem = driver.find_element_by_id("txtQuotes")
	elem.send_keys(ticker)
	elem.send_keys(Keys.RETURN)
	time.sleep(1.5)
	return driver

def Navigate_to_headlines(driver):
	driver.find_element_by_partial_link_text("Headlines").click()
	time.sleep(1.5)
	return driver

def click_get_older_news(driver):
	
	TempSoup=BeautifulSoup(driver.page_source)
	info = TempSoup.find_all('a')
	for item in info:
		if "Older Headlines" in item.text:
			link = "http://finance.yahoo.com" + item.get('href')
			break
	#driver.get(link)
	driver.get(link)
	time.sleep(2.0)
	soup=BeautifulSoup(driver.page_source)
	return {'soup':soup, 'driver': driver} #dictionary result['y0']  http://stackoverflow.com/questions/354883/how-do-you-return-multiple-values-in-python


def create_text_file_name(ticker):
	fileName = 'YahooHeadlines_' + ticker + '.csv'
	return fileName

def Scrape_YahooFinance_Headlines(ticker):
	driver = enterTicker(ticker)
	fileName = create_text_file_name(ticker)
	driver = Navigate_to_headlines(driver)

	#for first iteration
	soup=BeautifulSoup(driver.page_source)

	while True: #ensures we don;t hit a "No headlines available for QCOR prior to May 14, 2012." Event. If this does happen, startCt and endCt are None
		#soup=BeautifulSoup(driver.page_source)
		val = 0
		startCt = 0
		endCt = 0

		with open(fileName, 'a', newline='') as csvfile:
			#writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE)
			writer = csv.writer(csvfile, delimiter=',')

			info = soup.find_all(['span', 'li'])
			startCt = find_Open_Ct(info)
			endCt = find_End_Ct (info)

			if ( (startCt == None) or (endCt == None)): #BREAK statement to end search
				print("------------END----------------")
				driver.close()
				break
					
			currDateStamp = ''
			headline = ''
			link = ''
			newCitation = ''

			for item in info[startCt:endCt]:
				print('line 115--->', item.encode('ascii')) #<+_+_+_+_+_+_+_+_+_+_

				#Check if full month name and full weekday/weekend name is in string, otherwise we could grab "(Thu, May 30)" by accident
				if item.name == "span":
					for m in month_names:
						if (m in item.text):
							for d in day_names:
								if (d in item.text):
									currDateStamp = item.text
									currDateStampArray = parseDate(currDateStamp) #<----------------------------
									currDateStamp = item.text.encode('ascii')
									#print('----->',currDateStamp)

							#print(currDateStamp)
				if item.name == "li":
					#for citation
					citation = item.find('cite').text
					parens = citation.find('(')
					newCitation = citation[0:parens-1] #extra one space back to remove encoding error

					#removing 'at' from 'at Wall St. Cheat Sheet' if 'at' is present
					if 'at ' in newCitation:
						newCitation = newCitation[3:]
		
					#encode newCitation after manipulation in teh if statement
					newCitation = newCitation.encode('ascii') #<------------
		

					#get headline name
					headline = item.find('a').text.encode('ascii',errors='ignore') #<-----------
					#headline = item.find('a').text.encode('utf',errors='ignore') #<-----------
		
					#get link
					link = item.find('a').get('href').encode('ascii') #<------
		

				if currDateStamp and headline and link and newCitation and currDateStampArray:
					YYYMMDD_Date = Convert_2_YYYMMDD_Date((currDateStampArray[3]), str(Convert_2_Month_Num(currDateStampArray[1])), str(currDateStampArray[2])) #an example of Integer date (my b-day): 19910210
					newsLine = [YYYMMDD_Date, currDateStampArray[0], currDateStampArray[1], currDateStampArray[2], currDateStampArray[3], ticker, headline.decode("ascii"), newCitation.decode("ascii"), link.decode("ascii")]			
					writer.writerow( newsLine )#<-----------------------------------------------------------------------------------------------------------------------------
					#print(newsLine)
					link = ''
					newCitation = ''
					IntegerDate = ''

		Driver_dict = click_get_older_news(driver)	
		soup = Driver_dict['soup']
		driver = Driver_dict['driver']
		Driver_dict = ''



Ticker_List = ["CSCO", "JNPR", "HPQ"]
for stck in Ticker_List:
	Scrape_YahooFinance_Headlines(stck)

#--------------------------------READING WRITING CSV----------------------------------------
 
#with open('test.csv', 'w', newline='') as csvfile:
	#writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONE)
 	#writer.writerow(  .. )
#for row in reader:
    #writer.writerow(row)

#-------------------------------------------------------------------------------------------

#b'<span>Wednesday, September 25, 2013</span>'
#Home
#http://us.lrd.yahoo.com/_ylt=AvH.CdwQX6U5rypAMylCiMGuv7gF/SIG=119r32ntr/EXP=1381429544/**http%3A//www.yahoo.com/


#for line in soup.find_all(['span', 'li']):
	#startCt = startCt + 1
	#print(line.getText().encode('utf-8'))
	#if line.name == "span":
		#for m in month_names:
			#if m in line.text:	
				#val = 5
	#if line.name == "li":
		#val = 2

	#print(val,line.encode('utf-8'))
	#print(val, line.encode('utf-8'))


	#print(spans.get('attr'))





	#strs = spans.findAll(text=True)
	#for s in strs:
		#for monthNames in month_names:
			#if monthNames in s:
				#print(s)




#for spans in soup.find_all('span', text = "September"):
	#for monthName in month_names:
		#if monthName in spans:
			#print(spans.encode('utf-8'))


#in soup.find_all('span')
#soupW.find_all(["a", "b"])


#	p = spans.parent

#b'<span>Wednesday, September 11, 2013</span>' basically, if the span contains a (full name of weekdate like Wednesday), then a Month name, then a 4 digit #. This is a sign that the tag is what you are looking for

#b'<span>(Wed, Sep 11)</span>'


#print(soup.prettify())

#for link in soup.find_all('li'):
    #print(link)

#A function -> used to define a function, see the website http://www.crummy.com/software/BeautifulSoup/bs4/doc/#a-regular-expression

#soup.find_all('a')
#print soup.encode('utf-8')
#print(soup.prettify())
#print(soup.find_all("a"))
#print(soup.get_text())

#for link in soup.find_all('li'):
    #print(link.get('href'))