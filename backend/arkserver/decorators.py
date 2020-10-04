import codecs
import threading
import time
from functools import wraps

from django.shortcuts import redirect


def _check_user(request):
    from .models import Player, Game
    print('request', request)
    if 'uid' not in request.session:
        return 

    user = Player.objects.filter(id=request.session['uid']).first()
    print('user',user)
    
    return user


def user_required(func):
    from .models import Player, Game

    def view(request, *args, **kwargs):
        user = _check_user(request)

        
        if not user:
            return redirect(f'/')

        request.user = user
        # request.game = Game.objects.filter(link=request.session['link']).first()
        print('link', request.session['link'])

        return func(request, user=user, *args, **kwargs)

    return view


def after_waitingroom(func):
    from .models import Player, WaitingRoomMember
    def view(request, *args, **kwargs):
        user = _check_user(request)
        print('user-valid', user.valid)
        if not user.valid:
            return redirect(f'/')
        return func(request, *args, **kwargs)
    return view