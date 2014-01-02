from helpers import list_to_dict_list, is_num
import matplotlib.pyplot as plt
import numpy as np
from pandas import*

#p =list_to_dict_list(list_of_lists, user_def_headers = header)
#print(p)
#print(np.random.rand(10, 4))

"""
ts = Series(np.random.randn(1000), index=date_range('1/1/2000', periods=1000))
ts = ts.cumsum()
ts.plot(style='k--', label='Series')
plt.legend()
plt.show()
"""
"""
ts = Series(np.random.randn(1000), index=date_range('1/1/2000', periods=1000))
df = DataFrame(np.random.randn(1000, 4), index=ts.index, columns=list('ABCD'))
df = df.cumsum()
df.plot(); plt.legend(loc='best')
plt.show()
"""
ts = Series(np.random.randn(1000), index=date_range('1/1/2000', periods=1000))
df = DataFrame(np.random.randn(1000, 4), index=ts.index, columns=list('ABCD'))
print(ts.index)
plt.figure();
df.ix[5].plot(kind='bar'); plt.axhline(0, color='k')
print(df.ix[0])
plt.show()
