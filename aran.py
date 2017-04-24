import itchat, time, requests, json
from itchat.content import *

tuling_key = "c697910a18b540d4a63838871ee9a671"
DEBUG = True

def tuling_auto_reply(msg, uid):
    if tuling_key:
        url = "http://www.tuling123.com/openapi/api"
        user_id = uid.replace('@', '')[:30]
        body = {'key': tuling_key, 'info': msg.encode('utf8'), 'userid': user_id}
        if DEBUG:
            print 'Body -->', body
        r = requests.post(url, data = body)
        respond = json.loads(r.text)

        print respond
        result = ''
        if respond['code'] == 100000:
            result = respond['text']
        print 'ROBOT:', result
        return result
    else:
        return 'test'

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
