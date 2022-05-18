## la coppia di contatori sceleti da 2iretegas è "id": 69

import json
import utils.cleaner as cl
import utils.calcolo as calc


######
# file opening
with open('./start/concentratori.json') as file:
    dcs = json.load(file)
    print("numero DC :", len(dcs))
with open('./start/contatori.json') as file:
    meters = json.load(file)
    print("meters normali sono :", len(meters))
with open('./start/contatori_N_I.json') as file:
    meters_NI = json.load(file)
    print("meters NI sono :", len(meters_NI))
######

######
    # take meter and put them in 1 "file"
for meter_NI in meters_NI:
    meters.append(meter_NI)
print("i meters totali sono :", len(meters))
######


######
# rename key
for meter in meters:
    meter["id"] = meter.pop("numero")
    meter["latitudine"] = meter.pop("latitudine")
    meter["longitudine"] = meter.pop("longitudine")
    meter["ubicazione"] = meter.pop("ubicazione")
with open('./risultati/contatori_totali.json', 'w') as file:
    json.dump(meters, file)

for dc in dcs:
    dc["id"] = dc.pop("id_site")
    dc["matricola"] = dc.pop("matricola")
    dc["latitudine"] = dc.pop("lat")
    dc["longitudine"] = dc.pop("long")
with open('./risultati/concentratori.json', 'w') as file:
    json.dump(dcs, file)
######


######
    # cliean meters and keep only the one in a smaller area
meters = cl.circoscrizione(meters)
######

######
# ordering by key value
meters = cl.ordering_by_key_value(meters, "id")
with open('./risultati/contatori_totali.json', 'w') as file:
    json.dump(meters, file)

dcs = cl.ordering_by_key_value(dcs, "id")
with open('./risultati/concentratori.json', 'w') as file:
    json.dump(dcs, file)
######

######
    # distance calculation and recived power with freespace and Hata loss
dcsToMeters = dcs

for i in dcsToMeters:
    i['meters'] = []
    for j in meters:

        # try:
        # creo una variabile tipo dict
        dictionary = {
            "id": j['id'],
            "ditance(Km)": calc.testHevers(i['latitudine'], i['longitudine'], j['latitudine'], j['longitudine']),
            "recPow": {"freeSpace": calc.potRic(-16.020, 11.2, 11.2, calc.testHevers(i['latitudine'], i['longitudine'], j['latitudine'], j['longitudine']), 868, "FS"),
                       "hata": calc.potRic(-16.020, 11.2, 11.2, calc.testHevers(i['latitudine'], i['longitudine'], j['latitudine'], j['longitudine']), 868, "hata")}
        }

        # poiche prima ho inizializzato lista vuota uso la funzione append!
        i["meters"].append(dictionary)
with open('./risultati/distance_power.json', 'w') as file:
    json.dump(dcsToMeters, file)
######

######
    # single coverage calculation for each DC
singleCoverage = []

for dcToMeter in dcsToMeters:

    coverage = calc.coverage(dcToMeter["meters"])

    singleCoverage.append({"id_dc": dcToMeter["id"],
                           "coverage": coverage})
with open('./risultati/single_coverage.json', 'w') as file:
    json.dump(singleCoverage, file)
######


######
    # Double coverage for each simple combination of DC (= m!/(m-n)!n! )
id_dc = []
dic = {}
doubleCoverage = []
for dc in dcs:
    id_dc.append(dc["id"])
counter = 0
for coppia in calc.simple_combination(dcsToMeters):
    dic = {"id": counter,
           "id_dc_1": coppia[0]["id"],
           "id_dc_2": coppia[1]["id"],
           "coverage": calc.double_coverage(coppia[0]["meters"], coppia[1]["meters"])
           }
    counter += 1
    doubleCoverage.append(dic)

with open('./risultati/double_coverage.json', 'w') as file:
    json.dump(doubleCoverage, file)
######

######
    ## Coupled for 2iretegas
