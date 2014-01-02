import pandas as pd 
import numpy as np 
import urllib.request
import csv
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from helpers import string_to_type, unique_order_preserved, delmited_text_arranger, plot_dict_list
from pandas import read_csv
from pandas.tools.plotting import radviz
#http://pandas.pydata.org/pandas-docs/stable/dsintro.html

#print(np.random.randn(5))
#s = pd.Series(np.random.randn(5), index=['a', 'b', 'c', 'd', 'e'])
#print(s)
"""
my_data = np.array([0,1,2,3,4])
s_two= pd.Series(my_data, index=['a', 'b', 'c', 'd', 'e'])

print(s_two)
"""

"""
a    0
b    1
c    2
d    3
e    4
dtype: int32
"""

"""
print(s_two.index)  #Index(['a', 'b', 'c', 'd', 'e'], dtype=object)
print(s_two.index[0]) #a


my_data = {'a' : 0., 'b' : 1., 'c' : 2.}
s_three_a = pd.Series(my_data)
print(s_three_a)
s_three_b = pd.Series(my_data, index=['b', 'c', 'd', 'a'])
print(s_three_b)
"""
#print(np.random.randn(2, 5, 4))
#===================


response = urllib.request.urlopen('http://archive.ics.uci.edu/ml/machine-learning-databases/iris/bezdekIris.data')
html = response.read().decode("utf-8")
headers = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'iris_label']
flower_names = ['Iris-setosa','Iris-virginica','Iris-versicolor']
html = html.split('\n')
df = delmited_text_arranger(html, ',', out_type = 'dict_list_rows', headers = False, user_def_headers = headers, reports = True)
#print(df)
df = pd.DataFrame(df)


#panel_data = {'Iris-setosa': df[(df['iris_label'] == 'Iris-setosa')], 'Iris-virginica': df[(df['iris_label'] == 'Iris-virginica')], 'Iris-versicolor': df[(df['iris_label'] == 'Iris-versicolor')]}
#panel = pd.Panel(panel_data)

df_a = df[(df['iris_label'] == 'Iris-setosa')]
df_b = df[(df['iris_label'] == 'Iris-versicolor')]
df_c = df[(df['iris_label'] == 'Iris-virginica')]


data2 = {'Iris-virginica' : df_c, 'Iris-versicolor' : df_b}
panel =pd.Panel(data2)
#panel['Iris-versicolor'] = df_b
#panel['Iris-virginica'] = df_c

print(panel['Iris-versicolor'].to_string())



"""
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x_a = df_a['sepal_length']
y_a = df_a['sepal_width']
z_a = df_a['petal_length']

x_b = df_b['sepal_length']
y_b = df_b['sepal_width']
z_b = df_b['petal_length']

x_c = df_c['sepal_length']
y_c = df_c['sepal_width']
z_c = df_c['petal_length']

ax.scatter(x_a, y_a, z_a, c='r', marker='o')
ax.scatter(x_b, y_b, z_b, c='g', marker='x')
ax.scatter(x_c, y_c, z_c, c='b', marker='^')

ax.set_xlabel('sepal_length')
ax.set_ylabel('sepal_width')
ax.set_zlabel('petal_length')

plt.show()
"""


"""
for c, m, flower  in [('r', 'o', 'Iris-setosa'), ('b', '^', 'Iris-virginica'), ('g', 'x', 'Iris-versicolor')]:
	xs = panel[flower]['sepal_length']
	ys = panel[flower]['sepal_width']
	zs = panel[flower]['petal_length']
	ax.scatter(xs, ys, zs, c=c, marker=m)
	ax.set_xlabel('sepal_length')
	ax.set_ylabel('sepal_width')
	ax.set_zlabel('petal_length')
	plt.show()
"""





"""
ax1 = plt.subplot(311) # creates first axis 
ax1.scatter(panel['Iris-setosa']['petal_length'], panel['Iris-setosa']['petal_width'], 'k-') 
ax2 = plt.subplot(312) # creates second axis 
ax2.scatter(panel['Iris-virginica']['petal_length'], panel['Iris-virginica']['petal_width'], 'k--') 
ax3 = plt.subplot(313) # creates third axis
ax3.scatter(panel['Iris-versicolor']['petal_length'], panel['Iris-versicolor']['petal_width'], 'k--') 
plt.show() 
"""



#df2 = df[df['iris_label'].isin('Iris-setosa')]
#print(df[(df['iris_label'] == 'Iris-setosa') & (df['petal_length'] > 1.5)])
#print(df[df['iris_label'].isin(['Iris-setosa','Iris-virginica'])][:60])





"""
new_df = [[] for x in range(3)]

for line in df:
	for idx, flower in enumerate(flower_names):
		if line[4] == flower:
			new_df[idx].append(line[0:3])
new_df = np.array(new_df)
"""