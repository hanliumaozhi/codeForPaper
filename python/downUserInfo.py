#coding=utf-8
"""
Created on 20130421

@author han
"""
import urllib2
from BeautifulSoup import BeautifulSoup


def downUserInfo(userName, dataList, haveDownUserNameList):
    if userName not in haveDownUserNameList:
        url = u"http://www.baidu.com/p/" + userName[1:] + u"?from=tieba"
        try:
            urlopen = urllib2.urlopen(url.encode("gbk"))
            content = urlopen.read()
            urlopen.close()
        except:
            pass
        else:
            soup = BeautifulSoup(content)
            try:
                a = soup.findAll("script")
                ss = a[9].text.split('":"')
                temCon = ss[2].replace('\/', '/')
            except :
                pass
            else:
                print userName
                haveDownUserNameList.append(userName)
                yy = BeautifulSoup(temCon.replace('"});', ''))
                reData = yy.findAll("div", {"class": "tieba-name"})
                level = yy.findAll("span", {"class": "level"})
                spTem = list()

                for i in xrange(len(reData)):
                    try:
                        ss = [reData[i].text, level[i].text[:-1]]
                    except:
                        ss = [reData[i].text, spTem[i-1][1]]
                        spTem.append(ss)
                    else:
                        spTem.append(ss)

                userInfoDict = dict()

                for i in spTem:
                    userInfoDict[i[0]] = int(i[1])
                userName = userName
                dataList.append([userName, userInfoDict])
