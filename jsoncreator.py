import json
import os


def json_creator_v2(fullpath):
    try:
        tgList = os.listdir(fullpath)
        rdList = []
        for i in range(0, len(tgList)):
            kk = tgList[i]
            if kk[len(kk) - 5:len(kk)] == '.json':
                rdList.append(kk)
            else:
                continue
        rtData = ""
        for i in range(0, len(rdList)):
            try:
                open_data = open(fullpath + "/" + rdList[i]).read()
                aa = open_data.replace("}\n{", "},\n{")
                bb = aa.replace("\n", "")
                cc = bb.replace(",,", ",")
            except:
                continue
            if len(rtData) == 0:
                rtData += cc
            elif len(cc) == 0:
                continue
            else:
                rtData += "," + cc
        if "mdmSrc.json" in tgList:
            rtResult = json.loads("[" + rtData + "]")
        else:
            rtResult = json.loads(rtData)
        return rtResult
    except:
        errorMsg = '{"cannot find json file/location within POST request"}'
        return errorMsg


def json_creator_v1(fullpath):
    tgList = os.listdir(fullpath)
    rdList = []
    for i in range(0, len(tgList)):
        kk = tgList[i]
        if kk[len(kk) - 5:len(kk)] == '.json':
            rdList.append(kk)
        else:
            continue
    rtData = []
    for i in range(0, len(rdList)):
        # try:
        with open(fullpath + "/" + rdList[i]) as open_data:
            lineJson = json.loads(open_data.read().encode('utf-8'))
        rtData.append(lineJson)
    # except:
    #     continue

    return rtData
