# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import requests, json
import decimal
import time

headers = {'Referer': 'http://lbs.qq.com/webservice_v1/guide-gcoder.html', 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

def floatrange(start, stop, steps):
    return [start+float(i)*(stop-start)/(float(steps)-1) for i in range(steps)]

areas = {'Init': 'sss'}

for i in  floatrange(39.9, 40.015, 30):
    for j in floatrange(116.25, 116.4, 30):
        r = requests.get('http://apis.map.qq.com/ws/geocoder/v1/?location=' +str(i) + ',' + str(j) + '&get_poi=1&key=OB4BZ-D4W3U-B7VVO-4PJWW-6TKDJ-WPB77', headers = headers)
        respond = json.loads(r.text)
        address_reference =  respond['result']['address_reference']
        print str(i) + ', ' + str(j) + '==>' + respond['result']['address']
        if 'famous_area' in address_reference:
            famous_area = address_reference['famous_area']['title']
            areas[famous_area] = '(' + str(i) + ', ' + str(j) + ')'

            print str(i) + ', ' + str(j) +  ': ' + respond['result']['address'] + '==>' + famous_area
        else :
            print str(i) + ', ' + str(j)  + ': ' + respond['result']['address'] + '==> No famous area'
        time.sleep(0.05)
for area in areas.keys():
    with open('map.txt','a') as f:
        f.write(area.encode('utf-8') +' ' +  areas[area] + '\n')
