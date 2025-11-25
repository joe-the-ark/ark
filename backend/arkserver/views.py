from django.shortcuts import render, redirect
from .utils import *
from .decorators import user_required, after_waitingroom
from meta.decorators import api, APIError
import json
from collections import defaultdict

from django.utils.translation import ugettext as _, gettext
from django.utils import translation
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from .models import *



@csrf_exempt
def testauth(request):
    if request.method == 'POST':
        name = request.POST.get('game')
        player_name = request.POST.get('player')  # Optional: player name or ID
        game = Game.objects.filter(name=name).first()
        if not game:
            return HttpResponse('Game not found')
        
        link = game.link
        print(link)
        
        # If player is specified, use that player; otherwise use game creator
        if player_name:
            # Try to find player by name first
            user = game.members.filter(name=player_name).first()
            # If not found by name, try by ID
            if not user:
                try:
                    player_id = int(player_name)
                    user = game.members.filter(id=player_id).first()
                except ValueError:
                    pass
            # If still not found, fall back to creator
            if not user:
                user = game.creator
        else:
            user = game.creator
        
        request.session['uid'] = user.id
        request.session['link'] = link
        return redirect('/potential-result')

    # Show form with game and optional player input
    return HttpResponse('''
        <form action="." method="POST">
            <label>Game name:</label><br>
            <input name="game" required /><br><br>
            <label>Player name or ID (optional, leave empty for creator):</label><br>
            <input name="player" placeholder="Player name or ID" /><br><br>
            <input type="submit" value="View Results" />
        </form>
    ''')



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
    ctx['used_avatars'] = []
    ctx['avatar_error'] = 0
    ctx['avatars_full'] = False

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

        game = Game.objects.filter(link=link).first()
        if not game:
            ctx['error'] = 1
            return render(request,'./views/auth-link.html', ctx)

        used_avatars = [i for i in list(game.members.values_list('avatar', flat=True)) if i]
        ctx['used_avatars'] = used_avatars
        ctx['avatars_full'] = len(set(used_avatars)) >= len(avatar_dict)

        if game.members.filter(name=username).first():
            # detect same name in this game
            ctx['error'] = 1
            return render(request,'./views/auth-link.html', ctx)

        if avatar in used_avatars:
            ctx['avatar_error'] = 1
            return render(request,'./views/auth-link.html', ctx)

        if ctx['avatars_full']:
            ctx['avatar_error'] = 1
            return render(request,'./views/auth-link.html', ctx)

        new_player = Player.objects.create(
            name = username,
            avatar = avatar,
        )
        request.session['uid'] = new_player.id
        game.members.add(new_player)
        WaitingRoomMember.objects.create(
            game = game,
            player = new_player,
            state = 0,
        )
        return redirect(f'/preview/')
            # return redirect(f'/wartezimmer/{link}/')

    return render(request,'./views/auth-link.html', ctx)


def link_enter(request, link):
    ctx = {}
    ctx['link'] = link
    game = Game.objects.filter(link=link).first()

    if not game:
        # invalid game link
        return redirect('/')

    used_avatars = []
    if game:
        used_avatars = [i for i in list(game.members.values_list('avatar', flat=True)) if i]
    ctx['used_avatars'] = used_avatars
    ctx['avatars_full'] = len(set(used_avatars)) >= len(avatar_dict)
    ctx['avatar_error'] = 0

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

        game = Game.objects.filter(link=link).first()
        if not game:
            ctx['error'] = 1
            return render(request,'./views/auth-link.html', ctx)

        used_avatars = [i for i in list(game.members.values_list('avatar', flat=True)) if i]
        ctx['used_avatars'] = used_avatars
        ctx['avatars_full'] = len(set(used_avatars)) >= len(avatar_dict)

        if game.members.filter(name=username).first():
            # detect same name in this game
            ctx['error'] = 1
            return render(request,'./views/auth-link.html', ctx)

        if avatar in used_avatars or ctx['avatars_full']:
            ctx['avatar_error'] = 1
            return render(request,'./views/auth-link.html', ctx)

        new_player = Player.objects.create(
            name = username,
            avatar = avatar,
        )
        request.session['uid'] = new_player.id
        game.members.add(new_player)
        WaitingRoomMember.objects.create(
            game = game,
            player = new_player,
            state = 0,
        )
        return redirect(f'/preview/')
            # return redirect(f'/wartezimmer/{link}/')

    return render(request,'./views/auth-link.html', ctx)


@user_required
def preview(request, user):
    ctx = {}
    ctx['game'] = Game.objects.filter(link=request.session['link']).first()
    return render(request, './views/preview.html', ctx)

@user_required
def ubung_2(request, user):
    ctx = {}
    ctx['game'] = game = Game.objects.filter(link=request.session['link']).first()

    if request.method == 'POST':
        link = request.session['link']
        digit_value = request.POST.get('digit_value')
        game = Game.objects.filter(link=link).first()
        Ubung2.objects.filter(game=game, player=user).delete()

        Ubung2.objects.create(
            game = game,
            player = user,
            value = digit_value,
        )
        return redirect(f'/ubung-1/')

    return render(request, './views/ubung-2.html', ctx)

@user_required
def ubung_1(request, user):
    ctx = {}
    ctx['game'] = game = Game.objects.filter(link=request.session['link']).first()
    player = user
    # temp = Ubung1.objects.filter(game=game).first()
    # if not temp:
    #     from .utils import ubung_1_term_list
    #     term_list = ubung_1_term_list
    #     for i in term_list:
    #         Ubung1.objects.create(
    #             game = game,
    #             player = None,
    #             state = 'tag',
    #             power = i['value'],
    #         )

    # ctx['term_list'] = [i.api_json for i in list(Ubung1.objects.filter(game=game))]

    # from .utils import ubung_1_term_list
    # term_list = ubung_1_term_list
    from .utils import ubung_1_term_list_i18n
    term_list = ubung_1_term_list_i18n
    ctx['term_list'] = term_list
    # print('term_list', term_list)

    return render(request, './views/ubung-1-pro.html', ctx)

@user_required
def ubung_3(request, user):
    ctx = {}
    ctx['game'] = game = Game.objects.filter(link=request.session['link']).first()


    player = user
    # temp = Ubung3.objects.filter(game=game).first()
    # if not temp:
    #     from .utils import ubung_3_term_list
    #     term_list = ubung_3_term_list
    #     for i in term_list:
    #         Ubung3.objects.create(
    #             game = game,
    #             player = None,
    #             state = 'tag',
    #             drainer = i['value'],
    #         )

    # ctx['term_list'] = [i.api_json for i in list(Ubung3.objects.filter(game=game))]

    # from .utils import ubung_3_term_list
    # term_list = ubung_3_term_list
    from .utils import ubung_3_term_list_i18n
    term_list = ubung_3_term_list_i18n
    ctx['term_list'] = term_list
    # print('term_list', term_list)

    return render(request, './views/ubung-3-pro.html', ctx)

