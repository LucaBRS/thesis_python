import json
import utils.cleaner as cl
import utils.calcolo as calc


######
    ## file opening
with open('./start/concentratori.json') as file:
    dcs = json.load(file)
    print("numero DC :", len(dcs))
with open('./start/contatori.json') as file:
    meters = json.load(file)
    print("meters normali sono :", len(meters))
with open('./start/contatori_N_I.json') as file:
    meters_NI= json.load(file)
    print("meters NI sono :",len(meters_NI))
######

######
    ## take meter and put them in 1 "file"
for meter_NI in meters_NI:
    meters.append(meter_NI)
print("i meters totali sono :",len(meters))
######


######
    ## rename key
for meter in meters:
    meter["id"] = meter.pop("numero")
    meter["latitudine"] = meter.pop("latitudine")
    meter["longitudine"] = meter.pop("longitudine")
    meter["ubicazione"] = meter.pop("ubicazione")
with open('./risultati/contatori_totali.json','w') as file:
    json.dump(meters,file)

for dc in dcs:
    dc["id"] = dc.pop("id_site")
    dc["matricola"] = dc.pop("matricola")
    dc["latitudine"] = dc.pop("lat")
    dc["longitudine"] = dc.pop("long")
with open('./risultati/concentratori.json','w') as file:
    json.dump(dcs,file)
######


######
    ## cliean meters and keep only the one in a smaller area
meters = cl.circoscrizione(meters)
######

######
    ## ordering by key value
meters = cl.ordering_by_key_value(meters,"id")
with open('./risultati/contatori_totali.json','w') as file:
    json.dump(meters,file)

dcs = cl.ordering_by_key_value(dcs,"id")
with open('./risultati/concentratori.json','w') as file:
    json.dump(dcs,file)
######

######
    ## distance calculation and recived power with freespace and Hata loss
dcsToMeters = dcs

for i in dcsToMeters:
    i['meters'] = []
    for j in meters:
        
        # try:
            # creo una variabile tipo dict
            dictionary ={
                    "id":j['id'],
                    "ditance(Km)":calc.testHevers(i['latitudine'],i['longitudine'],j['latitudine'],j['longitudine']),
                    "recPow":{"freeSpace":calc.potRic(-16.020,11.2,11.2,calc.testHevers(i['latitudine'],i['longitudine'],j['latitudine'],j['longitudine']),868,"FS"),
                              "hata":calc.potRic(-16.020,11.2,11.2,calc.testHevers(i['latitudine'],i['longitudine'],j['latitudine'],j['longitudine']),868,"hata")}
                }

            # poiche prima ho inizializzato lista vuota uso la funzione append!
            i["meters"].append(dictionary)
with open('./risultati/distance_power.json','w') as file:
    json.dump(dcsToMeters,file)
######    
    
######
    ## single coverage calculation for each DC
singleCoverage = []

for dcToMeter in dcsToMeters:

    coverage = calc.coverage(dcToMeter["meters"])

    singleCoverage.append({"id_dc":dcToMeter["id"],
                      "coverage":coverage})
with open('./risultati/single_coverage.json','w') as file:
    json.dump(singleCoverage,file)
######

######
    ## Double coverage for each simple combination of DC (= m!/(m-n)!n! )
id_dc=[]
dic ={}
doubleCoverage = []
for dc in dcs:
    id_dc.append(dc["id"])

for coppia in calc.simple_combination(dcsToMeters):
    dic = { "id_dc_1":coppia[0]["id"],
           "id_dc_2": coppia[1]["id"],
            "coverage": calc.double_coverage(coppia[0]["meters"],coppia[1]["meters"])

    }
    doubleCoverage.append(dic)

with open('./risultati/double_coverage.json','w') as file:
    json.dump(doubleCoverage,file)
######