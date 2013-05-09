#coding=utf-8
"""
Created on 20130423

@author han
"""
import json, time
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import couchdb
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
import baiduTiebaProcessing

class temData:
    def __init__(self, url, title, userID):
        self.url = url
        self.title = title
        self.userID = userID


@csrf_exempt
def index(request):
    message = "yyyyy"
    if request.method == "POST":
        #print request.POST
        temDataArr = request.POST["topicId"].split("##")
        temDataArr.pop()
        #print temDataArr
        userID = request.POST["userID"]
        topicRankResult = baiduTiebaProcessing.getRankProcessing(temDataArr,userID)
        stem = dict()
        stem["topicId"] = temDataArr
        stem["userID"] = request.POST["userID"]
        SERVER = couchdb.Server('http://127.0.0.1:5984')
        resultInfoDB = SERVER["result_info"]
        resultDict = dict()

         
        resultDict["_id"] = request.POST["userID"]
        resultDict["originRank"] = temDataArr[1:]
        resultDict["chickList"] = list()
        resultDict["topicRankResult"] = topicRankResult

        if resultDict["_id"] in resultInfoDB:
            revT = resultInfoDB[resultDict["_id"]]['_rev']
            resultDict['_rev'] = revT
            resultInfoDB[resultDict["_id"]] = resultDict
        else:
            resultInfoDB.update([resultDict])

        message = json.dumps({"userID" : userID },indent=4)
        return HttpResponse(message, mimetype="application/json")
    elif request.method == "GET":
        userID = request.path.split("/")[2]
        print userID
        SERVER = couchdb.Server('http://127.0.0.1:5984')
        reDB = SERVER["recommended_topic"]
        dataList = list()
        if userID in reDB:
            for i in reDB[userID]["content"]:
                dataList.append(temData(i[1],i[2],userID))
        c = {'rows':dataList}
        c.update(csrf(request))
        return render_to_response('receiveInfo/index.html', c)

@csrf_exempt
def getchick(request):
    if request.method == "POST":
        print request.POST
        topicID = request.POST["topicID"]
        userID = request.POST["userID"]
        SERVER = couchdb.Server('http://127.0.0.1:5984')
        resultInfoDB = SERVER["result_info"]
        if userID in resultInfoDB:
            resultDict =  resultInfoDB[userID]
            print resultDict
            if topicID not in resultDict["chickList"]:
                print topicID
                resultDict["chickList"].append(topicID)
                resultInfoDB.save(resultDict)

        return HttpResponse("")
    elif request.method == "GET":
        return HttpResponse("hello!")





