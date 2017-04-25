#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itchat, time, io
from itchat.content import *
from core import *

DEBUG = True
NAME = 'Aran'
AVATAR = 'http://i4.buimg.com/4851/43ac151be1c2697e.jpg'
ADMIN_USER_ID = '@8beb882e90aa7e5eb904f2b5f7ab0f411b3f85e63c00bd104bbab5589ee4bd01'

def group_send(friend_array, content):
    for friend in friend_array:
        itchat.send(content, friend['UserName'])

def process_command(content, from_user_id):
    if u'自拍' in content:
        send_image(AVATAR, from_user_id)
        itchat.send(u'嘻嘻，你猜猜哪个是我？', from_user_id)
        return True
    if u'群发' in content and from_user_id == ADMIN_USER_ID:
        group_send(itchat.get_friends(), content[content.index(u'群发：'):])
        return True
    return False

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    content =  msg['Text'].replace(NAME, '')
    from_user_id = msg['FromUserName']
    if DEBUG:
        print 'Content -->', content
        print 'fromUserId -->', from_user_id
    if not process_command(content, from_user_id):
        itchat.send(auto_reply(content, from_user_id), from_user_id)

@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    if DEBUG:
        print 'ActualNickName -->', msg['ActualNickName']

    content = msg['Content'].replace('@', '')
    from_user_id = msg['FromUserName']
    from_user_name = msg['ActualNickName']

    if msg['isAt'] or NAME.lower() in content or NAME in content:
        content = content.replace(NAME, '').replace(NAME.lower(), '')
        if not process_command(content, from_user_id):
            reply_prefix = '' if from_user_name == 'unknown' else '@' + from_user_name + '\n'
            itchat.send(reply_prefix + auto_reply(content, from_user_id), from_user_id)

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg['Text'](msg['FileName'])
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

@itchat.msg_register(FRIENDS)
def add_friend(msg):
    itchat.add_friend(**msg['Text'])
    itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])

def send_image(url, from_user_id):
    r = requests.get(url, stream=True)
    imageStorage = io.BytesIO()
    for block in r.iter_content(1024):
        imageStorage.write(block)
    imageStorage.seek(0)
    itchat.send_image(imageStorage, from_user_id)

itchat.auto_login(True)
itchat.run()
