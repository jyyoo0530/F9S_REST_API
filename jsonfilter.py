import os
from jsoncreator import json_creator_v2



def mw_summary_filter(polCode, podCode, baseYearWeek, jsonResult):
    kkk = []
    a = os.path.realpath(__file__).replace('\\', '/')
    mdmPath = a[:a.find("jsonfilter")]+"static/mdmJson"
    for j in range(0, len(jsonResult['cell'])):
        ttt = 0
        for i in range(0, len(jsonResult['cell'][j]['routeItem'])):
            if polCode == "" and podCode == "":
                ttt += 1
                break
            elif polCode != "" and podCode == "":
                if jsonResult['cell'][j]['routeItem'][i]['polCode'] == polCode:
                    ttt += 1
                    break
                else:
                    continue
            elif polCode == "" and podCode != "":
                if jsonResult['cell'][j]['routeItem'][i]['podCode'] == podCode:
                    ttt += 1
                    break
                else:
                    continue
            elif polCode != "" and podCode != "":
                if jsonResult['cell'][j]['routeItem'][i]['polCode'] == polCode and \
                        jsonResult['cell'][j]['routeItem'][i]['podCode'] == podCode:
                    ttt += 1
                    break
                else:
                    continue

        # 주차 filter로 lineItem 삭제 대상 설정
        ppp = []
        for i in range(0, len(jsonResult['cell'][j]['lineItem'])):
            if baseYearWeek == []:
                break
            elif jsonResult['cell'][j]['lineItem'][i]['baseYearWeek'] in baseYearWeek:
                break
            else:
                ppp.append(i)
        jsonResult['cell'][j]['lineItem'] = [i for k, i in enumerate(jsonResult['cell'][j]['lineItem']) if k not in ppp]
        sumQty = 0
        for i in range(0, len(jsonResult['cell'][j]['lineItem'])):
            sumQty += jsonResult['cell'][j]['lineItem'][i]['dealQty']
        jsonResult['cell'][j]['aggDealQty'] = sumQty
        sumQty = 0
        for i in range(0, len(jsonResult['cell'][j]['lineItem'])):
            sumQty += jsonResult['cell'][j]['lineItem'][i]['leftQty']
        jsonResult['cell'][j]['aggLeftQty'] = sumQty
        sumQty = 0
        for i in range(0, len(jsonResult['cell'][j]['lineItem'])):
            sumQty += jsonResult['cell'][j]['lineItem'][i]['priceValue']
        jsonResult['cell'][j]['priceValue'] = sumQty

        mdmSrc = json_creator_v2(mdmPath)

        if polCode == "":
            headPolCode = jsonResult['cell'][j]['routeItem'][0]['polCode']
            jsonResult['cell'][j]['headPolCode'] = headPolCode
        elif polCode != "":
            headPolCode = polCode
            jsonResult['cell'][j]['headPolCode'] = headPolCode
        if podCode == "":
            headPodCode = jsonResult['cell'][j]['routeItem'][0]['podCode']
            jsonResult['cell'][j]['headPodCode'] = headPodCode
        elif podCode != "":
            headPodCode = podCode
            jsonResult['cell'][j]['headPodCode'] = headPodCode

        jsonResult['cell'][j]['headPolName'] = [i for i in mdmSrc if i['locCd'] == headPolCode][0]['locNm']
        jsonResult['cell'][j]['headPodName'] = [i for i in mdmSrc if i['locCd'] == headPodCode][0]['locNm']

        if ttt == 0:
            kkk.append(j)
        else:
            continue
    jsonResult['cell'] = [i for j, i in enumerate(jsonResult['cell']) if j not in kkk]
    jsonResult['cell'] = [i for i in jsonResult['cell'] if i['lineItem'] != []]
    jsonResult['closedStsCount'] = len([i for i in jsonResult['cell'] if i['offerStatus'] == '0'])
    jsonResult['openStsCount'] = len([i for i in jsonResult['cell'] if i['offerStatus'] == '1'])

    return jsonResult
