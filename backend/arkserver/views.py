from django.shortcuts import render, redirect
from .utils import *
from .decorators import user_required, after_waitingroom
from meta.decorators import api, APIError
import json

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

        # if (not Player.objects.filter(name=username).first()):
        if not Game.objects.filter(name=gamename).first():
            # avatar = get_avatar_link(avatar)

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
    ctx['link'] = ''

    if request.method == 'POST':
        username = request.POST.get('Nutzername')
        avatar = request.POST.get('avatar')
        # gamename = request.POST.get('name-des-spiels')
        link = request.POST.get('link')
        print('username', username)
        # print('gamename', gamename)
        print('avatar', avatar)
        print('link', link)
        request.session['link'] = link

        if not Game.objects.filter(link=link).first().members.filter(name=username).first():
            # avatar = get_avatar_link(avatar)
            new_player = Player.objects.create(
                name = username,
                avatar = avatar,
            )
            request.session['uid'] = new_player.id
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
            return render(request,'./views/auth_link.html', ctx)

    return render(request,'./views/auth-link.html', ctx)


def link_enter(request, link):
    ctx = {}
    ctx['link'] = link
    game = Game.objects.filter(link=link).first()

    if not game:
        # invalid game link
        return redirect('/')

    if request.method == 'POST':
        username = request.POST.get('Nutzername')
        avatar = request.POST.get('avatar')
        # gamename = request.POST.get('name-des-spiels')
        # link = request.POST.get('link')
        print('username', username)
        # print('gamename', gamename)
        print('avatar', avatar)
        print('link', link)
        request.session['link'] = link

        if not Game.objects.filter(link=link).first().members.filter(name=username).first():
            # avatar = get_avatar_link(avatar)
            new_player = Player.objects.create(
                name = username,
                avatar = avatar,
            )
            request.session['uid'] = new_player.id
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
            return render(request,'./views/auth_link.html', ctx)

    return render(request,'./views/auth-link.html', ctx)


@user_required
def preview(request, user):
    ctx = {}
    ctx['game'] = Game.objects.filter(link=request.session['link']).first()
    return render(request, './views/preview.html', ctx)


@user_required
def ubung_1(request, user):
    ctx = {}
    ctx['game'] = game = Game.objects.filter(link=request.session['link']).first()
    player = user
    temp = Ubung1.objects.filter(game=game).first()
    if not temp:
        from .utils import ubung_1_term_list
        term_list = ubung_1_term_list
        for i in term_list:
            Ubung1.objects.create(
                game = game,
                player = None,
                state = 'tag',
                power = i['value'],
            )
    ctx['term_list'] = [i.api_json for i in list(Ubung1.objects.filter(game=game))]
    # if request.method == 'POST':
    #     link = request.session['link']

    #     kraftquelle = request.POST.get('kraftquelle')
    #     tags = request.POST.get('tags')
    #     tags = tags + kraftquelle
    #     tag_list = tags.split(',')
    #     uu = 0
    #     while uu < len(tag_list):
    #         if tag_list[uu] == '':
    #             del tag_list[uu]
    #         uu += 1
    #     print("tag_list", tag_list)

    #     game = Game.objects.filter(link=link).first()
    #     for i in tag_list:
    #         Ubung1.objects.create(
    #             game = game,
    #             player = user,
    #             power = i,
    #         )
    #     return redirect(f'/ubung-2/')

    return render(request, './views/ubung-1.html', ctx)

