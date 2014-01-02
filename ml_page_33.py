#dataset foud here: http://archive.ics.uci.edu/ml/machine-learning-databases/iris/bezdekIris.data
import urllib.request
import csv
from matplotlib import pyplot as plt
from helpers import string_to_type, unique_order_preserved, delmited_text_arranger, plot_dict_list
import numpy as np
import pandas as pd 

response = urllib.request.urlopen('http://archive.ics.uci.edu/ml/machine-learning-databases/iris/bezdekIris.data')
html = response.read().decode("utf-8")
headers = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'iris_label']
flower_names = ['Iris-setosa','Iris-virginica','Iris-versicolor']
html = html.split('\n')
df = delmited_text_arranger(html, ',', out_type = 'rows', headers = False, user_def_headers = headers, reports = True)

new_df = [[] for x in range(3)]

for line in df:
	for idx, flower in enumerate(flower_names):
		if line[4] == flower:
			new_df[idx].append(line[0:3])
new_df = np.array(new_df)
#print(new_df)
#print(np.random.rand(10, 4))

flw_idx = 0
df = pd.DataFrame(new_df[flw_idx], columns=headers[0:3])
ax = df.plot(kind='barh', stacked=True, style=['r','g','b','r'])
plt.legend(loc='best')
plt.title(str(flower_names[flw_idx]))
plt.tight_layout()
plt.show()


#print(np.array(df))
#print(np.random.rand(10, 4))
#df2 = pd.DataFrame(np.random.rand(10, 4), columns=['a', 'b', 'c', 'd'])
#print(df2)
#df.ix[1:4].plot(kind='bar'); plt.axhline(0, color='k')
#plt.show()

#f2.plot(kind='bar', stacked=True)
#plt.show()

#f2 = delmited_text_arranger(html, ',', out_type = 'dict_list_rows', headers = False, user_def_headers = headers, reports = True)

#plot_dict_list(f2, 'iris_label', ['sepal_length'])






"""
f = delmited_text_arranger(html, ',', out_type = 'rows', headers = False, user_def_headers = None, reports = True)
Iris_setosa_data = []
Iris_virginica_data = []
Iris_versicolor_data = []

for line in f:
	if line[4] == 'Iris-setosa':
		Iris_setosa_data.append(line[0:4])
	if line[4] == 'Iris-virginica':
		Iris_virginica_data.append(line[0:4])
	if line[4] == 'Iris-versicolor':
		Iris_versicolor_data.append(line[0:4])

Tot_data = [Iris_setosa_data,Iris_virginica_data,Iris_versicolor_data]

data_two = []
for item in f:
	if (item[4] == 'Iris-versicolor' or item[4] == 'Iris-virginica'):
		data_two.append(item)

#above threshold = verginica?
for feature in range(len(data_two[0])-1):
	best_acc = -1
	best_cutoff = -1
	versi_acc = 0
	#sort list of list by feature
	data_two.sort(key=lambda x: x[feature])
	thresh = unique_order_preserved([item[feature] for item in data_two])
	for thresh_val in thresh:
		versi_acc = -1
		pred = [item for item in data_two if (item[feature] < thresh_val)]
		print('--->thresh ' + str(thresh_val))
		versi_acc = sum([1 if item[4] == 'Iris-versicolor' else -1 for item in pred])/len(data_two)
		print('--->pred ' + str([1 if item[4] == 'Iris-versicolor' else -1 for item in pred]))
		print('--->acc ' + str(versi_acc))
		if versi_acc > best_acc:
			best_acc = versi_acc
			best_cutoff = thresh_val
		#cutoff = [item for item in data_two[feature] if item == ]

	print(headers[feature] + ' accuracy is : ' + str(best_acc) + ' threshhold for versicolor is: ' + str(best_cutoff))

#----------------------------------=========================


plt.subplot(2,3,0)
for flower, marker, color in zip(range(3),">ox","rgb"):
			plt.scatter([Tot_data[flower][x][0] for x in range(len(Iris_setosa_data))],
			[Tot_data[flower][x][1] for x in range(len(Iris_setosa_data))],
			marker=marker,
			c=color,
			)
plt.xlabel(headers[0])
plt.ylabel(headers[1])
plt.grid()

plt.subplot(2,3,1)
for flower, marker, color in zip(range(3),">ox","rgb"):
			plt.scatter([Tot_data[flower][x][0] for x in range(len(Iris_setosa_data))],
			[Tot_data[flower][x][2] for x in range(len(Iris_setosa_data))],
			marker=marker,
			c=color,
			)
plt.xlabel(headers[0])
plt.ylabel(headers[2])
plt.grid()

plt.subplot(2,3,2)
for flower, marker, color in zip(range(3),">ox","rgb"):
			plt.scatter([Tot_data[flower][x][0] for x in range(len(Iris_setosa_data))],
			[Tot_data[flower][x][3] for x in range(len(Iris_setosa_data))],
			marker=marker,
			c=color,
			)
plt.xlabel(headers[0])
plt.ylabel(headers[3])
plt.grid()
#------
plt.subplot(2,3,3)
for flower, marker, color in zip(range(3),">ox","rgb"):
			plt.scatter([Tot_data[flower][x][1] for x in range(len(Iris_setosa_data))],
			[Tot_data[flower][x][2] for x in range(len(Iris_setosa_data))],
			marker=marker,
			c=color,
			)
plt.xlabel(headers[1])
plt.ylabel(headers[2])
plt.grid()

plt.subplot(2,3,4)

for flower, marker, color in zip(range(3),">ox","rgb"):
			plt.scatter([Tot_data[flower][x][1] for x in range(len(Iris_setosa_data))],
			[Tot_data[flower][x][3] for x in range(len(Iris_setosa_data))],
			marker=marker,
			c=color,
			)
plt.xlabel(headers[1])
plt.ylabel(headers[3])
plt.grid()

plt.subplot(2,3,5)

for flower, marker, color in zip(range(3),">ox","rgb"):
			plt.scatter([Tot_data[flower][x][2] for x in range(len(Iris_setosa_data))],
			[Tot_data[flower][x][3] for x in range(len(Iris_setosa_data))],
			marker=marker,
			c=color,
			)
			max_petal_width = max([Tot_data[flower][x][3] for x in range(len(Iris_setosa_data))])
			max_petal_len = max([Tot_data[flower][x][2] for x in range(len(Iris_setosa_data))])
			print(str(max_petal_width) + " " + str(max_petal_len))
plt.plot([12/len(Iris_setosa_data)*x for x in range(len(Iris_setosa_data))], [.6 for x in range(len(Iris_setosa_data))], linestyle='--', color='r')
plt.plot([1.9 for x in range(len(Iris_setosa_data))], [3/len(Iris_setosa_data)*x for x in range(len(Iris_setosa_data))], linestyle='--', color='r')
plt.xlabel(headers[2])
plt.ylabel(headers[3])
plt.grid()
plt.show()


#===========================================================

"""


