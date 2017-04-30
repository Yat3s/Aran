#!/usr/bin/env python
# -*- coding: utf-8 -*-
import chatcore, time
from chatcore.content import *
from extension import *
from config import *
from utils import *

@chatcore.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    content =  msg['Text'].replace(NAME, '')
    from_user_id = msg['FromUserName']
    from_user_name = msg['User']['NickName']
    if DEBUG:
        print '[Private] ', from_user_name, '\t ---> ', content
    intercept_cmd = process_command(content, from_user_id, from_user_name)
    if not intercept_cmd:
        reply = auto_reply(content, from_user_id)
        chatcore.send(reply, from_user_id)
        if DEBUG:
            print '[Private] ', 'Aran', '\t ===> ', reply, '[CMD]' if intercept_cmd else '[Auto]'


@chatcore.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    content = msg['Content'].replace('@', '')
    from_user_id = msg['FromUserName']
    from_user_name = msg['ActualNickName']
    isAtMe = msg['isAt'] or NAME.lower() in content or NAME in content
    if DEBUG:
        print '[Group] ', from_user_name, '\t ---> ', content, ' (AtMe)' if isAtMe else ''

    if isAtMe:
        content = content.replace(NAME, '').replace(NAME.lower(), '')
        intercept_cmd = process_command(content, from_user_id, from_user_name)
        if not intercept_cmd:
            reply_prefix = '' if from_user_name == 'unknown' else '@' + from_user_name + ' '
            reply = reply_prefix + auto_reply(content, from_user_id)
            chatcore.send(reply, from_user_id)
            if DEBUG:
                print '[Group] ', 'Aran', '\t ===> ', reply, '[CMD]' if intercept_cmd else '[Auto]'


@chatcore.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg['Text'](msg['FileName']) ## Download File
    result = '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName']) ## Reply to sender
    return result

@chatcore.msg_register('Note', isGroupChat = True)
def get_note(msg):
    if any(s in msg['Text'] for s in (u'红包', u'转账', u'Red packet')):
        chatcore.send(u'@Yat3s， 叶爸爸有人发红包了，快抢~', msg['FromUserName'])


@chatcore.msg_register(FRIENDS)
def add_friend(msg):
    chatcore.add_friend(**msg['Text'])
    chatcore.send_msg(u'Hi\n, Wow又认识一位新朋友好开心，好开心~Mua', msg['RecommendInfo']['UserName'])

chatcore.auto_login(True)
chatcore.run()