choice2irg = {}
for double in doubleCoverage:
    if (double["id_dc_1"] == "61490730150009" and double["id_dc_2"] == "61490730150016"):
        choice2irg = double
######

######
    ## finding the best coverage with SF12
cover = 0
bestCoverage = {}
for double in doubleCoverage:
    if double["coverage"]["hata"]["SF12"] > cover:
        cover = double["coverage"]["hata"]["SF12"]
        bestCoverage = double
######

######
    # findign couple with min and max ToA
max_toa = 0
min_toa = 88888888888888888888888888888888
couple_max = {}
couple_min = {}
for double in doubleCoverage:
    if double["coverage"]["tot_trasmission_time_hata"]["tot_ToA"] > max_toa:
        max_toa = double["coverage"]["tot_trasmission_time_hata"]["tot_ToA"]
        couple_max = double
    if double["coverage"]["tot_trasmission_time_hata"]["tot_ToA"] < min_toa:
        min_toa = double["coverage"]["tot_trasmission_time_hata"]["tot_ToA"]
        couple_min = double

stringa = ("(HATA) chosen couple by 2irg: " + str(choice2irg["id"]) + " with SF12 coverage of " + str(choice2irg["coverage"]["hata"]["SF12"]) + "% "+"and total ToA: " + str(choice2irg["coverage"]["tot_trasmission_time_hata"]["tot_ToA"]) + "\n" +
           "(HATA) couple with best coverage: " + str(bestCoverage["id"]) + " with SF12 coverage of " + str(cover) + "% "+"and total ToA: " + str(bestCoverage["coverage"]["tot_trasmission_time_hata"]["tot_ToA"]) + "\n" +
           "(HATA) couple with min ToA: " + str(couple_min["id"]) + " with total ToA: " + str(couple_min["coverage"]["tot_trasmission_time_hata"]["tot_ToA"]) + "\n" +
           "(HATA) couple with min ToA: " + str(couple_max["id"]) + " with total ToA: " + str(couple_max["coverage"]["tot_trasmission_time_hata"]["tot_ToA"]) + "\n\n")


stringa = stringa + "\t\t\t\t\t ->(HATA)<- \n"
stringa = stringa+"Chosen couple \t\t" + "Best coverage \t\t" + "Min ToA \t\t" + "Max ToA" + "\n"
stringa = stringa+"------------------------------------------------------------------------------------\n"

for i in range(6):
    stringa = (stringa +
               "SF"+str(7+i) + ": " + str(choice2irg["coverage"]["hata"]["SF"+str(7+i)]) + "%" + "\t\t" +
               "SF"+str(7+i) + ": " + str(bestCoverage["coverage"]["hata"]["SF"+str(7+i)]) + "%" + "\t\t" +
               "SF"+str(7+i) + ": " + str(couple_min["coverage"]["hata"]["SF"+str(7+i)]) + "%" + "\t\t" +
               "SF"+str(7+i) + ": " + str(couple_max["coverage"]["hata"]["SF"+str(7+i)]) + "%" + "\n")

stringa = (stringa + "\n" +
           "ToA"+": " + str(choice2irg["coverage"]["tot_trasmission_time_hata"]["tot_ToA"]) + "\t\t" +
           "ToA"+": " + str(bestCoverage["coverage"]["tot_trasmission_time_hata"]["tot_ToA"]) + "\t\t" +
           "ToA"+": " + str(couple_min["coverage"]["tot_trasmission_time_hata"]["tot_ToA"]) + "\t\t" +
           "ToA"+": " + str(couple_max["coverage"]["tot_trasmission_time_hata"]["tot_ToA"]) + "\n")


stringa = stringa + "with rispect to the configurations: "  + str(calc.consideration_two_configuarition("chosen by 2irg",choice2irg,"Best Coverage",bestCoverage))
print(stringa)
with open("./risultati/consideration.txt",'w') as file:
    file.write(stringa)