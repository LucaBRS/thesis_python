from cmath import log, log10, pi, sqrt
from distutils.log import error
from itertools import permutations
from math import ceil
from msilib.schema import Error
import numpy as np



SNR_limit = [("SF7", -7.5), ("SF8", -10), ("SF9", -12.5),
                 ("SF10", -15), ("SF11", -17.5), ("SF12", -20)]
BW = 125*10**3  # in kHz
NF = 6  # dipende dal dispositivo in uso (hardwere)
SF = [7,8,9,10,11,12]

def _time_on_air(i):
    PL = 8 # payload in byte
    CRC = 1 # used to determine if all the byte are recived correctly "Cyclic Redundancy Ceck" (for LoRa defoult CRC = 1)
    H = 1 # header, explicit H=0; implicit H=1

    DE = 1 # low data rate optimize, enabled: DE=1
    CR = [1,2,3,4] # Coding Rate, defoult is CR = 1
    CR = 1

    sf=SF[i]
    T_s = 2**sf / BW # Symbol Time
    T_payload = ( T_s*(8 + np.maximum(   ceil(((8*PL - 4*sf +28 + 16*CRC -20*H)/(4*(sf - 2*DE)))*(CR +4))  ,0 )) )

    return T_payload

def _sensibility_calculation():
    S = []
    for snr in SNR_limit:
        S.append(
            (snr[0], np.round((-144 + 10*log10(BW) + NF + snr[1]).real, 3)))

    return S


# calcolo della distanza tramite coordinate
def distanza(lat1, long1, lat2, long2):

    dist = 100*0.9996*sqrt(pow((lat1-lat2), 2)+pow((long1-long2), 2))
    return dist.real

# calcolo distanza con formula Heversine


def testHevers(lat1, long1, lat2, long2):
    r = 6371
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    delta_phi = np.radians(lat2 - lat1)
    delta_lambda = np.radians(long2 - long1)
    a = np.sin(delta_phi / 2)**2 + np.cos(phi1) * \
        np.cos(phi2) * np.sin(delta_lambda / 2)**2
    res = r * (2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)))

    return np.round(res.real, 3)


# calcolo della potenza ricevuta tramite FreeSpaceLoss
def potRic(potTra, Gtx, Grx, dist, freq, lossType):
    c = 299792458
    potRic = 0
    loss = 0

    if lossType == "FS":
        loss = 20*log10((4*pi*dist*10**3)/((c)/(freq*10**6)))
    else:
        loss = lossHata(freq, 10, 0.5, dist)

    potRic = potTra + Gtx + Grx - loss

    return np.round(potRic.real, 3)


def lossHata(freq, hConc, hCont, distanza):
    loss = 0

    # OKOMURA_HATA per piccole/medie città
    C_h = 0.8 + (1.1*log10(freq)-0.7)*hCont - 1.56*log10(freq)

    loss = 69.55 + 26.16*log10(freq) - 13.82*log(hConc) - \
        C_h + (44.9 - 6.55*log10(hConc))*log10(distanza)

    return loss

    # calcolo copertuira del singolo contatore! accetta come argomento la lista dei contatori


def coverage(meters):
    sensibilities = []
    sensibilities = _sensibility_calculation()
    dic = {"freeSpace": {},
           "hata": {"%_tot":{}
                    }
           }
    fs_counter = 0
    hata_counter = 0

    for sensibility in sensibilities:
        fs_counter = 0
        hata_counter = 0
        for meter in meters:
            if meter["recPow"]["freeSpace"] > sensibility[1]:
                fs_counter += 1
            if meter["recPow"]["hata"] > sensibility[1]:
                hata_counter += 1

            # esprimo la copertura in percentuale
        dic["freeSpace"][sensibility[0]] = np.round(
            (fs_counter/len(meters))*100.2)
        dic["hata"]["%_tot"][sensibility[0]] = np.round(
            (hata_counter/len(meters))*100, 2)

    return dic


