from arkserver.models import *
from arkserver.management.commands.utils import *
from itertools import combinations
import math


def calc_circles(game):
    votes, n = get_u5(game)
    
    safezone = {}
    players = [_ for _ in votes.keys()]

    for player in votes:
        pvotes = votes[player]
        for power in pvotes:
            if power not in safezone:
                safezone[power] = 0

            cell = pvotes[power]
            for p in cell:
                score = cell[p]
                safezone[power] += score / (n*(n-0))

    result = {}
    for bar in range(1,100):
        data = calc_single(players, votes, n, safezone, bar)
        if not data['circles']: continue

        result[bar] = data

        if len(data['circle_count']) == n and len(data['circles']) == 1:
            mono_circle = True
            for k in data['circle_count']:
                if data['circle_count'][k] != 1:
                    mono_circle = False
                    break
            if mono_circle:
                break

    return { 'players': players, 'circles': result }


def calc_single(players, votes, n, safezone, safebar):
    result = {
        player: { player: {} for player in votes }
    for player in votes }

    for player in votes:
        pvotes = votes[player]
        for power in pvotes:
            cell = pvotes[power]
            for p in cell:
                score = cell[p]
                result[player][p][power] = score

    for p1 in result:
        for p2 in result[p1]:
            s = 0
            for p in result[p1][p2]:
                score = result[p1][p2][p]
                baseline = safezone[p]
                delta = abs(score-baseline)/safebar
                #if delta > s:
                #    s = delta
                s += delta/n

            result[p1][p2] = s

    print('\nMatrix:')
    print('\t', '\t'.join([_[:5] for _ in players]))
    for i in range(n):
        player = players[i]
        row = []
        for j in range(n):
            row.append(f'{round(result[players[i]][players[j]], 2)}')
        print(player[:5],'\t', '\t'.join(row))

    print('\nEdges:')
    edges = []
    for i in range(n):
        for j in range(i+1, n):
            s1 = result[players[i]][players[j]]
            s2 = result[players[j]][players[i]]
            if s1 <= 1 and s2 <= 1:
                edges.append((players[i], players[j], max(s1, s2)))
                print(players[i], players[j], round(max(s1, s2), 3))

    print('\nCircles:')
    circles = {}
    for i in range(n-1):
        for com in combinations(range(n), n-i):
            m = len(com)
            good = True

            s = 0
            for x in com:
                for y in com:
                    if x == y: continue

                    s1 = result[players[x]][players[y]]
                    s += s1
                    if s1 > 1:
                        good = False

            if good:
                skip = False
                for circle in circles:
                    e = True
                    for x in com:
                        if x not in circle:
                            e = False
                    if e:
                        skip = True
                if not skip:
                    circles[com] = s/len(com)/(len(com)-1)
    
    for circle in circles:
        print(' '.join([players[_] for _ in circle]), circles[circle])

    circle_count = {}
    for circle in circles:
        for _ in circle:
            if _ not in circle_count:
                circle_count[_] = 0
            circle_count[_] += 1

    print('\nCircle count:')
    total_circle_member_count = 0
    for p in circle_count:
        total_circle_member_count += circle_count[p]
        print(f'{p}: {circle_count[p]}')

    print('Total circle member count:', total_circle_member_count)

    return { 'circles': [[k for k in _] for _ in circles], 'circle_count': circle_count }