@user_required
def ubung_2(request, user):
    ctx = {}
    ctx['game'] = game = Game.objects.filter(link=request.session['link']).first()
    
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
    ctx['game'] = game = Game.objects.filter(link=request.session['link']).first()


    player = user
    temp = Ubung3.objects.filter(game=game).first()
    if not temp:
        from .utils import ubung_3_term_list
        term_list = ubung_3_term_list
        for i in term_list:
            Ubung3.objects.create(
                game = game,
                player = None,
                state = 'tag',
                drainer = i['value'],
            )
    
    ctx['term_list'] = [i.api_json for i in list(Ubung3.objects.filter(game=game))]

    # if request.method == 'POST':
    #     link = request.session['link']
    #     energiefresser = request.POST.get('energiefresser')
    #     tags = request.POST.get('tags')
    #     tags = tags + energiefresser
    #     tag_list = tags.split(',')
    #     uu = 0
    #     while uu < len(tag_list):
    #         if tag_list[uu] == '':
    #             del tag_list[uu]
    #         uu += 1
    #     print("tag_list", tag_list)

    #     game = Game.objects.filter(link=link).first()
    #     for i in tag_list:
    #         Ubung3.objects.create(
    #             game = game,
    #             player = user,
    #             drainer = i,
    #         )
    #     return redirect(f'/wartezimmer/{link}/')

    return render(request, './views/ubung-3.html', ctx)


@after_waitingroom
@user_required
def ubung_4(request, user):
    ctx = {}
    ctx['game'] = Game.objects.filter(link=request.session['link']).first()
    link = request.session['link']
    game = Game.objects.filter(link=link).first()
    # waiting_room = list(WaitingRoomMember.objects.filter(game=game).exclude(player=user))
    waiting_room = list(WaitingRoomMember.objects.filter(game=game))
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
        
        ubung4 = Ubung4.objects.filter(game=game,player=user).first()
        if not ubung4:
            ubung4 = Ubung4.objects.create(
                game = game,
                player = user,
            )
        print(row0)
        print(row1)
        print(row2)
        print(row3)
        print(row4)
        print(row5)
        for i in row0:
            mem = Player.objects.filter(id=i).first()
            ubung4.row0.add(mem)
        for i in row1:
            mem = Player.objects.filter(id=i).first()
            ubung4.row1.add(mem)
        for i in row2:
            mem = Player.objects.filter(id=i).first()
            ubung4.row2.add(mem)
        for i in row3:
            mem = Player.objects.filter(id=i).first()
            ubung4.row3.add(mem)
        for i in row4:
            mem = Player.objects.filter(id=i).first()
            ubung4.row4.add(mem)
        for i in row5:
            mem = Player.objects.filter(id=i).first()
            ubung4.row5.add(mem)     
        return redirect('/ubung-5/')

    return render(request, './views/ubung-4.html', ctx)


@after_waitingroom
@user_required
def ubung_5(request, user):
    ctx = {}
    ctx['game'] = Game.objects.filter(link=request.session['link']).first()
    link = request.session['link'] 
    game = Game.objects.filter(link=link).first()
    waiting_room = list(WaitingRoomMember.objects.filter(game=game))
    member_list = [i.player.player_json for i in waiting_room]
    ctx['member_list'] = member_list

    if request.method == 'POST':
        data = request.POST.get('data')
        data = json.loads(data)
        ubung5 = Ubung5.objects.filter(game=game,player=user).first()
        if ubung5:
            ubung5.delete()
        for i in data:
            Ubung5.objects.create(
                game = game,
                player = user,
                goal = Player.objects.filter(id=int(i['id'])).first(),
                score = int(i['status']),
            )
    
        return redirect('/team-potential/')

    return render(request, './views/ubung-5.html', ctx)


@after_waitingroom
@user_required
def team_potential(request, user):
    ctx = {}
    ctx['game'] = Game.objects.filter(link=request.session['link']).first()
    link = request.session['link']
    game = Game.objects.filter(link=link).first()
    ubung2 = Ubung2.objects.filter(game=game)
    value_list = [int(i.value) for i in ubung2]
    value_list = list(set(value_list))
    temp = len(value_list)/2
    if temp.__class__ == int:
        median = (value_list[temp-1] + value_list[temp])/2
    else:
        temp = round(temp)
        median = value_list[temp]
    ctx['minimal'] = min(value_list)
    ctx['maximal'] = max(value_list)
    ctx['median'] = median
    ctx['user'] = user

    all_result = []
    for i in value_list:
        if i == ubung2.filter(player=user).first().value:
            all_result.append(
                {
                    'name': user.name,
                    'avatar': user.avatar,
                    'statusSide': i
                }
            )
        else:
            all_result.append({"statusSide": i})
    ctx['all_result'] = all_result
    return render(request, './views/team-potential.html', ctx)


