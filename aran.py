#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import itchat, time
from itchat.content import *
from core import *

DEBUG = True

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    content =  msg['Text']
    fromUserId = msg['FromUserName']
    if DEBUG:
        print 'Content -->', content
        print 'fromUserId -->', fromUserId

    itchat.send(tuling_auto_reply(content, fromUserId), fromUserId)

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg['Text'](msg['FileName'])
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

@itchat.msg_register(FRIENDS)
def add_friend(msg):
    itchat.add_friend(**msg['Text'])
    itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])

@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if msg['isAt']:
        itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])

itchat.auto_login(True)
itchat.run()
