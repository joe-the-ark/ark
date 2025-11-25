from django.http import JsonResponse, HttpResponse
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.conf import settings

from .exceptions import APIError
from .log import log, error

import inspect
import json
import traceback
import functools


def comments(**kwargs):

    def wrapper(func):
        func.__comments__ = kwargs
        return func

    return wrapper


def params(*params_sample):
    
    def wrapper(func):
        func.__params_sample__ = params_sample
        return func

    return wrapper


def returns(*returns_sample):

    def wrapper(func):
        func.__returns_sample__ = returns_sample
        return func

    return wrapper


def errors(*errors_sample):

    def wrapper(func):
        func.__errors_sample__ = errors_sample
        return func

    return wrapper


def api(func):
    from .urls import urlpatterns
    from .apis import all_apis
    print ('api', func.__name__, 'registered')

    all_apis.append(func)
    arg_spec = inspect.getargspec(func)

    func.__args__ = args = [{
        'name': _,
        'required': True,
        'default': None,
    } for _ in arg_spec.args]

    if not hasattr(func, '__params_sample__'):
        func.__params_sample__ = {}

    if not hasattr(func, '__returns_sample__'):
        func.__returns_sample__ = {}

    if not hasattr(func, '__errors_sample__'):
        func.__errors_sample__ = {}

    if not hasattr(func, '__comments__'):
        func.__comments__ = {}

    default_count = len(arg_spec.defaults) if arg_spec.defaults else 0
    for i in range(default_count):
        arg = args[len(args) - default_count + i]
        arg['required'] = False
        arg['default'] = arg_spec.defaults[i]

    @csrf_exempt
    @functools.wraps(func)
    def django_view(request):

        if request.method != 'POST':
            is_json = request.GET.get('json', None)
            ctx = {
                'all_apis': [_.__name__ for _ in all_apis],

                'name': func.__name__, 'doc': func.__doc__, 'args': func.__args__, 'comments': func.__comments__,
                'params_sample': [json.dumps(_, indent=2) for _ in func.__params_sample__],
                'returns_sample': [json.dumps(_, indent=2) for _ in func.__returns_sample__],
                'errors_sample': [json.dumps(_, indent=2) for _ in func.__errors_sample__]}
            if is_json:
                return JsonResponse(ctx)
            else:
                return render(request, 'meta/api.html', ctx)

        try:
            params = json.loads(request.body.decode('utf-8'))
        except:
            return HttpResponse('参数无法解析', status=400)

        try:
            result = func(**params)
            success = True
            log('[%s] called success' % func.__name__)
        except APIError as ex:
            result = {
                'success': False,
                'result': {
                    'code': ex.code,
                    'msg': ex.msg,
                }
            }
            error('[%s] called with exception' % func.__name__)
            error('exception: %s' % str(ex))
            return JsonResponse(result, status=200)
        except Exception as ex:
            result = {
                'success': False,
                'result': {
                    'code': -1,
                    'msg': str(ex),
                }
            }
            error('[%s] called with exception' % func.__name__)
            error('exception: %s' % str(ex))
            return JsonResponse(result, status=200)

        return JsonResponse({ 'success': success, 'result': result })

    urlpatterns.append(path('api/%s/' % func.__name__, django_view))
    return func


def user_required(func):

    @functools.wraps(func)
    def wrapper(request, *args, **kwargs):
        from . import api
        
        wrapper.__name__ = func.__name__

        token = request.GET.get('token', '')
        if token:
            request.session['token'] = token
        else:
            token = request.session['token'] if 'token' in request.session else ''


        # token = request.session['token'] if 'token' in request.session else ''
        
        # if not token:
        #     token = request.GET.get('token', '')
        #     if token:
        #         request.session['token'] = token

        next_url = request.get_full_path()

        if not token:
            return redirect('/login?next=' + next_url)

        try:
            user = api.check_token(token)
        except APIError:
            return redirect('/login?next=' + next_url)

        request.user = user
        result = func(request, user=user, *args, **kwargs)
        return result

    return wrapper
