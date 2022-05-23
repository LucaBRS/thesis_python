from cProfile import label
from cmath import log, log10, pi, sqrt
from turtle import color
import numpy as np
import matplotlib.pyplot as plt


choice2irg = {'id': 69, 'id_dc_1': '61490730150009', 'id_dc_2': '61490730150016',
            'coverage': {'freeSpace': {'SF7': 100.0, 'SF8': 100.0, 'SF9': 100.0, 'SF10': 100.0, 'SF11': 100.0, 'SF12': 100.0},
                         'hata': {'%_tot': {'SF7': 42.46, 'SF8': 54.31, 'SF9': 64.82, 'SF10': 73.95, 'SF11': 81.31, 'SF12': 88.69},
                                  '#_meters_optimizzation_sf': {'SF7': 2049, 'SF8': 572, 'SF9': 507, 'SF10': 441, 'SF11': 355, 'SF12': 356},
                                  'avg_optimize_ToA': 0.035}}}
bestCoverage = {'id': 65, 'id_dc_1': '61490730150009', 'id_dc_2': '61490730150012',
            'coverage': {'freeSpace': {'SF7': 100.0, 'SF8': 100.0, 'SF9': 100.0, 'SF10': 100.0, 'SF11': 100.0, 'SF12': 100.0},
                         'hata': {'%_tot': {'SF7': 30.44, 'SF8': 44.53, 'SF9': 59.16, 'SF10': 75.07, 'SF11': 86.26, 'SF12': 92.35},
                                  '#_meters_optimizzation_sf': {'SF7': 1469, 'SF8': 680, 'SF9': 706, 'SF10': 768, 'SF11': 540, 'SF12': 294},
                                  'avg_optimize_ToA': 0.028}}}
couple_min = {'id': 38, 'id_dc_1': '61490730150005', 'id_dc_2': '61490730150009',
            'coverage': {'freeSpace': {'SF7': 100.0, 'SF8': 100.0, 'SF9': 100.0, 'SF10': 100.0, 'SF11': 100.0, 'SF12': 100.0},
                         'hata': {'%_tot': {'SF7': 48.84, 'SF8': 61.75, 'SF9': 72.32, 'SF10': 80.07, 'SF11': 85.33, 'SF12': 88.69},
                                  '#_meters_optimizzation_sf': {'SF7': 2357, 'SF8': 623, 'SF9': 510, 'SF10': 374, 'SF11': 254, 'SF12': 162},
                                  'avg_optimize_ToA': 0.016}}}
couple_max = {'id': 79, 'id_dc_1': '61490730150011', 'id_dc_2': '61490730150015',
            'coverage': {'freeSpace': {'SF7': 100.0, 'SF8': 100.0, 'SF9': 100.0, 'SF10': 100.0, 'SF11': 100.0, 'SF12': 100.0},
                         'hata': {'%_tot': {'SF7': 14.07, 'SF8': 18.73, 'SF9': 25.63, 'SF10': 34.5, 'SF11': 45.65, 'SF12': 61.75},
                                  '#_meters_optimizzation_sf': {'SF7': 679, 'SF8': 225, 'SF9': 333, 'SF10': 428, 'SF11': 538, 'SF12': 777},
                                  'avg_optimize_ToA': 0.111}}}

fig = plt.subplots(figsize =(12, 8))

sf_name=[]
arr2i=[]
arrBC=[]
arr_min=[]
arr_max=[]
for i in range(6):
    sf_name.append("SF"+str(7+i))
    arr2i.append(choice2irg['coverage']['hata']['%_tot']['SF'+str(7+i)])
    arrBC.append(bestCoverage['coverage']['hata']['%_tot']['SF'+str(7+i)])
    arr_min.append(couple_min['coverage']['hata']['%_tot']['SF'+str(7+i)])
    arr_max.append(couple_max['coverage']['hata']['%_tot']['SF'+str(7+i)])
sf_name = np.array(sf_name)
arr2i = np.array(arr2i)
arrBC = np.array(arrBC)
arr_min = np.array(arr_min)
arr_max = np.array(arr_max)

largbar = 0.25
point2ir = np.arange(len(arr2i))
pointBC = [(x + largbar) for x in point2ir]
point_min = [(x+largbar) for x in pointBC ]
point_max = [(x + largbar) for x in point_min]

plt.bar(point2ir,arr2i,width=largbar,color='y',label="2irg")
plt.bar(pointBC,arrBC,width=largbar,color='b',label="BC")
plt.bar(point_min,arr_min,width=largbar,color='g',label="min")
plt.bar(point_max,arr_max,width=largbar,color='r',label="Max")
plt.ylabel('Coverage [%]')
plt.xticks([(r+ largbar + largbar/2) for r in range(len(arr2i))],sf_name)

plt.legend()
plt.show()