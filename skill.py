import numpy as np
v = np.array([4.2, 8.4, 9.8, 11.2, 12.6, 14, 15.4, 16.8, 18.2, 19.6, 21])
x = np.array([1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
p = np.polyfit(x, v, 1)
print(p)
