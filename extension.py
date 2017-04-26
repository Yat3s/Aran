#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, json, chatcore, io, time
from config import *
from utils import *

def auto_reply(msg, uid):
    if TULING_KEY:
        url = "http://www.tuling123.com/openapi/api"
        user_id = uid.replace('@', '')[:30]
        body = {'key': TULING_KEY, 'info': msg.encode('utf8'), 'userid': user_id}
        r = requests.post(url, data = body)
        respond = json.loads(r.text)
        result = ''
        code = respond['code']
        text = respond['text']
        if code == 100000: # TEXT
            result = text
        elif code == 200000: # URL
            result = text + '\n' + respond['url']
        elif code == 302000: # News list
            for item in respond['list']:
                result += u'【'+ item['source'] + u'】' + item['article'] + '\n' + item['detailurl'] + '\n\n'
        elif code == 308000: # Cook menu
            for item in respond['list']:
                result += u'【'+ item['name'] + u'】' + item['info'] + '\n' + item['detailurl'] + '\n\n'
        return result
    else:
        return u'我知道啦'

def process_command(content, from_user_id, from_user_name):
    isAdmin = from_user_name == ADMIN_NAME

    if u'自拍' in content:
        send_image(AVATAR, from_user_id)
        chatcore.send(u'嘻嘻ლ(＾ω＾ლ)，你猜猜哪个是我？', from_user_id)
        return True

    if u'加我加我' in content:
        chatcore.add_friend(from_user_id, verifyContent=u'嘻嘻，我可以添加你为好友吗？')
        chatcore.send(u'好的，我已经添加 ' + from_user_name + u' 为好友了', from_user_id)
        return True
    if u'自我介绍' in content or u'打个招呼' in content:
        chatcore.send(u'好的，我已经添加 ' + from_user_name + u' 为好友了', from_user_id)
        return True
    if u'色情网站' in content or u'黄色网站' in content:
        chatcore.send(u'你可以看看1024，tumblr，91，草榴，等等，如果想知道更多，可以联系我的主人哦嘻嘻ლ(＾ω＾ლ)', from_user_id)
        return True
    if u'黄图' in content:
        for url in SEX_PIC_URL:
            send_image(url, from_user_id)
            time.sleep(0.2)
        return True

    ## Administrator command
    if isAdmin:
        if u'[Search]' in content:
            keyword = content[content.index(u']') + 1:]
            print 'Search-->', keyword
            result = ''
            search_result = chatcore.search_friends(name = keyword)
            if isinstance(search_result, list):
                for item in search_result:
                    result += jsonify(item) + '\n'
            elif isinstance(search_result, dict):
                result += jsonify(search_result) + '\n'
            chatcore.send(u'没有搜索到结果' if result == '' else result, from_user_id)
            return True
        if u'叫爸爸' in content:
            chatcore.send(u'叶爸爸好~，叶爸爸有什么吩咐吗？', from_user_id)
            return True

        if u'[GroupSend]' in content :
            friends = chatcore.get_friends()
            group_send(friends, content[content.index(u']') + 1:])
            chatcore.send(u'已经给 ' + str(len(friends)) + u' 位好友发送了消息' )
            return True

        if u'[Info]' == content:
            chatcore.send(jsonify(chatcore.search_friends()), from_user_id)
            return True

        if u'[Friends]' == content:
            friends = chatcore.get_friends()
            friend_result = u'共计获取到 ' + str(len(friends)) + u' 位好友信息\n\n'
            for friend in friends:
                gender = u'男' if friend['Sex'] == 1 else u'女'
                friend_result += friend['NickName'] + ' ---- ' + friend['Alias'] + ' ---- ' + gender + '\n'
            chatcore.send(friend_result, from_user_id)
            print friend_result
            return True
    return False

def group_send(users, content):
    for user in users:
        chatcore.send(content, user['UserName'])

# Send image by URL
def send_image(url, from_user_id):
    r = requests.get(url, stream=True)
    imageStorage = io.BytesIO()
    for block in r.iter_content(1024):
        imageStorage.write(block)
    imageStorage.seek(0)
    chatcore.send_image(imageStorage, from_user_id)
