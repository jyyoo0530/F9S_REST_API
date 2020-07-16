import os

from flask import Flask, request, jsonify
# from flask_socketio import SocketIO
from werkzeug.serving import WSGIRequestHandler

from jsoncreator import json_creator_v1, json_creator_v2
from jsonfilter import mw_summary_filter

app = Flask(__name__)
# socketio = SocketIO(app)
a = os.path.realpath(__file__).replace('\\', '/')
srcDir = a[:a.find("app")]
statsPath = '/api/v1/stats/'
dashboardPath = '/api/v1/dashboard/'
srcPath = srcDir + 'src/f9s'


# 공통할일
# 1) Zeppelin OFER_CRYR_CD -> 삭제 및 filter 기능으로 변환

##### API #####
@app.route('/')  # route 설정
def hello_world():
    return 'Hello, World!'


# @app.route(statsPath + '/carrierlist', methods=['GET'])
# def get_mw_cryr_list():
#     fullPath = srcPath + "/F9S_CRYR_LST"
#     response = json_creator_v1(fullPath)
#     return jsonify(response)


@app.route(statsPath + '/idxlist', methods=['GET'])
def get_mw_idx_list():
    fullPath = srcPath + "/F9S_IDX_LST"
    response = json_creator_v1(fullPath)
    return jsonify(response)


@app.route(dashboardPath + '/list/summary/rtelist', methods=['POST'])
def post_dsbd_rtelist():
    rqPost = request.get_json()
    userId = rqPost["userId"]
    offerTypeCode = rqPost["offerTypeCode"]

    rteListPath = "/" + userId + "/" + offerTypeCode
    fullPath = srcPath + "/F9S_DSBD_RTELIST" + rteListPath
    response = json_creator_v2(fullPath)
    return jsonify(response)


@app.route(dashboardPath + '/list/summary/weeklist', methods=['POST'])
def post_dsbd_wklist():
    rqPost = request.get_json()
    userId = rqPost["userId"]
    offerTypeCode = rqPost["offerTypeCode"]
    polCode = rqPost["polCode"]
    podCode = rqPost["podCode"]

    if polCode == "":
        polCode = "all"
    if podCode == "":
        podCode = "all"

    wkListPath = "/" + userId + "/" + offerTypeCode + "/" + polCode + podCode
    fullPath = srcPath + "/F9S_DSBD_WKLIST" + wkListPath

    response = json_creator_v2(fullPath)
    return jsonify(response)


@app.route(dashboardPath + '/list/summary', methods=['POST'])
def post_dsbd_summary():
    rqPost = request.get_json()
    userId = rqPost["userId"]
    offerTypeCode = rqPost["offerTypeCode"]
    polCode = rqPost["polCode"]
    podCode = rqPost["podCode"]
    baseYearWeek = rqPost["baseYearWeek"]

    dsbdSumPath = "/" + userId + "/" + offerTypeCode
    fullPath = srcPath + "/F9S_DSBD_SUM" + dsbdSumPath

    jsonResult = json_creator_v2(fullPath)
    response = mw_summary_filter(polCode, podCode, baseYearWeek, jsonResult)
    return jsonify(response)


@app.route(dashboardPath + '/offer/weekdetail', methods=['GET'])
def get_ofer_wkdetail():
    offerNumber = request.args.get('offernumber')
    baseYearWeek = request.args.get('baseyearweek')

    wdetailPath = "/" + offerNumber + "/" + baseYearWeek
    fullPath = srcPath + "/F9S_DSBD_WKDETAIL" + wdetailPath
    response = json_creator_v2(fullPath)
    return jsonify(response)


@app.route(dashboardPath + '/offer/offerevents', methods=['GET'])
def get_ofer_evnts():
    offerNumber = request.args.get('offernumber')

    evntLogPath = "/" + offerNumber
    fullPath = srcPath + "/F9S_DSBD_EVNTLOG" + evntLogPath

    response = json_creator_v2(fullPath)
    return jsonify(response)


@app.route(statsPath + '/filtered/marketwatch/productdealhistory', methods=['POST'])
def post_rq_mw_hst():
    mwFilter = request.get_json()
    companyCodes = mwFilter["companyCodes"]
    containerTypeCode = mwFilter["containerTypeCode"]
    marketTypeCode = mwFilter["marketTypeCode"]
    paymentTermCode = mwFilter["paymentTermCode"]
    polCode = mwFilter["polCode"]
    podCode = mwFilter["podCode"]
    rdTermCode = mwFilter["rdTermCode"]
    baseYearWeek = mwFilter["baseYearWeek"]

    hstPath = "/" + marketTypeCode + "/" + baseYearWeek + "/" + paymentTermCode + "/" + rdTermCode + "/" + containerTypeCode + "/" + polCode + podCode
    fullPath = srcPath + "/F9S_MW_HST" + hstPath
    response = json_creator_v2(fullPath)
    return jsonify(response)


