from helpers import delmited_text_arranger
import csv

with open('C:\\Users\\William\\Desktop\\YahooHeadlines_CSCO.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	dates = [] #0
	headline = [] #6
	provider = [] #7
	link = [] #9

	for row in reader:
		dates.append(row[0])
		headline.append(row[6])
		provider.append(row[7])
		link.append(row[8])

providers = set(provider)
headline_a = set(headline[0:100])
print(headline_a)
#links_with_mw = [link[idx] for idx, item in enumerate(provider) if item == 'MarketWatch']
#print(links_with_mw)
