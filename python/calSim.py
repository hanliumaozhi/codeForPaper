#coding=utf-8
"""
Created on 20130421

@author han
"""
from __future__ import division
import math
#import couchdb

#server = couchdb.Server(r'http://localhost:5984')


def calSim(peopleA, peopleB):
    #userSimDB = server['user_sim']
    meanA = 0
    for i in peopleA.keys():
        if i != '_id' and i != '_rev':
            meanA += peopleA[i]

    meanA /= len(peopleA.keys())

    meanB = 0
    for i in peopleB.keys():
        if i != '_id' and i != '_rev':
            meanB += peopleB[i]

    meanB /= len(peopleB.keys())

    numerator = 0

    for i in peopleA.keys():
        if i != '_id' and i != '_rev':
            if i in peopleB.keys():
                numerator += (peopleA[i] - meanA) * (peopleB[i] - meanB)


    temA = 0
    for i in peopleA.keys():
        if i != '_id' and i != '_rev':
            temA += math.pow((peopleA[i] - meanA), 2)

    temB = 0
    for i in peopleB.keys():
        if i != '_id' and i != '_rev':
            temB += math.pow((peopleB[i] - meanB), 2)

    denominator = math.sqrt(temA)*math.sqrt(temB)

    #print len(peopleA)
    #print len(peopleB)
    if denominator == 0:
        goal = 0
    else:
        #print "goal is not zero"
        goal = (numerator/denominator)
        #print goal
    #upSimDict = dict()
    #upSimDict['_id'] = peopleA['_id'] + "$$" + peopleB['_id']
    #upSimDict['sim'] = goal
    #userSimDB.update([upSimDict])
    return goal