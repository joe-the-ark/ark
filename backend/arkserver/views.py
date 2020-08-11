from django.shortcuts import render, redirect
from .utils import *
from .decorators import user_required
from meta.decorators import api, APIError

# Create your views here.
from .models import *

def result(request, name, player, game_secret, inviter):

    ctx = {}
    ctx['results'] = Result.objects.filter(player=player, game_secret=game_secret, inviter=inviter)
    print(ctx['results'])

    _player = Player.objects.filter(
        name=player,
        game_secret=game_secret,
        inviter_name=inviter
    ).first()

    _inviter = Player.objects.filter(
        name=inviter,
        game_secret=game_secret,
        inviter_name=inviter,
    ).first()

    game = Game.objects.filter(
        game_secret=game_secret,
        inviter=_inviter,
    ).first()

    feedbacks = Feedback.objects.filter(teammate=_player, game=game)

    loveFeedback = []
    addFeedback = []
    askFeedback = []

    for feedback in feedbacks:
        loveFeedback.append(feedback.love)
        addFeedback.append(feedback.add)
        askFeedback.append(feedback.ask)

    ctx['loveFeedback'] = loveFeedback
    ctx['addFeedback'] = addFeedback
    ctx['askFeedback'] = askFeedback

    return render(request, 'result.html', ctx)



def index(request):
    ctx = {}
    return render(request,'./index.html', ctx)

def auth(request):
    ctx = {}

    if request.method == 'POST':

        username = request.POST.get('Nutzername')
        gamename = request.POST.get('name-des-spiels')
        avatar = request.POST.get('avatar')
        link = request.POST.get('link')

        if (not Player.objects.filter(name=username).first()):
            avatar = get_avatar_link(avatar)

            new_player = Player.objects.create(
                name = username,
                avatar = avatar,
            )
            new_game = Game.objects.create(
                name = gamename,
                link = link,
                creator = new_player,
                status = 0,
            )

            new_game.members.set([new_player])

            request.session['uid'] = new_player.id
            
            print('username', username)
            print('gamename', gamename)
            print('avatar', avatar)
            print('link', link)
            return redirect(f'/wartezimmer/{link}/')
        else:
            # same player-name or same game-name
            ctx['error'] = 1
            return render(request,'./views/auth.html', ctx)

    return render(request,'./views/auth.html', ctx)

def auth_link(request):
    ctx = {}

    if request.method == 'POST':
        username = request.POST.get('Nutzername')
        avatar = request.POST.get('name-des-spiels')
        # gamename = request.POST.get('name-des-spiels')
        link = request.POST.get('link')
        print('username', username)
        # print('gamename', gamename)
        print('avatar', avatar)
        print('link', link)

        if not Game.objects.filter(link=link).first().members.filter(name=username).first():
            avatar = get_avatar_link(avatar)
            new_player = Player.objects.create(
                name = username,
                avatar = avatar,
            )
            game = Game.objects.filter(link=link).first()
            new_game.members.set([new_player])
            return redirect(f'/wartezimmer/{link}/')

        else:
            # detect same name in this game
            ctx['error'] = 1
            return render(request,'./views/auth.html', ctx)

    return render(request,'./views/auth-link.html', ctx)

def preview(request):
    ctx = {}
    return render(request, './views/preview.html', ctx)

def ubung_1(request):
    ctx = {}
    if request.method == 'POST':
        kraftquelle = request.POST.get('kraftquelle')
        tags = request.POST.get('tags')
        tags = tags + kraftquelle
        tag_list = tags.split(',')
        uu = 0
        while uu < len(tag_list):
            if tag_list[uu] == '':
                del tag_list[uu]
            uu += 1
        print("tag_list", tag_list)

    return render(request, './views/ubung-1.html', ctx)

def ubung_2(request):
    ctx = {}
    if request.method == 'POST':
        digit_value = request.POST.get('digit_value')
        print('digit_value',digit_value)

    return render(request, './views/ubung-2.html', ctx)

def ubung_3(request):
    ctx = {}
    if request.method == 'POST':
        energiefresser = request.POST.get('energiefresser')
        tags = request.POST.get('tags')
        tags = tags + energiefresser
        tag_list = tags.split(',')
        uu = 0
        while uu < len(tag_list):
            if tag_list[uu] == '':
                del tag_list[uu]
            uu += 1
        print("tag_list", tag_list)

    return render(request, './views/ubung-3.html', ctx)

def ubung_4(request):
    ctx = {}
    return render(request, './views/ubung-4.html', ctx)

def ubung_5(request):
    ctx = {}
    return render(request, './views/ubung-5.html', ctx)

def team_potential(request):
    ctx = {}
    return render(request, './views/team-potential.html', ctx)

def spannungsfelder(request):
    ctx = {}
    return render(request, './views/spannungsfelder.html', ctx)

def preview_2(request):
    ctx = {}
    return render(request, './views/preview-2.html', ctx)

def mission_2_ubung_1(request):
    ctx = {}
    return render(request, './views/mission-2-ubung-1.html', ctx)

def mission_2_ubung_2(request):
    ctx = {}
    return render(request, './views/mission-2-ubung-2.html', ctx)

def assessment(request):
    ctx = {}
    return render(request, './views/assessment.html', ctx)

def goodbye(request):
    ctx = {}
    return render(request, './views/goodbye.html', ctx)

def arche(request):
    ctx = {}
    return render(request, './views/arche.html', ctx)


# @user_required
def wartezimmer(request, link):
    ctx = {}
    user = ctx['user'] = Player.objects.filter(id=request.session.get('uid')).first()
    ctx['avatar'] = user.avatar
    ctx['player_name'] = user.name
    ctx['player_id'] = user.id
    ctx['link'] = link
    return render(request, './views/wartezimmer.html', ctx)


def psychologischer(request):
    ctx = {}
    return render(request, './views/psychologischer.html', ctx)


@api
def waiting_room(player_id, link):
    from .models import Player, Game

    player = Player.objects.filter(id=player_id).first()
    game = Game.objects.filter(link=link).first()
    members = list(game.members.all())
    uu = 0
    # while uu < len(members):
    #     if members[uu] == game:
    #         del members[uu]
    #     uu += 1
    members_list = []
    for i in members:
        members_list.append(i.player_json)
    player = player.player_json
    return members_list