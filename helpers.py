

def unique_order_preserved(seq, idfun=None): #for finding uniqyes with order preserving note that list(print(set(data[4]))) returns unordered
   # order preserving
   if idfun is None:
       def idfun(x): return x
   seen = {}
   result = []
   for item in seq:
       marker = idfun(item)
       # in old Python versions:
       # if seen.has_key(marker)
       # but in new ones:
       if marker in seen: continue
       seen[marker] = 1
       result.append(item)
   return result

def is_num(item):
	try:
		i = int(item)
		i = float(item)
	except ValueError:
		return False
	return True

#--------------------------------------------------------------------------------------------------------------------------------
def string_to_type(s):
	#check for bytecode vs. str
	try:
		s = s.decode("utf-8")
	#'str' object has no attribute 'decode'
	except: AttributeError
	pass


	num_periods = 0
	num_digits = 0
	num_plus_minus = 0
	num_e_E = 0
	period_loc = None
	plus_neg_begin_sign_loc = None
	plus_neg_exponent_sign_loc = None
	e_E_location = None
	plus_neg_begin_sign = False
	plus_neg_exponent_sign = False
	exponent_correct = False


	for idx, c in enumerate(s):
		#print(c)
		if c.isdigit() == False and c not in '.+-eE':
			return s 
		if num_periods >1:
			return s
		if c in 'eE':
			e_E_location = idx
			num_e_E += 1		
			if num_e_E >1:
				return s
		if c in '+-':
			num_plus_minus += 1
			if num_plus_minus > 2:
				return s
			if idx == 0:
				plus_neg_begin_sign = True
				plus_neg_begin_sign_loc = idx
			elif idx > 0:
				plus_neg_exponent_sign = True
				plus_neg_exponent_sign_loc = idx

		elif c in '.':
			num_periods += 1
			period_loc = idx
		elif c.isdigit():
			num_digits += 1

	if e_E_location != None:
		if e_E_location == len(s) -1:
			exponent_correct = False
		if plus_neg_exponent_sign == True and period_loc != None:
			if plus_neg_exponent_sign_loc == e_E_location + 1 and \
	   			period_loc < e_E_location-1: #225252.e10
				exponent_correct = True
		elif plus_neg_exponent_sign == True and period_loc == None:
			if plus_neg_exponent_sign_loc == e_E_location + 1:
				exponent_correct = True #'2253351e-100'
		elif plus_neg_exponent_sign == False and period_loc != None:
			if period_loc < e_E_location-1:
				exponent_correct = True
		elif plus_neg_exponent_sign == False and period_loc == None:
				exponent_correct = True

	if num_periods == 1 and num_digits >=2 and \
	   ((num_periods + num_digits + num_plus_minus + num_e_E) == len(s)) and \
	   period_loc != len(s)-1 and \
	   exponent_correct == True:
	   	#print('zz1')
	   	return float(s)

	if num_periods == 1 and num_digits >=2 and \
	   ((num_periods + num_digits + num_plus_minus) == len(s)) and \
	   period_loc != len(s)-1:
	   	#print('zz1')
	   	return float(s)

	if num_periods == 0 and num_digits >=1 and \
	   ((num_digits + num_plus_minus + num_e_E) == len(s)) and \
	   e_E_location != None and \
	   exponent_correct == True:
	   	#print('zz3')
	   	return float(s)  	

	#no exponents available for ints
	if num_periods == 0 and num_digits >= 1 and \
	   ((num_digits + num_plus_minus) == len(s)) and \
	   num_plus_minus <= 1: 
	   return int(s)	


	else:
		return s

#-------------------------------------------------------------------------------------------------------

