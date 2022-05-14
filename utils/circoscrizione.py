
def circoscrizione(dic):
    itemToPop = []
    cont = dic

        ## questo ciclo mi permette di individuare gli indici degli "oggetti" da levare nella lista
    for i in range(len(cont)-1):
        if (cont[i]["latitudine"] > 40.608 or cont[i]["latitudine"] < 40.57) or (cont[i]["longitudine"] > 17.146 or cont[i]["longitudine"] < 17.08) or (cont[i]["longitudine"]==0 or cont[i]["latitudine"]==0):
            itemToPop.append(i)

    print(itemToPop)

        ## inverto gli indici in modo da iniziare dalla fine ed evitare errori nel rimuovere elementi
    itemToPop.reverse()
    for item in itemToPop:
        cont.pop(item)

    return cont