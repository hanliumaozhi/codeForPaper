# -*- coding: utf-8 -*-
"""
Created on 20130423

@author han
"""

import hanWebCal
import couchdb
import operator
import calSim
import SocketServer

#下面为猴子补丁 用于消除 错误的提示
from wsgiref import handlers

SocketServer.BaseServer.handle_error = lambda *args, **kwargs: None
handlers.BaseHandler.log_exception = lambda *args, **kwargs: None
#猴子补丁结束 

server = couchdb.Server(r'http://localhost:5984')
userSimDB = server['user_sim']
userNameDB = server['user_info']

def calUserSim(userA, userB):

    temA = userA + "$$" + userB
    temB = userB + "$$" +userA
    if temA in userSimDB:
        return userSimDB[temA]['sim']
    if temB in userSimDB:
        return userSimDB[temB]['sim']

    #userA = userA
    #userB = userB
    if (userA in userNameDB) and (userB in userNameDB):
        temName = userA + "$$" + userB
        #print ("@@@" + temName)
        simGoal = calSim.calSim(userNameDB[userA], userNameDB[userB])
        upSimDict = dict()
        upSimDict['_id'] = temName
        upSimDict['sim'] = simGoal
        userSimDB.update([upSimDict])
        return simGoal
    else:
        return 0



def getRankProcessing(infoList, userID):
    hanWebCal.hanWebCal(infoList)
    topicInfoDB = server['topic_info']

    toRankTopic = list()

    for i in infoList[1:]:
        if i in topicInfoDB:
            temData = 0.0
            for j in topicInfoDB[i]:
                if j != "topicTitle"and j != '_id' and j != '_rev':
                    
                    temData += (calUserSim(('$' + infoList[0]), j) * topicInfoDB[i][j])
            print temData
            toRankTopic.append([temData, i, topicInfoDB[i]['topicTitle']])

    toRankTopic.sort(key=operator.itemgetter(0), reverse=True)

    topicRankResult = list()
    for i in toRankTopic:
        topicRankResult.append(i[1])

    recommendedDB = server['recommended_topic']
    upRecommendedDict = dict()
    upRecommendedDict['_id'] = userID
    print userID
    upRecommendedDict['content'] = toRankTopic
    #upRecommendedDict.pop('_rev')
    if userID in recommendedDB:
        revT = recommendedDB[userID]['_rev']
        upRecommendedDict['_rev'] = revT
        recommendedDB[userID] = upRecommendedDict
    else:
        recommendedDB.update([upRecommendedDict])

    print "success"

    return topicRankResult






