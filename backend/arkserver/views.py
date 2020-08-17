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
        request.session['link'] = link

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
            WaitingRoomMember.objects.create(
                game = new_game,
                player = new_player,
                state = 0,
            )

            new_game.members.set([new_player])

            request.session['uid'] = new_player.id
            
            print('username', username)
            print('gamename', gamename)
            print('avatar', avatar)
            print('link', link)

            return redirect(f'/preview/')
            # return redirect(f'/wartezimmer/{link}/')
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
        request.session['link'] = link

        if not Game.objects.filter(link=link).first().members.filter(name=username).first():
            avatar = get_avatar_link(avatar)
            new_player = Player.objects.create(
                name = username,
                avatar = avatar,
            )
            game = Game.objects.filter(link=link).first()
            game.members.set([new_player])
            WaitingRoomMember.objects.create(
                game = game,
                player = new_player,
                state = 0,
            )
            return redirect(f'/preview/')
            # return redirect(f'/wartezimmer/{link}/')

        else:
            # detect same name in this game
            ctx['error'] = 1
            return render(request,'./views/auth.html', ctx)

    return render(request,'./views/auth-link.html', ctx)

@user_required
def preview(request, user):
    ctx = {}
    return render(request, './views/preview.html', ctx)


@user_required
def ubung_1(request, user):
    ctx = {}
    if request.method == 'POST':
        link = request.session['link']

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

        game = Game.objects.filter(link=link).first()
        for i in tag_list:
            Ubung1.objects.create(
                game = game,
                player = user,
                power = i,
            )
        return redirect(f'/ubung-2/')

    return render(request, './views/ubung-1.html', ctx)

@user_required
def ubung_2(request, user):
    ctx = {}
    if request.method == 'POST':
        link = request.session['link']
        digit_value = request.POST.get('digit_value')
        game = Game.objects.filter(link=link).first()
        Ubung2.objects.create(
            game = game,
            player = user,
            value = digit_value, 
        )
        return redirect(f'/ubung-3/')

    return render(request, './views/ubung-2.html', ctx)

@user_required
def ubung_3(request, user):
    ctx = {}
    if request.method == 'POST':
        link = request.session['link']
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

        game = Game.objects.filter(link=link).first()
        for i in tag_list:
            Ubung3.objects.create(
                game = game,
                player = user,
                drainer = i,
            )
        return redirect(f'/wartezimmer/{link}/')

    return render(request, './views/ubung-3.html', ctx)


@user_required
def ubung_4(request, user):
    ctx = {}
    link = request.session['link']
    game = Game.objects.filter(link=link).first()
    waiting_room = list(WaitingRoomMember.objects.filter(game=game).exclude(player=user))
    member_list = [i.player.player_json for i in waiting_room]
    ctx['member_list'] = member_list

    if request.method == 'POST':
        # send user.id
        row0 = request.POST.get('row-0')
        row1 = request.POST.get('row-1')
        row2 = request.POST.get('row-2')
        row3 = request.POST.get('row-3')
        row4 = request.POST.get('row-4')
        row5 = request.POST.get('row-5')
        
        print(11111111111111111111111111111111)
        print(row0)
        print(row1)
        print(row2)
        print(row3)
        print(row4)
        print(row5)
        from .utils import list2int
        row0 = list2int(row0.split(','))
        row1 = list2int(row1.split(','))
        row2 = list2int(row2.split(','))
        row3 = list2int(row3.split(','))
        row4 = list2int(row4.split(','))
        row5 = list2int(row5.split(','))
        
        ubung4 = Ubung4.objects.filter(game=game,user=user).first()
        if not ubung4:
            ubung4 = Ubung4.objects.create(
                game = game,
                player = user,
            )

        for i in row0:
            for u in i:
                mem = Player.objects.filter(id=u).first()
                ubung4.row0.add(mem)
        for i in row1:
            for u in i:
                mem = Player.objects.filter(id=u).first()
                ubung4.row1.add(mem)
        for i in row2:
            for u in i:
                mem = Player.objects.filter(id=u).first()
                ubung4.row2.add(mem)
        for i in row3:
            for u in i:
                mem = Player.objects.filter(id=u).first()
                ubung4.row3.add(mem)
        for i in row4:
            for u in i:
                mem = Player.objects.filter(id=u).first()
                ubung4.row4.add(mem)
        for i in row5:
            for u in i:
                mem = Player.objects.filter(id=u).first()
                ubung4.row5.add(mem)     
        return redirect('/ubung-5/')

    return render(request, './views/ubung-4.html', ctx)


def ubung_5(request):
    ctx = {}
    return render(request, './views/ubung-5.html', ctx)


@user_required
def team_potential(request, user):
    ctx = {}
    link = request.session['link']
    game = Game.objects.filter(link=link).first()
    ubung2 = Ubung2.objects.filter(game=game)
    value_list = [int(i.value) for i in ubung2]
    value_list = list(set(value_list))
    temp = len(value_list)/2
    if temp.__class__ == int:
        result = (value_list[temp-1] + value_list[temp])/2
    else:
        temp = round(temp)
        result = value_list[temp]
    ctx['result'] = result

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


@user_required
def wartezimmer(request, user, link):
    ctx = {}
    link = request.session['link']
    # user = ctx['user'] = Player.objects.filter(id=request.session.get('uid')).first()
    game = Game.objects.filter(link=link).first()
    room_member = WaitingRoomMember.objects.filter(game=game,player=user).first()
    room_member.state = 1
    room_member.save()

    ctx['avatar'] = user.avatar
    ctx['player_name'] = user.name
    ctx['player_id'] = user.id
    ctx['link'] = link
    return render(request, './views/wartezimmer.html', ctx)


def psychologischer(request):
    ctx = {}
    return render(request, './views/psychologischer.html', ctx)


@api
def waiting_room_active(player_id, link):
    from .models import Player, Game

    # player = Player.objects.filter(id=player_id).first()
    game = Game.objects.filter(link=link).first()
    waiting_room = list(WaitingRoomMember.objects.filter(game=game,state=1))
    
    members_list = [i.player.player_json for i in waiting_room]

    return members_list


@api
def waiting_room_yet(player_id, link):
    from .models import Player, Game
    game = Game.objects.filter(link=link).first()
    waiting_room = list(WaitingRoomMember.objects.filter(game=game,state=0))
    
    members_list = [i.player.player_json for i in waiting_room]
    return members_list