@after_waitingroom
@user_required
def ubung_5(request, user):
    from .utils import span_choose

    ctx = {}
    ctx['game'] = Game.objects.filter(link=request.session['link']).first()
    link = request.session['link']
    game = Game.objects.filter(link=link).first()
    waiting_room = list(WaitingRoomMember.objects.filter(game=game,state=1))
    member_list = [i.player.player_json for i in waiting_room]
    ctx['member_list'] = member_list

    ubung1, ubung3 = span_choose(user.id, link)
    ctx['ubung1'] = ubung1
    ctx['ubung3'] = ubung3

    if not ubung1:
        return redirect('/ubung-4/')
        # ctx['loading'] = 1
        # return render(request, './views/ubung-5.html', ctx)

    # if request.method == 'POST':
    #     data = request.POST.get('data')
    #     ubung1_id = request.POST.get('ubung1_id')
    #     ubung3_id = request.POST.get('ubung3_id')
    #     data = json.loads(data)
    #     ubung5 = Ubung5.objects.filter(game=game,player=user,ubung3__id=ubung3_id).first()
    #     if ubung5:
    #         ubung5_list = list(Ubung5.objects.filter(game=game,player=user,ubung3__id=ubung3_id))
    #         uu = 0
    #         while uu < len(ubung5_list):
    #             ubung5_list[uu].delete()
    #             uu += 1
    #     for i in data:
    #         goal = Player.objects.filter(id=int(i['id'])).first()
    #         score = int(i['status'])
    #         ubung5 = span_add(user, goal, game, score, ubung1_id, ubung3_id)

    #         # Ubung5.objects.create(
    #         #     game = game,
    #         #     player = user,
    #         #     goal = Player.objects.filter(id=int(i['id'])).first(),
    #         #     score = int(i['status']),
    #         # )
    #     return redirect('/ubung-5/')

        # return redirect('/potential-result/')

    return render(request, './views/ubung-5.html', ctx)

@after_waitingroom
@user_required
def ubung_4(request, user):
    ctx = {}
    ctx['game'] = Game.objects.filter(link=request.session['link']).first()
    link = request.session['link']
    game = Game.objects.filter(link=link).first()
    # waiting_room = list(WaitingRoomMember.objects.filter(game=game).exclude(player=user))
    waiting_room = list(WaitingRoomMember.objects.filter(game=game,state=1))
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
        # reset previous selections so subsequent submissions replace earlier votes
        ubung4.row0.clear()
        ubung4.row1.clear()
        ubung4.row2.clear()
        ubung4.row3.clear()
        ubung4.row4.clear()
        ubung4.row5.clear()
        print(row0)
        print(row1)
        print(row2)
        print(row3)
        print(row4)
        print(row5)
        for i in set(row0):
            mem = Player.objects.filter(id=i).first()
            if mem:
                ubung4.row0.add(mem)
        for i in set(row1):
            mem = Player.objects.filter(id=i).first()
            if mem:
                ubung4.row1.add(mem)
        for i in set(row2):
            mem = Player.objects.filter(id=i).first()
            if mem:
                ubung4.row2.add(mem)
        for i in set(row3):
            mem = Player.objects.filter(id=i).first()
            if mem:
                ubung4.row3.add(mem)
        for i in set(row4):
            mem = Player.objects.filter(id=i).first()
            if mem:
                ubung4.row4.add(mem)
        for i in set(row5):
            mem = Player.objects.filter(id=i).first()
            if mem:
                ubung4.row5.add(mem)
        return redirect('/waiting-room2/')

    return render(request, './views/ubung-4.html', ctx)


@after_waitingroom
@user_required
def team_potential(request, user):
    ctx = {}
    ctx['game'] = Game.objects.filter(link=request.session['link']).first()
    link = request.session['link']
    game = Game.objects.filter(link=link).first()

    from .circle import calc_circles, calc_in_groups
    circles = calc_circles(game)
    in_groups = calc_in_groups(game, min_tolerance=1, max_tolerance=20)

    players = WaitingRoomMember.objects.filter(game=game, state=1)
    players_dict = { _.player.name: _.player.avatar for _ in players }

    anchors = {}
    current_lang = translation.get_language() or 'en'
    for member in players:
        anchor_entry = Ubung1.objects.filter(game=game, player=member.player).order_by('-create_time').first()
        if anchor_entry:
            if isinstance(anchor_entry.power_i18n, str):
                power_i18n = json.loads(anchor_entry.power_i18n)
            else:
                power_i18n = anchor_entry.power_i18n
            localized = power_i18n.get(current_lang, anchor_entry.power) if power_i18n else anchor_entry.power
            anchors[member.player.name] = localized
        else:
            anchors[member.player.name] = ''
    
    # Pass data directly to template - Django automatically handles serialization to JavaScript
    # This preserves Unicode characters correctly for Firefox compatibility
    ctx['circles'] = circles
    ctx['in_groups'] = in_groups
    ctx['players'] = players_dict
    ctx['anchors'] = anchors
    
    # Add PRIO 1 tooltip text for translation
    ctx['prio1_tooltip_text'] = gettext("PRIO 1: How to Put Integrators in Service of the Team's Psychological Safety Development\n\nIntegrators are team members who naturally belong to multiple psychological safe circles, acting as crucial bridges between different subgroups. To harness them for the team's safety development, a deliberate, multi-step approach is essential. First, identify these individuals by mapping the team's safe circles; they are the ones present in several overlapping zones of trust. Their strength lies in their ability to mediate between conflicting parties without being entangled in the drama. Second, provide them with support, protection, and relief. Acknowledge the often-unseen burden they carry and create structures that allow them to perform this role without burning out. Third, enable and encourage them to share their observations and suggestions within the team. Their unique, cross-cutting perspective can reveal tensions and offer solutions without forcing direct confrontation. Finally, only pursue the small, concrete steps (Babysteps) they propose that have broad team support. By strengthening these integrators, you leverage their existing trust to maintain and enhance psychological safety sustainably, focusing on the team's connective tissue rather than its fault lines.")
    
    # Add PRIO 2 tooltip text for translation
    ctx['prio2_tooltip_text'] = gettext("Priority 2: How to Integrate Solists / Satellites\n\nSatellites are team members who operate on the periphery, not yet integrated into any core safe circle. Integrating them requires a sensitive and intentional process. The first step is to identify them and recognize their potential. Their distanced position often grants them a clearer view of \"elephants in the room\" or hidden dynamics that more embedded members might miss. The second step is to facilitate their inclusion by identifying natural connection points. Look for existing integrators who can act as bridge-builders, or find projects or tasks where closer collaboration can occur organically. It is crucial, however, to first verify the satellite's own desire for greater integration; not everyone seeks deeper immersion, and forcing it can be counterproductive. If the interest is mutual, the final step involves targeted interventions for belonging, such as establishing regular check-ins or peer-learning formats. The goal is not to force everyone into one large, homogenous circle, but to carefully bring the satellite into at least one safe micro-structure, thereby enriching the team with their unique perspective and reducing the defensive reactions that isolation can foster.")
    
    # Add PRIO 3 tooltip text for translation
    ctx['prio3_tooltip_text'] = gettext("Priority 3: How to Securely Connect the Boss\n\nA leader's integration into the team's safe circles is a critical performance factor, yet they often systematically overestimate their own centrality and positive influence. To securely connect, the boss must first engage in honest self-reflection and seek a realistic assessment of the team's actual perception of psychological safety, contrasting it with one's own. The foundation for secure connection is the leader's inner security. This self-regulation ability—staying calm, curious, and flexible under pressure—is the safety anchor that prevents their stress from triggering defensive reactions across the team. With this foundation, the leader can then take conscious steps to increase their centrality. This is achieved not by command, but by actively participating in the team's safe circles, listening, and demonstrating vulnerability. The leader's role shifts to holding the space—creating and protecting an environment where open, drama-free communication can flourish. Ultimately, a leader can only foster a safe team if they are themselves a stable, integrated part of its psychological safe circles.")

    # ubung2 = Ubung2.objects.filter(game=game)
    ubung2 = []
    for i in list(Ubung2.objects.filter(game=game)):
        if i.player.valid:
            ubung2.append(i)
    value_list = [int(i.value) for i in ubung2]
    # print('value list111111111111111111', value_list)
    value_list.sort()
    temp = len(value_list)/2
    # print('-------------------------')
    temp_ = str(temp)
    # try:
    #     type(int(temp)) == int
    # except:
    #     # print('temp1',temp)
    #     temp = round(temp)
    #     median = value_list[temp]
    # else:
    #     # print('temp2',temp)
    #     temp = int(temp)
    #     median = (value_list[temp-1] + value_list[temp])/2

    # median = mean(value_list)
    from .utils import mean
    median = round(mean(value_list))
    # if temp_[-1] == '0':
    #     temp = int(temp)
    #     median = (value_list[temp-1] + value_list[temp])/2
    # else:
    #     temp = int(temp)
    #     median = value_list[temp]

    # if type(temp) == int:
    #     median = (value_list[temp-1] + value_list[temp])/2
    # else:
    #     temp = round(temp)
    #     median = value_list[temp]
    ctx['minimal'] = round(min(value_list))
    ctx['maximal'] = round(max(value_list))
    ctx['median'] = median
    ctx['user'] = user

    all_result = []
    flag =  0
    for i in value_list:
        if i == Ubung2.objects.filter(player=user).first().value:
            if flag == 0:
                all_result.append(
                    {
                        'name': user.name,
                        'avatar': user.avatar,
                        'statusSide': i
                    }
                )
                flag = 1
            else:
                all_result.append({"statusSide": i})
        else:
            all_result.append({"statusSide": i})
   
     # … dein Code bis hierher, der ctx['all_result'] und ctx['loading'] gesetzt hat …
    ctx['all_result'] = all_result
    ctx['loading']    = 0

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

    ctx['others'] = round(others, 2)
    ctx['himself'] = round(himself, 2)
    ctx['tension'] = round(tension, 2)

    json_list = [ i.span_1 for i in list(Ubung5.objects.filter(game=game)) ]
    # print('json_list', json_list)
    json_list.sort(key = lambda x:x['value'])
    ctx['json_list'] = json_list
    ctx['user'] = user

    players_qs = WaitingRoomMember.objects.filter(game=game, state=1)
    current_lang = translation.get_language() or 'en'
    anchor_map = {}
    for member in players_qs:
        anchor_entry = Ubung1.objects.filter(game=game, player=member.player).order_by('-create_time').first()
        if anchor_entry:
            label = anchor_entry.power_i18n.get(current_lang, anchor_entry.power)
            anchor_map.setdefault(label, []).append(member.player.name)
    ctx['anchor_map'] = json.dumps(anchor_map)
 
    return render(request, './views/spannungsfelder.html', ctx)


