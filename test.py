# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import requests, json

content = u'你好明天'
keys = [u'开多', u'开空', u'涨',u'跌',u'震荡', u'今晚', u'明天', u'1/10']
find = False
for key in keys:
    if key in content:
        print 'find' + key
        find = True
        break
if find:
    print 'Ok'
