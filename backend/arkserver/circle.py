from arkserver.models import *
from arkserver.management.commands.utils import *
from itertools import combinations
import math

def calc_circles(game):
    votes, n = get_u5(game)

    safezone = {}
    players = list(votes.keys())

    for player in votes:
        pvotes = votes[player]
        for power in pvotes:
            if power not in safezone:
                safezone[power] = 0
            cell = pvotes[power]
            for p in cell:
                score = cell[p]
                safezone[power] += score / (n * n)

    result = {}
    for bar in range(1, 100):
        data = calc_single(players, votes, n, safezone, bar)
        if not data['circles'] and not data['dyads']:
            continue

        result[bar] = data

        if len(data['circle_count']) == n and len(data['circles']) == 1:
            mono_circle = all(data['circle_count'][k] == 1 for k in data['circle_count'])
            if mono_circle:
                break

    return {'players': players, 'circles': result}

def calc_single(players, votes, n, safezone, safebar):
    result = {
        player: {target: {} for target in votes} for player in votes
    }

    for player in votes:
        pvotes = votes[player]
        for power in pvotes:
            cell = pvotes[power]
            for target in cell:
                result[player][target][power] = cell[target]

    for p1 in result:
        for p2 in result[p1]:
            s = 0
            for p in result[p1][p2]:
                score = result[p1][p2][p]
                baseline = safezone[p]
                delta = abs(score - baseline) / safebar
                s += delta / n
            result[p1][p2] = s

    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = players[i], players[j]
            s1 = result[p1][p2]
            s2 = result[p2][p1]
            if s1 <= 1 and s2 <= 1:
                cell_ij = votes[p1].get(p2, {})
                cell_ji = votes[p2].get(p1, {})
                raw1 = sum(cell_ij.values()) / len(cell_ij) if cell_ij else 0
                raw2 = sum(cell_ji.values()) / len(cell_ji) if cell_ji else 0
                edges.append({
                    'i': i,
                    'j': j,
                    'normDist': max(s1, s2),
                    'raw1': raw1,
                    'raw2': raw2,
                    'baseline1': safezone.get(p2, 0),
                    'baseline2': safezone.get(p1, 0),
                })

    circles = {}
    seen = set()
    for size in range(n, 1, -1):
        for com in combinations(range(n), size):
            if any(set(com).issubset(set(existing)) for existing in circles):
                continue
            good = True
            s = 0
            for x in com:
                for y in com:
                    if x == y:
                        continue
                    s1 = result[players[x]][players[y]]
                    if s1 > 1:
                        good = False
                        break
                    s += s1
                if not good:
                    break
            if good:
                circles[tuple(com)] = s / (len(com) * (len(com) - 1))

    dyads = []
    used_in_circle = set()
    for c in circles:
        used_in_circle.update(c)

    for edge in edges:
        i, j = edge['i'], edge['j']
        if i in used_in_circle and j in used_in_circle:
            continue
        if all(i not in circle or j not in circle for circle in circles):
            dyads.append([i, j])

    circle_count = {}
    for circle in list(circles.keys()) + dyads:
        for idx in circle:
            circle_count[idx] = circle_count.get(idx, 0) + 1

    return {
        "circles": [[idx for idx in c] for c in circles],
        "dyads": dyads,
        "circle_count": circle_count,
        "edges": edges,
    }