@user_required
def heatmap(request, user):
    from .utils import mean
    from arkserver.management.commands.utils import get_u5b
    ctx = {}
    game = Game.objects.filter(link=request.session['link']).first()

    if not game:
        return render(request, './views/heatmap.html', ctx)

    user_list = list(game.ubung5_player_order)
    user_number = len(user_list)
    ctx['user_number'] = user_number
    player_ids = [player.id for player in user_list]

    scale_order = list(game.ubung5_scale_order)

    ubung5_entries = list(
        Ubung5.objects.filter(game=game).select_related('player', 'goal', 'ubung1', 'ubung3')
    )

    score_lookup = {}
    goal_axis_counts = defaultdict(int)
    scale_axis_map = {}
    scale_drainer_map = {}

    for entry in ubung5_entries:
        axis_key = (entry.ubung1_id, entry.ubung3_id)
        score_lookup[(entry.player_id, entry.goal_id, axis_key)] = entry.score
        goal_axis_counts[(entry.goal_id, axis_key)] += 1
        if entry.ubung1_id not in scale_axis_map:
            scale_axis_map[entry.ubung1_id] = axis_key
        if entry.ubung1_id not in scale_drainer_map:
            scale_drainer_map[entry.ubung1_id] = entry.ubung3.drainer_i18n

    axis_keys = [
        scale_axis_map.get(scale.id, (scale.id, None))
        for scale in scale_order
    ]

    user_number_sq = user_number ** 2 if user_number else 1

    def classify_color(user_self_score, others_average, scale_avg):
        low_bound = scale_avg - 16
        high_bound = scale_avg + 16
        in_self = low_bound <= user_self_score <= high_bound
        in_others = low_bound <= others_average <= high_bound

        if not in_self and not in_others:
            return 'black'
        if not in_self and in_others:
            return 'red'
        if in_self and not in_others:
            return 'yellow'
        return 'None'

    main_map = []
    for player in user_list:
        player_id = player.id
        player_columns = []
        diff_values = []

        for index, scale in enumerate(scale_order):
            axis_key = axis_keys[index]

            user_self_score = score_lookup.get((player_id, player_id, axis_key), 0)
            others_scores = [
                score_lookup.get((other_id, player_id, axis_key), 0)
                for other_id in player_ids
                if other_id != player_id
            ]
            others_average = mean(others_scores) if others_scores else 0

            # Original calculation logic: direct difference and others average (no normalization)
            diff_value = round(user_self_score - others_average, 1)
            others_value = round(others_average, 1)
            color = classify_color(user_self_score, others_average, scale.ubung5_avg)

            player_columns.append([diff_value, color, others_value])
            diff_values.append(diff_value)

        total_diff = round(sum(diff_values))

        main_map.append([
            round(player.ubung5_sum / user_number_sq) if user_number else 0,
            player.name,
            player.avatar,
            player_columns,
            total_diff,
        ])

    row0 = []
    if main_map:
        column_count = len(main_map[0][3])
        for column_index in range(column_count):
            values = [player_data[3][column_index][0] for player_data in main_map]
            row0.append(round(mean(values)))

    pair_table = []
    for i in range(len(user_list)):
        for j in range(i + 1, len(user_list)):
            pair_table.append((user_list[i], user_list[j]))

    def fetch_score(player_id, goal_id, axis_key):
        return score_lookup.get((player_id, goal_id, axis_key), 0)

    beef_table = []
    for user1, user2 in pair_table:
        u1_id = user1.id
        u2_id = user2.id
        tension = 0

        for axis_key in axis_keys:
            u1_self = fetch_score(u1_id, u1_id, axis_key)
            u1_foreign = fetch_score(u2_id, u1_id, axis_key)
            u2_self = fetch_score(u2_id, u2_id, axis_key)
            u2_foreign = fetch_score(u1_id, u2_id, axis_key)

            tension += abs(u1_self - u1_foreign) + abs(u2_self - u2_foreign)

        beef_table.append({
            "user1": {"name": user1.name},
            "user2": {"name": user2.name},
            "tension": tension
        })

    u5b = get_u5b(game)
    ctx['stress'] = {key: round(value) for key, value in u5b.items()}

    ctx['row0'] = row0
    ctx['main_map'] = main_map

    def translate_drainer(scale):
        if scale.id in scale_drainer_map:
            return scale_drainer_map[scale.id]
        related = Ubung5.objects.filter(game=game, ubung1=scale).select_related('ubung3').first()
        return related.ubung3.drainer_i18n if related else {}

    ctx['scale_list'] = [
        [scale.power_i18n, translate_drainer(scale)]
        for scale in scale_order
    ]
    ctx['scale_value_list'] = [
        round(scale.ubung5_sum / user_number_sq) if user_number else 0
        for scale in scale_order
    ]
    ctx['beef_table'] = beef_table

    return render(request, './views/heatmap.html', ctx)


@after_waitingroom
@user_required
def preview_2(request, user):
    ctx = {}
    ctx['game'] = Game.objects.filter(link=request.session['link']).first()
    return render(request, './views/preview-2.html', ctx)


