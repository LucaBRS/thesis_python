from cmath import isnan, log, log10, pi, sqrt
from distutils.log import error
from itertools import permutations
from math import ceil, dist
from msilib.schema import Error
import numpy as np
import utils.losses as los


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

    n_preamble = 8
    T_preamble = (n_preamble + 4.25)*T_s

    ToA = T_preamble + T_payload

    return ToA

def _sensibility_calculation():
    S = []
    for snr in SNR_limit:
        S.append(
            (snr[0], np.round((-144 + 10*log10(BW) + NF + snr[1]).real, 3)))

    return S


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
    elif lossType == "HATA_MEDIUM":
        loss = los.loss_hata_medium(freq, 15, 1.5, dist)
    elif lossType == "HATA_BIG":
        loss  = los.loss_hata_big(freq, 15, 1.5, dist)
    elif lossType == "SUI_MEDIUM":
        loss  = los.loss_SUI_medium(freq, 15, 1.5, dist)
    elif lossType == "SUI_BIG":
        loss  = los.loss_SUI_big(freq, 15, 1.5, dist)
    elif lossType == "ERICSSON":
        loss  = los.loss_ericsson(freq, 15, 1.5, dist)
    elif lossType == "ERICSSON MEDIUM":
        loss  = los.loss_ericsson_medium(freq, 15, 1.5, dist)
    potRic = potTra + Gtx + Grx - loss

    return np.round(potRic.real, 3)


    # calcolo copertuira del singolo contatore! accetta come argomento la lista dei contatori
def coverage(meters):
    sensibilities = []
    sensibilities = _sensibility_calculation()
    dic = {"freeSpace": {},
           "hata_medium": {"%_tot":{}
                    }
           }
    fs_counter = 0
    hata_medium_counter = 0

    for sensibility in sensibilities:
        fs_counter = 0
        hata_medium_counter = 0
        for meter in meters:
            if meter["recPow"]["freeSpace"] > sensibility[1]:
                fs_counter += 1
            if meter["recPow"]["hata_medium"] > sensibility[1]:
                hata_medium_counter += 1

            # esprimo la copertura in percentuale
        dic["freeSpace"][sensibility[0]] = np.round(
            (fs_counter/len(meters))*100.2)
        dic["hata_medium"]["%_tot"][sensibility[0]] = np.round(
            (hata_medium_counter/len(meters))*100, 2)

    return dic


