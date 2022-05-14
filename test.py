from cmath import log, log10, pi, sqrt
import numpy as np


BW = 125*10**3 # in kHz
NF = 6 # dipende dal dispositivo in uso (hardwere)
SNR_limit = [("SF7",-7.5),("SF8",-10),("SF9",-12.5),("SF10",-15),("SF11",-17.5),("SF12",-20)]
S = []
for snr in SNR_limit:
    S.append( (snr[0],np.round( (-144 + 10*log10(BW) + NF + snr[1]).real , 3 ) ) )

print(S)