@after_waitingroom
@user_required
def mission_2_ubung_1(request, user):
    from .utils import m2_span_choose
    ctx = {}
    ctx['game'] = Game.objects.filter(link=request.session['link']).first()
    link = request.session['link']
    game = Game.objects.filter(link=link).first()
    waiting_room = list(WaitingRoomMember.objects.filter(game=game,state=1))
    # member_list = [i.player.player_json for i in waiting_room]


    ctx['member_list'] = []
    # print('member_list',member_list)

    ubung5 = m2_span_choose(user.id, link)
    if not ubung5:
        return redirect('/farewell/')
    ctx['ubung5'] = ubung5

    member_list = [ i.span_1 for i in Ubung5.objects.filter(game=game,goal=user,ubung1=ubung5.ubung1) ]

    temp = []
    if member_list[0]['id'] == user.id:
        pass
    else:
        uu = 0
        while uu < len(member_list):
            if member_list[uu]['id'] == user.id:
                temp.append(member_list[uu])
                del member_list[uu]
                break
            uu += 1
    member_list = temp + member_list
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
    waiting_room = list(WaitingRoomMember.objects.filter(game=game,state=1))
    member_list = [i.player.player_json for i in waiting_room]
    ctx['member_list'] = member_list

    json_list_all = [ i.span_1 for i in list(Ubung5.objects.filter(game=game)) ]
    json_list = [ i.span_1 for i in list(Ubung5.objects.filter(goal=user,game=game)) ]
    json_list.sort(key = lambda x:x['statusSide'])
    ctx['json_list'] = json_list
    ctx['json_list_all'] = json_list_all
    ctx['loading'] = 0
    ctx['user'] = user


    if request.method == 'POST':
        data = request.POST.get('data')
        # print(data)
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

        # from .utils import add_laststop
        # add_laststop(user, game)
        # ctx['loading'] = 1
        # return render(request, './views/mission-2-ubung-2.html', ctx)
        return redirect('/waiting-room3/')


    return render(request, './views/mission-2-ubung-2.html', ctx)


@after_waitingroom
@user_required
def assessment(request, user):
    ctx = {}
    ctx['game'] = Game.objects.filter(link=request.session['link']).first()
    link = request.session['link']
    game = Game.objects.filter(link=link).first()
    ubung2 = Ubung2.objects.filter(game=game)

    # bug fix #105 - no need to de-dup the value-list
    my_index = cnt = 0
    value_list = []

    for i in ubung2:
        if i.player == user:
            my_index = cnt

        value_list.append(int(i.value))
        cnt += 1

    temp = len(value_list)/2
    from .utils import mean
    median = mean(value_list)
    # if temp.__class__ == int:
    #     median = (value_list[temp-1] + value_list[temp])/2
    # else:
    #     temp = round(temp)
    #     median = value_list[temp]
    ctx['team_potential_minimal'] = round(min(value_list))
    ctx['team_potential_maximal'] = round(max(value_list))
    ctx['team_potential_median'] = round(median)
    ctx['user'] = user

    all_result = []
    cnt = 0
    for i in value_list:
        if cnt == my_index:
            all_result.append(
                {
                    'name': user.name,
                    'avatar': user.avatar,
                    'statusSide': i
                }
            )
        else:
            all_result.append({"statusSide": i})
        cnt += 1
    ctx['team_potential_all_result'] = all_result

    game_place = list(Ubung4.objects.filter(game=game))
    row_0 = 0
    row_1 = 0
    row_2 = 0
    row_3 = 0
    row_4 = 0
    row_5 = 0
    for game_ in game_place:

        row_0 += game_.row0.all().count()
        row_1 += game_.row1.all().count()
        row_2 += game_.row2.all().count()
        row_3 += game_.row3.all().count()
        row_4 += game_.row4.all().count()
        row_5 += game_.row5.all().count()

        # if game_.player == user:
        #     continue
        # else:
        #     if user in game_.row0.all():

        #         row_0 += 1
        #     if user in game_.row1.all():
        #         row_1 += 1
        #     if user in game_.row2.all():
        #         row_2 += 1
        #     if user in game_.row3.all():
        #         row_3 += 1
        #     if user in game_.row4.all():
        #         row_4 += 1
        #     if user in game_.row5.all():
        #         row_5 += 1

    score = (row_0 * 4 + row_1 * 1 + row_2 * 3 + row_3 * 5 + row_4 * 0 + row_5 * 2) * 20
    num = (WaitingRoomMember.objects.filter(game=game,state=1).count()) ** 2
    score = score / num

    ctx['psy_score'] = round(score)
    ctx['psy_row0'] = row_0
    ctx['psy_row1'] = row_1
    ctx['psy_row2'] = row_2
    ctx['psy_row3'] = row_3
    ctx['psy_row4'] = row_4
    ctx['psy_row5'] = row_5

    # print(game.ubung4_target)
    ubung4_target = game.ubung4_target
    ctx['row0'] = ubung4_target['row0']
    ctx['row1'] = ubung4_target['row1']
    ctx['row2'] = ubung4_target['row2']
    ctx['row3'] = ubung4_target['row3']
    ctx['row4'] = ubung4_target['row4']
    ctx['row5'] = ubung4_target['row5']

    # ubung4_list = Ubung4.objects.filter(game=game, player=user)


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
    json_list_all = [ i.span_1 for i in list(Ubung5.objects.filter(game=game)) ]
    json_list = [ i.span_1 for i in list(Ubung5.objects.filter(goal=user,game=game)) ]
    json_list.sort(key = lambda x:x['statusSide'])
    ctx['span_json_list'] = json_list
    ctx['json_all'] = json_list_all


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
    ctx['game'] = game = Game.objects.filter(link=request.session['link']).first()
    ctx['user'] = user
    
    # Calculate team potential median (performance value) from Ubung2
    ubung2 = Ubung2.objects.filter(game=game)
    value_list = []
    for i in ubung2:
        value_list.append(int(i.value))
    
    if value_list:
        from .utils import mean
        median = mean(value_list)
        ctx['team_potential_median'] = round(median)
    else:
        ctx['team_potential_median'] = None
    
    # Calculate psychological safety score (psy_score) from Ubung4
    game_place = list(Ubung4.objects.filter(game=game))
    row_0 = 0
    row_1 = 0
    row_2 = 0
    row_3 = 0
    row_4 = 0
    row_5 = 0
    for game_ in game_place:
        row_0 += game_.row0.all().count()
        row_1 += game_.row1.all().count()
        row_2 += game_.row2.all().count()
        row_3 += game_.row3.all().count()
        row_4 += game_.row4.all().count()
        row_5 += game_.row5.all().count()
    
    num = (WaitingRoomMember.objects.filter(game=game,state=1).count()) ** 2
    if num > 0:
        score = (row_0 * 4 + row_1 * 1 + row_2 * 3 + row_3 * 5 + row_4 * 0 + row_5 * 2) * 20
        score = score / num
        ctx['psy_score'] = round(score)
    else:
        ctx['psy_score'] = None
    
    # Determine scenario based on values
    # Threshold: 50 (middle of 0-99/0-100 scale)
    threshold = 50
    ctx['scenario'] = None
    ctx['orientation_text'] = None
    
    if ctx['psy_score'] is not None and ctx['team_potential_median'] is not None:
        psy_high = ctx['psy_score'] >= threshold
        performance_high = ctx['team_potential_median'] >= threshold
        difference = ctx['team_potential_median'] - ctx['psy_score']
        
        if psy_high and performance_high:
            # Both high - Normal case (high values)
            ctx['scenario'] = 'normal_high'
        elif not psy_high and not performance_high:
            # Both low - Normal case (low values)
            ctx['scenario'] = 'normal_low'
        elif not psy_high and performance_high:
            # Low safety, high performance - Case 1
            ctx['scenario'] = 'case1'
        elif psy_high and not performance_high:
            # High safety, low performance - Case 2
            ctx['scenario'] = 'case2'
        
        # Add orientation text based on difference
        orientation_threshold = 16
        if difference > orientation_threshold:
            # Performance deutlich höher als psychologische Sicherheit
            ctx['orientation_text'] = 'performance_higher'
            ctx['orientation_difference'] = difference
        elif difference < -orientation_threshold:
            # Psychologische Sicherheit deutlich höher als Performance
            ctx['orientation_text'] = 'safety_higher'
            ctx['orientation_difference'] = abs(difference)
        else:
            # Werte liegen nah beieinander
            ctx['orientation_text'] = 'values_close'
            ctx['orientation_difference'] = abs(difference)
    
    return render(request, './views/arche.html', ctx)


