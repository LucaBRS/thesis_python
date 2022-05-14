def circoscrizione(dic):
    itemToPop = []
    cont = dic

        ## to find the idex of the item to remove
    for i in range(len(cont)-1):
        if (cont[i]["latitudine"] > 40.608 or cont[i]["latitudine"] < 40.57) or (cont[i]["longitudine"] > 17.146 or cont[i]["longitudine"] < 17.08) or (cont[i]["longitudine"]==0 or cont[i]["latitudine"]==0):
            itemToPop.append(i)

    print(itemToPop)

        ## invert index in order to start removing from bottom ad avoid errors
    for item in itemToPop:
        cont.pop(item)

    return cont


def remove_keys(dic,*keys):

    for key in keys:
        for dato in dic:
            dato.pop(key)
    return dic



def ordering_by_key_value(dic,key_name):

    def id_siteReturn(dic):
        return dic[key_name]


    dic.sort(key = id_siteReturn)


    return dic

