from cProfile import label
from cmath import log, log10, pi, sqrt
from turtle import color
import numpy as np
import matplotlib.pyplot as plt
import json

from utils.finding import finding

with open('./risultati/findings.json') as file:
    findings = json.load(file)

choice2irg = findings['choice2irg']

sf_name=[]
arr2i= np.zeros((5,6))
arrBC=np.zeros((5,6))
arr_min=np.zeros((5,6))
arr_max=np.zeros((5,6))
for i in range(6):
    sf_name.append("SF"+str(7+i))
    
    arr2i[0][i] = (choice2irg['coverage']['hata_medium']['%_tot']['SF'+str(7+i)])
    arrBC[0][i] = (findings['hata_medium']['bestCoverage_hata_medium']['%_tot']['SF'+str(7+i)])
    arr_min[0][i] = (findings['hata_medium']['min_toa_hata_medium']['%_tot']['SF'+str(7+i)])
    arr_max[0][i] = (findings['hata_medium']['max_toa_hata_medium']['%_tot']['SF'+str(7+i)])

    arr2i[1][i] = (choice2irg['coverage']['hata_big']['%_tot']['SF'+str(7+i)])
    arrBC[1][i] = (findings['hata_big']['bestCoverage_hata_big']['%_tot']['SF'+str(7+i)])
    arr_min[1][i] = (findings['hata_big']['min_toa_hata_big']['%_tot']['SF'+str(7+i)])
    arr_max[1][i] = (findings['hata_big']['max_toa_hata_big']['%_tot']['SF'+str(7+i)])

    arr2i[2][i] = (choice2irg['coverage']['SUI_medium']['%_tot']['SF'+str(7+i)])
    arrBC[2][i] = (findings['SUI_medium']['bestCoverage_SUI_medium']['%_tot']['SF'+str(7+i)])
    arr_min[2][i] = (findings['SUI_medium']['min_toa_SUI_medium']['%_tot']['SF'+str(7+i)])
    arr_max[2][i] = (findings['SUI_medium']['max_toa_SUI_medium']['%_tot']['SF'+str(7+i)])
    
    arr2i[3][i] = (choice2irg['coverage']['SUI_big']['%_tot']['SF'+str(7+i)])
    arrBC[3][i] = (findings['SUI_big']['bestCoverage_SUI_big']['%_tot']['SF'+str(7+i)])
    arr_min[3][i] = (findings['SUI_big']['min_toa_SUI_big']['%_tot']['SF'+str(7+i)])
    arr_max[3][i] = (findings['SUI_big']['max_toa_SUI_big']['%_tot']['SF'+str(7+i)])
    
    arr2i[4][i] = (choice2irg['coverage']['ericsson']['%_tot']['SF'+str(7+i)])
    arrBC[4][i] = (findings['ericsson']['bestCoverage_ericsson']['%_tot']['SF'+str(7+i)])
    arr_min[4][i] = (findings['ericsson']['min_toa_ericsson']['%_tot']['SF'+str(7+i)])
    arr_max[4][i] = (findings['ericsson']['max_toa_ericsson']['%_tot']['SF'+str(7+i)])
    
    
largbar = 0.25   
X = np.arange(6)
 
   
plt.subplot(2,3,1)

plt.title('HATA MEDIUM')
plt.bar(X ,              arr2i[0],  width=largbar,color='y',label="2irg")
plt.bar(X + largbar,     arrBC[0],  width=largbar,color='b',label="BC")
plt.bar(X + largbar*2,   arr_min[0],width=largbar,color='g',label="min")
plt.bar(X + largbar*3,   arr_max[0],width=largbar,color='r',label="Max")

plt.xticks([(r+ largbar + largbar/2) for r in range(len(arr2i[0]))],sf_name)
plt.legend()


plt.subplot(2,3,2)

plt.title('HATA BIG')
plt.bar(X ,              arr2i[1],  width=largbar,color='y',label="2irg")
plt.bar(X + largbar,     arrBC[1],  width=largbar,color='b',label="BC")
plt.bar(X + largbar*2,   arr_min[1],width=largbar,color='g',label="min")
plt.bar(X + largbar*3,   arr_max[1],width=largbar,color='r',label="Max")

plt.xticks([(r+ largbar + largbar/2) for r in range(len(arr2i[0]))],sf_name)
plt.legend()


plt.subplot(2,3,3)

plt.title('SUI MEDIUM')
plt.bar(X ,              arr2i[2],  width=largbar,color='y',label="2irg")
plt.bar(X + largbar,     arrBC[2],  width=largbar,color='b',label="BC")
plt.bar(X + largbar*2,   arr_min[2],width=largbar,color='g',label="min")
plt.bar(X + largbar*3,   arr_max[2],width=largbar,color='r',label="Max")

plt.xticks([(r+ largbar + largbar/2) for r in range(len(arr2i[0]))],sf_name)
plt.legend()


plt.subplot(2,3,4)

plt.title('SUI BIG')
plt.bar(X ,              arr2i[3],  width=largbar,color='y',label="2irg")
plt.bar(X + largbar,     arrBC[3],  width=largbar,color='b',label="BC")
plt.bar(X + largbar*2,   arr_min[3],width=largbar,color='g',label="min")
plt.bar(X + largbar*3,   arr_max[3],width=largbar,color='r',label="Max")

plt.xticks([(r+ largbar + largbar/2) for r in range(len(arr2i[0]))],sf_name)
plt.legend()


plt.subplot(2,3,5)

plt.title('ERICSSON')
plt.bar(X ,              arr2i[4],  width=largbar,color='y',label="2irg")
plt.bar(X + largbar,     arrBC[4],  width=largbar,color='b',label="BC")
plt.bar(X + largbar*2,   arr_min[4],width=largbar,color='g',label="min")
plt.bar(X + largbar*3,   arr_max[4],width=largbar,color='r',label="Max")

plt.xticks([(r+ largbar + largbar/2) for r in range(len(arr2i[0]))],sf_name)
plt.legend()


plt.show()