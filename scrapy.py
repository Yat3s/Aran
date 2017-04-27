# -*- coding:utf-8 -*-
import urllib
import urllib2
import re

page = 1
user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = { 'User-Agent' : user_agent }

def scrapy_data(url):
    result = []
    try:
        request = urllib2.Request(url,headers = headers)
        response = urllib2.urlopen(request)
        content = response.read().decode('gbk')
        pattern = re.compile('<article class="excerpt">.*?<img src="(.*?)" alt=.*?', re.S)
        items = re.findall(pattern,content)
        return items
    except urllib2.URLError, e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reason
    return result

#     <ul class="product01">
#   <li>
#   <a href="http://mvpday.com/av/19.html" class="pic" title="波多野结衣"><img src="/i/boduoyejieyi.jpg" alt="波多野结衣"></a>
#   <a href="http://mvpday.com/av/19.html" class="pic" title="波多野结衣"><h2>波多野结衣</h2></a>
#   <span>人气:23689</span>
# </li>
#   </ul>

def scrapy_av():
    url = 'http://mvpday.com/av'
    result = [[]]
    try:
        request = urllib2.Request(url,headers = headers)
        response = urllib2.urlopen(request)
        content = response.read().decode('gbk')
        pattern = re.compile('<ul class="product01">.*?class="pic" title="(.*?)".*?<img src="(.*?)" alt=', re.S)
        items = re.findall(pattern,content)
        return items
    except urllib2.URLError, e:
        if hasattr(e,"code"):
            print e.code
        if hasattr(e,"reason"):
            print e.reason
    return result
