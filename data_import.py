import scipy as sp
import csv
import matplotlib.pyplot as plt 
from scipy.optimize import fsolve

def preprocess_yahoo_data(file): 
	results = {}
	date = []
	open_ = []
	high = []
	low = []
	close = []
	volume = []
	adj_close = []

	with open(file, newline = '') as fid:
		ct = 0
		"""
		for row in csv.reader(fid):
			if row is not None:
				print (row)
		"""

		for row in csv.reader(fid):	
			if ct == 0:
				pass
			if ct > 0:
				line = {}
				line["date"] = int(row[0].replace("-", ""))
				line["open"]= float(row[1])
				line["high"] = float(row[2])
				line["low"]  = float(row[3])
				line["close"] = float(row[4])
				line["volume"] = float(row[5])
				line["adj_close"] = float(row[6])
			
			if ct !=0 :
				results[line.get("date")] = line

			ct = ct +1
	return results



def grab_range(data, start_date,end_date):
	filtered_data  = { k: v for k, v in data.items() if (k >= start_date and k <= end_date) }

	#filtered_data = {k: for k,v in data.items() if ((k >= start_date) and (k <= end_date)}
	return filtered_data

def error(f,x,y):
	return sp.sum((f(x)-y)**2)

	

data = []
start_date = 20130601
end_date = 20141230
out = preprocess_yahoo_data('C:\\Users\\William\\Desktop\\Dtop5\\AAPL.csv')
#print(out)
print("----------------------------------------------")

data_sample = grab_range(out, start_date,end_date)
date = []
adj_close = []
vol = []



for k,v in sorted(data_sample.items()):
	date.append(k)
	adj_close.append(v['adj_close'])
	vol.append(v['volume'])


#print(date)
#print(adj_close)

fpl, redisdials, rank, sv, rcond = sp.polyfit(date,adj_close,1,full = True)
print("model params: %s" % fpl)
f1 = sp.poly1d(fpl)
print("error: %s" % error(f1, date, adj_close) )

fpl2, redisdials2, rank2, sv2, rcond2 = sp.polyfit(date,adj_close,2,full = True)
print("model params: %s" % fpl2)
f2 = sp.poly1d(fpl2)
print("error: %s" % error(f2, date, adj_close) )

fpl3, redisdials3, rank3, sv3, rcond3 = sp.polyfit(date,adj_close,3,full = True)
print("model params: %s" % fpl3)
f3 = sp.poly1d(fpl3)
print("error: %s" % error(f3, date, adj_close) )

plt.subplot(2,1,1)
plt.title('monthly adjusted close prices for DATE stock')
plt.scatter(date,adj_close)
plt.plot(date,f1(date), 'r')
plt.plot(date,f2(date), 'g')
plt.plot(date,f2(date), 'm')
plt.xlabel('date')
plt.ylabel('adjusted close')

plt.subplot(2,1,2)
plt.title('monthly closing volumes for DATE stock')
plt.scatter(date,vol)
plt.xlabel('date')
plt.ylabel('closing volume')

#plt.autoscale(tight = 'true')
plt.grid()
plt.show()

reached_max = fsolve(f2 -900,800)
print("reached_max is: %s" % reached_max)

"""
for i in range(len(data)):
	print(i)
	"""



