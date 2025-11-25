from django.shortcuts import render, redirect, reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.conf import settings

from .decorators import user_required
from .exceptions import APIError


def login_miniapp(request):
    from . import api

    code = request.GET.get('code')
    encrypted_data = request.GET.get('encrypted_data')
    iv = request.GET.get('iv')

    next_url = request.GET.get('next', '/')

    miniapp_user = api.get_miniapp_user(code, encrypted_data, iv)
    token = api.create_token(miniapp_user.wechat_user.user, 1)

    return JsonResponse({
        'token': token,
        'next_url': next_url
    })


def login_public_account(request):
    from . import api

    next_url = request.GET.get('next', '/')

    code = request.GET.get('code')
    if not code:
        return redirect(api.auth_then_go(reverse(login_public_account)+'?next='+next_url))

    try:
        public_account_user = api.get_public_account_user(code)
    except:
       return redirect(login_public_account)

    token = api.create_token(public_account_user.wechat_user.user, 2)
    request.session['token'] = token

    return redirect(next_url)


def login(request):
    next_url = request.GET.get('next', '/')

    return render(request, 'meta/login.html', { 'next_url': next_url })


@user_required
def order_public_account(request, user, product_id):
    from . import api
    from .models import Product, PublicAccountUser

    product = Product.objects.filter(id=product_id, status=0).first()
    client_ip = request.META['HTTP_X_FORWARDED_FOR'] if 'HTTP_X_FORWARDED_FOR' in request.META else request.META['REMOTE_ADDR']

    order = api.order(user, product)

    pa = PublicAccountUser.objects.filter(wechat_user=user.wechat_user()).first()
    result = api.pay('pa', pa.open_id, order, client_ip)

    return JsonResponse(result)


def get_token(request):
    token = request.session['token'] if 'token' in request.session else ''
    return JsonResponse({ 'token': token })
    

def order_miniapp(request, product_id):
    from . import api
    from .models import Product, MiniappUser

    token = request.GET.get('token', '')
    user = api._get_user(token)

    product = Product.objects.filter(id=product_id, status=0).first()
    client_ip = request.META['HTTP_X_FORWARDED_FOR'] if 'HTTP_X_FORWARDED_FOR' in request.META else request.META['REMOTE_ADDR']

    order = api.order(user, product)

    ma = MiniappUser.objects.filter(wechat_user=user.wechat_user()).first()
    result = api.pay('ma', ma.open_id, order, client_ip)
    print(result)
    return JsonResponse(result)


@user_required
def order_success(request, user, product_id):
    return redirect('/')


@csrf_exempt
def wechat_pay_confirm(request):
    import xml.etree.ElementTree as ET
    from . import api
    print(request.body)
    token = request.GET.get('token', '')
    print(token)
    print('hehhehhehe')
    root = ET.fromstring(request.body)
    result_code = root.find('result_code').text

    if result_code == 'SUCCESS':
        openid = root.find('openid').text
        total_fee = root.find('total_fee').text
        order_id = root.find('out_trade_no').text[4:]
        api.pay_confirm(openid, total_fee, order_id)

    return HttpResponse("""
<xml>

  <return_code><![CDATA[SUCCESS]]></return_code>
  <return_msg><![CDATA[OK]]></return_msg>
</xml>
""")


@csrf_exempt
def zhifu(request, order_id):
    from . import api
    from lspace.models import Order as LOrder
    from .models import MiniappUser

    token = request.session['token']
    user = api._get_user(token)
    order = LOrder.objects.filter(id=order_id).first()
    client_ip = request.META['HTTP_X_FORWARDED_FOR'] if 'HTTP_X_FORWARDED_FOR' in request.META else request.META['REMOTE_ADDR']
    ma = MiniappUser.objects.filter(wechat_user=user.wechat_user()).first()
    result = api.zhifu_pay('pa', ma.open_id, order, client_ip)

    return JsonResponse(result)


@user_required
def test(request, user):
    ctx = {
        'user': user
    }

    return render(request, 'meta/test.html', ctx)


def bind_phone(request, template='meta/bind_phone.html', redirect_to='profile'):
    from . import api

    ctx = {
        'errors': [],
        'messages': [],
    }
    token = request.session['token'] if 'token' in request.session else ''
    try:
        ctx['user'] = api._get_user(token)
    except APIError:
        return redirect('/')

    if request.method == 'GET':
        return render(request, template, ctx)

    ctx['phone'] = phone = request.POST.get('phone')
    code = request.POST.get('code')

    try:
        api.bind_phone(token, phone, code)
        return redirect(redirect_to)
    except APIError as ex:
        ctx['errors'].append(ex.msg)

    return render(request, template, ctx)
