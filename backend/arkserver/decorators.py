import codecs
import threading
import time
from functools import wraps

from django.shortcuts import redirect


def _check_user(request):
    from .models import Player
    print('request', request)
    if 'uid' not in request.session:
        return 

    user = Player.objects.filter(id=request.session['uid']).first()
    print('user',user)
    
    return user


def user_required(func):

    def view(request, *args, **kwargs):
        user = _check_user(request)

        
        if not user:
            return redirect(f'/')

        request.user = user
        print('link', request.session['link'])

        return func(request, user=user, *args, **kwargs)

    return view