# questo dovrebbe comparare i concentratori a due a due e ritornare la percetuale di copertura di entrambi...
def double_coverage(meters1, meters2):
    sensibilities = []
    sensibilities = _sensibility_calculation()
    dic = {"freeSpace": {},
           "hata": {"%_tot":{},
                    "#_meters_optimizzation_sf":{},
                    "avg_optimize_ToA":0
                    }}
    fs_counter = 0
    hata_counter = 0
    previous_sf_meters = 0
    sf_counter=0
    if(len(meters1) != len(meters2)):
        print("problema con i meters qualcosa non coincide con lunghezza")
        return Error

    for sensibility in sensibilities:
        fs_counter = 0
        hata_counter = 0

        for i in range(len(meters1)):
            if(meters1[i]["id"] != meters2[i]["id"]):
                print("meters non in ordine crescente")
                return error
            else:
                if (meters1[i]["recPow"]["freeSpace"] > sensibility[1] and meters2[i]["recPow"]["freeSpace"] > sensibility[1]):
                    fs_counter += 1
                elif (meters1[i]["recPow"]["freeSpace"] > sensibility[1] and meters2[i]["recPow"]["freeSpace"] < sensibility[1]):
                    fs_counter += 1
                elif (meters1[i]["recPow"]["freeSpace"] < sensibility[1] and meters2[i]["recPow"]["freeSpace"] > sensibility[1]):
                    fs_counter += 1

                if (meters1[i]["recPow"]["hata"] > sensibility[1] and meters2[i]["recPow"]["hata"] > sensibility[1]):
                    hata_counter += 1
                elif (meters1[i]["recPow"]["hata"] > sensibility[1] and meters2[i]["recPow"]["hata"] < sensibility[1]):
                    hata_counter += 1
                elif (meters1[i]["recPow"]["hata"] < sensibility[1] and meters2[i]["recPow"]["hata"] > sensibility[1]):
                    hata_counter += 1

        dic["freeSpace"][sensibility[0]] = np.round(
            (fs_counter/len(meters1))*100.2)

        dic["hata"]["%_tot"][sensibility[0]] = np.round(
            (hata_counter/len(meters1))*100, 2)

        dic["hata"]["#_meters_optimizzation_sf"][sensibility[0]] = hata_counter - previous_sf_meters
        previous_sf_meters = hata_counter

        dic["hata"]["avg_optimize_ToA"] = (dic["hata"]["avg_optimize_ToA"] + dic["hata"]["#_meters_optimizzation_sf"][sensibility[0]] * _time_on_air(sf_counter))

        if i == len(meters1)-1:
            dic["hata"]["avg_optimize_ToA"] = np.round( dic["hata"]["avg_optimize_ToA"] / hata_counter , 3 )
        sf_counter +=1
    return dic




    ## thease code does a simple combination between elemnt
def simple_combination(list):
    print(len(list))
    permutation = []

    for site1 in list:
        for site2 in list:
            if site1 != site2:
                if (not((site1, site2) in permutation) and not((site2, site1) in permutation)):
                    permutation.append((site1, site2))
    print(len(permutation))
    return permutation


    ## thiease are the "filan consideration" between each SF of lora and the coverage between two different couple of DC
def consideration_two_configuarition(firstConfig, config1, secondConfig, config2):
    difference = 0
    stringa = firstConfig + " and " + secondConfig + "we have: \n"
    for i in range(6):
        difference =( 100*(config1["coverage"]["hata"]["%_tot"]["SF"+str(7+i)]-config2["coverage"]["hata"]["%_tot"]["SF"+str(7+i)])/
                    ( (config1["coverage"]["hata"]["%_tot"]["SF"+str(7+i)]+config2["coverage"]["hata"]["%_tot"]["SF"+str(7+i)])/2 ) )
        difference =  np.round(difference,2)

        if (config1["coverage"]["hata"]["%_tot"]["SF"+str(7+i)] > config2["coverage"]["hata"]["%_tot"]["SF"+str(7+i)]):
            stringa = stringa +"in the SF"+str(7+i)+" LoRa configuration there is a gain of: "+ str(abs(difference)) + "% \n"
        else:
            stringa = stringa +"in the SF"+str(7+i)+" LoRa configuration there is a loss of: "+ str(abs(difference)) + "% \n"
    return stringa