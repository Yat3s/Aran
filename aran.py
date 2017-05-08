#!/usr/bin/env python
# -*- coding: utf-8 -*-
import chatcore, time, re, time, os
from chatcore.content import *
from extension import *
from config import *
from utils import *
from face import *

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


@chatcore.msg_register([PICTURE], isGroupChat = True)
def download_files(msg):
    fileName = 'assets/' + msg['FileName']
    print '[Picture] --->', fileName
    msg['Text'](fileName) ## Download File
    result = u'我更喜欢看帅哥/美女的照片哦，嘻嘻~'
    faceCount = detectFaceAndEyes(fileName)
    if faceCount > 0 :
        print '[Picture] --->', fileName, 'Detect ' + str(faceCount) + 'face(s)'
        chatcore.send_image('assets/processed_img.jpg', msg['FromUserName'])
        result = u'发现了' + str(faceCount) + u'张美丽帅气的脸蛋儿，(*^__^*) 嘻嘻……' ## Reply to sender
    os.remove(fileName)
    return result

@chatcore.msg_register('Note', isGroupChat = True)
def get_note(msg):
    note = msg['Text']
    print 'Note -->', note

    joined_names = get_note_name(note, 'joined')
    if get_note_name(note, 'joined'):
        chatcore.send(u'欢迎欢迎 @' + get_note_name(note, 'joined')[0] + u' 加入群，有什么吩咐可以@我哦，嘻嘻~', msg['FromUserName'])
    elif get_note_name(note, 'to the group'):
        chatcore.send(u'欢迎欢迎 @' + get_note_name(note, 'to the group')[0] + u' 加入群，有什么吩咐可以@我哦，嘻嘻~', msg['FromUserName'])
    elif get_note_name(note, 'has recalled'):
        print jsonify(msg)
        chatcore.send(u'@' + get_note_name(note, 'has recalled')[0] + u' 你撤回了什么!!!', msg['FromUserName'])

    if any(s in msg['Text'] for s in (u'红包', u'转账', u'Red packet')):
        chatcore.send(u'@Yat3s， 叶爸爸有人发红包了，快抢~', msg['FromUserName'])

def get_note_name(content, keyword):
    pattern = re.compile('"(.*?)" ' + keyword, re.S)
    return re.findall(pattern, content)

@chatcore.msg_register(FRIENDS)
def add_friend(msg):
    chatcore.add_friend(**msg['Text'])
    chatcore.send_msg(u'Hi\n, Wow又认识一位新朋友好开心，好开心~Mua', msg['RecommendInfo']['UserName'])

chatcore.auto_login(True)
chatcore.run()
