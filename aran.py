#!/usr/bin/env python
# -*- coding: utf-8 -*-
import itchat, time, io
from itchat.content import *
from core import *
from utils import *

DEBUG = True
NAME = 'Aran'
AVATAR = 'http://i4.buimg.com/4851/43ac151be1c2697e.jpg'
ADMIN_NAME = 'Yat3s'

def process_command(content, from_user_id, from_user_name):
    isAdmin = from_user_name == ADMIN_NAME

    if u'自拍' in content:
        send_image(AVATAR, from_user_id)
        itchat.send(u'嘻嘻ლ(＾ω＾ლ)，你猜猜哪个是我？', from_user_id)
        return True

    if u'加我加我' in content:
        itchat.add_friend(from_user_id, verifyContent=u'嘻嘻，我可以添加你为好友吗？')
        itchat.send(u'好的，我已经添加 ' + from_user_name + u' 为好友了', from_user_id)
        return True

    if isAdmin:
        if u'[Search]' in content:
            keyword = content[content.index(u']') + 1:]
            print 'Search-->', keyword
            result = ''
            search_result = itchat.search_friends(name = keyword)
            if isinstance(search_result, list):
                for item in search_result:
                    result += jsonify(item) + '\n'
            elif isinstance(search_result, dict):
                result += jsonify(search_result) + '\n'
            itchat.send(u'没有搜索到结果' if result == '' else result, from_user_id)
            return True

        if u'[GroupSend]' in content :
            friends = itchat.get_friends()
            group_send(friends, content[content.index(u']') + 1:])
            itchat.send(u'已经给 ' + str(len(friends)) + u' 位好友发送了消息' )
            return True

        if u'[Info]' == content:
            itchat.send(jsonify(itchat.search_friends()), from_user_id)
            return True

        if u'[Friends]' == content:
            friends = itchat.get_friends()
            friend_result = u'共计获取到 ' + str(len(friends)) + u' 位好友信息\n\n'
            for friend in friends:
                gender = u'男' if friend['Sex'] == 1 else u'女'
                friend_result += friend['NickName'] + ' ---- ' + friend['Alias'] + ' ---- ' + gender + '\n'
            itchat.send(friend_result, from_user_id)
            print friend_result
            return True
    return False


def group_send(users, content):
    for user in users:
        itchat.send(content, user['UserName'])

# Send image by URL
def send_image(url, from_user_id):
    r = requests.get(url, stream=True)
    imageStorage = io.BytesIO()
    for block in r.iter_content(1024):
        imageStorage.write(block)
    imageStorage.seek(0)
    itchat.send_image(imageStorage, from_user_id)


@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    print jsonify(msg)
    content =  msg['Text'].replace(NAME, '')
    from_user_id = msg['FromUserName']
    from_user_name = msg['User']['NickName']
    if DEBUG:
        print 'Content -->', content
        print 'fromUserId -->', from_user_id
    if not process_command(content, from_user_id, from_user_name):
        itchat.send(auto_reply(content, from_user_id), from_user_id)


@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    content = msg['Content'].replace('@', '')
    from_user_id = msg['FromUserName']
    from_user_name = msg['ActualNickName']
    if DEBUG:
        print from_user_name, ' ---> ', content

    if msg['isAt'] or NAME.lower() in content or NAME in content:
        content = content.replace(NAME, '').replace(NAME.lower(), '')
        print 'Group content -->', content
        if not process_command(content, from_user_id, from_user_name):
            reply_prefix = '' if from_user_name == 'unknown' else '@' + from_user_name + '\n'
            itchat.send(reply_prefix + auto_reply(content, from_user_id), from_user_id)


@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg['Text'](msg['FileName'])
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])


@itchat.msg_register(FRIENDS)
def add_friend(msg):
    gender = u'小帅哥' if msg['User']['Sex'] == 1 else u'小美女'
    itchat.add_friend(**msg['Text'])
    itchat.send_msg(u'Hi\n, Wow又认识一位' + gender + u'，好开心~Mua', msg['RecommendInfo']['UserName'])


itchat.auto_login(True)
itchat.run()
