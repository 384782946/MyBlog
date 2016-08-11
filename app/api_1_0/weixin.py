# coding:utf-8

import urllib2,json,sys
from functools import wraps
from wechat_sdk import WechatBasic#,WechatConf
from flask import request,redirect
from . import api

wechat = WechatBasic(token='xiaojian',
        appid='wxa7efb4ea17e8d080',
        appsecret='943d32ed8153dedb33d10b91c77cb8e0')

def check_signature(func):
    """
    微信签名认证
    """
    @wraps(func)
    def decorated_function(*args,**kwargs):
        signature = request.args.get('signature','')
        timestamp = request.args.get('timestamp','')
        nonce = request.args.get('nonce','')
        echostr = request.args.get('echostr','default')

        print signature,timestamp,nonce
        if echostr != 'default':
            return echostr
        elif not wechat.check_signature(signature=signature, timestamp = timestamp,nonce=nonce):
            return u'signatue failed'
        return func(*args,**kwargs)
    return decorated_function

routing_map = {}

def dispatch(msg_type):
    def decorator(func):
        routing_map[msg_type] = func
        return func
    return decorator

@api.route('/weixin',methods=['GET','POST'])
def handle_wechat_request():
    """
    处理微信请求
    """
    if request.method == 'POST':
        wechat.parse_data(request.data)
        message = wechat.get_message()
        openid = message.source #用户id
        try:
            resp_func = routing_map[message.type]
            response = resp_func()
        except KeyError:
            response = 'success'
        return response
    else:
        return request.args.get('echostr','')
@dispatch('subscribe')
def subscribe_resp():
    return wechat.response_text(u'欢迎主人，我会陪你聊天，帮你查日历、天气、快递、车票、新闻、菜谱等，快跟我聊天吧！')

@dispatch('voice')
def voice_resp():
    message = wechat.get_message()
    return turing(message.recognition,message.source)

@dispatch('text')
def text_resp():
    message = wechat.get_message()
    return turing(message.content.encode('utf-8'),message.source)

def turing(msg,userid):
    data={'key':'18b33e26019a4beb943d16bd7d3388b1','info':msg ,'userid':userid }
    url = 'http://www.tuling123.com/openapi/api'
    headers = {'Content-Type':'application/json'}
    request = urllib2.Request(url=url,headers=headers,data=json.dumps(data))
    response = urllib2.urlopen(request)
    content = response.read()
    content = json.loads(content)
    if content:
        code = content['code']
        if code == 100000:#文字类
            return wechat.response_text(content['text'])
        elif code == 200000:#链接类
            articles = [{'title':content['text'],'description':u'链接','url':content['url']}]
            return wechat.response_news(articles)
        elif code == 302000:#新闻类
            articles = []
            for item in content['list'][:9]:
                row = {}
                row['title'] = item['article']
                row['description'] = item['source']
                row['url'] = item['detailurl']
                row['picurl'] = item['icon']
                articles.append(row)
            return wechat.response_news(articles)
        elif code == 308000:#菜谱类
            articles = []
            for item in content['list'][:9]:
                row = {}
                row['title'] = item['name']
                row['description'] = item['info']
                row['url'] = item['detailurl']
                row['picurl'] = item['icon']
                articles.append(row)
            return wechat.response_news(articles)
        else:#其他
            return wechat.response_text(content['text'])
    else:
        return wechat.response_text(u'说嘞啥？我都懵逼了！')