@user_required
def wartezimmer(request, user):
    ctx = {}
    ctx['game'] = Game.objects.filter(link=request.session['link']).first()
    link = request.session['link']
    # user = ctx['user'] = Player.objects.filter(id=request.session.get('uid')).first()
    game = Game.objects.filter(link=link).first()

    # check whehter the ubung1 and ubung3 have 2 or more records by the player
    # player_list = list(game.members.all())
    # for player in player_list:
    ubung1_list = list(Ubung1.objects.filter(player=user).order_by('-create_time'))
    if len(ubung1_list) >= 2:
        uu = 1
        while uu < len(ubung1_list):
            ubung1_list[uu].player = None
            ubung1_list[uu].state = 'tag'
            ubung1_list[uu].save()
            uu += 1
    ubung3_list = list(Ubung3.objects.filter(player=user).order_by('-create_time'))
    if len(ubung3_list) >= 2:
        uu = 1
        while uu < len(ubung3_list):
            ubung3_list[uu].player = None
            ubung3_list[uu].state = 'tag'
            ubung3_list[uu].save()
            uu += 1

    ubung1_temp = Ubung1.objects.filter(player=user).first()
    if not ubung1_temp:
        return redirect(f'/ubung-1/')
    ubung3_temp = Ubung3.objects.filter(player=user).first()
    if not ubung3_temp:
        return redirect(f'/ubung-3/')



    if game.status != 0:
        return redirect('/ubung-5/')
    room_member = WaitingRoomMember.objects.filter(game=game,player=user).first()
    room_member.state = 1
    room_member.save()

    ctx['avatar'] = user.avatar
    ctx['player_name'] = user.name
    ctx['player_id'] = user.id
    ctx['link'] = link
    ctx['host'] = game.creator

    if request.method == 'POST':
        nums = WaitingRoomMember.objects.filter(game=game).count()
        if user != game.creator:
            if nums < 3:
                return render(request, './views/wartezimmer.html', ctx)
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
                game.save()

                player_ = WaitingRoomMember.objects.filter(game=game,player=user).first()
                player_.state = 1
                player_.save()
                return redirect('/ubung-5/')

        # if nums < 3:
        #     return
        #     # pass
        #     # return redirect('/ubung-4/')
        # else:

        #     return redirect('/ubung-4/')
    ubung1 = Ubung1.objects.filter(player=user).first()
    ubung3 = Ubung3.objects.filter(player=user).first()
    ctx['scale'] = [ubung1.power_i18n, ubung3.drainer_i18n]

    return render(request, './views/wartezimmer.html', ctx)


@api
def check_ubung1_ubung3_blank(user_id):
    user = Player.objects.filter(id=int(user_id)).first()
    ubung1 = Ubung1.objects.filter(player=user).first()
    ubung3 = Ubung3.objects.filter(player=user).first()
    if not ubung1:
        return '1'
    if not ubung3:
        return '3'
    return 0


@user_required
def waiting_room2(request, user):
    ctx = {}
    ctx['game'] = game = Game.objects.filter(link=request.session['link']).first()

    ctx['avatar'] = user.avatar
    ctx['player_name'] = user.name
    ctx['player_id'] = user.id
    ctx['link'] = game.link
    ctx['host'] = game.creator
    user_waiting = Waitingroom2.objects.filter(game=game, player=user).first()
    if user_waiting:
        pass
    else:
        user_waiting = Waitingroom2.objects.create(
            game = game,
            player = user,
        )

    link = request.session['link']
    game = Game.objects.filter(link=link).first()

    from .circle import calc_circles
    ctx['circles'] = circles = calc_circles(game)

    players = WaitingRoomMember.objects.filter(game=game, state=1)

    ctx['players'] = { _.player.name: _.player.avatar for _ in players }

    # ubung2 = Ubung2.objects.filter(game=game)
    ubung2 = []
    for i in list(Ubung2.objects.filter(game=game)):
        if i.player.valid:
            ubung2.append(i)
    value_list = [int(i.value) for i in ubung2]
    # print('value list111111111111111111', value_list)
    value_list.sort()
    temp = len(value_list)/2
    # print('-------------------------')
    temp_ = str(temp)
    # try:
    #     type(int(temp)) == int
    # except:
    #     # print('temp1',temp)
    #     temp = round(temp)
    #     median = value_list[temp]
    # else:
    #     # print('temp2',temp)
    #     temp = int(temp)
    #     median = (value_list[temp-1] + value_list[temp])/2

    # median = mean(value_list)
    from .utils import mean
    median = round(mean(value_list))
    # if temp_[-1] == '0':
    #     temp = int(temp)
    #     median = (value_list[temp-1] + value_list[temp])/2
    # else:
    #     temp = int(temp)
    #     median = value_list[temp]

    # if type(temp) == int:
    #     median = (value_list[temp-1] + value_list[temp])/2
    # else:
    #     temp = round(temp)
    #     median = value_list[temp]
    ctx['minimal'] = round(min(value_list))
    ctx['maximal'] = round(max(value_list))
    ctx['median'] = median
    ctx['user'] = user

    all_result = []
    flag =  0
    for i in value_list:
        if i == Ubung2.objects.filter(player=user).first().value:
            if flag == 0:
                all_result.append(
                    {
                        'name': user.name,
                        'avatar': user.avatar,
                        'statusSide': i
                    }
                )
                flag = 1
            else:
                all_result.append({"statusSide": i})
        else:
            all_result.append({"statusSide": i})
    ctx['all_result'] = all_result
    ctx['loading'] = 0
    # damit das Mini‑Graph‑Script in waiting_room2.html funktioniert
    ctx['team_potential_all_result'] = all_result

    ctx['team_potential_minimal'] = ctx['minimal']
    ctx['team_potential_median']  = ctx['median']
    ctx['team_potential_maximal'] = ctx['maximal']

    # --- BEGIN: provide graph‑ and feedback‑data for waiting_room2.html ---
    # safezoneData → an array of all statusSide values (for the blue “safe zone” overlay).
    ctx['safezoneData'] = [item['statusSide'] for item in ctx['all_result']]

    # Waitingroom2Start
    if request.method == 'POST':

        # ubung5 check finish
        mem_list = [i.player for i in list(WaitingRoomMember.objects.filter(game=game,state=1))]
        ubung5_list = Ubung5.objects.filter(game=game)
        mem_num = len(mem_list)
        item_num = len(list(ubung5_list))
        if item_num != (mem_num ** 3):
            return redirect('/psychologischer/')

        if user == game.creator:
            waiting2 = Waitingroom2Start.objects.filter(
                game = game
            ).first()
            if waiting2:
                waiting2.status = 1
                waiting2.save()
            else:
                Waitingroom2Start.objects.create(
                    game = game,
                    status = 1,
                )
            return redirect('/psychologischer/')

    return render(request, './views/waiting_room2.html', ctx)