def delmited_text_arranger(data, delimiter,  out_type = 'columns', headers = False, user_def_headers = None, reports = True):
	#data is assumed to be a list with n rows
	params = {'data': data, 'delimiter': delimiter, 'out_type': out_type, 'headers': headers, 'user_def_headers': user_def_headers, 'reports': reports}
	odd_data = []

	try:
		#extract 1st line in data 
		first_line_items = data[0].split(delimiter)
	#TypeError: Type str doesn't support the buffer API occurs when you extract from an html (which is class <class 'bytes'>), you have to decode it
	except TypeError:
		data = data.decode("utf-8")
		first_line_items = data[0].split(delimiter)

	first_line_items = data[0].split(delimiter)

	#skip first line
	if headers == True:
		del data[0]
	
	if out_type == 'rows':
		out = []
		for line in data:
			#print(line) #<====
			categories = line.split(delimiter)
			#print(categories) #<====
			if len(categories) == len(first_line_items):
				for category_idx, category_item in enumerate(categories):
					categories[category_idx] = string_to_type(category_item)
				out.append(categories)
			elif len(categories) != len(first_line_items):
				odd_data.append(line)

	if out_type == 'columns':
		#pre-allocate
		#create enough lists to hold each column of data
		out = [[] for x in range(len(first_line_items))]

		for idx, line in enumerate(data):
			#print(line) #<=============
			categories = line.split(delimiter)
			#if each column contains an item, thus no missing element (might be all ' ' empties)
			if len(categories) == len(first_line_items):
				line = []
				for category_idx, categories in enumerate(categories):
					out[category_idx].append(string_to_type(categories))		
			elif len(categories) != len(first_line_items):
				odd_data.append(line)

	if out_type == 'pandas_Series':
		import pandas as pd 
		import numpy as np 
		params['out_type'] = 'dict_columns'
		temp = delmited_text_arranger(**params)
		out = pd.DataFrame(temp)
		#passing in s dict does not seem to be working
		"""
		if headers == False and user_def_headers == None:
			temp = delmited_text_arranger(data, delimiter,  out_type = 'dict_columns', headers = False, user_def_headers = None, reports = True)		
		elif headers == False and user_def_headers != None:
		elif headers == True:
		"""

		#if user_def_headers != None:
			#out = pd.Series(temp, index=user_def_headers)
		#elif user_def_headers == None:
			#out = pd.Series(temp)


	if out_type == 'matrix':
		#pre-allocate matrix
		out = []
		for idx, line in enumerate(data):
			categories = line.split(delimiter)
			if len(categories) == len(first_line_items):
				out.append([[] for c in range(len(first_line_items))])
				for category_idx, categories in enumerate(categories):
					out[idx][category_idx] = string_to_type(categories)
			elif len(categories) != len(first_line_items):
				odd_data.append(line)

	if out_type == 'dict_list_rows':
		out = []
		#define field names for list of dicts
		if headers == False and user_def_headers == None:
			attributes = [str(column_idx) for column_idx in range(len(first_line_items))]
		elif headers == False and user_def_headers != None:
			attributes = user_def_headers		
		elif headers == True:
			attributes = first_line_items
		for idx, line in enumerate(data):
			categories = line.split(delimiter)
			if len(categories) == len(first_line_items):
				obj = dict()
				for cat_idx, categories in enumerate(categories):
					obj[attributes[cat_idx]] = string_to_type(categories)
				obj['id'] = idx
				out.append(obj)	
			elif len(categories) != len(first_line_items):
				odd_data.append(line)

	if out_type == 'dict_columns':#<==========================
		out = {}
		params['out_type'] = 'columns'
		temp = delmited_text_arranger(**params)
		#temp = delmited_text_arranger(data, delimiter,  out_type = 'columns')
		if headers == False and user_def_headers == None:
			for idx in range(len(first_line_items)):
				out[str(idx)] = temp[idx]
		elif headers == False and user_def_headers != None:
			for idx, header in enumerate(user_def_headers):
				out[str(header)] = temp[idx]
		elif headers == True:
			for idx, header in enumerate(first_line_items):
				out[str(header)] = temp[idx]		
	return out


def list_to_dict_list_rows(data, user_def_headers = None):
	#where data is a list of lists
	out = []
	first_line_items = data[0]
	if user_def_headers == None:
		attributes = [str(column_idx) for column_idx in range(len(first_line_items))]
	elif user_def_headers != None:
		attributes = user_def_headers
	#as key for each line of data
	id = 0		
	for idx, line in enumerate(data):
		if len(line) == len(first_line_items):
			obj = dict()
			for item_idx, item in enumerate(line):
				obj[attributes[item_idx]] = item
			obj['id'] = idx	
			out.append(obj)	
		elif len(line) != len(first_line_items):
			odd_data.append(line)

	return out


#number of dimensions depends on number of feature you want to plot against. 
#There is only ONE label, but you can create a new label from 2 other lables and combine them. Then add them to the data.
#This will serve as a new label scheme, which you can then plot
#for item in data: if..something...item['new_key'] = value
def plot_dict_list(data, label, features):
	import matplotlib.pyplot as plt
	from pandas import DataFrame, Series
	num_features = len(features)
	unique_sub_labels = unique_order_preserved([line[label] for line in data])

	#if only one feature, use a histogram
	if num_features == 1:	
		#we leave as a list and convert to tuple later as tuple is immutable
		filtered_data_tuple = []
		maxi = 0.0
		mini = 0.0
		for unique_sub_label in unique_sub_labels:
			#should only be one feature here, but allows input as [features] rather than 'features'
			for feature in features:
				filtered_data = [line[feature] for line in data if line[label] == unique_sub_label]
				filtered_data_tuple.append(filtered_data)
				if all( is_num(item) is True for item in filtered_data ):
					print(filtered_data)
					temp_max = max(filtered_data)
					temp_min = min(filtered_data)
					if temp_max > maxi:
						maxi = temp_max
					if temp_min < mini:
						mini = temp_min
					common_params = dict(bins=50, range=(mini, maxi), normed=1)
				elif all( isinstance(item, string_types) is True for item in filtered_data ):
					pass


					#common_params = dict(bins=50, range=(mini, maxi), normed=True)

		filtered_data_tuple = tuple(filtered_data_tuple)	
		plt.hist(filtered_data_tuple, **common_params)
		plt.xlabel(*features)
		plt.ylabel('Count')
		plt.legend(tuple(unique_sub_labels), loc='upper right')
		plt.grid(True)
		plt.show()



	#if more than one feature, use a scatter
	if num_features >= 2:	
		pass # implement later







