#coding=utf-8
"""
Created on 20130421

@author han
"""
from __future__ import division

import downTopicInfo
import downUserInfo
import couchdb
import Queue
import socket
import downWorker
import topicRank

socket.setdefaulttimeout(50)
server = couchdb.Server(r'http://localhost:5984')


def hanWebCal(infoList):
    userName = infoList[0]
    topicIDList = infoList[1:]
    userNameList = topicDown(topicIDList)
    userNameList.append(('$' + userName))
    userDown(userNameList)



def mainTopicDown(func, dataList, haveDownTopicIDList, toDownTopicID, getUserNameList):
    work_queue = Queue.Queue()
    for i in xrange(15):
        worker = downWorker.Worker(work_queue, func, dataList, haveDownTopicIDList, getUserNameList)
        worker.setDaemon(True)
        worker.start()
    for i in toDownTopicID:
        work_queue.put(i)
    work_queue.join()


def mainUserDown(func, dataList, haveDownUserNameList, toDownUserName):
    work_queue = Queue.Queue()
    for i in xrange(40):
        worker = downWorker.UWorker(work_queue, func, dataList, haveDownUserNameList)
        worker.setDaemon(True)
        worker.start()
    for i in toDownUserName:
        work_queue.put(i)
    work_queue.join()


def mapingDate(dataDict):
    sumOfDict = 0
    for i in dataDict.keys():
        if i != 'topicTitle' and i != '_id' and i != '_rev':
            sumOfDict += dataDict[i]
    for i in dataDict.keys():
        if i != 'topicTitle' and i != '_id' and i != '_rev':
            dataDict[i] /= sumOfDict

def topicDown(topicIDList):
    toDownTopicID = list()
    topicDB = server[u"topic_info"]
    for i in topicIDList:
        if not i in topicDB:
            toDownTopicID.append(i)

    haveDownList = list()
    dataList = list()
    getUserNameList = list()

    timesCount = 0
    while len(haveDownList) != len(toDownTopicID) and timesCount < 10:
        mainTopicDown(downTopicInfo.downTopicInfo, dataList, haveDownList, toDownTopicID, getUserNameList)
        timesCount += 1

    upDataList = list()
    for i in dataList:
        i[1] = topicRank.rank(i[1])
        mapingDate(i[1])
        i[1]['_id'] = i[0]
        upDataList.append(i[1])
    #for i in getUserNameList:
    #    print i
    for i in upDataList:
        print i
    topicDB.update(upDataList)
    return getUserNameList


def userDown(userNameList):
    toDownName = list()
    userInfoDB = server[u"user_info"]

    for i in userNameList:
        #ss = i[1:]
        if i not in userInfoDB:
            toDownName.append(i)

    haveDownList = list()
    dataList = list()

    timesCount = 0
    while len(haveDownList) != len(toDownName) and timesCount < 10:
        mainUserDown(downUserInfo.downUserInfo, dataList, haveDownList, toDownName)
        timesCount += 1

    upDataList = list()
    for i in dataList:
        temDict = dict()
        temDict['_id'] = i[0]
        for j in i[1]:
            temI = '$' + j
            temDict[temI] = i[1][j]
        upDataList.append(temDict)

    userInfoDB.update(upDataList)