import json
from django.utils.translation import get_language
from .models import Game, Waitingroom2, Ubung1, Ubung3, Player
from meta.decorators import api

@api
def waiting_room2_active(player_id, link):
    game         = Game.objects.filter(link=link).first()
    waiting_room = Waitingroom2.objects.filter(game=game)
    lang         = get_language()  # z.B. 'de', 'en', …

    members = []
    for wr in waiting_room:
        p   = wr.player
        ub1 = Ubung1.objects.filter(game=game, player=p).order_by('-create_time').first()
        ub3 = Ubung3.objects.filter(game=game, player=p).order_by('-create_time').first()

        power_dict = (json.loads(ub1.power_i18n)   if isinstance(ub1.power_i18n, str)   else ub1.power_i18n)   if ub1 else {}
        drain_dict = (json.loads(ub3.drainer_i18n) if isinstance(ub3.drainer_i18n, str) else ub3.drainer_i18n) if ub3 else {}

        power   = power_dict.get(lang, power_dict.get('en', ''))
        drainer = drain_dict.get(lang, drain_dict.get('en', ''))

        members.append({
            'id'           : p.id,
            'name'         : p.name,
            'avatar'       : p.avatar,
            'item_power'   : power,
            'item_drainer' : drainer,
        })
    return members


@api
def waiting_room2_yet(player_id, link):
    game = Game.objects.filter(link=link).first()
    all_members = game.valid_players
    waiting_room2 = [i.player for i in Waitingroom2.objects.filter(game=game)]
    result = []
    for i in all_members:
        if i not in waiting_room2:
            result.append(i)
    results = [i.player_json for i in result]
    return results

@api
def waiting_room2_game_start(link):
    game = Game.objects.filter(link=link).first()
    waiting2 = Waitingroom2Start.objects.filter(game=game).first()
    if waiting2:
        if waiting2.status == 1:
            return 1
        else:
            return 0
    else:
        return 0


@user_required
def waiting_room3(request, user):
    ctx = {}
    ctx['game'] = game = Game.objects.filter(link=request.session['link']).first()
    ctx['avatar'] = user.avatar
    ctx['player_name'] = user.name
    ctx['player_id'] = user.id
    ctx['link'] = game.link
    ctx['host'] = game.creator

    user_waiting = Waitingroom3.objects.filter(game=game, player=user).first()
    if user_waiting:
        pass
    else:
        user_waiting = Waitingroom3.objects.create(
            game = game,
            player = user,
        )

    # Waitingroom3Start
    if request.method == 'POST':
        if user ==  game.creator:
            waiting3 = Waitingroom3Start.objects.filter(
                game = game,
            ).first()
            if waiting3:
                waiting3.status = 1
                waiting3.save()
            else:
                Waitingroom3Start.objects.create(
                    game = game,
                    status = 1,
                )
            return redirect('/assessment/')

    return render(request, './views/waiting_room3.html', ctx)

import json
from django.utils.translation import get_language
from .models import Game, Waitingroom3, Ubung1, Ubung3, Player
from meta.decorators import api

@api
def waiting_room3_active(player_id, link):
    game         = Game.objects.filter(link=link).first()
    waiting_room = Waitingroom3.objects.filter(game=game)
    lang         = get_language()  # e.g. 'de', 'en', …

    members = []
    for wr in waiting_room:
        p   = wr.player
        ub1 = Ubung1.objects.filter(game=game, player=p).order_by('-create_time').first()
        ub3 = Ubung3.objects.filter(game=game, player=p).order_by('-create_time').first()

        power_dict = (json.loads(ub1.power_i18n)   if isinstance(ub1.power_i18n, str)   else ub1.power_i18n)   if ub1 else {}
        drain_dict = (json.loads(ub3.drainer_i18n) if isinstance(ub3.drainer_i18n, str) else ub3.drainer_i18n) if ub3 else {}

        power   = power_dict.get(lang, power_dict.get('en', ''))
        drainer = drain_dict.get(lang, drain_dict.get('en', ''))

        members.append({
            'id'           : p.id,
            'name'         : p.name,
            'avatar'       : p.avatar,
            'item_power'   : power,
            'item_drainer' : drainer,
        })
    return members

@api
def waiting_room3_yet(player_id, link):
    game = Game.objects.filter(link=link).first()
    all_members = game.valid_players
    waiting_room3 = [i.player for i in Waitingroom3.objects.filter(game=game)]
    result = []
    for i in all_members:
        if i not in waiting_room3:
            result.append(i)
    results = [i.player_json for i in result]
    return results

@api
def waiting_room3_game_start(link):
    game = Game.objects.filter(link=link).first()
    waiting3 = Waitingroom3Start.objects.filter(game=game).first()
    if waiting3:
        if waiting3.status == 1:
            return 1
        else:
            return 0
    else:
        return 0


