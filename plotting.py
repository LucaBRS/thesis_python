from cProfile import label
from cmath import log, log10, pi, sqrt
from turtle import color
import numpy as np
import matplotlib.pyplot as plt
import json


with open('./risultati/findings.json') as file:
    findings = json.load(file)

choice2irg = findings['choice2irg']

sf_name=[]
arr2i= np.zeros((5,6))
arrBC=np.zeros((5,6))
arr_min=np.zeros((5,6))
# arr_max=np.zeros((5,6))
for i in range(6):
    sf_name.append("SF"+str(7+i))

    arr2i[0][i] = (choice2irg['coverage']['hata_medium']['%_tot']['SF'+str(7+i)])
    arrBC[0][i] = (findings['hata_medium']['bestCoverage_hata_medium']['%_tot']['SF'+str(7+i)])
    arr_min[0][i] = (findings['hata_medium']['min_toa_hata_medium']['%_tot']['SF'+str(7+i)])
  # arr_max[0][i] = (findings['hata_medium']['max_toa_hata_medium']['%_tot']['SF'+str(7+i)])

    arr2i[1][i] = (choice2irg['coverage']['hata_big']['%_tot']['SF'+str(7+i)])
    arrBC[1][i] = (findings['hata_big']['bestCoverage_hata_big']['%_tot']['SF'+str(7+i)])
    arr_min[1][i] = (findings['hata_big']['min_toa_hata_big']['%_tot']['SF'+str(7+i)])
   # arr_max[1][i] = (findings['hata_big']['max_toa_hata_big']['%_tot']['SF'+str(7+i)])

    arr2i[2][i] = (choice2irg['coverage']['SUI_medium']['%_tot']['SF'+str(7+i)])
    arrBC[2][i] = (findings['SUI_medium']['bestCoverage_SUI_medium']['%_tot']['SF'+str(7+i)])
    arr_min[2][i] = (findings['SUI_medium']['min_toa_SUI_medium']['%_tot']['SF'+str(7+i)])
   # arr_max[2][i] = (findings['SUI_medium']['max_toa_SUI_medium']['%_tot']['SF'+str(7+i)])

    arr2i[3][i] = (choice2irg['coverage']['SUI_big']['%_tot']['SF'+str(7+i)])
    arrBC[3][i] = (findings['SUI_big']['bestCoverage_SUI_big']['%_tot']['SF'+str(7+i)])
    arr_min[3][i] = (findings['SUI_big']['min_toa_SUI_big']['%_tot']['SF'+str(7+i)])
   # arr_max[3][i] = (findings['SUI_big']['max_toa_SUI_big']['%_tot']['SF'+str(7+i)])

    arr2i[4][i] = (choice2irg['coverage']['ericsson']['%_tot']['SF'+str(7+i)])
    arrBC[4][i] = (findings['ericsson']['bestCoverage_ericsson']['%_tot']['SF'+str(7+i)])
    arr_min[4][i] = (findings['ericsson']['min_toa_ericsson']['%_tot']['SF'+str(7+i)])
  #  arr_max[4][i] = (findings['ericsson']['max_toa_ericsson']['%_tot']['SF'+str(7+i)])


largbar = 0.26
X = np.arange(6)

########################
## COVERAGE #########
########################

plt.figure()

plt.title('HATA MEDIUM')
plt.bar(X ,              arr2i[0],  width=largbar,color='y',label="Choice 2iReteGas")
plt.bar(X + largbar,     arrBC[0],  width=largbar,color='b',label="Best Coverage Couple")
plt.bar(X + largbar*2,   arr_min[0],width=largbar,color='g',label="Minimum ToA Couple")
# plt.bar(X + largbar*3,   arr_max[0],width=largbar,color='r',label="Max")
plt.yticks(np.arange(stop=110,step=10))
plt.xticks([(r+ largbar ) for r in range(len(arr2i[0]))],sf_name)
plt.ylabel('Coverage %')
plt.xlabel('Spreding Factor')
plt.legend()


plt.figure()

plt.title('HATA BIG')
plt.bar(X ,              arr2i[1],  width=largbar,color='y',label="Choice 2iReteGas")
plt.bar(X + largbar,     arrBC[1],  width=largbar,color='b',label="Best Coverage Couple")
plt.bar(X + largbar*2,   arr_min[1],width=largbar,color='g',label="Minimum ToA Couple")
# plt.bar(X + largbar*3,   arr_max[1],width=largbar,color='r',label="Max")
plt.yticks(np.arange(stop=110,step=10))
plt.xticks([(r+ largbar ) for r in range(len(arr2i[0]))],sf_name)
plt.ylabel('Coverage %')
plt.xlabel('Spreding Factor')
plt.legend()


# plt.figure()