@after_waitingroom
@user_required
def spannungsfelder(request, user):
    ctx = {}
    ctx['game'] = Game.objects.filter(link=request.session['link']).first()
    link = request.session['link']  
    game = Game.objects.filter(link=link).first()
    ubung5 = list(Ubung5.objects.filter(goal=user).exclude(player=user))
    other_list = [i.score for i in ubung5]
    if len(other_list) != 0:
        others = sum(other_list) / len(other_list)
    else:
        others = sum(other_list) / 1
    ubung5 = Ubung5.objects.filter(player=user).first()
    himself = ubung5.score
    tension = others - himself

    ctx['others'] = others
    ctx['himself'] = himself
    ctx['tension'] = tension

    json_list = [ i.span_1 for i in list(Ubung5.objects.filter(goal=user)) ]
    json_list.sort(key = lambda x:x['statusSide'])
    ctx['json_list'] = json_list
    # print(json_list)
    ctx['user'] = user
    return render(request, './views/spannungsfelder.html', ctx)


@after_waitingroom
@user_required
def preview_2(request, user):
    ctx = {}
    ctx['game'] = Game.objects.filter(link=request.session['link']).first()
    return render(request, './views/preview-2.html', ctx)


@after_waitingroom
@user_required
def mission_2_ubung_1(request, user):
    ctx = {}
    ctx['game'] = Game.objects.filter(link=request.session['link']).first()
    link = request.session['link']  
    game = Game.objects.filter(link=link).first()
    waiting_room = list(WaitingRoomMember.objects.filter(game=game))
    member_list = [i.player.player_json for i in waiting_room]
    ctx['member_list'] = member_list

    if request.method == 'POST':
        data = request.POST.get('data')
        data = json.loads(data)
        m2ubung1 = M2Ubung1.objects.filter(game=game,player=user).first()
        if m2ubung1:
            m2ubung1.delete()
        for i in data:
            M2Ubung1.objects.create(
                game = game,
                player = user,
                goal = Player.objects.filter(id=int(i['id'])).first(),
                score = int(i['status']),
            )
        return redirect('/mission-2-ubung-2/')

    return render(request, './views/mission-2-ubung-1.html', ctx)


@after_waitingroom
@user_required
def mission_2_ubung_2(request, user):
    ctx = {}
    ctx['game'] = Game.objects.filter(link=request.session['link']).first()
    link = request.session['link']  
    game = Game.objects.filter(link=link).first()
    waiting_room = list(WaitingRoomMember.objects.filter(game=game))
    member_list = [i.player.player_json for i in waiting_room]
    ctx['member_list'] = member_list

    if request.method == 'POST':
        data = request.POST.get('data')
        print(data)
        data = json.loads(data)
        m2ubung2 = M2Ubung2.objects.filter(game=game,player=user).first()
        if m2ubung2:
            m2ubung2.delete()
        for i in data:
            M2Ubung2.objects.create(
                game = game,
                player = user,
                goal  = Player.objects.filter(id=int(i['id'])).first(),
                row1 = i['feedback'][0]['text'],
                row2 = i['feedback'][1]['text'],
                row3 = i['feedback'][2]['text'],
            )
        
        return redirect('/goodbye/')


    json_list = [ i.span_1 for i in list(Ubung5.objects.filter(goal=user,game=game)) ]
    json_list.sort(key = lambda x:x['statusSide'])
    ctx['json_list'] = json_list
    

    return render(request, './views/mission-2-ubung-2.html', ctx)


