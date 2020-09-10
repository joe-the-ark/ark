from django.conf import settings

from Crypto.Cipher import AES
from .exceptions import APIError

import requests
import json
import base64
import random
import string
import hashlib
import time


unpad = lambda s: s[:-ord(s[len(s)-1:])]


def js_code_to_session(code):
    appid = settings.WECHAT['miniapp']['appid']
    secret = settings.WECHAT['miniapp']['secret']

    url = 'https://api.weixin.qq.com/sns/jscode2session?appid={0}&secret={1}&js_code={2}&grant_type=authorization_code'.format(appid, secret, code)
        
    res = requests.get(url)
    res = json.loads(res.text)
    if 'openid' not in res:
        raise APIError(400, '小程序登录错误', 1)

    unionid = res['unionid'] if 'unionid' in res else ''
    openid = res['openid']
    session_key = res['session_key']

    return unionid, openid, session_key


def decode_user_info(session_key, encrypted_data, iv):
    appid = settings.WECHAT['miniapp']['appid']

    session_key = base64.b64decode(session_key)
    encrypted_data = base64.b64decode(encrypted_data)
    iv = base64.b64decode(iv)

    cipher = AES.new(session_key, AES.MODE_CBC, iv)

    data = unpad(cipher.decrypt(encrypted_data)).decode('utf-8')
    user_info = json.loads(data)

    if user_info['watermark']['appid'] != appid:
        raise APIError(400, '小程序用户信息获取错误', 2)

    return user_info


def get_pa_auth_url(url):
    url = settings.WECHAT['domain'] + url
    url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&scope=snsapi_userinfo" % (settings.WECHAT['public_account']['appid'], url)
    return url


def get_pa_user(open_id, access_token):
    get_user_info_url = 'https://api.weixin.qq.com/sns/userinfo'
    user_info_params = {
        'access_token': access_token,
        'openid': open_id
    }
    res = requests.get(url=get_user_info_url, params=user_info_params)
    res.encoding = 'utf-8'
    user_info = json.loads(res.text)
    
    return user_info


def get_access_token(code):
    from .models import AccessToken
    from time import time

    appid = settings.WECHAT['public_account']['appid']
    secret = settings.WECHAT['public_account']['secret']

    now = time()
    token = AccessToken.objects.filter(appid=appid, code=code, expire_time__gt=now).first()

    if token:
        return token.openid, token.access_token

    access_token_params = {
        'appid': appid,
        'secret': secret,
        'code': code,
        'grant_type': 'authorization_code'
    }
    get_access_token_url = 'https://api.weixin.qq.com/sns/oauth2/access_token'
    response = requests.get(
        url=get_access_token_url,
        params=access_token_params)
    response.encoding = 'utf-8'

    response = json.loads(response.text)

    token = AccessToken.objects.create(appid=appid, code=code,
        access_token=response['access_token'], expire_time=now+response['expires_in'],
        unionid=response['unionid'], openid=response['openid'])

    return token.openid, token.access_token


def get_js_ticket(current_url):
    from .models import PublicAccountTicket

    import time
    import random
    import json
    import string
    import hashlib

    now = time.time()
    ticket = PublicAccountTicket.objects.filter(expire_time__gt=now).first()

    appid = settings.WECHAT['public_account']['appid']
    secret = settings.WECHAT['public_account']['secret']

    if ticket:
        access_token = ticket.access_token
        jsapi_ticket = ticket.jsapi_ticket
    else:
        access_token_params = {
            'appid': appid,
            'secret': secret,
            'grant_type': 'client_credential'
        }
        get_access_token_url = 'https://api.weixin.qq.com/cgi-bin/token'

        response = requests.get(
            url=get_access_token_url,
            params=access_token_params)
        response.encoding = 'utf-8'
        response = json.loads(response.text)

        access_token = response['access_token']
        get_jsapi_ticket_url = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={0}&type=jsapi'.format(
            access_token)

        jsapi_response = requests.get(url=get_jsapi_ticket_url)
        jsapi_response.encoding = 'utf-8'
        jsapi_response = json.loads(jsapi_response.text)
        jsapi_ticket = jsapi_response['ticket']
        expires_in = jsapi_response['expires_in']

        PublicAccountTicket.objects.create(access_token=access_token, jsapi_ticket=jsapi_ticket, expire_time=now+expires_in)

    noncestr = ''.join(random.sample(string.ascii_letters + string.digits, 8))

    timestamp = int(time.time())

    string1 = 'jsapi_ticket={0}&noncestr={1}&timestamp={2}&url={3}'.format(
        jsapi_ticket, noncestr, timestamp, current_url)
    signature = hashlib.sha1(string1.encode('utf-8')).hexdigest()

    params = {
        'appId': appid,
        'timestamp': timestamp,
        'nonceStr': noncestr,
        'signature': signature,
    }
    return params


def _make_sign(params):
    """ 微信签名算法: https://pay.weixin.qq.com/wiki/doc/api/jsapi.php?chapter=4_3 """
    keys = [k for k in params if k]
    keys.sort()
    stringA = '&'.join(['%s=%s' % (k, str(params[k])) for k in keys])
    stringA += '&key=' + settings.WECHAT['pay']['pay_secret']
    sign = hashlib.md5(stringA.encode('utf-8')).hexdigest().upper()
    return sign

def _make_xml(params, *args):
    result = '<xml>'

    for k, v in params.items():
        result += '<%s>' % k
        result += '<![CDATA[%s]]>' % json.dumps(v) if k in args else str(v) 
        result += '</%s>' %k

    result += '</xml>'
    return result

_make_noncestr = lambda: ''.join(random.sample(string.ascii_letters + string.digits, 8))

def pay(channel, open_id, order_id, price, company, category, client_ip):
    import xml.etree.ElementTree as ET

    api_url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'

    params = {}
    if channel == 'pa':
        appid = settings.WECHAT['public_account']['appid']
    elif channel == 'ma':
        appid = settings.WECHAT['miniapp']['appid']

    print(appid)
    print(settings.WECHAT['pay']['mch_id'])
    print('settings.WECHAT')

    params['appid'] = appid
    params['sign_type'] = sign_type = 'MD5'
    params['mch_id'] = settings.WECHAT['pay']['mch_id']
    params['nonce_str'] = nonce_str = _make_noncestr()

    params['body'] = '%s-%s' % (company, category)
    params['out_trade_no'] = order_id
    params['total_fee'] = int(price * 100)
    params['spbill_create_ip'] = client_ip

    params['notify_url'] = settings.WECHAT['domain'] + '/wechat/pay/confirm/'
    params['trade_type'] = 'JSAPI'
    params['openid'] = open_id

    params['sign'] = sign = _make_sign(params)

    post_body = _make_xml(params)
    print (post_body)

    text = requests.post(api_url, data=post_body).content
    root = ET.fromstring(text)
    print (text)

    result = {}
    return_msg = root.find('return_msg').text
    print (return_msg)
    if return_msg == 'OK':
        result['appId'] = root.find('appid').text
        result['timeStamp'] = str(int(time.time()))
        result['nonceStr'] = root.find('nonce_str').text
        result['package'] = 'prepay_id='+root.find('prepay_id').text
        result['signType'] = sign_type
        result['paySign'] = _make_sign(result)

    return result
