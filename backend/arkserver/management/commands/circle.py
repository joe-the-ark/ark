from django.core.management import BaseCommand
from arkserver.models import *
from .utils import *
from itertools import combinations
import math

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("games", nargs="*", type=str)
        parser.add_argument("-bar", type=int)

    def get_games(self, games):
        if games: return games
        return [_.name for _ in Game.objects.all() if not 'test' in _.name.lower() and get_n(_) > 2]

    def handle(self, **options):
        result = {}
        safebar = 16 if not options['bar'] else options['bar']

        for name in self.get_games(options['games']):
            game = Game.objects.filter(name=name).first()
            if not game: continue

            result, n = self.handle_game(game, safebar)
            # print(result, n)

    def handle_game(self, game, safebar):
        votes, n = get_u5(game)
        
        result = {
            player: { player: {} for player in votes }
        for player in votes }

        safezone = {}

        for player in votes:
            pvotes = votes[player]
            for power in pvotes:
                if power not in safezone:
                    safezone[power] = 0

                cell = pvotes[power]
                for p in cell:
                    score = cell[p]
                    result[player][p][power] = score
                    safezone[power] += score / (n*(n-0))

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
        players = [_ for _ in votes.keys()]
        n = len(players)
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
                p = players[_]
                if p not in circle_count:
                    circle_count[p] = 0
                circle_count[p] += 1

        print('\nCircle count:')
        total_circle_member_count = 0
        for p in circle_count:
            total_circle_member_count += circle_count[p]
            print(f'{p}: {circle_count[p]}')

        print('Total circle member count:', total_circle_member_count)

        return result, n