@after_waitingroom
@user_required
def assessment(request, user):
    ctx = {}
    ctx['game'] = Game.objects.filter(link=request.session['link']).first()
    link = request.session['link']  
    game = Game.objects.filter(link=link).first()
    ubung2 = Ubung2.objects.filter(game=game)
    value_list = [int(i.value) for i in ubung2]
    value_list = list(set(value_list))
    temp = len(value_list)/2
    if temp.__class__ == int:
        median = (value_list[temp-1] + value_list[temp])/2
    else:
        temp = round(temp)
        median = value_list[temp]
    ctx['team_potential_minimal'] = min(value_list)
    ctx['team_potential_maximal'] = max(value_list)
    ctx['team_potential_median'] = median
    ctx['user'] = user

    all_result = []
    for i in value_list:
        if i == ubung2.filter(player=user,game=game).first().value:
            all_result.append(
                {
                    'name': user.name,
                    'avatar': user.avatar,
                    'statusSide': i
                }
            )
        else:
            all_result.append({"statusSide": i})
    ctx['team_potential_all_result'] = all_result

    game_place = list(Ubung4.objects.filter(game=game))
    row_0 = 0
    row_1 = 0
    row_2 = 0
    row_3 = 0
    row_4 = 0
    row_5 = 0
    for game_ in game_place:
        if game_.player == user:
            continue
        else:
            if user in game_.row0:

                row_0 += 1
            if user in game_.row1:
                row_1 += 1
            if user in game_.row2:
                row_2 += 1
            if user in game_.row3:
                row_3 += 1
            if user in game_.row4:
                row_4 += 1
            if user in game_.row5:
                row_5 += 1

    score = row_0 * 4 + row_1 * 1 + row_2 * 3 + row_3 * 5 + row_4 * 0 + row_5 * 2
    num = (WaitingRoomMember.objects.filter(game=game,state=1).count()) ** 2
    score = score / num

    ctx['psy_score'] = score
    ctx['psy_row0'] = row_0
    ctx['psy_row1'] = row_1
    ctx['psy_row2'] = row_2
    ctx['psy_row3'] = row_3
    ctx['psy_row4'] = row_4
    ctx['psy_row5'] = row_5

    ubung5 = list(Ubung5.objects.filter(goal=user,game=game).exclude(player=user))
    other_list = [i.score for i in ubung5]
    if len(other_list) != 0:
        others = sum(other_list) / len(other_list)
    else:
        others = sum(other_list) / 1
    ubung5 = Ubung5.objects.filter(player=user).first()
    himself = ubung5.score
    tension = others - himself

    ctx['others'] = others
    ctx['himself'] = himself
    ctx['tension'] = tension

    json_list = [ i.span_1 for i in list(Ubung5.objects.filter(goal=user,game=game)) ]
    json_list.sort(key = lambda x:x['statusSide'])
    ctx['span_json_list'] = json_list


    feedback1 = []
    feedback2 = []
    feedback3 = []
    m2ubung2 = list(M2Ubung2.objects.filter(game=game,goal=user))
    for i in m2ubung2:
        feedback1.append(i.row1)
        feedback2.append(i.row2)
        feedback3.append(i.row3)
    ctx['feedback1'] = feedback1
    ctx['feedback2'] = feedback2
    ctx['feedback3'] = feedback3

    # for i in m2ubung2:
    #     feedback.append(
    #         {
    #             'name': i.player.name,
    #             'avatar': i.player.avatar,
    #             'statusSide': Ubung5.objects.filter(goal=user,game=game,player=i.player).first().score,
    #             'feedback': [
    #                 {
    #                     'title': 'MEHR davon: Ich schätze deinen Beitrag zum gelingenden Zusammenspiel im Team…',
    #                     'text': i.row1,
    #                 },
    #                 {
    #                     'title':  'ÄNDERN: du könntest zur psychologischen Sicherheit im Team beitragen, in dem...',
    #                     'text': i.row2,
    #                 },
    #                 {
    #                     'title': 'FRAGEZEICHEN: ich wollte dich schon immer mal fragen…',
    #                     'text': i.row3,
    #                 }
    #             ]
    #         }
    #     ) 
    return render(request, './views/assessment.html', ctx)

