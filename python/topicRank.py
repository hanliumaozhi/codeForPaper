#coding=utf-8
"""
Created on 20130421

@author han
"""
from __future__ import division
import copy


def sumOfItem(dicta, item):
    sumM = 0
    for i in dicta[item].keys():
        sumM += dicta[item][i]
    return sumM


def rank(topicInfo):
    toRankContent = dict()

    topicTitle = topicInfo['topicTitle']
    topicInfo.pop('topicTitle')

    for i in topicInfo.keys():
        toRankContent[i] = 1/len(topicInfo.keys())

    for count in xrange(50):
        temRank = copy.deepcopy(toRankContent)
        for i in topicInfo.keys():

            summation = 0
            for j in topicInfo.keys():
                if i != j:
                    if not topicInfo[j].has_key(i):
                        pass
                    else:
                        summation += topicInfo[j][i]/(sumOfItem(topicInfo, j))*temRank[j]
            toRankContent[i] = 0.15/15 + 0.85*summation

    toRankContent['topicTitle'] = topicTitle
    return toRankContent


