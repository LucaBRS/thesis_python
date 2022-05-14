## ordinamento dei file json!

def ordinamento_nome(dic,type):

    def id_siteReturn(dic):
        return dic["id_site"]

    def numeroReturn(dic):
        return dic["numero"]


    if type == "dc":
        dic.sort(key = id_siteReturn)
    else:
        dic.sort(key = numeroReturn)

    return dic



