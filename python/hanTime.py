# -*- coding: utf-8 -*-
"""
Created on 20130420

@author han
"""
__metaclass__=type

import re

class hTime:
    def __init__(self, timeStr):
        self.calculate(timeStr)

    def calculate(self, timeStr):
        tem = re.split('[-: ]', timeStr)
        self.year = int(tem[0])
        self.month = int(tem[1])
        self.day = int(tem[2])
        self.hour = int(tem[3])
        self.minute = int(tem[4])
        self.currentMin = (self.hour * 60 + self.minute)
        self.timeStr = timeStr

    def equalDay(self, otherHTime):
        if self.day == otherHTime.day:
            return True
        return False

    def __sub__(self, other):
        return abs(self.currentMin - other.currentMin)

    def __cmp__(self, other):
        if self.currentMin > other.currentMin:
            return 1
        elif self.currentMin == other.currentMin:
            return 0
        elif self.currentMin < other.currentMin:
            return -1

    def __str__(self):
        return self.timeStr

    def show(self):
        #print self.currentMin
        pass






