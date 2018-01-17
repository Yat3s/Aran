# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import requests, json


btc_url = 'https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
btc_r = requests.get(btc_url)
btc_respond = json.loads(btc_r.text)
btc_price = float(btc_respond['price'])

print btc_price

coin_text = 'eos'.upper()
baseurl = 'https://api.binance.com/api/v3/ticker/price?symbol='
coins = [coin_text + 'BTC', coin_text + "ETH",  coin_text + "USDT", ]

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
print result + str(price_cny)
