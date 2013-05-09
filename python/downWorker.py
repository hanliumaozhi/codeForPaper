# -*- coding: utf-8 -*-
"""
Created on 20130419

@author han
"""
__metaclass__=type

import threading


class Worker(threading.Thread):
    def __init__(self, work_queue, func, dataList, haveDownTopicIDList, getUserNameList):
        super(Worker, self).__init__()
        self.work_queue = work_queue
        self.func = func
        self.dataList = dataList
        self.haveDownTopicIDList = haveDownTopicIDList
        self.getUserNameList = getUserNameList

    def run(self):
        while True:
            try:
                elemt = self.work_queue.get()
                self.func(elemt, self.dataList, self.haveDownTopicIDList, self.getUserNameList)
            finally:
                self.work_queue.task_done()


class UWorker(threading.Thread):
    def __init__(self, work_queue, func, dataList, haveDownUserNameList):
        super(UWorker, self).__init__()
        self.work_queue = work_queue
        self.func = func
        self.dataList = dataList
        self.haveDownUserNameList = haveDownUserNameList

    def run(self):
        while True:
            try:
                elemt = self.work_queue.get()
                self.func(elemt, self.dataList, self.haveDownUserNameList)
            finally:
                self.work_queue.task_done()