@user_required
def goodbye(request, user):
    ctx = {}
    ctx['game'] = Game.objects.filter(link=request.session['link']).first()
    return render(request, './views/goodbye.html', ctx)

@user_required
def arche(request, user):
    ctx = {}
    ctx['game'] = Game.objects.filter(link=request.session['link']).first()
    return render(request, './views/arche.html', ctx)


@user_required
def wartezimmer(request, user):
    ctx = {}
    ctx['game'] = Game.objects.filter(link=request.session['link']).first()
    link = request.session['link']
    # user = ctx['user'] = Player.objects.filter(id=request.session.get('uid')).first()
    game = Game.objects.filter(link=link).first()
    if game.status != 0:
        return redirect('/')
    room_member = WaitingRoomMember.objects.filter(game=game,player=user).first()
    room_member.state = 1
    room_member.save()

    ctx['avatar'] = user.avatar
    ctx['player_name'] = user.name
    ctx['player_id'] = user.id
    ctx['link'] = link

    if request.method == 'POST':
        nums = WaitingRoomMember.objects.filter(game=game).count()
        if user != game.creator:
            if nums < 3:
                return
            if game.status == 1:
                player_ = WaitingRoomMember.objects.filter(game=game,user=user).first()
                player_.state = 1
                player_.save()
                return redirect('/ubung-4/')
            else:
                return render(request, './views/wartezimmer.html', ctx)
        elif user == game.creator:
            if nums < 3:
                return render(request, './views/wartezimmer.html', ctx)
            else:
                game.status = 1
                game.saves()

                player_ = WaitingRoomMember.objects.filter(game=game,user=user).first()
                player_.state = 1
                player_.save()
                return redirect('/ubung-4/')
        
        # if nums < 3:
        #     return
        #     # pass
        #     # return redirect('/ubung-4/')
        # else:

        #     return redirect('/ubung-4/')

    return render(request, './views/wartezimmer.html', ctx)


@user_required
def psychologischer(request, user):
    ctx = {}
    ctx['game'] = Game.objects.filter(link=request.session['link']).first()
    link = request.session['link']
    game = Game.objects.filter(link=link).first()
    game_place = list(Ubung4.objects.filter(game=game))
    row_0 = 0
    row_1 = 0
    row_2 = 0
    row_3 = 0
    row_4 = 0
    row_5 = 0
    for game_ in game_place:
        if game_.player == user:
            continue
        else:
            if user in game_.row0.all():
                row_0 += 1
            if user in game_.row1.all():
                row_1 += 1
            if user in game_.row2.all():
                row_2 += 1
            if user in game_.row3.all():
                row_3 += 1
            if user in game_.row4.all():
                row_4 += 1
            if user in game_.row5.all():
                row_5 += 1

    score = row_0 * 4 + row_1 * 1 + row_2 * 3 + row_3 * 5 + row_4 * 0 + row_5 * 2
    num = (WaitingRoomMember.objects.filter(game=game,state=1).count()) ** 2
    score = score / num

    ctx['score'] = score
    ctx['row0'] = row_0
    ctx['row1'] = row_1
    ctx['row2'] = row_2
    ctx['row3'] = row_3
    ctx['row4'] = row_4
    ctx['row5'] = row_5
    # print(score)
    # print(row_0)
    # print(row_1)
    # print(row_2)
    # print(row_3)
    # print(row_4)
    # print(row_5)
    return render(request, './views/psychologischer.html', ctx)


def logout(request):
    if 'uid' in request.session:
        del request.session['uid']
    if 'link' in request.session:
        del request.session['link']
    return redirect('/')




# apis

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

@api
def check_ubung_1(player_id, link):
    from .models import Player, Game, Ubung1
    game = Game.objects.filter(link=link).first()
    player = Player.objects.filter(id=player_id).first()    
    temp = Ubung1.objects.filter(game=game).first()
    if temp:
        return 1
    else:
        return 0

@api
def ubung_1_get_data(player_id, link):
    from .models import Player, Game, Ubung1
    game = Game.objects.filter(link=link).first()
    player = Player.objects.filter(id=player_id).first()
    result = [i.api_json for i in Ubung1.objects.filter(game=game)]
    return result


