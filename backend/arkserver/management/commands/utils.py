from arkserver.models import *
from arkserver.utils import *


r1 = lambda x: round(x)



def get_n(game):
    nplayers = WaitingRoomMember.objects.filter(game=game,state=1)
    n = nplayers.count()
    return n

def get_u2_avg(game):
    players = game.members.all()
    #n = get_n(game)
    n = 0

    u2_score = 0
    for player in players:
        u2 = Ubung2.objects.filter(game=game, player=player).first()
        if not u2: continue
        
        value = u2.value
        u2_score += value
        n += 1

    u2_score /= n
    return u2_score

def get_u4_avg(game):
    n = get_n(game)
    r0, r1, r2, r3, r4, r5 = 0, 0, 0, 0, 0, 0
    w0, w1, w2, w3, w4, w5 = 4, 1, 3, 5, 0, 2
    for vote in Ubung4.objects.filter(game=game):
        r0 += vote.row0.count()
        r1 += vote.row1.count()
        r2 += vote.row2.count()
        r3 += vote.row3.count()
        r4 += vote.row4.count()
        r5 += vote.row5.count()

    u4_score = r0*w0+r1*w1+r2*w2+r3*w3+r4*w4+r5*w5
    u4_score = u4_score * 20 / n**2
    return u4_score

def get_u5(game):
    n = get_n(game)
    players = WaitingRoomMember.objects.filter(game=game, state=1)

    votes = {}
    count = 0
    for player in players:
        p = player.player

        if not Ubung5.objects.filter(game=game, goal=p).exists():
            continue

        pvotes = votes[p.name] = {}
        count += 1

        for vote in Ubung5.objects.filter(game=game, goal=p):
            power = vote.ubung1.power + '~' + vote.ubung3.drainer
            if power not in pvotes:
                pvotes[power] = {}

            pvotes[power][vote.player.name] = vote.score

    return votes, count


def get_u5_avg(game):
    n = get_n(game)
    players = WaitingRoomMember.objects.filter(game=game,state=1)
    u5_sum = 0
    u5_cnt = 0
    for player in players:
        for u5_item in Ubung5.objects.filter(game=game, player=player.player):
            u5_sum += u5_item.score
            u5_cnt += 1

    return u5_sum/u5_cnt if u5_cnt else 0

def get_u5b(game):
    n = get_n(game)
    players = WaitingRoomMember.objects.filter(game=game,state=1)
    result = {}
    for player in players:
        result[player.player.name] = 0
        cnt = 0
        for u5_item in Ubung5.objects.filter(game=game, player=player.player):
            result[player.player.name] += u5_item.score
            cnt += 1

        result[player.player.name] /= cnt if cnt else 1
    return result

def get_u1_u3(game):
    n = get_n(game)
    players = WaitingRoomMember.objects.filter(game=game,state=1)

    def get_id(lookup, name):
        for lang in lookup:
            items = lookup[lang]
            for item in items:
                if item['value'].lower() == name.lower():
                    return item['id']

        return name

    d = {}
    c = 0
    for player in players:
        u1 = Ubung1.objects.filter(game=game, player=player.player).first()
        if not u1: continue
        u1_id = get_id(ubung_1_term_list_i18n, u1.power)

        u3 = Ubung3.objects.filter(game=game, player=player.player).first()
        if not u3: continue
        u3_id = get_id(ubung_3_term_list_i18n, u3.drainer)

        c += 1

        u5_sum = 0
        u5_cnt = 0
        for u5 in Ubung5.objects.filter(game=game, ubung1=u1, ubung3=u3):
            u5_sum += u5.score
            u5_cnt += 1

        if u1_id not in d:
            d[u1_id] = { 'count': 0, 'opposites': {}, 'u5_sum': 0, 'u5_cnt': 0, 'players': [] }
        d[u1_id]['count'] += 1
        d[u1_id]['players'].append(player.player.name)
        d[u1_id]['u5_sum'] += u5_sum / u5_cnt if u5_cnt else 0
        d[u1_id]['u5_cnt'] += 1

        if u3_id not in d[u1_id]['opposites']:
            d[u1_id]['opposites'][u3_id] = { 'count': 0, 'u5_sum': 0, 'u5_cnt': 0, 'players': [] }
        
        d[u1_id]['opposites'][u3_id]['count'] += 1
        d[u1_id]['opposites'][u3_id]['players'].append(player.player.name)
        d[u1_id]['opposites'][u3_id]['u5_sum'] += u5_sum / u5_cnt if u5_cnt else 0
        d[u1_id]['opposites'][u3_id]['u5_cnt'] += 1
    return d


def get_u3_u1(game):
    n = get_n(game)
    players = WaitingRoomMember.objects.filter(game=game,state=1)

    def get_id(lookup, name):
        for lang in lookup:
            items = lookup[lang]
            for item in items:
                if item['value'].lower() == name.lower():
                    return item['id']

        return name

    d = {}
    c = 0
    for player in players:
        u1 = Ubung1.objects.filter(game=game, player=player.player).first()
        if not u1: continue
        u1_id = get_id(ubung_1_term_list_i18n, u1.power)

        u3 = Ubung3.objects.filter(game=game, player=player.player).first()
        if not u3: continue
        u3_id = get_id(ubung_3_term_list_i18n, u3.drainer)

        c += 1

        u5_sum = 0
        u5_cnt = 0
        for u5 in Ubung5.objects.filter(game=game, ubung1=u1, ubung3=u3):
            u5_sum += u5.score
            u5_cnt += 1

        if u3_id not in d:
            d[u3_id] = { 'count': 0, 'opposites': {}, 'u5_sum': 0, 'u5_cnt': 0, 'players': [] }

        d[u3_id]['count'] += 1
        d[u3_id]['players'].append(player.player.name)
        d[u3_id]['u5_sum'] += u5_sum / u5_cnt if u5_cnt else 0
        d[u3_id]['u5_cnt'] += 1

        if u1_id not in d[u3_id]['opposites']:
            d[u3_id]['opposites'][u1_id] = { 'count': 0, 'u5_sum': 0, 'u5_cnt': 0, 'players': [] }

        d[u3_id]['opposites'][u1_id]['count'] += 1
        d[u3_id]['opposites'][u1_id]['players'].append(player.player.name)
        d[u3_id]['opposites'][u1_id]['u5_sum'] += u5_sum / u5_cnt if u5_cnt else 0
        d[u3_id]['opposites'][u1_id]['u5_cnt'] += 1

    return d
