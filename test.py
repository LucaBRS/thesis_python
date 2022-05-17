from cmath import log, log10, pi, sqrt
import numpy as np
from math import ceil

BW = 125*10**3  # in kHz
NF = 6  # dipende dal dispositivo in uso (hardwere)
SF = [7,8,9,10,11,12]

PL = 16 # payload in byte
CRC = 1 # used to determine if all the byte are recived correctly "Cyclic Redundancy Ceck" (for LoRa defoult CRC = 1)
H = 1 # header, explicit H=0; implicit H=1

DE = 1 # low data rate optimize, enabled: DE=1 
CR = [1,2,3,4] # Coding Rate, defoult is CR = 1
CR = 1

T_payload = []

for sf in SF:
    print(sf)
    T_s = 2**sf / BW # Symbol Time
    T_payload.append( T_s*(8 + np.maximum(   ceil(((8*PL - 4*sf +28 + 16*CRC -20*H)/(4*(sf - 2*DE)))*(CR +4))  ,0 )) )
    
print(T_payload)