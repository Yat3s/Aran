#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests, json, chatcore, io, time, random, re
from config import *
from utils import *
from scrapy import *

lastSequenceId = ''
def auto_reply(msg, uid):
    if TULING_KEY:
        # url = "http://www.tuling123.com/openapi/api"
        # user_id = uid.replace('@', '')[:30]
        # body = {'key': TULING_KEY, 'info': msg.encode('utf8'), 'userid': user_id}
        # r = requests.post(url, data = body)
        # respond = json.loads(r.text)
        # result = ''
        # code = respond['code']
        # text = respond['text']
        # if code == 100000: # TEXT
        #     result = text
        # elif code == 200000: # URL
        #     result = text + '\n' + respond['url']
        # elif code == 302000: # News list
        #     for item in respond['list']:
        #         result += u'【'+ item['source'] + u'】' + item['article'] + '\n' + item['detailurl'] + '\n\n'
        # elif code == 308000: # Cook menu
        #     for item in respond['list']:
        #         result += u'【'+ item['name'] + u'】' + item['info'] + '\n' + item['detailurl'] + '\n\n'
        # return result
        global lastSequenceId
        if msg.isdigit() :
            if int(msg) > 0 and int(msg) < 6:
                return score(msg, lastSequenceId)
            else:
                return u'你评的这个分有点飘吧....'
        else:
            url = "http://jnlu.jd.com/jnlu/getAiNlu.ajax"
            params = {'sessionId': lastSequenceId, 'inputText' : msg.encode('utf8')}
            headers = {'Cookie': 'sso.jd.com=39c9b9883e2545aea9c5ed5792dcde83;'}
            r = requests.post(url, data = params, headers = headers)
            respond = json.loads(r.text)
            result = msg
            data = respond['data']
            if data:
                type = data['type']
                lastSequenceId = data['sequenceId']
                if type == 'TYPE_STRING':
                    result = data['responses']['string']
                elif type == 'TYPE_MEDIA':
                    result = u'[Media]' + data['responses']['string'] + '\n' + data['responses']['media']
                return result
    else:
        return u'我知道啦'

def score(score, id):
    url = "http://jnlu.jd.com/jnlu/userScore.ajax"
    params = {'sequenceId': id, 'score' : score}
    headers = {'Cookie': 'sso.jd.com=39c9b9883e2545aea9c5ed5792dcde83;'}
    r = requests.post(url, data = params, headers = headers)
    respond = json.loads(r.text)
    return (u'么么哒~ 谢谢你的评分(' + score + u')，请拿好你的小票：\n' + id) if respond['success'] else u'评分失败'

## return: if True consume this action.
def process_command(content, from_user_id, from_user_name):
    isAdmin = (from_user_name == ADMIN_NAME)
    content = content.lstrip()
    ## Face emoji
    if re.match('\[\S+\]\Z', content):
        chatcore.send(content, from_user_id)
        return True

    if u'自拍' in content:
        send_image(AVATAR, from_user_id)
        chatcore.send(u'嘻嘻ლ(＾ω＾ლ)，你觉得我好看吗？[Shy]', from_user_id)
        return True

    if u'你的爸爸' in content:
        chatcore.send(u'我的爸爸是风流倜傥的老叶子同学~嘻嘻[Hey]', from_user_id)
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
        chatcore.send(u'好的爸爸，已经帮你开启: ' + time, from_user_id)
        return True
    if u'头像' in content:
        chatcore.send_image(chatcore.get_head_img(chatroomUserName=from_user_id), from_user_id)
        return True

    if u'梁肠美吗' in content:
        chatcore.send(u'梁肠是全球最美的少女，鼻子最漂亮，身材最棒~嘻嘻', from_user_id)
        return True
    if u'群信息' in content or u'群成员' in content:
        reply = ''
        group_info = chatcore.update_chatroom(from_user_id)
        chat_room_owner_id = group_info['ChatRoomOwner']
        chatRoomOwnerName = ''
        memberList = group_info['MemberList']
        if group_info['NickName']:
            reply += u'群名称：' + group_info['NickName'] + u'\n----------------\n群成员：(' + str(len(memberList)) +')\n'
        for member in memberList:
            if chat_room_owner_id == member['UserName']:
                chatRoomOwnerName = member['NickName']
            reply += member['NickName'] + u'\n'
        reply += u'----------------\n群主：' + chatRoomOwnerName
        chatcore.send(reply, from_user_id)
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
    if u'Search' in content:
        if isAdmin:
            keyword = content[content.index(u'Search') + 6:]
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
    if u'叫爸爸' in content or u'叫爸爸' in content:
        if isAdmin:
            chatcore.send(u'叶爸爸好~，爸爸有什么吩咐吗？', from_user_id)
        else:
            chatcore.send(u'这个指令爸爸说了不能给别人用哦TT', from_user_id)
        return True

    if u'GroupSend' in content :
        if isAdmin:
            friends = chatcore.get_friends()
            group_send(friends, content[content.index(u'GroupSend') + 9:])
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
