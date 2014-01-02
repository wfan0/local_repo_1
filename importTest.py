import numpy


norm_array = [1,2,3,4,5]
numpy_array = numpy.array(norm_array)
print("normal" + " " + str(numpy_array))

greater_than_2 = numpy_array >2
print(greater_than_2)

c = norm_array.copy()
c [1] = "poop"
print(c)
print(norm_array)

#-------------------
num_array = numpy.array([1,2,3,4,5,numpy.NAN,7])
print(num_array)


num_array = numpy.isnan(num_array) #filter out nan's
print(num_array)
print(numpy.where(numpy.logical_and(num_array >= 2, num_array <= 4)))

