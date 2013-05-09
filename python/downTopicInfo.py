#coding=utf-8
"""
Created on 20130419

@author han
"""
from __future__ import division

import urllib2
from BeautifulSoup import BeautifulSoup
import hanTime

def calReplyToWho(content):
    replyToName = u"blankOfName"
    if u"回复" == content[:2]:
        count = 3
        if content[3] == u"@":
            count = 4
        replyToName = content[count:content.find(u":",count)]
        replyToName = replyToName.replace(" ","")
    return replyToName

def storeDataToDict(latter, former, dataDict):
    if latter == former:
        return
    if not dataDict.has_key(former):
        dataDict[former] = dict()
        dataDict[former][latter] = 1
    else:
        if not dataDict[former].has_key(latter):
            dataDict[former][latter] = 1
        else:
            dataDict[former][latter] = dataDict[former][latter] + 1

def storeTimeToDict(latter, former, timeDict, timeInfo):
    if latter == former:
        return
    if not timeDict.has_key(former):
        timeDict[former] = dict()
        timeDict[former][latter] = list()
        timeDict[former][latter].append(timeInfo)

    else:
        if not timeDict[former].has_key(latter):
            timeDict[former][latter] = list()
            timeDict[former][latter].append(timeInfo)
        else:
            timeDict[former][latter].append(timeInfo)

def calRpply(dataDict):
    for i in dataDict.keys():
        temSum = 0.0
        for j in dataDict[i].keys():
            temSum += dataDict[i][j]
        for j in dataDict[i].keys():
            dataDict[i][j] = dataDict[i][j]/temSum

def calTime(timeDict):
    for i in timeDict.keys():
        temSum = 0
        for j in timeDict[i].keys():
            timeDict[i][j].sort()
            timeDict[i][j] = timeDict[i][j][len(timeDict[i][j])-1].currentMin - timeDict[i][j][0].currentMin
            temSum += timeDict[i][j]
        if temSum == 0:
            timeDict[i][j] = 0
        else:
            for j in timeDict[i].keys():
                timeDict[i][j] = timeDict[i][j]/temSum

def crossMat(dataDict, timeDict):
    mixDict = dict()
    for i in dataDict.keys():
        mixDict[i]=dict()
        for j in dataDict[i].keys():
            mixDict[i][j] = dataDict[i][j] + timeDict[i][j]
    return mixDict

def addDo(str):
    return ("$" + str)



def downTopicInfo(topicID, dataList, haveDownTopicIDList, getUserNameList):
    if topicID not in haveDownTopicIDList:
        url = "http://tieba.baidu.com/p/" + topicID
        try:
            urlopen = urllib2.urlopen(url)
            content = urlopen.read().decode('gb18030').encode('utf-8')
            urlopen.close()
        except:
            pass
        else:
            haveDownTopicIDList.append(topicID)
            soup = BeautifulSoup(content)
            topicTitle = [i.text for i in soup.findAll("title")]
            itemAuthor = [addDo(i['username']) for i in soup.findAll("img",onmouseout="hideTipPanel(this);")]
            replyAuthor = soup.findAll("div",{"class":"j_lzl_container core_reply_wrapper "})
            print len(replyAuthor)
            data = dict()
            timeDict = dict()

            for i in xrange(len(itemAuthor)):
                temSoup = BeautifulSoup(str(replyAuthor[i]))

                if itemAuthor[i] not in getUserNameList:
                        getUserNameList.append(itemAuthor[i])

                replyName = [addDo(j["username"]) for j in temSoup.findAll("a",{"class":"at"},{"target":"_blank"})]
                replyContent = [j.text for j in temSoup.findAll("span",{"class":"lzl_content_main"})]
                replyTime = [j.text for j in temSoup.findAll("span",{"class":"lzl_time"})]

                for j in xrange(min(len(replyName), len(replyContent))):
                    replyRealName = addDo(calReplyToWho(replyContent[j]))
                    if replyName[j] not in getUserNameList:
                        getUserNameList.append(replyName[j])
                    if replyRealName != u"$blankOfName":
                        storeDataToDict(replyRealName, replyName[j], data)
                        storeTimeToDict(replyRealName, replyName[j], timeDict, hanTime.hTime(replyTime[j]))
                    else:
                        storeDataToDict(itemAuthor[i], replyName[j], data)
                        storeTimeToDict(itemAuthor[i], replyName[j], timeDict, hanTime.hTime(replyTime[j]))
            calRpply(data)
            calTime(timeDict)
            mixDict = crossMat(data, timeDict)
            #mixDict['topicTitle'] = topicTitle[0]
            #mixDict = data
            mixDict['topicTitle'] = topicTitle[0]

            contentToRank = list()
            #for i in data.keys():
                #print i
                #data[i][u"_id"] = u"$" + i
            #    contentToRank.append(data[i])
            dataList.append([topicID, mixDict])