@user_required
def psychologischer(request, user):
    ctx = {}
    ctx['game'] = Game.objects.filter(link=request.session['link']).first()
    link = request.session['link']
    game = Game.objects.filter(link=link).first()
    game_place = list(Ubung4.objects.filter(game=game))
    
    # Count how many times the current user appears in each row
    row_0 = 0
    row_1 = 0
    row_2 = 0
    row_3 = 0
    row_4 = 0
    row_5 = 0
    
    # Count how many times the current user appears in each row across all Ubung4 entries
    # Use ubung4_target which contains all players in each box, then filter for current user
    # This is more reliable than iterating through Ubung4 entries
    ubung4_target = game.ubung4_target
    
    # Get all players in each row
    row0_all = ubung4_target.get('row0', [])
    row1_all = ubung4_target.get('row1', [])
    row2_all = ubung4_target.get('row2', [])
    row3_all = ubung4_target.get('row3', [])
    row4_all = ubung4_target.get('row4', [])
    row5_all = ubung4_target.get('row5', [])
    
    # Get all players in each box using ubung4_target
    ubung4_target = game.ubung4_target
    row0_all = ubung4_target.get('row0', [])
    row1_all = ubung4_target.get('row1', [])
    row2_all = ubung4_target.get('row2', [])
    row3_all = ubung4_target.get('row3', [])
    row4_all = ubung4_target.get('row4', [])
    row5_all = ubung4_target.get('row5', [])
    
    # Separate current user votes from other players' votes
    # Current user votes will be shown with avatar in blue circles
    # Other players' votes will be shown as anonymous gray circles
    row0_current_user = [p for p in row0_all if p.get('id') == user.id]
    row0_other_players = [p for p in row0_all if p.get('id') != user.id]
    
    row1_current_user = [p for p in row1_all if p.get('id') == user.id]
    row1_other_players = [p for p in row1_all if p.get('id') != user.id]
    
    row2_current_user = [p for p in row2_all if p.get('id') == user.id]
    row2_other_players = [p for p in row2_all if p.get('id') != user.id]
    
    row3_current_user = [p for p in row3_all if p.get('id') == user.id]
    row3_other_players = [p for p in row3_all if p.get('id') != user.id]
    
    row4_current_user = [p for p in row4_all if p.get('id') == user.id]
    row4_other_players = [p for p in row4_all if p.get('id') != user.id]
    
    row5_current_user = [p for p in row5_all if p.get('id') == user.id]
    row5_other_players = [p for p in row5_all if p.get('id') != user.id]
    
    # Count occurrences for score calculation
    row_0 = len(row0_current_user)
    row_1 = len(row1_current_user)
    row_2 = len(row2_current_user)
    row_3 = len(row3_current_user)
    row_4 = len(row4_current_user)
    row_5 = len(row5_current_user)
    
    # Debug: Print info
    print(f"DEBUG psychologischer: user {user.id} ({user.name}) appears:")
    print(f"  row0: {row_0} times (others: {len(row0_other_players)})")
    print(f"  row1: {row_1} times (others: {len(row1_other_players)})")
    print(f"  row2: {row_2} times (others: {len(row2_other_players)})")
    print(f"  row3: {row_3} times (others: {len(row3_other_players)})")
    print(f"  row4: {row_4} times (others: {len(row4_other_players)})")
    print(f"  row5: {row_5} times (others: {len(row5_other_players)})")

    score = (row_0 * 4 + row_1 * 1 + row_2 * 3 + row_3 * 5 + row_4 * 0 + row_5 * 2) * 20
    num = (WaitingRoomMember.objects.filter(game=game,state=1).count()) ** 2
    score = score / num if num > 0 else 0

    ctx['score'] = round(score)
    
    # Pass arrays for Vue.js
    # Each row has two arrays: current_user (blue circles with avatar) and other_players (gray anonymous circles)
    import json
    ctx['row0_current_user'] = json.dumps([{} for _ in range(max(0, row_0))])
    ctx['row0_other_players'] = json.dumps([{} for _ in range(max(0, len(row0_other_players)))])
    ctx['row1_current_user'] = json.dumps([{} for _ in range(max(0, row_1))])
    ctx['row1_other_players'] = json.dumps([{} for _ in range(max(0, len(row1_other_players)))])
    ctx['row2_current_user'] = json.dumps([{} for _ in range(max(0, row_2))])
    ctx['row2_other_players'] = json.dumps([{} for _ in range(max(0, len(row2_other_players)))])
    ctx['row3_current_user'] = json.dumps([{} for _ in range(max(0, row_3))])
    ctx['row3_other_players'] = json.dumps([{} for _ in range(max(0, len(row3_other_players)))])
    ctx['row4_current_user'] = json.dumps([{} for _ in range(max(0, row_4))])
    ctx['row4_other_players'] = json.dumps([{} for _ in range(max(0, len(row4_other_players)))])
    ctx['row5_current_user'] = json.dumps([{} for _ in range(max(0, row_5))])
    ctx['row5_other_players'] = json.dumps([{} for _ in range(max(0, len(row5_other_players)))])
    
    # Pass current user's avatar and name to frontend
    ctx['current_user_avatar'] = user.avatar
    ctx['current_user_name'] = user.name
    
    # Debug: Add counts to context for debugging
    ctx['debug_counts'] = json.dumps({
        'row0_current_user': row_0,
        'row0_other_players': len(row0_other_players),
        'row1_current_user': row_1,
        'row1_other_players': len(row1_other_players),
        'row2_current_user': row_2,
        'row2_other_players': len(row2_other_players),
        'row3_current_user': row_3,
        'row3_other_players': len(row3_other_players),
        'row4_current_user': row_4,
        'row4_other_players': len(row4_other_players),
        'row5_current_user': row_5,
        'row5_other_players': len(row5_other_players),
        'total_ubung4_entries': len(game_place),
    })
    
    return render(request, './views/psychologischer.html', ctx)

def logout(request):
    if 'uid' in request.session:
        del request.session['uid']
    if 'link' in request.session:
        del request.session['link']
    return redirect('/')




# apis

@api
def waiting_room_game_start(link):
    game = Game.objects.filter(link=link).first()
    if game.status == 1:
        return 1
    else:
        return 0

from .models import Ubung1, Ubung3
import json
from django.utils.translation import get_language

@api
def waiting_room_active(player_id, link):
    from .models import Player, Game, WaitingRoomMember, Ubung1, Ubung3

    game         = Game.objects.filter(link=link).first()
    waiting_room = WaitingRoomMember.objects.filter(game=game, state=1)
    lang         = get_language()  # z.B. 'de', 'en', 'fr', 'it'

    members = []
    for wr in waiting_room:
        p   = wr.player

        # hole die zuletzt gespeicherten Begriffe
        ub1 = Ubung1.objects.filter(game=game, player=p).order_by('-create_time').first()
        ub3 = Ubung3.objects.filter(game=game, player=p).order_by('-create_time').first()

        # power_i18n und drainer_i18n sind Dicts oder JSON‑Strings
        power_dict = (
            json.loads(ub1.power_i18n) if isinstance(ub1.power_i18n, str)
            else ub1.power_i18n
        ) if ub1 else {}
        drainer_dict = (
            json.loads(ub3.drainer_i18n) if isinstance(ub3.drainer_i18n, str)
            else ub3.drainer_i18n
        ) if ub3 else {}

        # nur das aktuelle Sprach‑Feld nehmen, ansonsten Fallback auf 'en'
        power   = power_dict.get(lang,   power_dict.get('en', ''))
        drainer = drainer_dict.get(lang, drainer_dict.get('en', ''))

        members.append({
            'id'           : p.id,
            'name'         : p.name,
            'avatar'       : p.avatar,
            'item_power'   : power,
            'item_drainer' : drainer,
        })

    return members


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
    # print('data', data)
    from .models import Player, Game, Ubung1
    game = Game.objects.filter(link=link).first()
    player = Player.objects.filter(id=player_id).first()

    already = list(Ubung1.objects.filter(game=game))
    already_term_list = [i.power for i in already]
    # print('already_term_list',already_term_list)
    # print('------------------------------------------')
    # print('data',data)
    for i in data:
        if i['value'] not in already_term_list:
            if i['player_id'] == -1:
                # Ubung1.objects.create(
                #     game=game,
                #     player=None,
                #     power=i['value'],
                #     state=i['state'],
                # )
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
    # print('------------------------------------------')
    # print('result_data', result_data)
    print('result_data', result_data)
    return result_data


# Add Turkish language support to all your API functions

@api
def ubung_1_api_pro(player_id, link, item, lang_code):
    from .models import Player, Game, Ubung1
    from .utils import ubung_1_term_list_i18n
    game = Game.objects.filter(link=link).first()
    player = Player.objects.filter(id=player_id).first()

    if lang_code == 'en':
        lang_name = 'English'
    elif lang_code == 'de':
        lang_name = 'Deutsch'
    elif lang_code == 'zh-hans':
        lang_name = 'Chinese'
    elif lang_code == 'fr':
        lang_name = 'French'
    elif lang_code == 'tr':  # Add Turkish support
        lang_name = 'Turkish'
    else:
        lang_name = 'English'  # Default to English

    item_id = -1
    for i in ubung_1_term_list_i18n[lang_name]:
        if i['value'] == item:
            item_id = i['id']
    if item_id != -1:
        for i in ubung_1_term_list_i18n['English']:
            if item_id == i['id']:
                item = i['value']

    ubung1 = Ubung1.objects.filter(game=game,player=player).first()
    if ubung1:
        ubung1.power = item
        ubung1.save()
    else:
        Ubung1.objects.create(game=game,player=player,power=item,state='line-through')

    result_data = [i.api_json for i in list(Ubung1.objects.filter(game=game,player=player))]
    print('result_data', result_data)
    return result_data