# plt.title('SUI MEDIUM')
# plt.bar(X ,              arr2i[2],  width=largbar,color='y',label="2irg")
# plt.bar(X + largbar,     arrBC[2],  width=largbar,color='b',label="BC")
# plt.bar(X + largbar*2,   arr_min[2],width=largbar,color='g',label="min")
# # plt.bar(X + largbar*3,   arr_max[2],width=largbar,color='r',label="Max")
# plt.yticks(np.arange(stop=110,step=10))
# plt.xticks([(r+ largbar + largbar/2) for r in range(len(arr2i[0]))],sf_name)
# plt.ylabel('Coverage')
# plt.xlabel('Spreding Factor')
# plt.legend()


# plt.figure()

# plt.title('SUI BIG')
# plt.bar(X ,              arr2i[3],  width=largbar,color='y',label="2irg")
# plt.bar(X + largbar,     arrBC[3],  width=largbar,color='b',label="BC")
# plt.bar(X + largbar*2,   arr_min[3],width=largbar,color='g',label="min")
# # plt.bar(X + largbar*3,   arr_max[3],width=largbar,color='r',label="Max")
# plt.yticks(np.arange(stop=110,step=10))
# plt.xticks([(r+ largbar + largbar/2) for r in range(len(arr2i[0]))],sf_name)
# plt.ylabel('Coverage')
# plt.xlabel('Spreding Factor')
# plt.legend()


plt.figure()

plt.title('ERICSSON')
plt.bar(X ,              arr2i[4],  width=largbar,color='y',label="Choice 2iReteGas")
plt.bar(X + largbar,     arrBC[4],  width=largbar,color='b',label="Best Coverage Couple")
plt.bar(X + largbar*2,   arr_min[4],width=largbar,color='g',label="Minimum ToA Couple")
# plt.bar(X + largbar*3,   arr_max[4],width=largbar,color='r',label="Max")
plt.yticks(np.arange(stop=110,step=10))
plt.xticks([(r + largbar ) for r in range(len(arr2i[0]))],sf_name)
plt.ylabel('Coverage %')
plt.xlabel('Spreding Factor')
plt.legend()


################
## ToA ######
################
delay_name = ['Hata medium','Hata big','Ericsson']

ToA_2i = np.zeros((3))
ToA_BC = np.zeros((3))
ToA_min = np.zeros((3))

X = np.arange(3)

ToA_2i[0] = (choice2irg['coverage']['hata_medium']['avg_optimize_ToA'])
ToA_BC[0] = (findings['hata_medium']['bestCoverage_hata_medium']['avg_optimize_ToA'])
ToA_min[0] = (findings['hata_medium']['min_toa_hata_medium']['avg_optimize_ToA'])

ToA_2i[1]= (choice2irg['coverage']['hata_big']['avg_optimize_ToA'])
ToA_BC[1] = (findings['hata_big']['bestCoverage_hata_big']['avg_optimize_ToA'])
ToA_min[1]= (findings['hata_big']['min_toa_hata_big']['avg_optimize_ToA'])

ToA_2i[2] = (choice2irg['coverage']['ericsson']['avg_optimize_ToA'])
ToA_BC[2] = (findings['ericsson']['bestCoverage_ericsson']['avg_optimize_ToA'])
ToA_min[2] = (findings['ericsson']['min_toa_ericsson']['avg_optimize_ToA'])

plt.figure()

plt.title('ToA Comparison')
plt.bar(X ,              ToA_2i,  width=largbar,color='y',label="Choice 2iReteGas")
plt.bar(X + largbar,     ToA_BC,  width=largbar,color='b',label="Best Coverage Couple")
plt.bar(X + largbar*2,   ToA_min,width=largbar,color='g',label="Minimum ToA Couple")
plt.xticks([(r + largbar ) for r in range(len(ToA_2i))],delay_name)
plt.legend()
plt.ylabel('Avarage ToA (sec)')
plt.xlabel('Loss Type')


##########################################################################################
##########################################################################################

with open('./risultati/distance_power.json') as file:
    distance_power = json.load(file)

x = np.zeros((7,len(distance_power[0]['meters'])))


index = 0
for meter in distance_power[0]['meters']:

    x[0][index] = meter["ditance(Km)"]
    x[1][index] = meter["recPow"]["freeSpace"]
    x[2][index] = meter["recPow"]["hata_medium"]
    x[3][index] = meter["recPow"]["hata_big"]
    x[4][index] = meter["recPow"]["SUI_medium"]
    x[5][index] = meter["recPow"]["SUI_big"]
    x[6][index] = meter["recPow"]["ericsson"]
    index +=1

plt.figure()
plt.title("Recived Power")
plt.plot(x[0][:],x[1][:],'r', x[0][:],x[2][:],'g', x[0][:],x[3][:],'g--', x[0][:],x[4][:],'b', x[0][:],x[5][:],'b--' , x[0][:],x[6][:],'black' )
plt.ylabel('Decibiel')
plt.xlabel('Distance (km)')
plt.legend(['FreeSpace','Hata (medium)','Hata (big)','SUI (medium)','SUI (big)','Ericsson'])
plt.show()