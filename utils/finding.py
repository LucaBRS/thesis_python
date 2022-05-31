def finding(doubleCoverage):

    dic = {
        "choice2irg": {},
        "hata_medium": {"bestCoverage_hata_medium": {},
                        "max_toa_hata_medium": {},
                        "min_toa_hata_medium": {}
                        },
        "hata_big": {"bestCoverage_hata_big": {},
                     "max_toa_hata_big": {},
                     "min_toa_hata_big": {}
                     },
        "SUI_medium": {"bestCoverage_SUI_medium": {},
                       "max_toa_SUI_medium": {},
                       "min_toa_SUI_medium": {}
                       },
        "SUI_big": {"bestCoverage_SUI_big": {},
                    "max_toa_SUI_big": {},
                    "min_toa_SUI_big": {}
                    },
        "ericsson": {"bestCoverage_ericsson": {},
                     "max_toa_ericsson": {},
                     "min_toa_ericsson": {}
                     }
    }
    ######
    # DC COUPLE FOR 2IRG
    choice2irg = {}
    for double in doubleCoverage:
        if (double["id_dc_1"] == "61490730150009" and double["id_dc_2"] == "61490730150016"):
            dic["choice2irg"] = double
    ######

            ###################################
            ######### hata_medium #############
            ###################################
    ######
        # FINSIGN BEST COVERAGE WITH SF12
    cover = 0
    bestCoverage_hata_medium = {}
    for double in doubleCoverage:
        if double["coverage"]["hata_medium"]["%_tot"]["SF12"] > cover:
            cover = double["coverage"]["hata_medium"]["%_tot"]["SF12"]
            
            dic["hata_medium"]["bestCoverage_hata_medium"] = double["coverage"]["hata_medium"]
            dic["hata_medium"]["bestCoverage_hata_medium"]["id"] = double["id"] 
    ######

    ######
        # FINDIG COUPLE WITH min AND MAX ToA
    max_toa_hata_medium = 0
    min_toa_hata_medium = 88888888888888888888888888888888
    couple_max_hata_medium = {}
    couple_min_hata_medium = {}
    for double in doubleCoverage:
        if double["coverage"]["hata_medium"]["avg_optimize_ToA"] > max_toa_hata_medium:
            max_toa_hata_medium = double["coverage"]["hata_medium"]["avg_optimize_ToA"]
            
            dic["hata_medium"]["max_toa_hata_medium"] = double["coverage"]["hata_medium"]
            dic["hata_medium"]["max_toa_hata_medium"]["id"] = double["id"]
            
        if double["coverage"]["hata_medium"]["avg_optimize_ToA"] < min_toa_hata_medium:
            min_toa_hata_medium = double["coverage"]["hata_medium"]["avg_optimize_ToA"]
            
            dic["hata_medium"]["min_toa_hata_medium"] = double["coverage"]["hata_medium"]
            dic["hata_medium"]["min_toa_hata_medium"]["id"] = double["id"]
    ######

            ###################################
            ######### hata_big #############
            ###################################
    ######
        # FINSIGN BEST COVERAGE WITH SF12
    cover = 0
    bestCoverage_hata_big = {}
    for double in doubleCoverage:
        if double["coverage"]["hata_big"]["%_tot"]["SF12"] > cover:
            cover = double["coverage"]["hata_big"]["%_tot"]["SF12"]
            dic["hata_big"]["bestCoverage_hata_big"] = double["coverage"]["hata_big"]
            dic["hata_big"]["bestCoverage_hata_big"]['id'] = double['id']
    ######

    ######
        # FINDIG COUPLE WITH min AND MAX ToA
    max_toa_hata_big = 0
    min_toa_hata_big = 88888888888888888888888888888888
    couple_max_hata_big = {}
    couple_min_hata_big = {}
    for double in doubleCoverage:
        if double["coverage"]["hata_big"]["avg_optimize_ToA"] > max_toa_hata_big:
            max_toa_hata_big = double["coverage"]["hata_big"]["avg_optimize_ToA"]
            dic["hata_big"]["max_toa_hata_big"] = double["coverage"]["hata_big"]
            dic["hata_big"]["max_toa_hata_big"]['id'] = double['id']
            
        if double["coverage"]["hata_big"]["avg_optimize_ToA"] < min_toa_hata_big:
            min_toa_hata_big = double["coverage"]["hata_big"]["avg_optimize_ToA"]
            dic["hata_big"]["min_toa_hata_big"] = double["coverage"]["hata_big"]
            dic["hata_big"]["min_toa_hata_big"]['id'] = double['id']
    ######

            ###################################
            ######### SUI_medium #############
            ###################################
    ######
        # FINSIGN BEST COVERAGE WITH SF12
    cover = 0
    bestCoverage_SUI_medium = {}
    for double in doubleCoverage:
        if double["coverage"]["SUI_medium"]["%_tot"]["SF12"] > cover:
            cover = double["coverage"]["SUI_medium"]["%_tot"]["SF12"]
            dic["SUI_medium"]["bestCoverage_SUI_medium"] = double["coverage"]["SUI_medium"]
            dic["SUI_medium"]["bestCoverage_SUI_medium"]['id'] = double['id']
    ######

    ######
        # FINDIG COUPLE WITH min AND MAX ToA
    max_toa_SUI_medium = 0
    min_toa_SUI_medium = 88888888888888888888888888888888
    couple_max_SUI_medium = {}
    couple_min_SUI_medium = {}
    for double in doubleCoverage:
        if double["coverage"]["SUI_medium"]["avg_optimize_ToA"] > max_toa_SUI_medium:
            max_toa_SUI_medium = double["coverage"]["SUI_medium"]["avg_optimize_ToA"]
            dic["SUI_medium"]["max_toa_SUI_medium"] = double["coverage"]["SUI_medium"]
            dic["SUI_medium"]["max_toa_SUI_medium"]['id'] = double['id']
            
        if double["coverage"]["SUI_medium"]["avg_optimize_ToA"] < min_toa_SUI_medium:
            min_toa_SUI_medium = double["coverage"]["SUI_medium"]["avg_optimize_ToA"]
            dic["SUI_medium"]["min_toa_SUI_medium"] = double["coverage"]["SUI_medium"]
            dic["SUI_medium"]["min_toa_SUI_medium"]['id'] = double['id']
    ######

            ###################################
            ######### SUI_big #############
            ###################################
    ######
        # FINSIGN BEST COVERAGE WITH SF12
    cover = 0
    bestCoverage_SUI_big = {}
    for double in doubleCoverage:
        if double["coverage"]["SUI_big"]["%_tot"]["SF12"] > cover:
            cover = double["coverage"]["SUI_big"]["%_tot"]["SF12"]
            dic["SUI_big"]["bestCoverage_SUI_big"] = double["coverage"]["SUI_big"]
            dic["SUI_big"]["bestCoverage_SUI_big"]['id'] = double['id']
    ######

    ######
        # FINDIG COUPLE WITH min AND MAX ToA
    max_toa_SUI_big = 0
    min_toa_SUI_big = 88888888888888888888888888888888
    couple_max_SUI_big = {}
    couple_min_SUI_big = {}
    for double in doubleCoverage:
        if double["coverage"]["SUI_big"]["avg_optimize_ToA"] > max_toa_SUI_big:
            max_toa_SUI_big = double["coverage"]["SUI_big"]["avg_optimize_ToA"]
            dic["SUI_big"]["max_toa_SUI_big"] = double["coverage"]["SUI_big"]
            dic["SUI_big"]["max_toa_SUI_big"]['id'] = double['id']
            
        if double["coverage"]["SUI_big"]["avg_optimize_ToA"] < min_toa_SUI_big:
            min_toa_SUI_big = double["coverage"]["SUI_big"]["avg_optimize_ToA"]
            dic["SUI_big"]["min_toa_SUI_big"] = double["coverage"]["SUI_big"]
            dic["SUI_big"]["min_toa_SUI_big"]['id'] = double['id']
    ######

            ###################################
            ######### ericsson #############
            ###################################
    ######
        # FINSIGN BEST COVERAGE WITH SF12
    cover = 0
    bestCoverage_ericsson = {}
    for double in doubleCoverage:
        if double["coverage"]["ericsson"]["%_tot"]["SF12"] > cover:
            cover = double["coverage"]["ericsson"]["%_tot"]["SF12"]
            dic["ericsson"]["bestCoverage_ericsson"] = double["coverage"]["ericsson"]
            dic["ericsson"]["bestCoverage_ericsson"]['id'] = double['id']
    ######

    ######
        # FINDIG COUPLE WITH min AND MAX ToA
    max_toa_ericsson = 0
    min_toa_ericsson = 88888888888888888888888888888888
    couple_max_ericsson = {}
    couple_min_ericsson = {}
    for double in doubleCoverage:
        if double["coverage"]["ericsson"]["avg_optimize_ToA"] > max_toa_ericsson:
            max_toa_ericsson = double["coverage"]["ericsson"]["avg_optimize_ToA"]
            dic["ericsson"]["max_toa_ericsson"] = double["coverage"]["ericsson"]
            dic["ericsson"]["max_toa_ericsson"]['id'] = double['id']
            
        if double["coverage"]["ericsson"]["avg_optimize_ToA"] < min_toa_ericsson:
            min_toa_ericsson = double["coverage"]["ericsson"]["avg_optimize_ToA"]
            dic["ericsson"]["min_toa_ericsson"] = double["coverage"]["ericsson"]
            dic["ericsson"]["min_toa_ericsson"]['id'] = double['id']
    ######

    return dic