@api
def warteimmer_api_pro(player_id, link, item_power, item_drainer, lang_code):
    from .models import Player, Game, Ubung1, Ubung3
    from .utils import ubung_1_term_list_i18n
    from .utils import ubung_3_term_list_i18n
    game = Game.objects.filter(link=link).first()
    player = Player.objects.filter(id=player_id).first()

    if lang_code == 'en':
        lang_name = 'English'
    elif lang_code == 'de':
        lang_name = 'Deutsch'
    elif lang_code == 'zh-hans':
        lang_name = 'Chinese'
    elif lang_code == 'fr':
        lang_name = 'French'
    elif lang_code == 'tr':  # Add Turkish support
        lang_name = 'Turkish'
    else:
        lang_name = 'English'  # Default to English

    item_id = -1
    for i in ubung_1_term_list_i18n[lang_name]:
        if i['value'] == item_power:
            item_id = i['id']
    if item_id != -1:
        for i in ubung_1_term_list_i18n['English']:
            if item_id == i['id']:
                item_power= i['value']

    ubung1 = Ubung1.objects.filter(game=game,player=player).first()
    if ubung1:
        ubung1.power = item_power
        ubung1.save()
    else:
        Ubung1.objects.create(game=game,player=player,power=item_power,state='line-through')


    item_id = -1
    for i in ubung_3_term_list_i18n[lang_name]:
        if i['value'] == item_drainer:
            item_id = i['id']
    if item_id != -1:
        for i in ubung_3_term_list_i18n['English']:
            if item_id == i['id']:
                item_drainer = i['value']

    ubung3 = Ubung3.objects.filter(game=game,player=player).first()
    if ubung3:
        ubung3.drainer = item_drainer
        ubung3.save()
    else:
        Ubung3.objects.create(game=game,player=player,drainer=item_drainer,state='line-through')


    result_data = ''
    print('result_data', result_data)
    return result_data

@api
def ubung_3_api_pro(player_id, link, item, lang_code):
    from .models import Player, Game, Ubung3, Ubung1
    from .utils import ubung_3_term_list_i18n
    game = Game.objects.filter(link=link).first()
    player = Player.objects.filter(id=player_id).first()

    if lang_code == 'en':
        lang_name = 'English'
    elif lang_code == 'de':
        lang_name = 'Deutsch'
    elif lang_code == 'zh-hans':
        lang_name = 'Chinese'
    elif lang_code == 'fr':
        lang_name = 'French'
    elif lang_code == 'tr':  # Add Turkish support
        lang_name = 'Turkish'
    else:
        lang_name = 'English'  # Default to English

    item_id = -1
    for i in ubung_3_term_list_i18n[lang_name]:
        if i['value'] == item:
            item_id = i['id']
    if item_id != -1:
        for i in ubung_3_term_list_i18n['English']:
            if item_id == i['id']:
                item = i['value']

    ubung3 = Ubung3.objects.filter(game=game,player=player).first()
    if ubung3:
        ubung3.drainer = item
        ubung3.save()
    else:
        ubung3 = Ubung3.objects.create(game=game,player=player,drainer=item,state='line-through')

    if Ubung3.objects.filter(game=game,drainer=item).exclude(player=player).first():
        if Ubung1.objects.filter(game=game,player=Ubung3.objects.filter(game=game,drainer=item).exclude(player=player).first().player).first().power == ubung3.connect_ubung1.power:
            ubung3.delete()
            return 0
    result_data = [i.api_json for i in list(Ubung3.objects.filter(game=game,player=player))]
    print('result_data', result_data)
    return result_data

@api
def check_ubung5_finish(link):
    from .models import Ubung5
    game = Game.objects.filter(link=link).first()
    mem_list = [i.player for i in list(WaitingRoomMember.objects.filter(game=game,state=1))]
    ubung5_list = Ubung5.objects.filter(game=game)

    # delete ubung-5 if someone change the ubung-1 or ubung-3
    # ubung5_ubung1_user_list = [i.ubung1.player for i in ubung5_list]
    # if None in ubung5_ubung1_user_list:
    #     delete_list = []
    #     for i in ubung5_list:
    #         if i.ubung1.player == None:
    #             delete_list.append(i)
    #     for i in delete_list:
    #         i.delete()
    #     return 2
    # ubung5_ubung3_user_list = [i.ubung3.player for i in ubung5_list]
    # if None in ubung5_ubung3_user_list:
    #     delete_list = []
    #     for i in ubung5_list:
    #         if i.ubung3.player == None:
    #             delete_list.append(i)
    #     for i in delete_list:
    #         i.delete()
    #     return 2


    # ubung5_player_list = [i.player for i in list(Ubung5.objects.filter(game=game))]
    mem_num = len(mem_list)
    # for i in mem_list:
    item_num = len(list(ubung5_list))
    if item_num != (mem_num ** 3):
        return 0
    return 1


@api
def ubung5_data(link, user_id, data, ubung1_id, ubung3_id):

    ubung1_id = int(ubung1_id)
    ubung3_id = int(ubung3_id)
    print(ubung1_id)
    print(ubung3_id)
    import json
    game = Game.objects.filter(link=link).first()
    user = Player.objects.filter(id=user_id).first()
    data = json.loads(data)
    print(data, data.__class__)
    ubung5 = Ubung5.objects.filter(game=game,player=user,ubung3__id=ubung3_id).first()
    if ubung5:
        ubung5_list = list(Ubung5.objects.filter(game=game,player=user,ubung3__id=ubung3_id))
        uu = 0
        while uu < len(ubung5_list):
            ubung5_list[uu].delete()
            uu += 1
    for i in data:
        goal = Player.objects.filter(id=int(i['id'])).first()
        score = int(i['status'])
        ubung5 = span_add(user, goal, game, score, ubung1_id, ubung3_id)
    return 1
        # Ubung5.objects.create(
        #     game = game,
        #     player = user,
        #     goal = Player.objects.filter(id=int(i['id'])).first(),
        #     score = int(i['status']),
        # )
    # check whether others finish
    # ubung_5 = [i.player for i in list(Ubung5.objects.filter(game=game))]
    # waiting_room = [i.player for i in list(WaitingRoomMember.objects.filter(game=game))]
    # for i in waiting_room:
    #     if i not in ubung_5:
    #         # someone not finished
    #         return 0
    # # all finished
    # return 1

@api
def m2_ubung5_data(link, user_id, data, ubung1_id, ubung3_id):
    from .models import M2Ubung1
    ubung1_id = int(ubung1_id)
    ubung3_id = int(ubung3_id)
    import json
    game = Game.objects.filter(link=link).first()
    user = Player.objects.filter(id=user_id).first()
    data = json.loads(data)
    print(data, data.__class__)
    m2 = M2Ubung1.objects.filter(game=game,player=user,ubung3__id=ubung3_id).first()
    if m2:
        m2_list = list(M2Ubung1.objects.filter(game=game,player=user,ubung3__id=ubung3_id))
        uu = 0
        while uu < len(m2_list):
            m2_list[uu].delete()
            uu += 1
    for i in data:
        goal = Player.objects.filter(id=int(i['id'])).first()
        score = int(i['status'])
        m2 = m2_span_add(user, goal, game, score, ubung1_id, ubung3_id)
    return 1


@api
def check_game_name(game_name):
    game = Game.objects.filter(name=game_name).first()
    if game:
        # already taken
        return 0
    else:
        # name is valid
        return 1

@api
def check_player_name(player_name, link):
    game = Game.objects.filter(link=link).first()
    player = Player.objects.filter(name=player_name,game=game).first()
    if player:
        # already taken
        return 0
    else:
        # name is valid
        return 1



@api
def check_game_is_after_waiting_room(link):
    game = Game.objects.filter(link=link).first()
    if game.status == 1:
        # game can't join anymore
        return 0
    else:
        return 1


@api
def last_stop_check(link):
    game = Game.objects.filter(link=link).first()
    stop_list = [i.player for i in list(LastStop.objects.filter(game=game))]
    player_list = game.valid_players
    # print(stop_list)
    # print(player_list)
    for i in player_list:
        if i not in stop_list:
            return 0
    return 1
