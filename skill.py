import numpy as np

v = np.array([
  [1, 454],
  [2, 500],
  [3, 546],
  [4, 592],
  [5, 638],
  [6, 684],
  [7, 730],
  [8, 776], 
  [9, 823], #
  [10, 869],
  [11, 915],
  [12, 961],
  [13, 1007],
  [14, 1053],
  [15, 1099],
  [16, 1145],
  [17, 1191],
  [18, 1237],
  [19, 1283],
  [20, 1329],
  [21, 1376], #
  [22, 1422],
  [23, 1468],
  [24, 1514],
  [25, 1560],
  [26, 1606],
  [27, 1652],
  [28, 1698],
  [29, 1744],
  [30, 1790],
  [31, 1836],
  [32, 1883], #
]).transpose()

p = np.polyfit(v[0], v[1], 1)
print(p)