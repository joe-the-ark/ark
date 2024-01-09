from django.core.management import BaseCommand
from arkserver.models import *
from .utils import *
from datetime import datetime

class Command(BaseCommand):
    help = "Task1: Perceived team performance across the team"

    def add_arguments(self, parser):
        parser.add_argument("games", nargs="*", type=str)
        parser.add_argument("-start", type=str)
        parser.add_argument("-end", type=str)

    def get_games(self, games):
        if games: return games
        return [_.name for _ in Game.objects.all() if not 'test' in _.name.lower() and get_n(_) > 2]

    def handle(self, **options):
        start_time = options['start']
        end_time = options['end']

        total = [0, 0, 0, 0, 0, 0]
        count = 0
        print('Name\tPlayers\tU2 Avg\tU4 Avg\t100-U5\tBelow\tInside\tAbove\tBelow2\tInside2\tAbove2\tBelow3\tInside3\tAbove3')
        is_inside = lambda v, x: 0 if x-16<v<x+16 else 1 if v>=x+16 else -1
        r2 = lambda v: f'{round(v)}'
        p2 = lambda v: f'{round(v*100)}%'

        for name in self.get_games(options['games']):
            game = Game.objects.filter(name=name).first()
            if not game: continue

            if start_time and game.create_time.replace(tzinfo=None) < datetime.strptime(start_time, '%Y.%m'):
                continue

            if end_time and game.create_time.replace(tzinfo=None) > datetime.strptime(end_time, '%Y.%m'):
                continue

            n, u2, u4, u5 = self.handle_game(game)
            if u4 == 0 or u5 == 0:
                continue

            s1 = u2
            s2 = u4
            s3 = 100-u5
            b1, i1, a1 = 0, 0, 0
            b2, i2, a2 = 0, 0, 0
            b3, i3, a3 = 0, 0, 0

            def addup(v, s):
                inside = is_inside(v, s)
                if inside == 0:
                    return 0, 1/n, 0
                if inside == -1:
                    return 1/n, 0, 0
                if inside == 1:
                    return 0, 0, 1/n

            for player in WaitingRoomMember.objects.filter(game=game, state=1):
                u2 = Ubung2.objects.filter(game=game, player=player.player).first()
                b, i, a = addup(u2.value, s1)
                b1 += b
                i1 += i
                a1 += a

                b, i, a = addup(u2.value, s2)
                b2 += b
                i2 += i
                a2 += a

                b, i, a = addup(u2.value, s3)
                b3 += b
                i3 += i
                a3 += a
            print(f'{name[:6]}\t{n}\t{r2(s1)}\t{r2(s2)}\t{r2(s3)}\t{p2(b1)}\t{p2(i1)}\t{p2(a1)}\t{p2(b2)}\t{p2(i2)}\t{p2(a2)}\t{p2(b3)}\t{p2(i3)}\t{p2(a3)}')


    """
    #1 Display a list of selected games that connects U2 AVG, U4 AVG and U5 AVG based on the two hypothesis
    that connect the 3 values (mock-up of a possible visualisation in the appendix); #4 plot the data point on a graph.
    """
    def handle_game(self, game):
        n = get_n(game)
        u2_avg = get_u2_avg(game)
        u4_avg = get_u4_avg(game)
        u5_avg = get_u5_avg(game)
        return n, u2_avg, u4_avg, u5_avg