@app.route(statsPath + '/filtered/marketwatch', methods=['POST'])
def post_rq_mw():
    mwFilter = request.get_json()
    companyCodes = mwFilter["companyCodes"]
    containerTypeCode = mwFilter["containerTypeCode"]
    marketTypeCode = mwFilter["marketTypeCode"]
    paymentTermCode = mwFilter["paymentTermCode"]
    polCode = mwFilter["polCode"]
    podCode = mwFilter["podCode"]
    rdTermCode = mwFilter["rdTermCode"]

    mwPath = "/" + marketTypeCode + "/" + paymentTermCode + "/" + rdTermCode + "/" + containerTypeCode + "/" + polCode + podCode
    fullPath = srcPath + "/F9S_MW_SUM" + mwPath
    response = json_creator_v2(fullPath)
    return jsonify(response)


@app.route(statsPath + '/filtered/marketwatch/productweekdetail', methods=['POST'])
def post_rq_mw_detail():
    mwFilter = request.get_json()
    companyCodes = mwFilter["companyCodes"]
    containerTypeCode = mwFilter["containerTypeCode"]
    marketTypeCode = mwFilter["marketTypeCode"]
    paymentTermCode = mwFilter["paymentTermCode"]
    polCode = mwFilter["polCode"]
    podCode = mwFilter["podCode"]
    rdTermCode = mwFilter["rdTermCode"]
    baseYearWeek = mwFilter["baseYearWeek"]
    interval = mwFilter["interval"]

    wdetailPath = "/" + marketTypeCode + "/" + baseYearWeek + "/" + paymentTermCode + "/" + rdTermCode + "/" + containerTypeCode + "/" + polCode + podCode + "/" + interval
    fullPath = srcPath + "/F9S_MW_WKDETAIL" + wdetailPath
    response = json_creator_v2(fullPath)
    return jsonify(response)


@app.route(statsPath + '/filtered/marketwatch/bidask', methods=['POST'])
def post_rq_mw_oferlist():
    mwFilter = request.get_json()
    companyCodes = mwFilter["companyCodes"]
    containerTypeCode = mwFilter["containerTypeCode"]
    marketTypeCode = mwFilter["marketTypeCode"]
    paymentTermCode = mwFilter["paymentTermCode"]
    polCode = mwFilter["polCode"]
    podCode = mwFilter["podCode"]
    rdTermCode = mwFilter["rdTermCode"]
    baseYearWeek = mwFilter["baseYearWeek"]
    offerTypeCode = mwFilter["offerTypeCode"]

    badetailPath = "/" + marketTypeCode + "/" + offerTypeCode + "/" + baseYearWeek + "/" + paymentTermCode + "/" + rdTermCode + "/" + containerTypeCode + "/" + polCode + podCode
    fullPath = srcPath + "/F9S_MW_BIDASK" + badetailPath
    response = json_creator_v2(fullPath)
    return jsonify(response)


@app.route(statsPath + '/filtered/marketindex/summary', methods=['POST'])
def post_rq_mw_mi():
    mwFilter = request.get_json()
    idxSubject = mwFilter["idxSubject"]
    idxCategory = mwFilter["idxCategory"]
    idxCd = mwFilter["idxCd"]
    interval = mwFilter["interval"]

    misumPath = "/" + idxSubject + "/" + idxCategory + "/" + idxCd + "/" + interval
    fullPath = srcPath + "/F9S_MI_SUM" + misumPath
    response = json_creator_v2(fullPath)
    return jsonify(response)


# @socketio.on('connect', namespace='/socket')
# def connect_web():
#     print('[INFO] Web client connectd: {}'.format(request.sid))
#
# @socketio.on('disconnect', namespace='/socket')
# def disconnect_web():
#     print('[INFO] Web client disconnectd: {}'.format(request.sid))


if __name__ == "__main__":
    WSGIRequestHandler.protocol_version = "HTTP/1.1"
    app.run(host='0.0.0.0', port=8080)
    # print('[INFO] Starting server at http://localhost:5000')
    # socketio.run(app=app, host='0.0.0.0', port=5000)
