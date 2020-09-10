from django.conf import settings

from .exceptions import APIError
from .decorators import api, params, returns, errors, comments, user_required

import random
import string
import datetime
import hashlib
import uuid
import pytz
import requests


_make_password = lambda _: hashlib.sha256(_.encode('utf-8')).hexdigest()
_make_name = lambda _='': _ + uuid.uuid4().hex


@api
def send_sms_code(phone):
    from .models import SMSCode
    from . import sms

    if not phone:
        raise APIError(400, '手机号为空', 1)

    code = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    #code = '6666'

    SMSCode.objects.filter(phone=phone, status=0).update(status=-1)
    sms_code = SMSCode.objects.create(phone=phone, code=code)

    return sms.send_sms(phone, sms_code.code)


def verify_sms_code(phone, code):
    from .models import SMSCode

    sms_code = SMSCode.objects.filter(phone=phone, code=code, status=0).first()
    if not sms_code:
        return False

    SMSCode.objects.filter(phone=phone, status=0).update(status=-1)
    now = datetime.datetime.now()

    return sms_code.create_time.timetuple() > (now - datetime.timedelta(minutes=10)).timetuple()


def bind_phone(token, phone, code):
    from .models import Token

    t = Token.objects.filter(token=token, status=0).first()
    if not t:
        raise APIError(401, '登录过期', 1)

    if not phone:
        raise APIError(400, '手机号为空', 2)

    if not verify_sms_code(phone, code):
        raise APIError(401, '验证码错误', 3)

    user = t.user
    if user.phone:
        raise APIError(400, '已有绑定手机', 4)

    user.phone = phone
    user.save()
    return True


def _get_user(token):
    from .models import Token

    t = Token.objects.filter(token=token, status=0).first()
    if not t:
        raise APIError(401, '登录过期', 1)

    return t.user


def clean_dict(raw, *args):
    return { arg: raw[arg] if arg in raw else '' for arg in args}


def clean_nickname(nickname):
    clean_nickname = nickname.encode('raw_unicode_escape').decode('utf-8')
    return clean_nickname


def get_miniapp_user(code, encrypted_data, iv):
    from . import wechat
    from .models import MiniappTicket, MiniappUser, WechatUser, User

    ticket = MiniappTicket.objects.filter(code=code).last()
    if not ticket:
        union_id, open_id, session_key = wechat.js_code_to_session(code)
        ticket = MiniappTicket.objects.create(code=code, union_id=union_id, open_id=open_id, session_key=session_key)

    open_id = ticket.open_id
    session_key = ticket.session_key

    miniapp_user = MiniappUser.objects.filter(open_id=open_id).first()
    if miniapp_user:
        return miniapp_user

    user_info = wechat.decode_user_info(session_key, encrypted_data, iv)

    union_id = user_info['unionId'] if 'unionId' in user_info else ''
    wechat_user = WechatUser.objects.filter(status=0, union_id=union_id).last() if union_id else None
    
    if not wechat_user:
        name = clean_nickname(user_info['nickName'])

        user = User.objects.create(uid=_make_name('u_'), name=name, phone='', password_hex='')
        wechat_user = WechatUser.objects.create(user=user, union_id=union_id, nickname=name, head_img=user_info['avatarUrl'],
            **clean_dict(user_info, 'gender', 'language', 'country', 'province', 'city'))

    miniapp_user = MiniappUser.objects.create(wechat_user=wechat_user, open_id=open_id)
    return miniapp_user


def auth_then_go(url):
    from . import wechat
    return wechat.get_pa_auth_url(url)


def get_public_account_user(code):
    from . import wechat
    from .models import PublicAccountUser, WechatUser, User

    open_id, access_token = wechat.get_access_token(code)

    public_account_user = PublicAccountUser.objects.filter(open_id=open_id).first()
    if public_account_user:
        return public_account_user

    user_info = wechat.get_pa_user(open_id, access_token)

    union_id = user_info['unionid'] if 'unionid' in user_info else ''
    wechat_user = WechatUser.objects.filter(status=0, union_id=union_id).last() if union_id else None
    
    if not wechat_user:
        name = clean_nickname(user_info['nickname'])

        user = User.objects.create(uid=_make_name('u_'), name=name, phone='', password_hex='')
        wechat_user = WechatUser.objects.create(user=user, union_id=union_id, nickname=name, head_img=user_info['headimgurl'],
            gender=user_info['sex'], **clean_dict(user_info, 'language', 'country', 'province', 'city'))

    public_account_user = PublicAccountUser.objects.create(wechat_user=wechat_user, open_id=open_id)
    return public_account_user


def create_token(user, channel):
    from .models import Token

    token = Token.objects.create(user=user, token=_make_name('t_'), channel=channel)
    return token.token


def check_token(token):
    from .models import Token

    token = Token.objects.filter(status=0, token=token).last()
    if not token:
        raise APIError(401, '用户未登录', 1)

    return token.user


@api
def get_js_ticket(current_url):
    from . import wechat

    return wechat.get_js_ticket(current_url)


def order(user, product):
    from .models import Product, User, Order

    order = Order.objects.create(user=user, product=product, price=product.price)
    return order


def pay(channel, open_id, order, client_ip):
    from . import wechat

    return wechat.pay(channel, open_id,
        'ORD_%s_%s_%s_%s' % (order.product.company, order.product.category, order.id, ''.join(random.sample(string.ascii_letters, 6))),
        order.price,
        order.product.company,
        order.product.category,
        client_ip)


#lspace
def zhifu_pay(channel, open_id, order, client_ip):
    from . import wechat
    return wechat.pay(channel,open_id,
        'ORD_%s' % order.id,
        order.price,
        'lspace',
        'fuwufei',
        client_ip)


def pay_confirm(openid, total_fee, order_id):
    from .models import Payment, Order

    order = Order.objects.filter(id=order_id.split('_')[-2], status=0).first()

    if not Payment.objects.filter(order=order, status=0).exists():
        payment = Payment.objects.create(order=order, price=total_fee)


def phone_sms_code(id, phone, code):
    from .models import User, Token
    
    if not phone:
        raise APIError(400, '手机号为空', 1)

    if not verify_sms_code(phone, code):
        raise APIError(401, '验证码错误', 2)

    user = User.objects.filter(uid=id, status=0).first()
    if not user:
        name = phone[:3] + '***' + phone[-3:]
        user = User.objects.create(uid=_make_name('u_'), phone=phone, name=name, password_hex='')
    else:
        if not user.phone:
            user.phone = phone
            user.save()

    token = Token.objects.create(user=user, token=_make_name('t_'), channel=1)
    return token.token
    

@api
def ping():
    return 'pong'


@api
def error():
    raise APIError(400, '报错了！', 1)


@api
@comments(a='第一个数，必须是int', b='第二个数, 必须是int')
@params({
    'a': 1,
    'b': 2,
})
@returns(3)
@errors({ 'code': 1, 'msg': 'a is not int' }, { 'code': 2, 'msg': 'b is not int' })
def add(a, b=3):
    """
    返回a+b
    """
    if not isinstance(a, int):
        raise APIError(400, 'a is not int', 1)

    if not isinstance(b, int):
        raise APIError(400, 'b is not int', 2)

    return a + b