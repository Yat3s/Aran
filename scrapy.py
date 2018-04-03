# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import requests, json

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

def getOkexMessage():
    url = 'http://wexiner.com/wechat/getMsg'
    r = requests.get(url)
    respond = json.loads(r.text)
    msg = u'最近的情报消息如下：\n\n'
    for item in respond:
        msg = msg + u'- 【' + item['content'] + u'】 -- ' + item['created_at'][5:-3] + '\n'
    msg = msg + '\n 对我说“情报”获取最近的消息哦嘻嘻~'
    return msg

def sendOkexMessage(content):
    url = 'http://wexiner.com/wechat/setMsg'
    r = requests.post(url, data = {'content':content, 'type':'0'})
    print r.text

def load_coin_info(coin_text):
    btc_url = 'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
    btc_r = requests.get(btc_url)
    btc_respond = json.loads(btc_r.text)
    btc_price = float(btc_respond['price'])

    coin_text = coin_text.upper()
    baseurl = 'https://api.binance.com/api/v3/ticker/price?symbol='
    coins = [coin_text + 'BTC', coin_text + "ETH",  coin_text + "USDT"]
    result = ''
    price_cny = 0.0
    for coin in coins:
        r = requests.get(baseurl + coin)
        if 'code' not in r.text:
            respond = json.loads(r.text)
            name = respond['symbol']
            price = respond['price']
            if 'BTC' in name :
                if coin == 'BTCUSDT':
                    price_cny = float(price) * 6.5
                else:
                    price_cny = btc_price * float(price) * 6.5
            result = result + name + '==>' + price + "\n" ;
    if not result:
         result = u'未找到'+coin_text + u'相关数据'
    return result + u'约¥' + str(price_cny) + u'元'

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
