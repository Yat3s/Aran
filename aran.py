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


@chatcore.msg_register(FRIENDS)
def add_friend(msg):
    gender = u'小帅哥' if msg['User']['Sex'] == 1 else u'小美女'
    chatcore.add_friend(**msg['Text'])
    chatcore.send_msg(u'Hi\n, Wow又认识一位' + gender + u'，好开心~Mua', msg['RecommendInfo']['UserName'])

chatcore.auto_login(True)
chatcore.run()