@api
def ubung_1_api(player_id, link, data):
    from .models import Player, Game, Ubung1
    game = Game.objects.filter(link=link).first()
    player = Player.objects.filter(id=player_id).first()
    
    already = Ubung1.objects.filter(game=game)
    already_term_list = [i.power for i in already]
    for i in data:
        if i['value'] not in already_term_list:
            if i['player_id'] == -1:
                Ubung1.objects.create(
                    game=game,
                    player=None,
                    power=i['value'],
                    state=i['state'],
                )
                continue
            else:
                Ubung1.objects.create(
                    game=game,
                    player=player,
                    power=i['value'],
                    state=i['state'],
                )
                continue                
        else:
            temp = Ubung1.objects.filter(game=game,power=i['value']).first()
            if temp.state == i['state']:
                continue
            else:
                if i['state'] == 'tag':        
                    temp.state = i['state']
                    temp.player = None
                    temp.save()
                elif i['state'] == 'line-through':
                    temp.state = i['state']
                    temp.player = player
                    temp.save() 

    result_data = [i.api_json for i in list(Ubung1.objects.filter(game=game))]
    return result_data


@api
def check_ubung_3(player_id, link):
    from .models import Player, Game, Ubung3
    game = Game.objects.filter(link=link).first()
    player = Player.objects.filter(id=player_id).first()    
    temp = Ubung3.objects.filter(game=game).first()
    if temp:
        return 1
    else:
        return 0


@api 
def ubung_3_get_data(player_id, link):
    from .models import Player, Game, Ubung3
    game = Game.objects.filter(link=link).first()
    player = Player.objects.filter(id=player_id).first()
    result = [i.api_json for i in Ubung3.objects.filter(game=game)]
    return result


@api 
def ubung_3_api(player_id, link, data):
    from .models import Player, Game, Ubung3
    game = Game.objects.filter(link=link).first()
    player = Player.objects.filter(id=player_id).first()

    already = Ubung3.objects.filter(game=game)
    already_term_list = [i.drainer for i in already]
    for i in data:
        if i['value'] not in already_term_list:
            if i['player_id'] == -1:
                Ubung3.objects.create(
                    game=game,
                    player=None,
                    drainer=i['value'],
                    state=i['state'],
                )
                continue
            else:
                Ubung3.objects.create(
                    game=game,
                    player=player,
                    drainer=i['value'],
                    state=i['state'],
                )
                continue    
        else:
            temp = Ubung3.objects.filter(game=game,drainer=i['value']).first()
            if temp.state == i['state']:
                continue
            else:
                if i['state'] == 'tag':
                    temp.state = i['state']
                    temp.player = None
                    temp.save()
                elif i['state'] == 'line-through':
                    temp.state = i['state']
                    temp.player = player
                    temp.save()

    result_data = [i.api_json for i in list(Ubung3.objects.filter(game=game))]
    return result_data



@api
def ubung_5_data(link, user_id, data):
    import json
    game = Game.objects.filter(link=link).first()
    user = Player.objects.filter(id=user_id).first()
    data = json.loads(data)
    print(data, data.__class__)
    ubung5 = Ubung5.objects.filter(game=game,player=user).first()
    if ubung5:
        ubung5.delete()
    for i in data:
        Ubung5.objects.create(
            game = game,
            player = user,
            goal = Player.objects.filter(id=int(i['id'])).first(),
            score = int(i['status']),
        )
    # check whether others finish
    ubung_5 = [i.player for i in list(Ubung5.objects.filter(game=game))]
    waiting_room = [i.player for i in list(WaitingRoomMember.objects.filter(game=game))]
    for i in waiting_room:
        if i not in ubung_5:
            # someone not finished
            return 0
    # all finished
    return 1

    
@api
def check_game_name(game_name):
    game = Game.objects.filter(name=game_name).first()
    print(game)
    if game:
        # already taken
        return 0
    else:
        return 1
