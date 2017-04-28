#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, json, chatcore, io, time, random
from config import *
from utils import *
from scrapy import *

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
    isAdmin = (from_user_name == ADMIN_NAME)

    if u'自拍' in content:
        send_image(AVATAR, from_user_id)
        chatcore.send(u'嘻嘻ლ(＾ω＾ლ)，你觉得我好看吗？', from_user_id)
        return True

    if u'加我加我' in content:
        chatcore.add_friend(from_user_id, verifyContent=u'嘻嘻，我可以添加你为好友吗？')
        chatcore.send(u'好的，我已经添加 ' + from_user_name + u' 为好友了', from_user_id)
        return True
    if u'自我介绍' in content or u'打个招呼' in content or 'help' in content:
        chatcore.send(GROUP_HELP, from_user_id)
        return True
    if u'色情网站' in content or u'黄色网站' in content:
        chatcore.send(u'你可以看看1024，tumblr，91，草榴，等等，如果想知道更多，可以联系我爸爸哦嘻嘻ლ(＾ω＾ლ)', from_user_id)
        return True
    if u'Draw' in content or u'draw' in content:
        drawPic(content[4:])
        chatcore.send_image(fileDir='t.png', toUserName=from_user_id)
        return True
    if u'黄图' in content or u'黄片' in content:
        for url in SEX_PIC_URL:
            send_image(url, from_user_id)
        return True
    if u'[Alarm]' in content or u'提醒我' in content:
        time = content[content.index(u'提醒我') + 3:]
        chatcore.send(u'好的主人，已经帮你开启: ' + time, from_user_id)
        return True
    if u'头像' in content:
        chatcore.send_image(chatcore.get_head_img(chatroomUserName=from_user_id), from_user_id)
        return True

    if u'小萌' in content:
        chatcore.send(u'小萌是全世界最美的女孩子~Mua', from_user_id)
        return True


    ## Administrator command
    if u'美女图' in content:
        if isAdmin:
            data = scrapy_data(u'http://mvpday.com/go/meizitu')
            send_image(data[random.randrange(0, len(data)-1)], from_user_id)
        else:
            chatcore.send(u'这个指令爸爸说了不能给别人用哦TT', from_user_id)
        return True

    if u'女优' in content:
        if isAdmin:
            data = scrapy_av()
            random_item = random.randrange(0, len(data)-1)
            send_image('http://mvpday.com' + data[random_item][1], from_user_id)
            chatcore.send(u'这个女优是：' + data[random_item][0], from_user_id)
        else:
            chatcore.send(u'这个指令爸爸说了不能给别人用哦TT', from_user_id)
        return True
    if u'[Search]' in content:
        if isAdmin:
            keyword = content[content.index(u']') + 1:]
            result = ''
            search_result = chatcore.search_friends(name = keyword)
            if isinstance(search_result, list):
                for item in search_result:
                    result += jsonify(item) + '\n'
            elif isinstance(search_result, dict):
                result += jsonify(search_result) + '\n'
            chatcore.send(u'没有搜索到结果' if result == '' else result, from_user_id)
        else:
            chatcore.send(u'这个指令爸爸说了不能给别人用哦TT', from_user_id)
        return True
    if u'叫爸爸' in content:
        if isAdmin:
            chatcore.send(u'叶爸爸好~，爸爸有什么吩咐吗？', from_user_id)
        else:
            chatcore.send(u'这个指令爸爸说了不能给别人用哦TT', from_user_id)
        return True

    if u'[GroupSend]' in content :
        if isAdmin:
            friends = chatcore.get_friends()
            group_send(friends, content[content.index(u']') + 1:])
            chatcore.send(u'已经给 ' + str(len(friends)) + u' 位好友发送了消息' )
        else:
            chatcore.send(u'这个指令爸爸说了不能给别人用哦TT', from_user_id)
        return True

    if u'Info' == content:
        if isAdmin:
            chatcore.send(jsonify(chatcore.search_friends()), from_user_id)
        else:
            chatcore.send(u'这个指令爸爸说了不能给别人用哦TT', from_user_id)
        return True

    if u'Friends' in content:
        if isAdmin:
            friends = chatcore.get_friends()
            friend_result = u'共计获取到 ' + str(len(friends)) + u' 位好友信息\n\n'
            for friend in friends:
                gender = u'男' if friend['Sex'] == 1 else u'女'
                friend_result += friend['NickName'] + ' ---- ' + friend['Alias'] + ' ---- ' + gender + '\n'
            chatcore.send(friend_result, from_user_id)
        else:
            chatcore.send(u'这个指令爸爸说了不能给别人用哦TT', from_user_id)
        return True
    if u'每日福利' in content:
        if isAdmin:
            chatcore.send(u"嘻嘻~稍等", from_user_id)
            chatcore.send_video(u'170427-153615.mp4', from_user_id)
        else:
            chatcore.send(u'这个指令爸爸说了不能给别人用哦TT', from_user_id)
        return True

    if u'开放权限' in content:
        if isAdmin:
            OPEN_AUTH = True
            chatcore.send(u"叶爸爸，权限已经开放啦~", from_user_id)
        else:
            chatcore.send(u'这个指令爸爸说了不能给别人用哦TT', from_user_id)
        return True

    if u'关闭权限' in content:
        if isAdmin:
            OPEN_AUTH = False
            chatcore.send(u"叶爸爸，权限已经关闭了~", from_user_id)
        else:
            chatcore.send(u'这个指令爸爸说了不能给别人用哦TT', from_user_id)
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