# questo dovrebbe comparare i concentratori a due a due e ritornare la percetuale di copertura di entrambi...
def double_coverage(meters1, meters2):
    sensibilities = []
    sensibilities = _sensibility_calculation()
    dic = {"freeSpace": {},
           "hata_medium": {"%_tot":{},
                    "#_meters_optimizzation_sf":{},
                    "avg_optimize_ToA":0
                    },
           "hata_big": {"%_tot":{},
                    "#_meters_optimizzation_sf":{},
                    "avg_optimize_ToA":0
                    },
           "SUI_medium": {"%_tot":{},
                    "#_meters_optimizzation_sf":{},
                    "avg_optimize_ToA":0
                    },
           "SUI_big": {"%_tot":{},
                    "#_meters_optimizzation_sf":{},
                    "avg_optimize_ToA":0
                    },
           "ericsson": {"%_tot":{},
                    "#_meters_optimizzation_sf":{},
                    "avg_optimize_ToA":0
                    },
           "ericsson_medium": {"%_tot":{},
                    "#_meters_optimizzation_sf":{},
                    "avg_optimize_ToA":0
                    }}
    fs_counter = 0
    hata_medium_counter = 0
    previous_hata_medium_sf_meters = 0
    previous_hata_big_sf_meters = 0
    previous_SUI_medium_sf_meters=0
    previous_SUI_big_sf_meters=0
    previous_ericsson_sf_meters=0
    previous_ericsson_medium_sf_meters=0

    hata_big_counter = 0
    SUI_medium_counter = 0
    SUI_big_counter = 0
    ericsson_counter = 0
    ericsson_medium_counter=0

    sf_hata_medium_counter=0
    sf_hata_big_counter=0
    sf_SUI_medium_counter=0
    sf_SUI_big_counter=0
    sf_ericsson_counter=0
    sf_ericsson_medium_counter=0

    if(len(meters1) != len(meters2)):
        print("problema con i meters qualcosa non coincide con lunghezza")
        return Error

    for sensibility in sensibilities:
        fs_counter = 0
        hata_medium_counter = 0
        hata_big_counter = 0
        SUI_medium_counter = 0
        SUI_big_counter = 0
        ericsson_counter = 0
        ericsson_medium_counter=0


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

                ## HATA
                if (meters1[i]["recPow"]["hata_medium"] > sensibility[1] and meters2[i]["recPow"]["hata_medium"] > sensibility[1]):
                    hata_medium_counter += 1
                elif (meters1[i]["recPow"]["hata_medium"] > sensibility[1] and meters2[i]["recPow"]["hata_medium"] < sensibility[1]):
                    hata_medium_counter += 1
                elif (meters1[i]["recPow"]["hata_medium"] < sensibility[1] and meters2[i]["recPow"]["hata_medium"] > sensibility[1]):
                    hata_medium_counter += 1

                if (meters1[i]["recPow"]["hata_big"] > sensibility[1] and meters2[i]["recPow"]["hata_big"] > sensibility[1]):
                    hata_big_counter += 1
                elif (meters1[i]["recPow"]["hata_big"] > sensibility[1] and meters2[i]["recPow"]["hata_big"] < sensibility[1]):
                    hata_big_counter += 1
                elif (meters1[i]["recPow"]["hata_big"] < sensibility[1] and meters2[i]["recPow"]["hata_big"] > sensibility[1]):
                    hata_big_counter += 1

                ## SUI
                if (meters1[i]["recPow"]["SUI_medium"] > sensibility[1] and meters2[i]["recPow"]["SUI_medium"] > sensibility[1]):
                    SUI_medium_counter += 1
                elif (meters1[i]["recPow"]["SUI_medium"] > sensibility[1] and meters2[i]["recPow"]["SUI_medium"] < sensibility[1]):
                    SUI_medium_counter += 1
                elif (meters1[i]["recPow"]["SUI_medium"] < sensibility[1] and meters2[i]["recPow"]["SUI_medium"] > sensibility[1]):
                    SUI_medium_counter += 1

                if (meters1[i]["recPow"]["SUI_big"] > sensibility[1] and meters2[i]["recPow"]["SUI_big"] > sensibility[1]):
                    SUI_big_counter += 1
                elif (meters1[i]["recPow"]["SUI_big"] > sensibility[1] and meters2[i]["recPow"]["SUI_big"] < sensibility[1]):
                    SUI_big_counter += 1
                elif (meters1[i]["recPow"]["SUI_big"] < sensibility[1] and meters2[i]["recPow"]["SUI_big"] > sensibility[1]):
                    SUI_big_counter += 1

                ## ERICSSON
                if (meters1[i]["recPow"]["ericsson"] > sensibility[1] and meters2[i]["recPow"]["ericsson"] > sensibility[1]):
                    ericsson_counter += 1
                elif (meters1[i]["recPow"]["ericsson"] > sensibility[1] and meters2[i]["recPow"]["ericsson"] < sensibility[1]):
                    ericsson_counter += 1
                elif (meters1[i]["recPow"]["ericsson"] < sensibility[1] and meters2[i]["recPow"]["ericsson"] > sensibility[1]):
                    ericsson_counter += 1

                if (meters1[i]["recPow"]["ericsson_medium"] > sensibility[1] and meters2[i]["recPow"]["ericsson_medium"] > sensibility[1]):
                    ericsson_medium_counter += 1
                elif (meters1[i]["recPow"]["ericsson_medium"] > sensibility[1] and meters2[i]["recPow"]["ericsson_medium"] < sensibility[1]):
                    ericsson_medium_counter += 1
                elif (meters1[i]["recPow"]["ericsson_medium"] < sensibility[1] and meters2[i]["recPow"]["ericsson_medium"] > sensibility[1]):
                    ericsson_medium_counter += 1


        dic["freeSpace"][sensibility[0]] = np.round(
            (fs_counter/len(meters1))*100.2)

        # HATA MEDIUM
        dic["hata_medium"]["%_tot"][sensibility[0]] = np.round(
            (hata_medium_counter/len(meters1))*100, 2)

        dic["hata_medium"]["#_meters_optimizzation_sf"][sensibility[0]] = hata_medium_counter - previous_hata_medium_sf_meters
        previous_hata_medium_sf_meters = hata_medium_counter

        dic["hata_medium"]["avg_optimize_ToA"] = (dic["hata_medium"]["avg_optimize_ToA"] + dic["hata_medium"]["#_meters_optimizzation_sf"][sensibility[0]] * _time_on_air(sf_hata_medium_counter))

        if i == len(meters1)-1:
            dic["hata_medium"]["avg_optimize_ToA"] = np.round( dic["hata_medium"]["avg_optimize_ToA"] / hata_medium_counter , 3 )
        sf_hata_medium_counter +=1

        #HATA BIG
        dic["hata_big"]["%_tot"][sensibility[0]] = np.round(
            (hata_big_counter/len(meters1))*100, 2)

        dic["hata_big"]["#_meters_optimizzation_sf"][sensibility[0]] = hata_big_counter - previous_hata_big_sf_meters
        previous_hata_big_sf_meters = hata_big_counter

        dic["hata_big"]["avg_optimize_ToA"] = (dic["hata_big"]["avg_optimize_ToA"] + dic["hata_big"]["#_meters_optimizzation_sf"][sensibility[0]] * _time_on_air(sf_hata_big_counter))

        if i == len(meters1)-1:
            dic["hata_big"]["avg_optimize_ToA"] = np.round( dic["hata_big"]["avg_optimize_ToA"] / hata_big_counter , 3 )
        sf_hata_big_counter +=1

        # SUI MEDIUM
        dic["SUI_medium"]["%_tot"][sensibility[0]] = np.round(
            (SUI_medium_counter/len(meters1))*100, 2)

        dic["SUI_medium"]["#_meters_optimizzation_sf"][sensibility[0]] = SUI_medium_counter - previous_SUI_medium_sf_meters
        previous_SUI_medium_sf_meters = SUI_medium_counter

        dic["SUI_medium"]["avg_optimize_ToA"] = (dic["SUI_medium"]["avg_optimize_ToA"] + dic["SUI_medium"]["#_meters_optimizzation_sf"][sensibility[0]] * _time_on_air(sf_SUI_medium_counter))

        if i == len(meters1)-1:
            dic["SUI_medium"]["avg_optimize_ToA"] = np.round( dic["SUI_medium"]["avg_optimize_ToA"] / SUI_medium_counter , 3 )
        sf_SUI_medium_counter +=1

        # SUI BIG
        dic["SUI_big"]["%_tot"][sensibility[0]] = np.round(
            (SUI_big_counter/len(meters1))*100, 2)

        dic["SUI_big"]["#_meters_optimizzation_sf"][sensibility[0]] = SUI_big_counter - previous_SUI_big_sf_meters
        previous_SUI_big_sf_meters = SUI_big_counter

        dic["SUI_big"]["avg_optimize_ToA"] = (dic["SUI_big"]["avg_optimize_ToA"] + dic["SUI_big"]["#_meters_optimizzation_sf"][sensibility[0]] * _time_on_air(sf_SUI_big_counter))

        if i == len(meters1)-1:
            if isnan(dic["SUI_big"]["avg_optimize_ToA"]):
                dic["SUI_big"]["avg_optimize_ToA"] = 0
            else:
                dic["SUI_big"]["avg_optimize_ToA"] =  dic["SUI_big"]["avg_optimize_ToA"] / SUI_big_counter
        sf_SUI_big_counter +=1

        # ERICSSON
        dic["ericsson"]["%_tot"][sensibility[0]] = np.round(
            (ericsson_counter/len(meters1))*100, 2)

        dic["ericsson"]["#_meters_optimizzation_sf"][sensibility[0]] = ericsson_counter - previous_ericsson_sf_meters
        previous_ericsson_sf_meters = ericsson_counter

        dic["ericsson"]["avg_optimize_ToA"] = (dic["ericsson"]["avg_optimize_ToA"] + dic["ericsson"]["#_meters_optimizzation_sf"][sensibility[0]] * _time_on_air(sf_ericsson_counter))

        if i == len(meters1)-1:
            dic["ericsson"]["avg_optimize_ToA"] = np.round( dic["ericsson"]["avg_optimize_ToA"] / ericsson_counter , 3 )
        sf_ericsson_counter +=1


        dic["ericsson_medium"]["%_tot"][sensibility[0]] = np.round(
            (ericsson_medium_counter/len(meters1))*100, 2)

        dic["ericsson_medium"]["#_meters_optimizzation_sf"][sensibility[0]] = ericsson_medium_counter - previous_ericsson_medium_sf_meters
        previous_ericsson_medium_sf_meters = ericsson_medium_counter

        dic["ericsson_medium"]["avg_optimize_ToA"] = (dic["ericsson_medium"]["avg_optimize_ToA"] + dic["ericsson_medium"]["#_meters_optimizzation_sf"][sensibility[0]] * _time_on_air(sf_ericsson_medium_counter))

        if i == len(meters1)-1:
            dic["ericsson_medium"]["avg_optimize_ToA"] = np.round( dic["ericsson_medium"]["avg_optimize_ToA"] / ericsson_medium_counter , 3 )
        sf_ericsson_medium_counter +=1


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
    print("number of combination of DCç "+ str(len(permutation)))
    return permutation


    ## thiease are the "filan consideration" between each SF of lora and the coverage between two different couple of DC
def consideration_two_configuarition(firstConfig, choice2irg, secondConfig, config2):
    difference = 0
    stringa = firstConfig + " and " + secondConfig + "we have: \n"
    for i in range(6):
        difference =( 100*(choice2irg["coverage"]["hata_medium"]["%_tot"]["SF"+str(7+i)]-config2["%_tot"]["SF"+str(7+i)])/
                    ( (choice2irg["coverage"]["hata_medium"]["%_tot"]["SF"+str(7+i)]+config2["%_tot"]["SF"+str(7+i)])/2 ) )
        difference =  np.round(difference,2)

        if (choice2irg["coverage"]["hata_medium"]["%_tot"]["SF"+str(7+i)] > config2["%_tot"]["SF"+str(7+i)]):
            stringa = stringa +"in the SF"+str(7+i)+" LoRa configuration there is a gain of: "+ str(abs(difference)) + "% \n"
        else:
            stringa = stringa +"in the SF"+str(7+i)+" LoRa configuration there is a loss of: "+ str(abs(difference)) + "% \n"
    return stringa