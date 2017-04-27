# -*- coding:utf-8 -*-
import urllib
import urllib2
import re

page = 1
url = 'http://bter.com/trade/btc_cny'
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }

try:
    request = urllib2.Request(url,headers = headers)
    response = urllib2.urlopen(request)
    content = response.read().decode('utf-8')
    pattern = re.compile('<dt id="top_last_rate">(.*?)</dt>', re.S)
    items = re.findall(pattern,content)
    for item in items:
        print item
except urllib2.URLError, e:
    if hasattr(e,"code"):
        print e.code
    if hasattr(e,"reason"):
        print e.reason
